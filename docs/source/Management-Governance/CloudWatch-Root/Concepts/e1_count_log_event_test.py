# -*- coding: utf-8 -*-

"""
Ref:

- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CountingLogEventsExample.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_metric_filter.html
"""

from lib import create_log_group, create_log_stream, bsm

log_group = "/learn_cloudwatch_logs/count_log_event"
log_stream = "my_stream_1"

flag = create_log_group(bsm, log_group)
flag = create_log_stream(bsm, log_group, log_stream)
bsm.cloudwatchlogs_client.put_metric_filter(
    logGroupName=log_group,
    filterName="EventCount",
    filterPattern=" ",
    metricTransformations=[
        {
            "metricName": "CountLogEvent",
            "metricNamespace": "LearnCloudWatchLogs",
            "metricValue": "1",
            "defaultValue": 0,
        },
    ],
)
