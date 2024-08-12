# -*- coding: utf-8 -*-

from pprint import pprint
import boto3

s3_client = boto3.client("s3")


def main(bucket: str, key: str) -> int:
    return s3_client.get_object(Bucket=bucket, Key=key)["ContentLength"]


def lambda_handler(event: dict, context):
    print("----- event -----")
    pprint(event)
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    return main(bucket=bucket, key=key)
