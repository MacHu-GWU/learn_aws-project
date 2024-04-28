# -*- coding: utf-8 -*-

"""
A simple CDK stack to create and configure an OpenSearch serverless collection.
So you can create index, index data, search documents.
Please read the doc string in :class:`Stack` for more details.

Requirements: see ``requirements.txt``, or do ``pip install -r requirements.txt``.

Reference:

- https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_opensearchserverless.html
"""

import json

import aws_cdk as cdk
import aws_cdk.aws_opensearchserverless as oss
from constructs import Construct


class Stack(cdk.Stack):
    """
    We assume that you want to use IAM user to connect to the OpenSearch serverless
    collection.

    :param collection_name: the collection name, you can use alpha, letter, hyphen
        but not underscore.
    :param iam_entity_arn: the IAM entity arn that has the permission to manipulate
        the collection.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        collection_name: str,
        iam_entity_arn: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.encryption_policy = oss.CfnSecurityPolicy(
            self,
            "EncryptionPolicy",
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

        self.network_policy = oss.CfnSecurityPolicy(
            self,
            "NetworkPolicy",
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

        self.access_policy = oss.CfnAccessPolicy(
            self,
            "AccessPolicy",
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
                        "Principal": [
                            iam_entity_arn,
                        ],
                    }
                ]
            ),
        )

        self.collection = oss.CfnCollection(
            self,
            "OpenSearchServerlessCollection",
            name=collection_name,
            type="SEARCH",
        )
        self.collection.apply_removal_policy(cdk.RemovalPolicy.DESTROY)


if __name__ == "__main__":
    import boto3
    from config import aws_profile, collection_name, stack_name

    app = cdk.App()

    boto_ses = boto3.session.Session(profile_name=aws_profile)
    iam_entity_arn = boto_ses.client("sts").get_caller_identity()["Arn"]
    stack = Stack(
        app,
        construct_id=stack_name,
        collection_name=collection_name,
        iam_entity_arn=iam_entity_arn,
        stack_name=stack_name,
    )

    app.synth()
