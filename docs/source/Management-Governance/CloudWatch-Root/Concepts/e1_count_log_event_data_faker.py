# -*- coding: utf-8 -*-

import time
import uuid
import random
from lib import create_log_group, create_log_stream, put_log_events, bsm, Event

log_group = "/learn_cloudwatch_logs/count_log_event"
log_stream = "my_stream_1"

flag = create_log_group(bsm, log_group)
flag = create_log_stream(bsm, log_group, log_stream)


def make_events(n: int):
    """
    Generate events every one second.
    """
    events = list()
    for _ in range(n):
        event = Event(
            message=f"event {str(uuid.uuid4())}",
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
