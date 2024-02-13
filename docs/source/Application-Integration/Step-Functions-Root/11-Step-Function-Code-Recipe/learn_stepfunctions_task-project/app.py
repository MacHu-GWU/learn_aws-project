#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The app.py file should not contain much CDK stack declaration logics, it should be
managed by a Python library, so it is more manageable and testable.
"""

import aws_cdk as cdk
from learn_stepfunctions_task.stacks import (
    MySfnTaskStack1,
    MySfnTaskStack2,
    MySfnTaskStack3,
)

app = cdk.App()

# You can comment them in and out to deploy part of the stacks
# MySfnTaskStack1(app, "my-sfn-task-stack-1")
# MySfnTaskStack2(app, "my-sfn-task-stack-2")
MySfnTaskStack3(app, "my-sfn-task-stack-3")

# create CloudFormation template
app.synth()
