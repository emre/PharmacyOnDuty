# -*- coding: utf-8 -*-

import json

import redis
import unicode_tr.extras
from flask import Flask, abort, g, jsonify
from flask.ext.cors import CORS

from conf import API_SERVER_PREFIX, REDIS_INFO, REDIS_PREFIX

app = Flask(__name__)

CORS(app)


@app.before_request
def before_request():
    g.redis_connection = redis.StrictRedis(**REDIS_INFO)


def get_districts():
    districts = g.redis_connection.smembers("{0}:districts".format(REDIS_PREFIX))
    _district_list = []
    for district in districts:
        _district_list.append({
            "district": district,
            "slug": unicode_tr.extras.slugify(district)
        })

    return _district_list


@app.route("/{0}istanbul/".format(API_SERVER_PREFIX))
def district_list():
    return jsonify(districts=get_districts())


@app.route("/{0}istanbul/<district_slug>/".format(API_SERVER_PREFIX))
def district_pharmacies(district_slug):

    pharmacies = g.redis_connection.get("{0}:{1}".format(REDIS_PREFIX, district_slug))
    if not pharmacies:
        abort(404)

    pharmacies = json.loads(pharmacies)

    return jsonify(pharmacies)

if __name__ == "__main__":
    app.debug = True
    app.run()
