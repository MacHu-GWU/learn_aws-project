# -*- coding: utf-8 -*-

"""
This example shows how to connect to Redshift Serverless using redshift connector.
"""

import boto3
from pathlib import Path

import pylib.api as pylib

# load your config
dir_here = Path(__file__).absolute().parent
path_config_serverless = dir_here / "config-serverless.json"
config_serverless = pylib.Config.load(path_config_serverless)

# create boto session
boto_ses = boto3.session.Session(profile_name="awshsh_app_dev_us_east_1")

# create redshift connection
conn = pylib.create_connect_for_serverless_using_iam(
    boto_ses=boto_ses,
    workgroup_name=config_serverless.workgroup,
)

pylib.test_connection(conn)
