# -*- coding: utf8 -*-
import json
from base64 import b64decode, b64encode

import urllib3


# set your SCF_TOKEN here
SCF_TOKEN = ''


def main_handler(event: dict, context: dict):
    data = event["body"]
    kwargs = json.loads(data)
    kwargs['body'] = b64decode(kwargs['body'])
    if SCF_TOKEN != kwargs.get('SCF_TOKEN', None):
        raise Exception("NotAuthorized")
    del kwargs['SCF_TOKEN']

    http = urllib3.PoolManager(cert_reqs="CERT_NONE")
    r = http.request(**kwargs, retries=False, decode_content=False)
    
    response = {
        "headers": {k.lower(): v.lower() for k, v in r.headers.items()},
        "status_code": r.status,
        "content": b64encode(r._body).decode('utf-8')
    }

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(response)
    }
