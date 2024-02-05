# -*- coding: utf-8 -*-

import json


def lambda_handler(event, context):
    print(json.dumps(event, indent=4))
    return {"message": "hello world"}
