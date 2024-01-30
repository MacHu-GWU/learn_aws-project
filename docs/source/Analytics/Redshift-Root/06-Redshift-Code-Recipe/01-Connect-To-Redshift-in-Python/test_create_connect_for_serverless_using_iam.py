# -*- coding: utf-8 -*-

"""
This example shows how to connect to Redshift Serverless using redshift connector.
"""

import boto3
from pathlib import Path

import aws_redshift_helper.api as rs

# load your config
dir_here = Path(__file__).absolute().parent
path_config_serverless = dir_here / "config-serverless.json"
config_serverless = rs.Config.load(path_config_serverless)

# create boto session
boto_ses = boto3.session.Session(profile_name="awshsh_app_dev_us_east_1")

# create redshift connection
conn = rs.create_connect_for_serverless_using_iam(
    boto_ses=boto_ses,
    workgroup_name=config_serverless.workgroup,
)

rs.test_connection(conn)
