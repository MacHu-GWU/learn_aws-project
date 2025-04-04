# -*- coding: utf-8 -*-

import typing as T
import json
import subprocess
from pathlib_mate import Path
from boto_session_manager import BotoSesManager

dir_here = Path.dir_here(__file__)
path_params = dir_here / "params.json"


def destroy_cdk(
    params: dict[str, T.Any],
    bsm: BotoSesManager,
):
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


# fmt: off
params_dev = {"acc_name": "app_dev"}
bsm_dev = BotoSesManager(profile_name="bmt_app_dev_us_east_1")

params_test = {"acc_name": "app_test"}
bsm_test = BotoSesManager(profile_name="bmt_app_test_us_east_1")
# fmt on

if __name__ == "__main__":
    """
    """
    destroy_cdk(params_dev, bsm_dev)
    # destroy_cdk(params_test, bsm_test)
