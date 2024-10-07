# -*- coding: utf-8 -*-

"""
测试 s1_deploy_macro.py 中部署的 Macro.
"""

import json
from shared import bsm, s3dir
import aws_cloudformation as aws_cf

template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Parameters": {
        "ProjectName": {
            "Type": "String",
            "Description": "The name of the project to deploy. See details at https://www.google.com",
        },
    },
    "Resources": {
        "SnsTopic": {
            "Type": "AWS::SNS::Topic",
            "Properties": {
                "TopicName": {
                    "Fn::Sub": [
                        "${ProjectName}-sns-topic",
                        {"ProjectName": {"Ref": "ProjectName"}},
                    ]
                },
            },
        },
    },
}

s3path = s3dir.joinpath("template.json").write_text(
    json.dumps(template),
    content_type="application/json",
)
print(f"template uploaded to s3: {s3path.get_regional_console_url(bsm.aws_region)}")

stack_name = "cloudformation-public-facing-template-poc"
url = (
    f"https://{bsm.aws_region}.console.aws.amazon.com"
    f"/cloudformation/home?region={bsm.aws_region}#"
    f"/stacks/create?stackName={stack_name}&templateURL="
    f"https://{s3path.bucket}.s3.amazonaws.com/{s3path.key}"
    "&param_ProjectName=MyProject"
)
print(f"click this to create: {url}")
default_project_name = "MyProject"
url = (
    f"https://{bsm.aws_region}.console.aws.amazon.com"
    f"/cloudformation/home?region={bsm.aws_region}#"
    f"/stacks/create/review?stackName={stack_name}&templateURL="
    f"https://{s3path.bucket}.s3.amazonaws.com/{s3path.key}"
    f"&param_ProjectName={default_project_name}"
)
print(f"click this to deploy: {url}")


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
    # delete_stack()
    pass
