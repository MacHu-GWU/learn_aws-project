# -*- coding: utf-8 -*-

"""
Delete all CDK assets created before 90 days ago.
"""

from datetime import datetime, timezone, timedelta
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager

from learn_cdk.config import aws_profile

bsm = BotoSesManager(profile_name=aws_profile)
context.attach_boto_session(bsm.boto_ses)

res = bsm.cloudformation_client.describe_stacks(StackName="CDKToolkit")
outputs = {dct["OutputKey"]: dct["OutputValue"] for dct in res["Stacks"][0]["Outputs"]}
bucket = outputs["BucketName"]

utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
three_month_ago = utc_now - timedelta(days=90)
for ith, s3path in enumerate(S3Path(bucket).iter_objects(), start=1):
    if s3path.last_modified_at < three_month_ago:
        print(f"delete {ith} cdk asset: {s3path.uri}")
        s3path.delete()
