# -*- coding: utf-8 -*-

import json
import requests
from config import url

headers = {
    "content-type": "application/json",
}
print("--- request ---")
res = requests.get(
    url=url,
    headers=headers,
)
print("--- response ---")
if res.text[0] == "{":
    print(json.dumps(json.loads(res.text), indent=4))
else:
    print(res.text)
