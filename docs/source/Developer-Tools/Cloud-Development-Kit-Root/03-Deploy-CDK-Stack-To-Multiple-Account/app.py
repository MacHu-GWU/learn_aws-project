#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Read parameters
# ------------------------------------------------------------------------------
import json
from pathlib import Path
from datetime import datetime

path_params = Path(__file__).absolute().parent.joinpath("params.json")
# Ensure that this path_params file is created recently
ts_mtime = path_params.stat().st_mtime_ns / 1000000000
ts_now = datetime.now().timestamp()
elapsed = ts_now - ts_mtime
if elapsed > 3:
    raise SystemExit("The params.json file is too old.")
params = json.loads(path_params.read_text())

# ------------------------------------------------------------------------------
# Synth the Stack
# ------------------------------------------------------------------------------
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        acc_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam.CfnGroup(
            self,
            "IamGroup",
            group_name=f"deploy-cdk-stack-to-multiple-account-test-stack-{acc_name}",
        )


app = cdk.App()

# You can comment them in and out to deploy part of the stacks
Stack(
    app,
    "deploy-cdk-stack-to-multiple-account-test-stack",
    acc_name=params["acc_name"],
)

# create CloudFormation template
app.synth()
