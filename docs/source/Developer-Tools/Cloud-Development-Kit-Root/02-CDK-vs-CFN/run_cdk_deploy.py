# -*- coding: utf-8 -*-

import subprocess

from learn_cdk.config import aws_profile, param_value_project_name
from app import stack

params = {
    stack.param_project_name_id: param_value_project_name,
}
params_args = []
for k, v in params.items():
    params_args.append("--parameters")
    params_args.append(f"{k}={v}")

args = [
    "cdk",
    "deploy",
    "--all",
    "--require-approval",
    "never",
    "--profile",
    aws_profile,
    *params_args,
]
print(" ".join(args))
subprocess.run(args)
