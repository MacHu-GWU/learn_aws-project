# -*- coding: utf-8 -*-

import base64
import uuid
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
exec_name = str(uuid.uuid4())
exec_arn = f"arn:aws:states:{bsm.aws_region}:{bsm.aws_account_id}:execution:sfn-poc:{exec_name}"
filename = base64.b64encode(exec_arn.encode("utf-8")).decode("utf-8")
key_sfn_exec = f"projects/tmp/sfn-exec/{filename}.json"
bsm.s3_client.put_object(
    Bucket=bucket,
    Key=key_sfn_exec,
    Body=json.dumps(input_data),
)

bsm.sfn_client.start_execution(
    stateMachineArn=sfn_arn,
    input=json.dumps(input_data),
    name=exec_name,
)