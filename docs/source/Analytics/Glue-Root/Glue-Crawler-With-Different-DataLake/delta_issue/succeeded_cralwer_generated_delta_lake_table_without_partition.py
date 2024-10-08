import datetime

dct = {
    "Table": {
        "Name": "sample_delta_table",
        "DatabaseName": "glue_crawler_test",
        "Description": "",
        "CreateTime": datetime.datetime(2024, 8, 30, 9, 46, 25, tzinfo=tzlocal()),
        "UpdateTime": datetime.datetime(2024, 8, 30, 9, 51, 19, tzinfo=tzlocal()),
        "Retention": 0,
        "StorageDescriptor": {
            "Columns": [
                {"Name": "id", "Type": "bigint", "Comment": ""},
                {"Name": "name", "Type": "string", "Comment": ""},
                {"Name": "create_time", "Type": "timestamp", "Comment": ""},
            ],
            "Location": "s3://bmt-app-dev-us-east-1-data/projects/parquet_dynamodb/example/staging/sample_delta_table/",
            "AdditionalLocations": [],
            "InputFormat": "org.apache.hadoop.mapred.SequenceFileInputFormat",
            "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat",
            "Compressed": False,
            "NumberOfBuckets": -1,
            "SerdeInfo": {
                "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
                "Parameters": {
                    "serialization.format": "1",
                    "path": "s3://bmt-app-dev-us-east-1-data/projects/learn_aws/glue_crawler/databases/glue_crawler_test/delta_example_has_partition/",
                },
            },
            "BucketColumns": [],
            "SortColumns": [],
            "Parameters": {
                "UPDATED_BY_CRAWLER": "sample_delta_table",
                "EXTERNAL": "true",
                "spark.sql.sources.schema.part.0": '{"type":"struct","fields":[{"name":"product_id","type":"string","nullable":true,"metadata":{}},{"name":"product_name","type":"string","nullable":true,"metadata":{}},{"name":"price","type":"long","nullable":true,"metadata":{}},{"name":"CURRENCY","type":"string","nullable":true,"metadata":{}},{"name":"category","type":"string","nullable":true,"metadata":{}},{"name":"updated_at","type":"double","nullable":true,"metadata":{}}]}',
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
            "StoredAsSubDirectories": False,
        },
        "PartitionKeys": [],
        "TableType": "EXTERNAL_TABLE",
        "Parameters": {
            "UPDATED_BY_CRAWLER": "sample_delta_table",
            "EXTERNAL": "true",
            "spark.sql.sources.schema.part.0": '{"type":"struct","fields":[{"name":"product_id","type":"string","nullable":true,"metadata":{}},{"name":"product_name","type":"string","nullable":true,"metadata":{}},{"name":"price","type":"long","nullable":true,"metadata":{}},{"name":"CURRENCY","type":"string","nullable":true,"metadata":{}},{"name":"category","type":"string","nullable":true,"metadata":{}},{"name":"updated_at","type":"double","nullable":true,"metadata":{}}]}',
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
        "CreatedBy": "arn:aws:sts::878625312159:assumed-role/all-services-admin-role/AWS-Crawler",
        "IsRegisteredWithLakeFormation": False,
        "CatalogId": "878625312159",
        "VersionId": "2",
    },
}
