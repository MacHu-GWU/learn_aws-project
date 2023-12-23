# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager


def get_credentials(bsm: "BotoSesManager"):
    print("----- get_credentials ------")
    cred = bsm.boto_ses.get_credentials()
    aws_access_key_id = cred.access_key
    aws_secret_access_key = cred.secret_key
    aws_session_token = cred.token
    print(f"{aws_access_key_id = }")
    print(f"{aws_secret_access_key = }")
    print(f"{aws_session_token = }")
    return aws_access_key_id, aws_secret_access_key, aws_session_token


def get_session_token(bsm: "BotoSesManager"):
    print("----- get_session_token ------")
    res = bsm.sts_client.get_session_token(DurationSeconds=900)
    aws_access_key_id = res["Credentials"]["AccessKeyId"]
    aws_secret_access_key = res["Credentials"]["SecretAccessKey"]
    aws_session_token = res["Credentials"]["SessionToken"]
    print(f"{aws_access_key_id = }")
    print(f"{aws_secret_access_key = }")
    print(f"{aws_session_token = }")
    return aws_access_key_id, aws_secret_access_key, aws_session_token


# ------------------------------------------------------------------------------
# Only enable one boto session at time
# ------------------------------------------------------------------------------
bsm = BotoSesManager() # default profile, it is an IAM User
# bsm = BotoSesManager(profile_name="bmt_app_devops_us_east_1") # it is an IAM User
# bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1_assume_role") # it is an IAM role

# _bsm1 = BotoSesManager(profile_name="bmt_app_devops_us_east_1")
# _bsm2 = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
# bsm = _bsm1.assume_role(role_arn=f"arn:aws:iam::${_bsm2.aws_account_id}:role/bmt-sbx-sanhe-x-account-us-east-1", role_session_name="abc")

# ------------------------------------------------------------------------------
# OTest the boto session
# ------------------------------------------------------------------------------
bsm.print_who_am_i(masked=False)
aws_access_key_id, aws_secret_access_key, aws_session_token = get_credentials(bsm)
aws_access_key_id, aws_secret_access_key, aws_session_token = get_session_token(bsm)

# bsm_new = BotoSesManager(
#     region_name=bsm.aws_region,
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key,
#     aws_session_token=aws_session_token,
# )
# bsm.print_who_am_i(masked=False)
# get_credentials(bsm_new)
# get_session_token(bsm_new)
