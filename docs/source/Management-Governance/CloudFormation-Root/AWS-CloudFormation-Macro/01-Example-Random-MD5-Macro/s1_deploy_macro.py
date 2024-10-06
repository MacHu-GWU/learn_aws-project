# -*- coding: utf-8 -*-

"""
在这个 CloudFormation Template 中, 我们定义了一个 CloudFormation Macro 和其所需的
Lambda Function, 其功能是生成一个随机的 MD5 字符串.
"""

import json
from shared import dir_here, bsm, s3dir
import aws_cloudformation as aws_cf

# ------------------------------------------------------------------------------
# Put your settings here
# ------------------------------------------------------------------------------
iam_role_arn = "arn:aws:iam::{aws_account_id}:role/lambda-power-user-role"
name_prefix = "cfn_macro_poc_01_deploy_macro"

# ------------------------------------------------------------------------------
# Don't change the code below
# ------------------------------------------------------------------------------
iam_role_arn = iam_role_arn.format(aws_account_id=bsm.aws_account_id)

path_lbd_func = dir_here / "lambda_function.py"
path_lbd_deploy_package = dir_here / "lambda.zip"
path_lbd_func.make_zip_archive(path_lbd_deploy_package, overwrite=True)

s3path_lbd_deploy_package = s3dir / f"{path_lbd_func.md5}.zip"
s3path_lbd_deploy_package.upload_file(path_lbd_deploy_package, overwrite=True)


template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "CfnMacroMd5LambdaFunction": {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "FunctionName": "cfn_macro-md5",
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
                    "Variables": {"CODE_MD5": str(hash(path_lbd_func.read_text()))}
                },
            },
        },
        "CfnMacroMd5": {
            "Type": "AWS::CloudFormation::Macro",
            "Properties": {
                "Name": "Md5",
                "Description": "Generate random md5",
                "FunctionName": {"Fn::GetAtt": ["CfnMacroMd5LambdaFunction", "Arn"]},
            },
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
    # deploy_stack()
    delete_stack()
    # pass
