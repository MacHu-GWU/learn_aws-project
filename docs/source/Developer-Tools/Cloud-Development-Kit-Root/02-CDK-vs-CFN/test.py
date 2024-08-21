# -*- coding: utf-8 -*-

"""
Unit test for a CDK stack declaration.
"""

import os
import pytest
import json
import aws_cdk as cdk
import aws_cdk.assertions as assertions

from learn_cdk.stacks import MyCDKStack1, MyCDKStack2


def test():
    # Try to convert CDK stack to cloudformation template
    app = cdk.App()
    stack = MyCDKStack1(app, "my-cdk-stack-1")
    template = assertions.Template.from_stack(stack)
    # print(json.dumps(template.to_json(), indent=4))

    # for unit test, you have to create different app for each stack
    app = cdk.App()
    stack = MyCDKStack2(app, "my-cdk-stack-2")
    template = assertions.Template.from_stack(stack)
    # print(json.dumps(template.to_json(), indent=4))


if __name__ == "__main__":
    import subprocess

    subprocess.call(["pytest", "--tb=native", str(__file__)])
