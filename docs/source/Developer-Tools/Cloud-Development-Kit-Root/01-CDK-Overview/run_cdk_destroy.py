# -*- coding: utf-8 -*-

import subprocess

from learn_cdk.config import aws_profile

args = [
    "cdk",
    "destroy",
    "--all",
    "--force",
    "--profile",
    aws_profile,
]
subprocess.run(args)
