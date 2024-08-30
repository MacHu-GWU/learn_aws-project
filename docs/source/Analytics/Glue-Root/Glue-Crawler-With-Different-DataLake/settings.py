# -*- coding: utf-8 -*-

from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager
from aws_console_url.api import AWSConsole

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)
bucket = f"{bsm.aws_account_alias}-{bsm.aws_region}-data"
database_name = "glue_crawler_test"
s3dir_db = S3Path(f"s3://{bucket}/projects/learn_aws/glue_crawler/databases/{database_name}")
iam_role = "arn:aws:iam::878625312159:role/all-services-admin-role"
aws_console = AWSConsole.from_bsm(bsm=bsm)
