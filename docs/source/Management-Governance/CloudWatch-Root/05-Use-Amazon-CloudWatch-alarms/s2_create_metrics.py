# -*- coding: utf-8 -*-

"""
This script creates a custom metrics based on the log event data.
"""

from shared import logs_client, group_name

logs_client.put_metric_filter(
    logGroupName=group_name,
    filterName="ProcessingTime",
    filterPattern="{ $.processing_time = \"*\" }",
    metricTransformations=[
        {
            "metricName": "AverageProcessingTime",
            "metricNamespace": "LearnCloudWatchLogs",
            "metricValue": "$.processing_time",
            "defaultValue": 0,
        },
    ],
)
