# PharmacyOnDuty
Pharmacy *on duty* api for Istanbul.

## Installation

```bash
$ git clone git@github.com:emre/PharmacyOnDuty.git
$ (sudo) pip install -e .
```

This will install the api into your (virtual) environment as *editable*. If you make any changes in the codebase, you don't need to re-install the package. 

**Running the fetcher**

```bash
$ fetch_pharmacy_data
```

**Running the server**

```bash
$ python server.py
```

see the district list at: ```http://localhost:5000/api/v1/istanbul/```

**Note**: For production usage, use gunicorn or uwsgi.

## Endpoints

### Available Districts

GET http://pharmacy.emre.sh/api/v1/istanbul/

### Pharmacies (On duty) at spesific district

GET http://pharmacy.emre.sh/api/v1/istanbul/sisli

