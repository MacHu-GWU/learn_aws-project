# -*- coding: utf-8 -*-

import json
from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
sfn_arn = f"arn:aws:states:{bsm.aws_region}:{bsm.aws_account_id}:stateMachine:sfn-poc"
lbd_arn = f"arn:aws:lambda:{bsm.aws_region}:{bsm.aws_account_id}:function:sfn-poc-lbd-1"
bucket = f"{bsm.aws_account_alias}-{bsm.aws_region}-data"
key = "projects/tmp/fw2-1.pdf"

input_data = {
    "task1": {
        "bucket": bucket,
        "key": key,
    }
}
bsm.sfn_client.start_execution(
    stateMachineArn=sfn_arn,
    input=json.dumps(input_data),
)
