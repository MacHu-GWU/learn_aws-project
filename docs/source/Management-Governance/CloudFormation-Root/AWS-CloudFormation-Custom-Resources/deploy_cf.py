# -*- coding: utf-8 -*-

"""
This script deploy the CloudFormation to AWS.
"""

from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context
from pathlib_mate import Path
import aws_cloudformation as aws_cf

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)

s3dir_cft = S3Path(
    f"s3://{bsm.aws_account_id}-{bsm.aws_region}-artifacts"
    f"/projects/aws-lambda-backed-custom-resources-poc/cft/"
).to_dir()
dir_here = Path.dir_here(__file__)

deploy_stack_response = aws_cf.deploy_stack(
    bsm=bsm,
    stack_name="aws-lambda-backed-custom-resources-poc",
    template=dir_here.joinpath("template.json").read_text(),
    bucket=s3dir_cft.bucket,
    prefix=s3dir_cft.key,
    include_named_iam=True,
    skip_prompt=True,
)