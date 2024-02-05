# -*- coding: utf-8 -*-

import json
import requests
from requests_aws4auth import AWS4Auth
from config import url, bsm

headers = {
    "content-type": "application/json",
}
credentials = bsm.boto_ses.get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    bsm.aws_region,
    "lambda",
)
print("--- request ---")
payload = {"name": "Alice"}
res = requests.post(
    url=url,
    headers=headers,
    json=payload,
    auth=awsauth,
)
print(json.dumps(payload, indent=4))

print("--- response ---")
if res.text[0] == "{":
    print(json.dumps(json.loads(res.text), indent=4))
else:
    print(res.text)
