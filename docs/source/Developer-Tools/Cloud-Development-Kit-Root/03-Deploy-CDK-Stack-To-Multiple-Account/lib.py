# -*- coding: utf-8 -*-

import typing as T
import json
import subprocess
from pathlib_mate import Path
from boto_session_manager import BotoSesManager

dir_here = Path.dir_here(__file__)
path_params = dir_here / "params.json"


def deploy_cdk(
    params: dict[str, T.Any],
    bsm: BotoSesManager,
):
    print(f"Deploying CDK stack to {bsm.aws_account_id} {bsm.aws_region} ...")
    path_params.write_text(json.dumps(params))
    args = [
        "cdk",
        "deploy",
        "--all",
        "--require-approval",
        "never",
    ]
    with dir_here.temp_cwd():
        with bsm.awscli():
            subprocess.run(args)


def destroy_cdk(
    params: dict[str, T.Any],
    bsm: BotoSesManager,
):
    print(f"Delete CDK stack from {bsm.aws_account_id} {bsm.aws_region} ...")
    path_params.write_text(json.dumps(params))
    args = [
        "cdk",
        "destroy",
        "--all",
        "--force",
    ]
    with dir_here.temp_cwd():
        with bsm.awscli():
            subprocess.run(args)


params_dev = {"acc_name": "app_dev"}
bsm_dev = BotoSesManager(profile_name="bmt_app_dev_us_east_1")

params_test = {"acc_name": "app_test"}
bsm_test = BotoSesManager(profile_name="bmt_app_test_us_east_1")
