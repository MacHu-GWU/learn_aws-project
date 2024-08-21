#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The app.py file should not contain much CDK stack declaration logics, it should be
managed by a Python library, so it is more manageable and testable.
"""

import json
from pathlib import Path

import aws_cdk as cdk
import aws_cdk.assertions as assertions

from learn_cdk.config import stack_name, path_cfn
from learn_cdk.stacks import MyCDKStack

app = cdk.App()

stack = MyCDKStack(
    app,
    construct_id=stack_name,
    # comment it out if you use cdk for deployment
    # uncomment it if you use CloudFormation for deployment
    synthesizer=cdk.DefaultStackSynthesizer(
        generate_bootstrap_version_rule=False,
    ),
)

# create CloudFormation template
template = assertions.Template.from_stack(stack)
cfn_content = json.dumps(template.to_json(), indent=4)
path_cfn.write_text(cfn_content)

app.synth()
