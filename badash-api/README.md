# badash-api

## Purpose

This is the back-end server for BADash. It handles API calls for storing and retrieving Dashboards, Jobs and Events.

Each Dashboard object has a title, slug, description and list of Job objects.

Each Job object has a title, slug, description and a dynamic/flexible configuration object.

Each Event object is related back to a single Job object, has a date/time stamp value (stored in UTC) and a `result` (like an error-code or error-level value). Beyond that, the Event object can contain any number of dynamic fields including objects. For example, the Event object could contain a `text_output` string field, a `temperature` float field or even a more complex type like `geo_location` stored as an object like ```{"lat": 48.23421, "lon": 23.23421}```.

## Getting Started

Install the requirements into a fresh python3 virtualenv:

```pip install -r requirements.txt```

To run locally, have a locally available `mongodb` instance on the default port or specify the connection parameters to a mongodb server by setting the `MONGODB_URI` environment variable. The default value is `mongodb://localhost:27017/badash`.

> *Note:* the `python-jose` version is currently pinned to 1.4.0 which makes `pycrypto` the default backend and does not install `pycryptodome`. This makes running on AWS Lambda easier.

Start the hug server via:

`hug -f app.py`

Access the API via `http://localhost:8000` .

To execute the tests, install pytest (`pip install pytest`). And then just execute `pytest`. The a local mongodb running on the default port is currently required as it creates a temporary db called `test_badash` to execute the tests. Future version of the code will likely switch to `mongomock`.

## To deploy to AWS Lambda

... insert instructions here ...

```zappa init```

How to answer the questions... 

Make sure you have:
```"app_function": "app.__hug_wsgi__"```

```zappa deploy dev```

