# -*- coding: utf-8 -*-

"""
This script tests the connection to a local OpenSearch container.
"""

from datetime import datetime, timezone

from opensearchpy import OpenSearch
from rich import print as rprint


def create_oss_for_local_container(test_conn: bool = True) -> OpenSearch:
    """
    If you are using the OpenSearch Docker image for local developing following
    this https://hub.docker.com/r/opensearchproject/opensearch,
    and you are using this command to start the container:
    ``docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" --name opensearch-node -d opensearchproject/opensearch:latest``
    then this function should give you the right OSS object.
    """
    oss = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "admin"),
        http_compress=True,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        timeout=300,
    )
    if test_conn:
        res = oss.cat.indices(format="json")
        print(res)
    return oss


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


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


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


if __name__ == "__main__":
    oss = create_oss_for_local_container(test_conn=False)
    index_name = "app_log"

    # delete_index()
    create_index()
    # insert_document()
    # search_all()
    # search_by_fts()
