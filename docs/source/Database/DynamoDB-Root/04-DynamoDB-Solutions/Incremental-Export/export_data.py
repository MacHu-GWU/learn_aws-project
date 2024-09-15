# -*- coding: utf-8 -*-

import gzip
import polars as pl
from datetime import datetime, timezone, timedelta

from s3pathlib import S3Path
from aws_dynamodb_io.api import ExportJob, ExportFormatEnum, ExportTypeEnum
from simpletype.api import String, Integer
from dynamodb_json_seder.api import deserialize_df

from gen_data import (
    Measurement,
    tb_name,
    bsm,
)


bucket = f"{bsm.aws_account_alias}-{bsm.aws_region}-data"
s3dir_root = S3Path(
    f"s3://{bucket}/projects/learn_aws/dynamodb-solutions/incremental-export/"
).to_dir()
table_arn = f"arn:aws:dynamodb:{bsm.aws_region}:{bsm.aws_account_id}:table/{tb_name}"
simple_schema = {
    "id": String(),
    "time": String(),
    "value": Integer(),
}
polars_schema = {k: v.to_dynamodb_json_polars() for k, v in simple_schema.items()}


def export_initial_data():
    export_job = ExportJob.export_table_to_point_in_time(
        dynamodb_client=bsm.dynamodb_client,
        table_arn=table_arn,
        s3_bucket=s3dir_root.bucket,
        s3_prefix=s3dir_root.key,
        export_time=datetime(2024, 9, 14, 23, 5, 0).astimezone(timezone.utc),
        export_format=ExportFormatEnum.DYNAMODB_JSON.value,
    )
    print(f"export_arn = {export_job.arn}")


def export_incremental_data():
    export_job = ExportJob.export_table_to_point_in_time(
        dynamodb_client=bsm.dynamodb_client,
        table_arn=table_arn,
        s3_bucket=s3dir_root.bucket,
        s3_prefix=s3dir_root.key,
        export_format=ExportFormatEnum.DYNAMODB_JSON.value,
        export_type=ExportTypeEnum.INCREMENTAL_EXPORT.value,
        incremental_export_specification=dict(
            ExportFromTime=datetime(2024, 9, 14, 23, 5, 0).astimezone(timezone.utc),
            ExportToTime=datetime(2024, 9, 14, 23, 20, 0).astimezone(timezone.utc),
        ),
    )
    print(f"export_arn = {export_job.arn}")


def read_df_from_init_export(export_job: ExportJob):
    data_file_list = export_job.get_data_files(bsm.dynamodb_client, bsm.s3_client)
    sub_df_list = list()
    for data_file in data_file_list:
        s3path = S3Path(f"s3://{bucket}/{data_file.s3_key}")
        b = s3path.read_bytes(bsm=bsm)
        sub_df = pl.read_ndjson(
            gzip.decompress(b),
            schema={"Item": pl.Struct(polars_schema)},
        )
        sub_df_list.append(sub_df)
    df = pl.concat(sub_df_list)
    df = deserialize_df(df, simple_schema, dynamodb_json_col="Item")
    return df


def read_df_from_incr_export(export_job: ExportJob):
    data_file_list = export_job.get_data_files(bsm.dynamodb_client, bsm.s3_client)
    sub_df_list = list()
    for data_file in data_file_list:
        s3path = S3Path(f"s3://{bucket}/{data_file.s3_key}")
        b = s3path.read_bytes(bsm=bsm)
        sub_df = pl.read_ndjson(
            gzip.decompress(b),
            schema={"NewImage": pl.Struct(polars_schema)},
        )
        sub_df_list.append(sub_df)
    df = pl.concat(sub_df_list)
    df = deserialize_df(df, simple_schema, dynamodb_json_col="NewImage")
    return df


def exam_overlap(init_arn: str, incr_arn: str):
    init_export = ExportJob.describe_export(bsm.dynamodb_client, init_arn)
    incr_export = ExportJob.describe_export(bsm.dynamodb_client, incr_arn)
    df_init= read_df_from_init_export(init_export)
    df_incr = read_df_from_incr_export(incr_export)
    df_init = df_init.sort("time")
    df_incr = df_incr.sort("time")
    print(df_init.tail(1).to_dicts())
    print(df_incr.head(1).to_dicts())



if __name__ == "__main__":
    # export_initial_data()
    init_arn = "arn:aws:dynamodb:us-east-1:878625312159:table/incremental_export_poc-measurement/export/01726369892818-7b359b68"
    # export_incremental_data()
    incr_arn = "arn:aws:dynamodb:us-east-1:878625312159:table/incremental_export_poc-measurement/export/01726370424000-3dcd3992"
    exam_overlap(init_arn, incr_arn)
