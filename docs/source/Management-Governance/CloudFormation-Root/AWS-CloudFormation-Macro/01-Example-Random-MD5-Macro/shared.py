# -*- coding: utf-8 -*-

"""
Helper scripts to create shared variables.

Usage:

    from shared import dir_here, bsm, s3dir
"""

import typing as T
from pathlib_mate import Path
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager

aws_profile = "bmt_app_dev_us_east_1"
dir_here = Path.dir_here(__file__)


def create_vars(
    aws_profile: str,
    prefix: str,
    bucket: str = "{aws_account_alias}-{aws_region}-data",
) -> T.Tuple["BotoSesManager", "S3Path"]:
    bsm = BotoSesManager(profile_name=aws_profile)
    context.attach_boto_session(bsm.boto_ses)
    s3dir = S3Path(
        "s3://{}/{}".format(
            bucket.format(
                aws_account_id=bsm.aws_account_id,
                aws_account_alias=bsm.aws_account_alias,
                aws_region=bsm.aws_region,
            ),
            prefix,
        ),
    ).to_dir()
    return bsm, s3dir


# ------------------------------------------------------------------------------
# Put your settings here
# ------------------------------------------------------------------------------
(
    bsm,
    s3dir,
) = create_vars(
    aws_profile="bmt_app_dev_us_east_1",
    prefix="projects/aws-lambda-backed-cloudformation-macro-poc/01-Example-Random-MD5-Macro",
)
