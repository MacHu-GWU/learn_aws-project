# -*- coding: utf-8 -*-

"""
Unit test for a CDK stack declaration.
"""

import os
import pytest
import json
import aws_cdk as cdk
import aws_cdk.assertions as assertions

from learn_stepfunctions_task.stacks import MySfnTaskStack1


def test():
    # Try to convert CDK stack to cloudformation template
    app = cdk.App()
    stack = MySfnTaskStack1(app, "my-sfn-task-stack-1")
    template = assertions.Template.from_stack(stack)
    # print(json.dumps(template.to_json(), indent=4))


if __name__ == "__main__":
    import subprocess

    subprocess.call(["pytest", "--tb=native", str(__file__)])
