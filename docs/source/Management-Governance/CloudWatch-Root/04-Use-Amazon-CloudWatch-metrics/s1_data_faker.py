# -*- coding: utf-8 -*-

import typing as T
import time
import random
import dataclasses

from recipe import (
    create_log_group,
    delete_log_group,
    create_log_stream,
    Event,
    BaseJsonMessage,
    put_log_events,
)
from config import bsm, logs_client, aws, group_name, stream_name_1, stream_name_2


def set_up():
    """
    Set up cloudwatch logs resource for this example.
    """
    create_log_group(logs_client, group_name)
    create_log_stream(logs_client, group_name, stream_name_1)
    create_log_stream(logs_client, group_name, stream_name_2)
    print(aws.cloudwatch.get_log_group(group_name))


@dataclasses.dataclass
class StatusMessage(BaseJsonMessage):
    server_id: str = dataclasses.field()
    status: str = dataclasses.field()


@dataclasses.dataclass
class ProcessingTimeMessage(BaseJsonMessage):
    server_id: str = dataclasses.field()
    processing_time: int = dataclasses.field()


server_id_list = [stream_name_1, stream_name_2]


def rand_event() -> T.List[T.Union[ProcessingTimeMessage, StatusMessage]]:
    """
    70% chance it succeeds, 30% chance it fails. When succeeded, it will generate
    two messages, one for status and one for processing time. When failed, it will
    generate one failed message for status.
    """
    server_id = random.choice(server_id_list)
    stream_name = server_id
    if random.randint(1, 100) <= 70:
        messages = [
            StatusMessage(
                server_id=server_id,
                status="succeeded",
            ),
            ProcessingTimeMessage(
                server_id=server_id,
                processing_time=random.randint(1000, 10000),
            ),
        ]
    else:
        messages = [
            StatusMessage(
                server_id=server_id,
                status="failed",
            )
        ]
    put_log_events(
        bsm.cloudwatchlogs_client,
        group_name,
        stream_name,
        events=[Event(message=message.to_json()) for message in messages],
    )
    return messages


def run_data_faker():
    """
    Run :func:`rand_event` every 1 second.

    Ref: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/cloudwatch_limits_cwl.html

    The maximum batch size of a PutLogEvents request is 1MB.

    **800** transactions per second per account per Region, except for the following Regions where the quota is 1500 transactions per second per account per Region: US East (N. Virginia), US West (Oregon), and Europe (Ireland). You can request an increase to the per-second throttling quota by using the Service Quotas service.
    """
    ith = 0
    while True:
        ith += 1
        print(f"ith: {ith} sec")
        time.sleep(1)
        messages = rand_event()
        for message in messages:
            print(f"  {message}")


def clean_up():
    """
    Clearn up cloudwatch logs resource for this example.
    """
    delete_log_group(logs_client, group_name)


if __name__ == "__main__":
    set_up()
    run_data_faker()
    # clean_up()
