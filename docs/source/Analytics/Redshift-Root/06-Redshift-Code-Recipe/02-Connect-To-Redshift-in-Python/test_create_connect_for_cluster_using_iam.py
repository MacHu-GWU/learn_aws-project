# -*- coding: utf-8 -*-

"""
This example shows how to connect to Redshift Serverless using redshift connector.
"""

import boto3
from pathlib import Path

import pylib.api as pylib

# load your config
dir_here = Path(__file__).absolute().parent
path_config_cluster = dir_here / "config-cluster.json"
config_cluster = pylib.Config.load(path_config_cluster)

# create boto session
boto_ses = boto3.session.Session(profile_name="awshsh_app_dev_us_east_1")

# create redshift connection
conn = pylib.create_connect_for_cluster_using_iam(
    boto_ses=boto_ses,
    cluster_id=config_cluster.cluster_id,
)

pylib.test_connection(conn)
