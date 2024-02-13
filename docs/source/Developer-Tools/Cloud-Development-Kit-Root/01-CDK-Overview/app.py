#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The app.py file should not contain much CDK stack declaration logics, it should be
managed by a Python library, so it is more managable and testable.
"""

import aws_cdk as cdk
from learn_cdk.stacks import MyCDKStack1, MyCDKStack2

app = cdk.App()

# You can comment them in and out to deploy part of the stacks
MyCDKStack1(app, "my-cdk-stack-1")
MyCDKStack2(app, "my-cdk-stack-2")

# create CloudFormation template
app.synth()
