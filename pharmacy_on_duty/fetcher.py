# -*- coding: utf-8 -*-

import datetime
import HTMLParser
import json
import re

import redis
import requests
import unicode_tr.extras
from lxml import html

from conf import REDIS_INFO, REDIS_PREFIX


def smart_unicode(text):
    if text:
        html_parser = HTMLParser.HTMLParser()
        if not isinstance(text, unicode):
            text = unicode(text, "utf8")
        text = html_parser.unescape(text)
        text = text.encode("utf8")

        text = text.replace("Ä±", "ı")
        text = text.replace("Ä°", "İ")
        text = text.replace("Å", "ş")
        text = text.replace("Ä", "ğ")

    return text


def insert_to_redis(pharmacies):
    r = redis.StrictRedis(**REDIS_INFO)
    for pharmacy in pharmacies:
        r.set("{0}:{1}".format(REDIS_PREFIX, pharmacy["slug"]), json.dumps(pharmacy))
        r.sadd("{0}:districts".format(REDIS_PREFIX), pharmacy["name"])


def get_districts():

    _session = requests.session()

    r = _session.get("http://apps.istanbulsaglik.gov.tr/Eczane")
    page_source = r.text.encode("utf-8")

    districts_on_page = re.findall('data-value="(.*?)" data-ilcename=".*?" data-title="(.*?)"', page_source)
    district_list = []
    for _id, name in districts_on_page:
        name = smart_unicode(name)
        district_list.append({
            "id": _id,
            "name": name,
        })

    _token = re.search('"token": "(.*?)"', page_source)

    return _session, _token.group(1), district_list


def get_pharmacies_on_duty(session, district, token):
    headers = {
        'Origin': 'http://apps.istanbulsaglik.gov.tr',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'text/html, */*; q=0.01',
        'Referer': 'http://apps.istanbulsaglik.gov.tr/Eczane',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = 'id={0}&token={1}'.format(district["id"], token)

    r = session.post('http://apps.istanbulsaglik.gov.tr/Eczane/nobetci', headers=headers, data=data)
    page_source = r.text.encode("utf-8")
    tree = html.fromstring(page_source)

    addresses = tree.xpath('//*[@id="adres"]/td[2]/label')
    names = tree.xpath('//*/div/p')
    phone_numbers = tree.xpath('//*[@id="Tel"]/td[2]/label/a')
    directions = tree.xpath('//*/table/tbody/tr[4]/td[2]/label')
    coordinates = re.findall(
        'http://sehirharitasi.ibb.gov.tr/\?lat=(.*?)&lon=(.*?)&zoom=18',
        page_source
    )

    addresses = [smart_unicode(address.text) for address in addresses]
    names = [name.text for name in names]
    phone_numbers = [phone_number.text for phone_number in phone_numbers]
    directions = [smart_unicode(direction.text) for direction in directions]

    pharmacies = []
    for i in range(0, len(addresses)):
        pharmacies.append({
            "name": names[i],
            "address": addresses[i],
            "phone_number": phone_numbers[i],
            "directions": directions[i],
            "coordinates": coordinates[i],
        })

    return pharmacies


def update_pharmacy_info():
    session, token, districts = get_districts()
    district_data = []
    for district in districts:
        pharmacies = get_pharmacies_on_duty(session, district, token)
        district_data.append({
            "name": district["name"],
            "pharmacies": pharmacies,
            "date": datetime.date.today().strftime("%m-%d-%Y"),
            "slug": unicode_tr.extras.slugify(district["name"])
        })
    insert_to_redis(district_data)
    print " >> {0} districts updated.".format(len(district_data))

