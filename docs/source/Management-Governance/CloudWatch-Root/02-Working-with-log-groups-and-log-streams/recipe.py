# -*- coding: utf-8 -*-

"""
A helper module to work with CloudWatch Logs Group, Stream and put log events.

Usage:

.. code-block:: python

    from recipe import (
        get_log_group,
        create_log_group,
        delete_log_group,
        get_log_stream,
        create_log_stream,
        delete_log_stream,
        Event,
        BaseJsonMessage,
        put_log_events,
    )
"""

import typing as T
import json
import dataclasses
from datetime import datetime


def get_log_group(
    logs_client,
    group_name: str,
) -> T.Optional[dict]:
    """
    Get a log group details by name, if it doesn't exist, return None.

    :return: A dict with the log group details, or None if it doesn't exist.
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_groups.html
    res = logs_client.describe_log_groups(
        logGroupNamePrefix=group_name,
    )
    groups = [
        dct
        for dct in res.get("logGroups", [])
        if dct.get("logGroupName", "unknown-log-group-name") == group_name
    ]
    if len(groups):
        return groups[0]
    else:
        return None


def create_log_group(
    logs_client,
    group_name: str,
) -> bool:
    """
    Create a log group, if it already exists, do nothing.

    :return: True if the log group was created, False if it already existed.
    """
    group = get_log_group(logs_client, group_name)
    if group is None:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_group.html
        logs_client.create_log_group(
            logGroupName=group_name,
        )
        return True
    else:
        return False


def delete_log_group(
    logs_client,
    group_name: str,
) -> bool:
    """
    Delete a log group, if it doesn't exist, do nothing.

    :return: True if the log group was deleted, False if it didn't exist.
    """
    group = get_log_group(logs_client, group_name)
    if group is None:
        return False
    else:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_group.html
        logs_client.delete_log_group(
            logGroupName=group_name,
        )
        return True


def get_log_stream(
    logs_client,
    group_name: str,
    stream_name: str,
) -> T.Optional[dict]:
    """
    Get a log stream details by name, if it doesn't exist, return None.

    :return: A dict with the log stream details, or None if it doesn't exist.
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_streams.html
    res = logs_client.describe_log_streams(
        logGroupName=group_name,
        logStreamNamePrefix=stream_name,
    )
    streams = [
        dct
        for dct in res.get("logStreams", [])
        if dct.get("logStreamName", "unknown-log-stream-name") == stream_name
    ]
    if len(streams):
        return streams[0]
    else:
        return None


def create_log_stream(
    logs_client,
    group_name: str,
    stream_name: str,
) -> bool:
    """
    Create a log stream, if it already exists, do nothing.

    :return: True if the log stream was created, False if it already existed.
    """
    stream = get_log_stream(logs_client, group_name, stream_name)
    if stream is None:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_stream.html
        logs_client.create_log_stream(
            logGroupName=group_name,
            logStreamName=stream_name,
        )
        return True
    else:
        return False


def delete_log_stream(
    logs_client,
    group_name: str,
    stream_name: str,
) -> bool:
    """
    Delete a log stream, if it doesn't exist, do nothing.

    :return: True if the log stream was deleted, False if it didn't exist.
    """
    stream = get_log_stream(logs_client, group_name, stream_name)
    if stream is None:
        return False
    else:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/delete_log_stream.html
        logs_client.delete_log_stream(
            logGroupName=group_name,
            logStreamName=stream_name,
        )
        return True


EPOCH = datetime(1970, 1, 1)


def get_now_ts() -> int:
    """
    The put log events API expects a timestamp in milliseconds since epoch.
    """
    return int((datetime.utcnow() - EPOCH).total_seconds() * 1000)


@dataclasses.dataclass
class Event:
    """
    Log event data model.
    """

    message: str = dataclasses.field()
    timestamp: int = dataclasses.field(default_factory=get_now_ts)


@dataclasses.dataclass
class BaseJsonMessage:
    """
    Base class for json encoded log message.
    """

    def to_json(self) -> str:
        """
        Convert the object to a json string.

        You can override this method to customize the json serialization.
        """
        return json.dumps(dataclasses.asdict(self))

    @classmethod
    def from_json(cls, json_str: str):
        """
        You can override this module to customize the json deserialization.
        """
        dct = json.loads(json_str)
        return cls(**dct)


def put_log_events(
    logs_client,
    group_name: str,
    stream_name: str,
    events: T.List[Event],
) -> T.Optional[dict]:
    """
    Put a list of events into a log stream.

    :param logs_client: The boto3 logs client.
    :param group_name: The log group name.
    :param stream_name: The log stream name.
    :param events: A list of :class:`Event` objects.

    :return: A dict with the response from the put_log_events call.
    """
    if len(events) == 0:
        return None
    res = logs_client.put_log_events(
        logGroupName=group_name,
        logStreamName=stream_name,
        logEvents=[dataclasses.asdict(event) for event in events],
    )
    return res
