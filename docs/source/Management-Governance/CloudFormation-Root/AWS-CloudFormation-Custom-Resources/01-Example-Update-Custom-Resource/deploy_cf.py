# -*- coding: utf-8 -*-

"""
This script deploy the CloudFormation to AWS.
"""

import json
import uuid
from pathlib_mate import Path
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager
import aws_cloudformation as aws_cf

aws_profile = "bmt_app_dev_us_east_1"
iam_role_arn = "arn:aws:iam::{aws_account_id}:role/lambda-power-user-role"
name_prefix = "custom_resource_poc_example_02"

# ------------------------------------------------------------------------------
# Don't change the code below
# ------------------------------------------------------------------------------
bsm = BotoSesManager(profile_name=aws_profile)
context.attach_boto_session(bsm.boto_ses)
iam_role_arn = iam_role_arn.format(aws_account_id=bsm.aws_account_id)

dir_here = Path.dir_here(__file__)
path_lbd_func = dir_here / "lambda_function.py"
path_lbd_deploy_package = dir_here / "lambda.zip"
path_lbd_func.make_zip_archive(path_lbd_deploy_package, overwrite=True)

s3dir = S3Path(
    f"s3://{bsm.aws_account_id}-{bsm.aws_region}-data"
    f"/projects/aws-lambda-backed-custom-resources-poc/01-Example-Update-Custom-Resource/"
).to_dir()
s3path_lbd_deploy_package = s3dir / "lambda.zip"
s3path_lbd_deploy_package.upload_file(path_lbd_deploy_package, overwrite=True)

custom_resource_request_handler_lbd_func_name = (
    f"{name_prefix}-custom-resource-request-handler"
)
template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "LambdaFunctionCustomerResourceHandler": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "FunctionName": custom_resource_request_handler_lbd_func_name,
                "Handler": "lambda_function.lambda_handler",
                "Role": iam_role_arn,
                "Code": {
                    "S3Bucket": s3path_lbd_deploy_package.bucket,
                    "S3Key": s3path_lbd_deploy_package.key,
                },
                "Runtime": "python3.11",
                "MemorySize": 128,
                "Timeout": 30,
                "Environment": {
                    "Variables": {"CODE_HASH": str(hash(path_lbd_func.read_text()))}
                },
            },
        },
        # expected response object
        # :param name: the name of the IAM group
        "IamGroupInfo": {
            "Type": "Custom::IamGroupInfo",
            "Properties": {
                "ServiceToken": f"arn:aws:lambda:{bsm.aws_region}:{bsm.aws_account_id}:function:{custom_resource_request_handler_lbd_func_name}",
                # don't forget to set ServiceTimeout to a shorter value
                # otherwise you will wait for an hour if you made a mistake in your request lambda handler
                "ServiceTimeout": 30,
                # use a random generated value to send a update request to the request lambda handler
                # this value should comes from the CloudFormation Parameter
                "client_token": uuid.uuid4().hex,
            },
            # make sure this depends on the lambda function handler
            "DependsOn": "LambdaFunctionCustomerResourceHandler",
        },
        "IamGroup": {
            "Type": "AWS::IAM::Group",
            "Properties": {"GroupName": {"Fn::GetAtt": ["IamGroupInfo", "name"]}},
            # make sure this depends on the custom resource
            "DependsOn": "IamGroupInfo",
        },
    },
}
stack_name = name_prefix.replace("_", "-")


def deploy_stack():
    aws_cf.deploy_stack(
        bsm=bsm,
        stack_name=stack_name,
        template=json.dumps(template),
        include_named_iam=True,
        skip_prompt=True,
    )


def delete_stack():
    aws_cf.remove_stack(
        bsm=bsm,
        stack_name=stack_name,
        skip_prompt=True,
    )


if __name__ == "__main__":
    deploy_stack()
    # delete_stack()
    # pass
