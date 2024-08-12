# -*- coding: utf-8 -*-

from pprint import pprint
import json
import boto3
import base64

s3_client = boto3.client("s3")


def main(bucket: str, key: str) -> int:
    return s3_client.get_object(Bucket=bucket, Key=key)["ContentLength"]


def lambda_handler(event: dict, context):
    print("----- event -----")
    pprint(event)

    # event triggered
    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        print("event invocation")
        return main(bucket, key)
    except:
        pass

    # step function invocation
    # get input arg from s3
    if "exec_arn" in event:
        exec_arn = event["exec_arn"]
        bucket = "bmt-app-dev-us-east-1-data"

        filename = base64.b64encode(exec_arn.encode("utf-8")).decode("utf-8")
        key = f"projects/tmp/sfn-exec/{filename}.json"
        res = s3_client.get_object(Bucket=bucket, Key=key)
        data = json.loads(res["Body"].read().decode("utf-8"))
        print("----- data -----")
        pprint(data)
        params = data["task1"]
        return main(**params)

    # request, response styled invocation
    return main(**event)
