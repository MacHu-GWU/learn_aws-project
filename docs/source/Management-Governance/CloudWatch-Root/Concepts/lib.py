# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

from boto_session_manager import BotoSesManager
from rich import print as rprint


def get_log_group(
    bsm: BotoSesManager,
    group_name: str,
) -> T.Optional[dict]:
    res = bsm.cloudwatchlogs_client.describe_log_groups(
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
    bsm: BotoSesManager,
    group_name: str,
) -> bool:
    group = get_log_group(bsm, group_name)
    if group is None:
        bsm.cloudwatchlogs_client.create_log_group(logGroupName=group_name)
        return True
    else:
        return False


def get_log_stream(
    bsm: BotoSesManager,
    group_name: str,
    stream_name: str,
) -> T.Optional[dict]:
    res = bsm.cloudwatchlogs_client.describe_log_streams(
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
    bsm: BotoSesManager,
    group_name: str,
    stream_name: str,
) -> bool:
    stream = get_log_stream(bsm, group_name, stream_name)
    if stream is None:
        bsm.cloudwatchlogs_client.create_log_stream(
            logGroupName=group_name,
            logStreamName=stream_name,
        )
        return True
    else:
        return False


EPOCH = datetime(1970, 1, 1)


def get_now_ts() -> int:
    return int((datetime.utcnow() - EPOCH).total_seconds() * 1000)


@dataclasses.dataclass
class Event:
    message: str
    timestamp: int = dataclasses.field(default_factory=get_now_ts)


def put_log_events(
    bsm: BotoSesManager,
    group_name: str,
    stream_name: str,
    events: T.List[Event],
) -> T.Optional[dict]:
    if len(events) == 0:
        return None
    res = bsm.cloudwatchlogs_client.put_log_events(
        logGroupName=group_name,
        logStreamName=stream_name,
        logEvents=[dataclasses.asdict(event) for event in events],
    )
    return res


bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
