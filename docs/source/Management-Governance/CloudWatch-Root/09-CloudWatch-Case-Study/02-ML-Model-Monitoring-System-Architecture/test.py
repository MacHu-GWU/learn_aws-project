# -*- coding: utf-8 -*-

import typing as T
import json
import enum
from datetime import datetime, timedelta, timezone

from rich import print as rprint

from python_lib.config import bsm, logs_client, group_name, stream_name_1, stream_name_2
from python_lib.better_boto import (
    create_log_group,
    create_log_stream,
    put_log_events,
    delete_log_group,
    delete_log_stream,
    Event,
    run_query,
    reformat_query_results,
)

# delete_log_group(logs_client, group_name)
# create_log_group(logs_client, group_name)


def put_messages(records: T.List[T.Dict[str, T.Any]]) -> dict:
    return put_log_events(
        logs_client,
        group_name,
        stream_name_1,
        events=[Event(message=json.dumps(record)) for record in records],
    )


records = [
    # {"type": "inference_time", "server_id": stream_name_1, "elapsed": 250},
    # {"type": "cpu_usage", "server_id": stream_name_1, "cpu_usage": 70},
    {"type": "trace", "info": "hello world alice bob cathy is here"},
]
# put_messages(records)

query = """
fields @timestamp, @message, type, info
| filter info like "alice" OR info like "GOD"
| sort @timestamp desc
"""
now = datetime.utcnow().replace(tzinfo=timezone.utc)
five_minutes_ago = now - timedelta(minutes=15)
query_id, res = run_query(
    logs_client=logs_client,
    start_datetime=five_minutes_ago,
    end_datetime=now,
    query=query,
    log_group_name=group_name,
    limit=10,
)
# print(query_id)
# rprint(res)
records = reformat_query_results(res)
rprint(records)
