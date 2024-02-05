# -*- coding: utf-8 -*-

import json


def lambda_handler(event, context):
    print(json.dumps(event, indent=4))
    data = json.loads(event["body"])
    name = data["name"]
    return {"message": f"hello {name}"}
