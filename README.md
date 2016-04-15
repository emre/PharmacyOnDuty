# PharmacyOnDuty
Pharmacy *on duty* api for Istanbul

## Available Districts

GET http://pharmacy.emre.sh/api/v1/istanbul/

## Pharmacies (On duty) at spesific district

GET http://pharmacy.emre.sh/api/v1/istanbul/sisli

## Install
````
$ brew install python
$ easy_install pip
# Fork the project
$ git clone git@github.com:your_name/PharmacyOnDuty.git
$ cd PharmacyOnDuty
$ pip install -r requirements.txt
$ python pharmacy_on_duty/server.py
````
After all that go to ```http://localhost:5000/api/v1/istanbul/```
