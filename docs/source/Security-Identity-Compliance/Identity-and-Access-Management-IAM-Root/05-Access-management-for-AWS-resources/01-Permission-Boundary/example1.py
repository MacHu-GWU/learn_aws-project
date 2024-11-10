# -*- coding: utf-8 -*-

import json
import botocore.exceptions
from boto_session_manager import BotoSesManager
from app import bsm, prefix, stack, stack_name

iam_role_name = f"{prefix}_iam_role"
iam_role_policy_name = f"{iam_role_name}_policy"

res = bsm.cloudformation_client.describe_stacks(
    StackName=stack_name,
)
outputs = dict()
for dct in res["Stacks"][0]["Outputs"]:
    outputs[dct["OutputKey"]] = dct["OutputValue"]
bsm_user = BotoSesManager(
    aws_access_key_id=outputs["OutputIamUserAccessKey"],
    aws_secret_access_key=outputs["OutputIamUserSecretKey"],
    region_name=bsm.aws_region,
)


def test_iam_user_permission():
    """
    抛出 AccessDenied 就说明对了.
    """
    res = bsm_user.s3_client.list_buckets()
    print(res["Buckets"])


def create_assume_role():
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{bsm.aws_account_id}:user/{stack.iam_user_name}"
                },
                "Action": "sts:AssumeRole",
            }
        ],
    }
    try:
        bsm_user.iam_client.create_role(
            RoleName=iam_role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
            # User has to attach this permission boundary to the role
            # Otherwise it will not be able to CREATE the role
            # You can try to run this without the permission boundary (comment it out)
            PermissionsBoundary=f"arn:aws:iam::{bsm.aws_account_id}:policy/{stack.iam_permission_boundary_policy_name}",
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            pass
        else:
            raise e

    role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*",
            }
        ],
    }
    bsm_user.iam_client.put_role_policy(
        RoleName=iam_role_name,
        PolicyName=iam_role_policy_name,
        PolicyDocument=json.dumps(role_policy_document),
    )


def test_assume_role_permission():
    """
    抛出 AccessDenied 就说明对了. 虽然这个 Role 显式了可以访问 S3, 但是由于
    Permission Boundary Policy 的限制, 还是无法访问 S3.
    """
    bsm_assume_role = bsm_user.assume_role(
        role_arn=f"arn:aws:iam::{bsm.aws_account_id}:role/{iam_role_name}"
    )
    res = bsm_assume_role.s3_client.list_buckets()
    print(res["Buckets"])


def delete_assume_role():
    try:
        bsm_user.iam_client.delete_role_policy(
            RoleName=iam_role_name,
            PolicyName=iam_role_policy_name,
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchEntity":
            pass
        else:
            raise e

    try:
        bsm_user.iam_client.delete_role(RoleName=iam_role_name)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchEntity":
            pass
        else:
            raise e


if __name__ == "__main__":
    """ """
    # --- Run test
    # test_iam_user_permission()
    # create_assume_role()
    # test_assume_role_permission()

    # --- Clean up
    delete_assume_role()
