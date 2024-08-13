# -*- coding: utf-8 -*-

import json
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)
sfn_arn = f"arn:aws:states:{bsm.aws_region}:{bsm.aws_account_id}:stateMachine:sfn-poc"
bucket = f"{bsm.aws_account_alias}-{bsm.aws_region}-data"
s3dir_root = S3Path(f"s3://{bucket}/projects/tmp/").to_dir()
table_arn = f"arn:aws:dynamodb:{bsm.aws_region}:{bsm.aws_account_id}:table/orders"
res = bsm.dynamodb_client.export_table_to_point_in_time(
    TableArn=table_arn,
    S3Bucket=s3dir_root.bucket,
    S3Prefix=f"{s3dir_root.key}exports",
)
export_arn = res["ExportDescription"]["ExportArn"]
print(f"{export_arn = }")
input_data = {"ExportDescription": {"ExportArn": export_arn}}
bsm.sfn_client.start_execution(
    stateMachineArn=sfn_arn,
    input=json.dumps(input_data),
)
