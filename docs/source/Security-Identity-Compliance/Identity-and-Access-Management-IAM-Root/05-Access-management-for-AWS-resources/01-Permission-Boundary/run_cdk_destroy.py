# -*- coding: utf-8 -*-

"""
WARNING: This script will destroy all resources in the AWS CDK stack!!!
"""

import subprocess

from app import aws_profile

args = [
    "cdk",
    "destroy",
    "--all",
    "--force",
    "--profile",
    aws_profile,
]
subprocess.run(args)
