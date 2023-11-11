# -*- coding: utf-8 -*-

"""
Ref:

- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Counting404Responses.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_metric_filter.html
"""

import time
import json
import random
from lib import create_log_group, create_log_stream, put_log_events, bsm, Event

log_group = "/learn_cloudwatch_logs/processing_time"
log_stream = "my_stream_1"

create_log_group(bsm, log_group)
create_log_stream(bsm, log_group, log_stream)


def make_events(n: int):
    """
    Generate events every one second.
    """
    events = list()
    for _ in range(n):
        processing_time = random.randint(500, 1500)
        message = json.dumps({"processing_time": processing_time})
        event = Event(
            message=message,
        )
        events.append(event)
        time.sleep(random.randint(500, 1500) / 1000)
    return events


i = 0
n = 10
while 1:
    i += 1
    print(f"send {(i - 1) * n} - {i * n} ith events")
    events = make_events(n=n)
    put_log_events(bsm, log_group, log_stream, events)
