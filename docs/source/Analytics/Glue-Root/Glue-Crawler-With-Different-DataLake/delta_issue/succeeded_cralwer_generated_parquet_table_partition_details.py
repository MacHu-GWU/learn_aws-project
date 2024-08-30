import datetime

dct = {
    "Partition": {
        "Values": ["2005"],
        "DatabaseName": "glue_crawler_test",
        "TableName": "parquet_example_has_partition",
        "CreationTime": datetime.datetime(2024, 8, 30, 9, 29, 39, tzinfo=tzlocal()),
        "LastAccessTime": datetime.datetime(2024, 8, 30, 9, 29, 39, tzinfo=tzlocal()),
        "StorageDescriptor": {
            "Columns": [
                {"Name": "id", "Type": "bigint"},
                {"Name": "name", "Type": "string"},
                {"Name": "create_time", "Type": "timestamp"},
            ],
            "Location": "s3://bmt-app-dev-us-east-1-data/projects/learn_aws/glue_crawler/databases/glue_crawler_test/parquet_example_has_partition/year=2005/",
            "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
            "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
            "Compressed": False,
            "NumberOfBuckets": -1,
            "SerdeInfo": {
                "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
                "Parameters": {"serialization.format": "1"},
            },
            "BucketColumns": [],
            "SortColumns": [],
            "Parameters": {
                "sizeKey": "7620",
                "objectCount": "1",
                "recordCount": "107",
                "averageRecordSize": "102",
                "compressionType": "none",
                "classification": "parquet",
                "typeOfData": "file",
            },
            "StoredAsSubDirectories": False,
        },
        "Parameters": {},
        "CatalogId": "878625312159",
    },
}
