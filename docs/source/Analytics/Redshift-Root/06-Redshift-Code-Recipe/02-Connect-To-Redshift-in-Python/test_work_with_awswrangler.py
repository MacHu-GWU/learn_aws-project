# -*- coding: utf-8 -*-

"""
This example shows how to use awswrangler to work with Redshift Serverless.
"""

import boto3
from pathlib import Path

import pandas as pd
import awswrangler as wr

import pylib.api as pylib


def create_table_and_load_data():
    df = pd.DataFrame(
        [
            (
                "d87e0557-447c-4743-a527-cd26b59720b9",
                "2023-08-09T14:04:58.919920",
                "2023-08-09T14:04:58.919920",
                "note 111",
            ),
            (
                "959a2aec-b560-4b1e-9b59-cdca5546f091",
                "2023-08-09T14:04:58.919920",
                "2023-08-09T14:04:58.919920",
                "note 2",
            ),
        ],
        columns=["id", "create_at", "update_at", "note"],
    )
    wr.redshift.copy(
        df=df,
        path=s3_dir_uri,
        con=conn,
        schema="public",
        table=TABLE_NAME,
        mode="overwrite",  # append, overwrite or upsert.
        boto3_session=boto_ses,
        primary_keys=["id"],
    )


def read_dataframe():
    print("Read data from Redshift into pandas dataframe")
    sql = f"SELECT * FROM {TABLE_NAME} LIMIT 10;"
    df = wr.redshift.read_sql_query(sql, con=conn)
    print(df)


# load your config
dir_here = Path(__file__).absolute().parent
path_config_serverless = dir_here / "config-serverless.json"
config_serverless = pylib.Config.load(path_config_serverless)

# create boto session
boto_ses = boto3.session.Session(profile_name="awshsh_app_dev_us_east_1")
aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]
aws_region = boto_ses.region_name

# create redshift connection
conn = pylib.create_connect_for_serverless_using_iam(
    boto_ses=boto_ses,
    workgroup_name=config_serverless.workgroup,
)

pylib.test_connection(conn)

# write data and read data
bucket = f"{aws_account_id}-{aws_region}-data"
s3_dir_uri = f"s3://{bucket}/project/redshift-serverless-poc/"
TABLE_NAME = "transactions"

create_table_and_load_data()
read_dataframe()
