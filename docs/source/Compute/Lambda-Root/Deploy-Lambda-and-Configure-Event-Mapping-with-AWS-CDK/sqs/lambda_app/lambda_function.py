# -*- coding: utf-8 -*-

import json


def lambda_handler(event, context):
    print("------ Event ------")
    print(json.dumps(event, indent=4))
    return {"statusCode": 200, "body": "Hello World"}
