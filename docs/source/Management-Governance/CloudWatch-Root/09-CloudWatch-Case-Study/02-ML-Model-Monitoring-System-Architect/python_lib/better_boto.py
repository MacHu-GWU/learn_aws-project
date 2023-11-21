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
        get_ts_in_second,
        get_ts_in_millisecond,
        QueryStatusEnum,
        wait_logs_insights_query_to_succeed,
        run_query,
        reformat_query_results,
    )

Requirements:

    pip install "boto3-stubs[logs]"
"""

import typing as T
import time
import json
import enum
import dataclasses
from datetime import datetime, timezone

import botocore.exceptions

if T.TYPE_CHECKING:
    from mypy_boto3_logs import CloudWatchLogsClient


def get_log_group(
    logs_client: "CloudWatchLogsClient",
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
    logs_client: "CloudWatchLogsClient",
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
    logs_client: "CloudWatchLogsClient",
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
    logs_client: "CloudWatchLogsClient",
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
    logs_client: "CloudWatchLogsClient",
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
    logs_client: "CloudWatchLogsClient",
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


EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def get_now_ts() -> int:
    """
    The put log events API expects a timestamp in milliseconds since epoch.
    """
    return int(
        (datetime.utcnow().replace(tzinfo=timezone.utc) - EPOCH).total_seconds() * 1000
    )


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
    logs_client: "CloudWatchLogsClient",
    group_name: str,
    stream_name: str,
    events: T.List[Event],
    auto_create_stream: bool = True,
) -> T.Optional[dict]:
    """
    Put a list of events into a log stream.

    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_log_events.html

    :param logs_client: The boto3 logs client.
    :param group_name: The log group name.
    :param stream_name: The log stream name.
    :param events: A list of :class:`Event` objects.

    :return: A dict with the response from the put_log_events call.
    """
    if len(events) == 0:
        return None

    try:
        res = logs_client.put_log_events(
            logGroupName=group_name,
            logStreamName=stream_name,
            logEvents=[dataclasses.asdict(event) for event in events],
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            if auto_create_stream:
                create_log_stream(logs_client, group_name, stream_name)
                res = logs_client.put_log_events(
                    logGroupName=group_name,
                    logStreamName=stream_name,
                    logEvents=[dataclasses.asdict(event) for event in events],
                )
            else:
                raise e
        else:
            raise e
    return res


def get_ts(dt: datetime) -> float:
    """
    Convert a datetime object to a timestamp in seconds since epoch.

    It assumes the datetime object is in UTC if it doesn't have a timezone.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return (dt - EPOCH).total_seconds()


def get_ts_in_second(dt: datetime) -> int:
    """
    Convert a datetime object to a timestamp in seconds since epoch.
    """
    return int(get_ts(dt))


def get_ts_in_millisecond(dt: datetime) -> int:
    """
    Convert a datetime object to a timestamp in milliseconds since epoch.
    """
    return int(get_ts(dt) * 1000)


class QueryStatusEnum(str, enum.Enum):
    """
    Enum for the query status.

    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_query_results.html
    """

    Scheduled = "Scheduled"
    Running = "Running"
    Complete = "Complete"
    Failed = "Failed"
    Cancelled = "Cancelled"
    Timeout = "Timeout"
    Unknown = "Unknown"


def wait_logs_insights_query_to_succeed(
    logs_client: "CloudWatchLogsClient",
    query_id: str,
    delta: int = 1,
    timeout: int = 30,
) -> dict:
    """
    Wait a given athena query to reach ``Complete`` status. If failed,
    raise ``RuntimeError`` immediately. If timeout, raise ``TimeoutError``.

    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/get_query_results.html

    :param logs_client: The boto3 cloudwatch logs client.
    :param query_id: The query id from the response of ``start_query`` API call.
    :param delta: The time interval in seconds between each query status check.
    :param timeout: The maximum time in seconds to wait for the query to succeed.
    """
    elapsed = 0
    for _ in range(999999):
        res = logs_client.get_query_results(queryId=query_id)
        status = res["status"]
        if status == QueryStatusEnum.Complete.value:
            return res
        elif status in [
            QueryStatusEnum.Failed.value,
            QueryStatusEnum.Cancelled.value,
            QueryStatusEnum.Timeout.value,
        ]:
            raise RuntimeError(f"query {query_id} reached status: {status}")
        else:
            time.sleep(delta)
        elapsed += delta
        if elapsed > timeout:
            raise TimeoutError(f"logs insights query timeout in {timeout} seconds!")


def strip_out_limit_clause(query: str) -> str:
    """
    Strip out the limit clause from a query string.
    """
    lines = query.splitlines()
    return "\n".join([line for line in lines if not line.startswith("| limit")])


def run_query(
    logs_client: "CloudWatchLogsClient",
    start_datetime: datetime,
    end_datetime: datetime,
    query: str,
    log_group_name: T.Optional[str] = None,
    log_group_name_list: T.Optional[T.List[str]] = None,
    log_group_id_list: T.Optional[T.List[str]] = None,
    limit: int = 1000,
    delta: int = 1,
    timeout: int = 30,
) -> T.Tuple[str, dict]:
    """
    Run a logs insights query and wait for the query to succeed. It is a more
    human friendly wrapper of the ``start_query`` and ``get_query_results`` API.

    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/start_query.html

    :param logs_client: The boto3 cloudwatch logs client.
    :param start_datetime: python datetime object for start time,
        if timezone is not set, it assumes UTC.
    :param end_datetime: python datetime object for end time,
        if timezone is not set, it assumes UTC.
    :param query: The query string. don't use ``| limit abc`` in your query,
        use the ``limit`` parameter instead.
    :param log_group_name: see ``start_query`` API.
    :param log_group_name_list: see ``start_query`` API.
    :param log_group_id_list: see ``start_query`` API.
    :param limit: see ``start_query`` API.
    :param delta: The time interval in seconds between each query status check.
    :param timeout: The maximum time in seconds to wait for the query to succeed.
    """
    start_ts = get_ts_in_second(start_datetime)
    end_ts = get_ts_in_second(end_datetime)
    kwargs = dict(
        startTime=start_ts,
        endTime=end_ts,
        queryString=query,
        limit=limit,
    )
    if log_group_name is not None:
        kwargs["logGroupName"] = log_group_name
    elif log_group_name_list:
        kwargs["logGroupNames"] = log_group_name_list
    elif log_group_id_list:
        kwargs["logGroupIds"] = log_group_id_list
    else:  # it will raise error in API call
        pass
    res = logs_client.start_query(**kwargs)
    query_id = res["queryId"]
    res = wait_logs_insights_query_to_succeed(logs_client, query_id, delta, timeout)
    return query_id, res


def reformat_query_results(response: dict) -> T.List[dict]:
    """
    Convert the response from ``get_query_results`` API call to a more Pythonic
    format.

    :param response: the response from ``get_query_results`` API call.
    """
    return [
        {dct["field"]: dct["value"] for dct in result}
        for result in response.get("results", [])
    ]
