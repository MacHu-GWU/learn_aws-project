# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import awswrangler as wr
from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context

# define aws credential and s3 location
class Config:
    aws_profile = "bmt_app_dev_us_east_1"
    bucket = "bmt-app-dev-us-east-1-data"
    prefix = "poc/2023-12-01-athena-in-python"
    glue_database = "athena_in_python"
    glue_table = "events"


bsm = BotoSesManager(profile_name=Config.aws_profile)
context.attach_boto_session(bsm.boto_ses)


if __name__ == "__main__":
    s3dir = S3Path(
        Config.bucket,
        Config.prefix,
        "events",
    ).to_dir()
    print(f"preview data at {s3dir.console_url}")

    databases = wr.catalog.databases(boto3_session=bsm.boto_ses)
    if Config.glue_database not in databases.values:
        wr.catalog.create_database(Config.glue_database, boto3_session=bsm.boto_ses)

    # generate dummy data
    n_rows = 1000
    df = pd.DataFrame()
    df["id"] = range(1, n_rows + 1)
    df["time"] = pd.date_range(start="2000-01-01", end="2000-03-31", periods=n_rows)
    df["category"] = np.random.randint(1, 1 + 3, size=n_rows)
    df["value"] = np.random.randint(1, 1 + 100, size=n_rows)

    # write csv to s3
    wr.s3.to_csv(
        df=df,
        path=s3dir.uri,
        dataset=True,
        database=Config.glue_database,
        table=Config.glue_table,
        mode="overwrite",
        boto3_session=bsm.boto_ses,
    )
