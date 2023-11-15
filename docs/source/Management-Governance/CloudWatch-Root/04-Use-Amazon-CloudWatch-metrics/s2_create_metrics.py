# -*- coding: utf-8 -*-

"""
This script creates a custom metrics based on the log event data.
"""

from config import logs_client, group_name, metric_namespace, metric_name

# ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_metric_filter.html
logs_client.put_metric_filter(
    logGroupName=group_name,
    filterName="ProcessingTime",
    filterPattern='{ $.processing_time = "*" }',
    metricTransformations=[
        {
            "metricNamespace": metric_namespace,
            "metricName": metric_name,
            "metricValue": "$.processing_time",
            "dimensions": {
                "server_id": "$.server_id",
            },
        },
    ],
)
