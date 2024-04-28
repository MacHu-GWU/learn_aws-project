# -*- coding: utf-8 -*-

"""
This script creates a test index, insert a document and search it.
Reference:

- Low-level Python client: https://opensearch.org/docs/latest/clients/python-low-level/
"""

from datetime import datetime, timezone

import boto3
from rich import print as rprint

from config import aws_profile, collection_name, index_name
from create_and_configure import create_oss_object_by_collection_name


def delete_index():
    res = oss.indices.delete(index=index_name, ignore=[400, 404])
    # print(res)


def create_index():
    res = oss.indices.create(
        index=index_name,
        body={
            "mappings": {
                "properties": {
                    "time": {"type": "date"},
                    "log": {"type": "text"},
                }
            }
        },
        ignore=400,
    )
    # print(res)


def insert_document():
    oss.index(
        index=index_name,
        id="id-1",
        body={
            "time": get_utc_now(),
            "log": "login failed, username not found",
        },
    )


def search_all():
    res = oss.search(
        index=index_name,
        body={"query": {"match_all": {}}},
    )
    rprint(res)


def search_by_fts():
    res = oss.search(
        index=index_name,
        body={"query": {"match": {"log": "failed"}}},
    )
    rprint(res)


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


if __name__ == "__main__":
    boto_ses = boto3.session.Session(profile_name=aws_profile)
    oss = create_oss_object_by_collection_name(boto_ses, collection_name)

    # delete_index()
    create_index()
    # insert_document()
    # search_all()
    # search_by_fts()
