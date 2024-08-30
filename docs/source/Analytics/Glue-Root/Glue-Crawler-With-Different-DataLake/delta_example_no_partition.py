# -*- coding: utf-8 -*-

import io
import uuid
import random

import polars as pl
from faker import Faker

from better_glue import Database, Crawler
from settings import bsm, aws_console, s3dir_db, database_name, iam_role

table_name = "delta_example_no_partition"
s3dir_tb = s3dir_db.joinpath(table_name).to_dir()
crawler_name = f"{database_name}__{table_name}"
fake = Faker()

database_url = aws_console.glue.get_database(database_or_arn=database_name)
table_url = aws_console.glue.get_table(table_or_arn=table_name, database=database_name)
crawler_url = aws_console.glue.get_crawler(name_or_arn=crawler_name)
print(f"table s3dir = {s3dir_tb.console_url}")
print(f"{database_url = }")
print(f"{table_url = }")
print(f"{crawler_url = }")

credential = bsm.boto_ses.get_credentials()
storage_options = {
    "AWS_REGION": bsm.aws_region,
    "AWS_ACCESS_KEY_ID": credential.access_key,
    "AWS_SECRET_ACCESS_KEY": credential.secret_key,
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
}


def prepare_data():
    print("prepare data ...")
    s3dir_tb.delete()
    n_records = 1000
    df = pl.DataFrame(
        {
            "id": range(1, 1 + n_records),
            "name": [fake.name() for _ in range(n_records)],
            "create_time": [
                fake.date_time().replace(year=random.randint(2001, 2010))
                for _ in range(n_records)
            ],
        }
    ).with_columns(pl.col("create_time").dt.year().alias("year"))
    df.write_delta(
        s3dir_tb.uri,
        mode="append",
        storage_options=storage_options,
    )


def create_database():
    print("create database ...")
    db = Database.get(glue_client=bsm.glue_client, name=database_name)
    if db is None:
        bsm.glue_client.create_database(DatabaseInput=dict(Name=database_name))


def create_crawler():
    print("create crawler ...")
    crawler = Crawler.get(
        glue_client=bsm.glue_client,
        name=crawler_name,
    )
    if crawler is not None:
        bsm.glue_client.delete_crawler(Name=crawler_name)
    crawler = bsm.glue_client.create_crawler(
        Name=crawler_name,
        Role=iam_role,
        DatabaseName=database_name,
        Targets=dict(
            DeltaTargets=[
                dict(
                    DeltaTables=[s3dir_tb.uri],
                    CreateNativeDeltaTable=True,
                ),
            ],
        ),
        RecrawlPolicy=dict(
            RecrawlBehavior="CRAWL_EVERYTHING",
        ),
    )


def run_crawler():
    print("run crawler ...")
    bsm.glue_client.start_crawler(Name=crawler_name)


# prepare_data()
# create_database()
# create_crawler()
run_crawler()
