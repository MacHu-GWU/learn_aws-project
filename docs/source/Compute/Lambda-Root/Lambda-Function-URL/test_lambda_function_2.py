# -*- coding: utf-8 -*-

import json
import requests
from config import url

headers = {
    "content-type": "application/json",
}
print("--- request ---")
payload = {"name": "Alice"}
res = requests.post(
    url=url,
    headers=headers,
    json=payload,
)
print(json.dumps(payload, indent=4))

print("--- response ---")
if res.text[0] == "{":
    print(json.dumps(json.loads(res.text), indent=4))
else:
    print(res.text)
