# -*- coding: utf-8 -*-

"""
这是我研究出来的如何用 `delta-rs <https://github.com/delta-io/delta-rs>`_ Python
进行写入, 但是用 Glue Table 作为元数据, 使得之后可以直接用 Athena 查询的方法.
"""

import polars as pl
from faker import Faker

from better_glue import Database, Table
from settings import bsm, aws_console, s3dir_db, database_name

table_name = "delta_example_hpmct"
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

    df = pl.DataFrame(
        [
            {"id": 1, "name": "Alice", "year": "2001"},
            {"id": 2, "name": "Bob", "year": "2001"},
        ]
    )
    df.write_delta(
        s3dir_tb.uri,
        mode="append",
        delta_write_options=dict(
            partition_by=["year"],
        ),
        storage_options=storage_options,
    )

    df = pl.DataFrame(
        [
            {"id": 2, "name": "Bobby", "year": "2001"},
            {"id": 3, "name": "Cathy", "year": "2001"},
        ]
    )
    table_merger = df.write_delta(
        s3dir_tb.uri,
        mode="merge",
        delta_write_options=dict(
            partition_by=["year"],
        ),
        delta_merge_options=dict(
            predicate="s.id = t.id",
            source_alias="s",
            target_alias="t",
        ),
        storage_options=storage_options,
    )
    (
        table_merger.when_matched_update_all()  # will do update
        .when_not_matched_insert_all()  # will do insert
        .execute()
    )


def create_database():
    print("create database ...")
    db = Database.get(glue_client=bsm.glue_client, name=database_name)
    if db is None:
        bsm.glue_client.create_database(DatabaseInput=dict(Name=database_name))


def create_table():
    tb = Table.get(glue_client=bsm.glue_client, database=database_name, name=table_name)
    if tb is not None:
        bsm.glue_client.delete_table(DatabaseName=database_name, Name=table_name)

    bsm.glue_client.create_table(
        DatabaseName=database_name,
        TableInput=dict(
            Name=table_name,
            StorageDescriptor=dict(
                Columns=[
                    {"Name": "id", "Type": "bigint", "Comment": ""},
                    {"Name": "name", "Type": "string", "Comment": ""},
                ],
                Location=s3dir_tb.uri,
                InputFormat="org.apache.hadoop.mapred.SequenceFileInputFormat",
                OutputFormat="org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat",
                Compressed=False,
                NumberOfBuckets=-1,
                SerdeInfo={
                    "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
                    "Parameters": {
                        "serialization.format": "1",
                        "path": s3dir_tb.uri,
                    },
                },
                BucketColumns=[],
                SortColumns=[],
            ),
            Parameters={
                "EXTERNAL": "true",
                "spark.sql.sources.schema.part.0": '{"type":"struct","fields":[{"name":"id","type":"long","nullable":false,"metadata":{}},{"name":"name","type":"string","nullable":true,"metadata":{}}]}',
                "CrawlerSchemaSerializerVersion": "1.0",
                "CrawlerSchemaDeserializerVersion": "1.0",
                "spark.sql.partitionProvider": "catalog",
                "classification": "delta",
                "spark.sql.sources.schema.numParts": "1",
                "spark.sql.sources.provider": "delta",
                "delta.lastUpdateVersion": "6",
                "delta.lastCommitTimestamp": "1653462383292",
                "table_type": "delta",
            },
            PartitionKeys=[
                {"Name": "year", "Type": "string"},
            ],
            TableType="EXTERNAL_TABLE",
        ),
    )


# prepare_data()
# create_database()
# create_table()
# run_crawler()
