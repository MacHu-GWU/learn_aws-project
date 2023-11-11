# -*- coding: utf-8 -*-

import typing as T
import json
import time
import random
import dataclasses
from datetime import datetime

from boto_session_manager import BotoSesManager
from rich import print as rprint

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")


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
    bsm: BotoSesManager, group_name: str, stream_name: str
) -> T.Optional[dict]:
    res = bsm.cloudwatchlogs_client.describe_log_streams(
        logGroupName=group_name,
        logStreamNamePrefix=stream_name,
    )
    streams = [
        dct
        for dct in res.get("logStreams", [])
        if dct.get("logStreamName", "unknown-log-stream-name") == group_name
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


@dataclasses.dataclass
class PerformanceMessage:
    payload_size: int
    response_time: int

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))

    @classmethod
    def from_json(cls, js: str):
        return cls(**json.loads(js))


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


log_group = "/my-lob-1/my-model-1"
log_stream = "my-metric-1"

# flag = create_log_group(bsm, log_group)
# print(flag)

# flag = create_log_stream(bsm, log_group, log_stream)
# print(flag)


def make_events(n: int):
    events = list()
    for _ in range(n):
        event = Event(
            message=PerformanceMessage(
                payload_size=random.randint(100, 1000),
                response_time=random.randint(50, 3000),
            ).to_json(),
        )
        events.append(event)
        time.sleep(random.randint(500, 1500) / 1000)
    return events

res = bsm.cloudwatchlogs_client.put_metric_filter(
    logGroupName=log_group,
    filterName="my-filter",
    filterPattern="[response_time]",
    metricTransformations=[
        {
            'metricName': 'model-response-time',
            'metricNamespace': '/model-monitoring',
            'metricValue': '$response_time',
            'defaultValue': 0,
        },
    ]
)
rprint(res)