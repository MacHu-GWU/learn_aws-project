# -*- coding: utf-8 -*-

"""
测试 s1_deploy_macro.py 中部署的 Macro.
"""

import json
from shared import bsm
import aws_cloudformation as aws_cf

# ------------------------------------------------------------------------------
# Put your settings here
# ------------------------------------------------------------------------------
name_prefix = "cfn_macro_poc_01_test_macro"

# ------------------------------------------------------------------------------
# Don't change the code below
# ------------------------------------------------------------------------------
template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "IamGroup": {
            "Type": "AWS::IAM::Group",
            "Properties": {
                "GroupName": {
                    "Fn::Transform": {
                        # this value has to match the value at
                        # s1_deploy_macro.py -> CfnMacroMd5 -> Properties -> Name
                        "Name": "Md5",
                        "Parameters": {},
                    }
                },
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
