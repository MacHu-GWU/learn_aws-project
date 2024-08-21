# -*- coding: utf-8 -*-

from pathlib import Path

aws_profile = "bmt_app_dev_us_east_1"
stack_name = "my-cdk-stack"
param_value_project_name = "my_cdk_stack"

_dir_project_root = Path(__file__).absolute().parent.parent
path_cfn = _dir_project_root.joinpath("cloudformation-template.json")
