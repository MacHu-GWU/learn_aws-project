# -*- coding: utf-8 -*-

"""
Reference:

- Using the AWS SDKs to interact with Amazon OpenSearch Serverless: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-sdk.html#serverless-sdk-python
"""

import typing as T
import json
import time
from datetime import datetime, timezone

import boto3
import botocore.exceptions
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from rich import print as rprint


def slugify(text: str) -> str:
    """
    Convert a string to slug.
    """
    return text.replace("_", "-")


def create_encryption_policy(
    oss_client,
    collection_name: str,
    verbose: bool = True,
) -> T.Optional[dict]:
    """
    Creates an encryption policy that matches the given collection.
    """
    try:
        response = oss_client.create_security_policy(
            description=f"Encryption policy for {collection_name} collection",
            name=f"{collection_name}-policy",
            policy=json.dumps(
                {
                    "Rules": [
                        {
                            "ResourceType": "collection",
                            "Resource": [
                                f"collection/{collection_name}",
                            ],
                        }
                    ],
                    "AWSOwnedKey": True,
                }
            ),
            type="encryption",
        )
        if verbose:
            print("Encryption policy created:")
            print(response)
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            print(
                "[ConflictException] "
                "The policy name or rules conflict with an existing policy."
            )
            return None
        else:
            raise error


def create_network_policy(
    oss_client,
    collection_name: str,
    verbose: bool = True,
) -> T.Optional[dict]:
    """
    Creates a network policy that matches the given collection.
    """
    try:
        response = oss_client.create_security_policy(
            description=f"Network policy for {collection_name} collections",
            name=f"{collection_name}-policy",
            policy=json.dumps(
                [
                    {
                        "Description": f"Public access for {collection_name} collection",
                        "Rules": [
                            {
                                "ResourceType": "dashboard",
                                "Resource": [
                                    f"collection/{collection_name}",
                                ],
                            },
                            {
                                "ResourceType": "collection",
                                "Resource": [
                                    f"collection/{collection_name}",
                                ],
                            },
                        ],
                        "AllowFromPublic": True,
                    },
                ]
            ),
            type="network",
        )
        if verbose:
            print("Network policy created:")
            print(response)
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            print(
                "[ConflictException] " "A network policy with this name already exists."
            )
            return None
        else:
            raise error


def create_access_policy(
    oss_client,
    collection_name: str,
    trusted_iam_entity_arns,
    verbose: bool = True,
) -> T.Optional[dict]:
    """
    Creates a data access policy that matches the given collection.
    """
    try:
        response = oss_client.create_access_policy(
            description=f"Data access policy for {collection_name} collections",
            name=f"{collection_name}-policy",
            policy=json.dumps(
                [
                    {
                        "Rules": [
                            {
                                "Resource": [f"index/{collection_name}/*"],
                                "Permission": [
                                    "aoss:CreateIndex",
                                    "aoss:DeleteIndex",
                                    "aoss:UpdateIndex",
                                    "aoss:DescribeIndex",
                                    "aoss:ReadDocument",
                                    "aoss:WriteDocument",
                                ],
                                "ResourceType": "index",
                            },
                            {
                                "Resource": [
                                    f"collection/{collection_name}",
                                ],
                                "Permission": [
                                    "aoss:CreateCollectionItems",
                                ],
                                "ResourceType": "collection",
                            },
                        ],
                        "Principal": trusted_iam_entity_arns,
                    }
                ]
            ),
            type="data",
        )
        if verbose:
            print("Access policy created:")
            print(response)
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            print("[ConflictException] An access policy with this name already exists.")
            return None
        else:
            raise error


def create_collection(
    oss_client,
    collection_name: str,
) -> T.Optional[dict]:
    """
    Creates a collection.

    Ref:

    - create_collection: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/create_collection.html
    """
    try:
        response = oss_client.create_collection(
            name=collection_name,
            type="SEARCH",
        )
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            print(
                "[ConflictException] "
                "A collection with this name already exists. Try another name."
            )
            return None
        else:
            raise error


def wait_for_collection_creation(
    oss_client,
    collection_name: str,
    verbose: bool = True,
) -> str:
    """
    Waits for the collection to become active
    """
    response = oss_client.batch_get_collection(names=[collection_name])
    # Periodically check collection status
    while response["collectionDetails"][0]["status"] == "CREATING":
        if verbose:
            print("Creating collection...")
        time.sleep(10)
        response = oss_client.batch_get_collection(names=[collection_name])
    if verbose:
        print("Collection successfully created:")
        print(response["collectionDetails"])
    # Extract the collection endpoint from the response
    host = response["collectionDetails"][0]["collectionEndpoint"]
    collection_endpoint = host.replace("https://", "")
    return collection_endpoint


def create_oss_object(
    boto_ses: boto3.session.Session,
    collection_endpoint: str,
) -> OpenSearch:
    credentials = boto_ses.get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        boto_ses.region_name,
        "aoss",
        session_token=credentials.token,
    )
    oss = OpenSearch(
        hosts=[{"host": collection_endpoint, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=10,
    )
    return oss


def test_connection(oss: OpenSearch):
    print("test opensearch serverless connection by listing indices ...")
    res = oss.cat.indices(format="json")
    rprint(res)


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


if __name__ == "__main__":
    # ------------------------------------------------------------------------------
    # Enter your aws profile, trusted iam entity arn, collection name, and index name
    # ------------------------------------------------------------------------------
    aws_profile = "awshsh_app_dev_us_east_1"
    boto_ses = boto3.session.Session(profile_name=aws_profile)
    aws_account_id = boto_ses.client("sts").get_caller_identity()["Account"]
    trusted_iam_entity_arns = [
        f"arn:aws:iam::{aws_account_id}:user/sanhe",
    ]
    collection_name = "oss-demo"
    index_name = "app_log"

    oss_client = boto_ses.client("opensearchserverless")

    # ------------------------------------------------------------------------------
    create_encryption_policy(oss_client, collection_name)
    create_network_policy(oss_client, collection_name)
    create_access_policy(oss_client, collection_name, trusted_iam_entity_arns)
    res = create_collection(oss_client, collection_name)
    if res is None:
        verbose = False
    else:
        verbose = True
    collection_endpoint = wait_for_collection_creation(
        oss_client, collection_name, verbose
    )
    oss = create_oss_object(boto_ses, collection_endpoint)
    # test_connection(oss)

    # ------------------------------------------------------------------------------
    #
    # ------------------------------------------------------------------------------
    # oss.indices.delete(index=index_name, ignore=[400, 404])
    res = oss.indices.create(
        index=index_name,
        body={
            "mappings": {
                "properties": {
                    "time": {"type": "date", "format": "epoch_millis"},
                    "log": {"type": "text"},
                }
            }
        },
        ignore=400,
    )
    if "error" not in res:
        print(res)

    oss.index(
        index=index_name,
        body={
            "time": get_utc_now(),
            "log": "login failed, username not found",
        },
        id="id-1",
    )

    res = oss.search(
        index=index_name,
        body={"query": {"match_all": {}}},
    )
    rprint(res)

    res = oss.search(
        index=index_name,
        body={"query": {"match": {"log": "failed"}}},
    )
    rprint(res)
