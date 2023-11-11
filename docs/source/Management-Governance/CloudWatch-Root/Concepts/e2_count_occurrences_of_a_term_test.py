# -*- coding: utf-8 -*-

"""
Ref:

- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CountOccurrencesExample.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_metric_filter.html
"""

from lib import create_log_group, create_log_stream, bsm

log_group = "/learn_cloudwatch_logs/count_occurrences_of_a_term"
log_stream = "my_stream_1"

create_log_group(bsm, log_group)
create_log_stream(bsm, log_group, log_stream)
bsm.cloudwatchlogs_client.put_metric_filter(
    logGroupName=log_group,
    filterName="ErrorCount",
    filterPattern="Error",
    metricTransformations=[
        {
            "metricName": "CountOccurancesOfError",
            "metricNamespace": "LearnCloudWatchLogs",
            "metricValue": "1",
            "defaultValue": 0,
        },
    ],
)
