# -*- coding: utf-8 -*-

import subprocess

from learn_stepfunctions_task.config import aws_profile

args = [
    "cdk",
    "deploy",
    "--all",
    "--require-approval",
    "never",
    "--profile",
    aws_profile,
]
subprocess.run(args)
