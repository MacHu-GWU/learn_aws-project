# -*- coding: utf-8 -*-

import json
import textwrap
from pathlib import Path
from datetime import datetime

import boto3
import pandas as pd
import awswrangler as wr
from s3pathlib import S3Path, context
from rich import print as rprint

import aws_redshift_helper.api as rs

config = rs.Config.load(Path("config-serverless.json"))
boto_ses = boto3.session.Session(profile_name=config.aws_profile)
context.attach_boto_session(boto_ses)
aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]
aws_region = boto_ses.region_name
rs_sls_client = boto_ses.client("redshift-serverless")
rs_data_client = boto_ses.client("redshift-data")
database, _, _ = rs.get_database_by_workgroup(rs_sls_client, config.workgroup)
bucket = f"{aws_account_id}-{aws_region}-data"
s3dir_staging = S3Path(
    f"s3://{bucket}/projects/redshift-serverless-poc/staging/"
).to_dir()
s3dir_unload = S3Path(
    f"s3://{bucket}/projects/redshift-serverless-poc/unload/"
).to_dir()
conn = rs.create_connect_for_serverless_using_iam(
    boto_ses=boto_ses,
    workgroup_name=config.workgroup,
)
T_TRANSACTIONS = "transactions"
T_JSON_TEST = "json_test"


def run_sql(
    sql: str,
    no_result: bool = False,
):
    """
    A wrapper to automatically set parameters other than ``sql`` for ``run_sql``
    function.
    """
    columns, rows = rs.run_sql(
        rs_data_client=rs_data_client,
        sql=sql,
        database=database,
        workgroup_name=config.workgroup,
        delay=1,
        timeout=10,
        no_result=no_result,
    )
    rprint(columns, rows)


def drop_table():
    run_sql(sql=f"DROP TABLE IF EXISTS {T_JSON_TEST};", no_result=True)


def create_table():
    sql = textwrap.dedent(
        f"""
    CREATE TABLE IF NOT EXISTS {T_JSON_TEST}(
        id VARCHAR(255) NOT NULL,
        create_at TIMESTAMP NOT NULL,
        data SUPER NOT NULL,
        PRIMARY KEY (id, create_at)
    )
    distkey(id)
    sortkey(create_at);
    """
    )
    run_sql(sql=sql, no_result=True)


def delete_table():
    run_sql(sql=f"DELETE FROM {T_JSON_TEST};", no_result=True)


def get_utc_now():
    return datetime.utcnow()


def load_data():
    df = pd.DataFrame(
        {
            "id": ["id-1"],
            "create_at": [get_utc_now()],
            # just use dictionary to represent JSON object
            "data": [
                {
                    "name": "Alice",
                    "age": 25,
                    "tags": ["cool", "tall", "smart", "beauty"],
                },
            ],
        }
    )
    # awswrangler will dump the data to parquet file, parquet is schema self-contained format
    wr.redshift.copy(
        df=df,
        path=s3dir_staging.uri,
        con=conn,
        schema="public",
        table=T_JSON_TEST,
        mode="append",  # append, overwrite or upsert.
        boto3_session=boto_ses,
        primary_keys=["id"],
        # add this option if you have json field and need to load to SUPER data type column
        serialize_to_json=True,
    )


def select_data():
    run_sql(sql=f"SELECT * FROM {T_JSON_TEST};")


def unload_data():
    s3dir_unload.delete()
    sql = f"SELECT * FROM {T_TRANSACTIONS}"
    final_sql = rs.build_unload_sql(
        raw_sql=sql,
        s3_uri=s3dir_unload.uri,
        format="JSON",
    )
    run_sql(sql=final_sql, no_result=True)

    rows = list()
    for s3path in s3dir_unload.iter_objects():
        for line in s3path.read_text().split("\n"):
            if line:
                rows.append(json.loads(line))
    rprint(rows)


if __name__ == "__main__":
    # create_table()
    # drop_table()
    # delete_table()
    # load_data()
    # select_data()
    unload_data()
