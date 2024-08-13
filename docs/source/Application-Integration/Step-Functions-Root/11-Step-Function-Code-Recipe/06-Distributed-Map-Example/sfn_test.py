# -*- coding: utf-8 -*-

import json
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
context.attach_boto_session(boto_ses=bsm.boto_ses)
sfn_arn = f"arn:aws:states:{bsm.aws_region}:{bsm.aws_account_id}:stateMachine:sfn-poc"
lbd_arn = f"arn:aws:lambda:{bsm.aws_region}:{bsm.aws_account_id}:function:sfn-poc-lbd-1"
bucket = f"{bsm.aws_account_alias}-{bsm.aws_region}-data"
key = "projects/tmp/"

n_file = 3
s3dir_tmp = S3Path(bucket, key)

# prepare map payload
map_payload = []
for ith in range(1, 1 + n_file):
    s3path = s3dir_tmp.joinpath(f"data/{ith}.json")
    s3path.write_text("hello world")
    map_payload.append(
        {
            "bucket": s3path.bucket,
            "key": s3path.key,
        }
    )
s3path = s3dir_tmp.joinpath("map_payload.json")
s3path.write_text(json.dumps(map_payload))

input_data = {
    "map_input_s3_bucket": s3path.bucket,
    "map_input_s3_key": s3path.key,
}
bsm.sfn_client.start_execution(
    stateMachineArn=sfn_arn,
    input=json.dumps(input_data),
)
