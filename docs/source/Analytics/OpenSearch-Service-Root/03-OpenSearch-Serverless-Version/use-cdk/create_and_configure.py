# -*- coding: utf-8 -*-

"""
A simple script to create and configure an OpenSearch serverless collection,
then you can create index, index data, search documents.

Requirements: see ``requirements.txt``

Reference:

- Using the AWS SDKs to interact with Amazon OpenSearch Serverless: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-sdk.html#serverless-sdk-python
"""

import typing as T
import json
import time
import dataclasses

import boto3
import botocore.exceptions
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


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
            name=f"{collection_name}-policy",
            description=f"Encryption policy for {collection_name} collection",
            type="encryption",
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
        )
        if verbose:
            print("Encryption policy created:")
            print(response)
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            if verbose:
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
    The dashboard and collection are both public accessible.
    """
    try:
        response = oss_client.create_security_policy(
            name=f"{collection_name}-policy",
            description=f"Network policy for {collection_name} collections",
            type="network",
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
        )
        if verbose:
            print("Network policy created:")
            print(response)
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            if verbose:
                print(
                    "[ConflictException] "
                    "A network policy with this name already exists."
                )
            return None
        else:
            raise error


@dataclasses.dataclass
class IamUser:
    name: str

    def to_arn(self, aws_account_id: str):
        return f"arn:aws:iam::{aws_account_id}:user/{self.name}"


@dataclasses.dataclass
class IamRole:
    name: str

    def to_arn(self, aws_account_id: str):
        return f"arn:aws:iam::{aws_account_id}:role/{self.name}"


def create_access_policy(
    oss_client,
    collection_name: str,
    aws_account_id: str,
    trusted_iam_entity_arns: T.List[str],
    verbose: bool = True,
) -> T.Optional[dict]:
    """
    Creates a data access policy that matches the given collection,
    it allows the given IAM entities to access the collection.
    """
    try:
        response = oss_client.create_access_policy(
            name=f"{collection_name}-policy",
            description=f"Data access policy for {collection_name} collections",
            type="data",
            policy=json.dumps(
                [
                    {
                        "Rules": [
                            {
                                "Resource": [
                                    f"index/{collection_name}/*",
                                ],
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
        )
        if verbose:
            print("Access policy created:")
            print(response)
        return response
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "ConflictException":
            if verbose:
                print(
                    "[ConflictException] "
                    "An access policy with this name already exists."
                )
            return None
        else:
            raise error


def create_collection(
    oss_client,
    collection_name: str,
    verbose: bool = True,
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
            if verbose:
                print(
                    "[ConflictException] "
                    "A collection with this name already exists. Try another name."
                )
            return None
        else:
            raise error


def _get_endpoint_from_connection_details(connection_details: dict) -> str:
    return connection_details["collectionEndpoint"].replace("https://", "")


def wait_for_collection_creation(
    oss_client,
    collection_name: str,
    verbose: bool = True,
) -> str:
    """
    Waits for the collection to become active.

    :return: the collection endpoint.
    """
    response = oss_client.batch_get_collection(names=[collection_name])
    # Periodically check collection status
    while True:
        collection_details = response["collectionDetails"][0]
        status = collection_details["status"]
        if status == "CREATING":
            if verbose:
                print("Creating collection...")
            time.sleep(10)
            response = oss_client.batch_get_collection(names=[collection_name])
        elif status == "ACTIVE":
            if verbose:
                print("Collection successfully created:")
            return _get_endpoint_from_connection_details(collection_details)
        else:
            raise SystemError(f"status is {status!r}!")


def create_oss_object_by_collection_endpoint(
    boto_ses: boto3.session.Session,
    collection_endpoint: str,
) -> OpenSearch:
    """
    Create the opensearch-py SDK OpenSearch object from the boto3 session.
    """
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
        timeout=300,
    )
    return oss


def create_oss_object_by_collection_name(
    boto_ses: boto3.session.Session,
    collection_name: str,
) -> OpenSearch:
    oss_client = boto_ses.client("opensearchserverless")
    collection_endpoint = wait_for_collection_creation(
        oss_client, collection_name, False
    )
    return create_oss_object_by_collection_endpoint(boto_ses, collection_endpoint)


def test_oss_connection(
    oss: OpenSearch,
    verbose: bool = True,
):
    if verbose:
        print("test opensearch serverless connection by listing indices ...")
    res = oss.cat.indices(format="json")
    if verbose:
        print(res)
        print("success!")


def create_and_configure(
    aws_profile: str,
    collection_name: str,
    verbose: bool = True,
) -> OpenSearch:
    boto_ses = boto3.session.Session(profile_name=aws_profile)
    res = boto_ses.client("sts").get_caller_identity()
    aws_account_id = res["Account"]
    iam_entity_arn = res["Arn"]
    oss_client = boto_ses.client("opensearchserverless")
    create_encryption_policy(oss_client, collection_name, verbose)
    create_network_policy(oss_client, collection_name, verbose)
    create_access_policy(
        oss_client,
        collection_name,
        aws_account_id,
        [iam_entity_arn],
        verbose,
    )
    res = create_collection(oss_client, collection_name, verbose)
    if res is None:
        verbose_ = False
    else:
        verbose_ = True
    collection_endpoint = wait_for_collection_creation(
        oss_client,
        collection_name,
        verbose_,
    )
    oss = create_oss_object_by_collection_endpoint(boto_ses, collection_endpoint)
    test_oss_connection(oss, verbose)
    return oss


def delete_collection(
    aws_profile: str,
    collection_name: str,
    verbose: bool = True,
):
    """
    Ref:

    - delete_collection: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless/client/delete_collection.html
    """
    boto_ses = boto3.session.Session(profile_name=aws_profile)
    oss_client = boto_ses.client("opensearchserverless")
    response = oss_client.batch_get_collection(names=[collection_name])
    collection_details = response["collectionDetails"]
    if len(collection_details) == 1:
        collection_id = collection_details[0]["id"]
        if verbose:
            print("Deleting collection...")
        response = oss_client.delete_collection(
            id=collection_id,
        )
        if verbose:
            print("done")
    else:
        if verbose:
            print("Collection not found")


if __name__ == "__main__":
    from config import aws_profile, collection_name

    oss = create_and_configure(aws_profile, collection_name, verbose=True)
    # delete_collection(aws_profile, collection_name, verbose=True)
