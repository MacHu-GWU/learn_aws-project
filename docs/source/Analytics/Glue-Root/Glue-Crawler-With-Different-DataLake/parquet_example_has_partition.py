# -*- coding: utf-8 -*-

import io
import uuid
import random

import polars as pl
from faker import Faker

from better_glue import Database, Crawler
from settings import bsm, aws_console, s3dir_db, database_name, iam_role

table_name = "parquet_example_has_partition"
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
    for (year,), sub_df in df.group_by("year"):
        sub_df = sub_df.drop("year")
        s3path = s3dir_tb.joinpath(f"year={year}", f"{uuid.uuid4()}.snappy_parquet")
        buffer = io.BytesIO()
        sub_df.write_parquet(buffer, compression="snappy")
        s3path.write_bytes(
            buffer.getvalue(), bsm=bsm, content_type="application/x-parquet"
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
            S3Targets=[
                dict(
                    Path=s3dir_tb.uri,
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
# run_crawler()
