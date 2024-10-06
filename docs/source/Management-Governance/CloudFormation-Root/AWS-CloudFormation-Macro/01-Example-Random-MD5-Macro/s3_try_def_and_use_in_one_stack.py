# -*- coding: utf-8 -*-

"""
有了 deploy_macro.py 和 test_macro.py 两个成功例子, 我们来尝试将 Macro 的定义和 Macro
的使用放在一个 CloudFormation 中可不可以 (**结论, 不可以直接放**). 在 AWS 官方文档中我们已经
知道可以将 Macro 的定义和 Macro 的使用分别放在两个不同的 CloudFormation Stack 中,
然后使用 Nested Stack 的方式将两个 Stack 放在一个 Stack 中, 并且定义依赖关系, 这个是确定
可行的. 但我们还是想要动手尝试一下, 看看可不可以直接放在一个 CloudFormation 中.
"""

import json
from shared import dir_here, bsm, s3dir
import aws_cloudformation as aws_cf

# ------------------------------------------------------------------------------
# Put your settings here
# ------------------------------------------------------------------------------
iam_role_arn = "arn:aws:iam::{aws_account_id}:role/lambda-power-user-role"
name_prefix = "cfn_macro_poc_01_try_def_and_use_in_one_stack"

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
                "FunctionName": {
                    "Fn::GetAtt": ["CfnMacroMd5LambdaFunction", "Arn"],
                },
            },
        },
        "IamGroup": {
            "Type": "AWS::IAM::Group",
            "Properties": {
                "GroupName": {
                    "Fn::Transform": {
                        "Name": "Md5",
                        "Parameters": {},
                    }
                },
            },
            "DependsOn": "CfnMacroMd5",
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
