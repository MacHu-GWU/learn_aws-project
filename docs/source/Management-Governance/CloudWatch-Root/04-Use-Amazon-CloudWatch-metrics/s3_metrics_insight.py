# -*- coding: utf-8 -*-

"""
Learn how to use get_metric_data API to query metrics

Ref:

- Metrics Insights query components and syntax: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-querylanguage.html
- cloudwatch_client.get_metric_data: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_data.html
"""

from textwrap import dedent
from datetime import datetime, timezone, timedelta
from config import (
    cw_client,
    metric_namespace,
    metric_name,
    stream_name_1,
    stream_name_2,
)


now = datetime.utcnow().replace(tzinfo=timezone.utc)
five_minutes_ago = now - timedelta(minutes=5)


def print_get_metric_data_response(res: dict):
    dct = {
        "Timestamps": res["MetricDataResults"][0]["Timestamps"],
        "Values": res["MetricDataResults"][0]["Values"],
    }
    print(dct)


def _use_metric_stat(dimensions: list) -> dict:
    return cw_client.get_metric_data(
        MetricDataQueries=[
            dict(
                Id="id1",
                MetricStat=dict(
                    Metric=dict(
                        Namespace=metric_namespace,
                        MetricName=metric_name,
                        Dimensions=dimensions,
                    ),
                    Period=60,
                    Stat="Average",
                ),
                ReturnData=True,
            ),
        ],
        StartTime=five_minutes_ago,
        EndTime=now,
        ScanBy="TimestampAscending",
    )


def use_metric_stat():
    """
    Here's a tricky part, you cannot use multiple dimensions with same name,
    only the last one will be used.
    It is NOT logic OR, and metrics insight doesn't support logic OR.
    """
    dimensions = [
        dict(Name="server_id", Value=stream_name_1),
        dict(Name="server_id", Value=stream_name_2),
    ]
    res = _use_metric_stat(dimensions=dimensions)
    print(dimensions)
    print_get_metric_data_response(res)

    dimensions = [
        # dict(Name="server_id", Value=stream_name_1),
        dict(Name="server_id", Value=stream_name_2),
    ]
    res = _use_metric_stat(dimensions=dimensions)
    print(dimensions)
    print_get_metric_data_response(res)

    dimensions = [
        dict(Name="server_id", Value=stream_name_2),
        dict(Name="server_id", Value=stream_name_1),
    ]
    res = _use_metric_stat(dimensions=dimensions)
    print(dimensions)
    print_get_metric_data_response(res)

    dimensions = [
        dict(Name="server_id", Value=stream_name_1),
        # dict(Name="server_id", Value=stream_name_2),
    ]
    res = _use_metric_stat(dimensions=dimensions)
    print(dimensions)
    print_get_metric_data_response(res)

    res = _use_metric_stat(
        dimensions=[
            # dict(Name="server_id", Value=stream_name_1),
            # dict(Name="server_id", Value=stream_name_2),
        ]
    )
    print_get_metric_data_response(res)


def _use_expression(sql: str) -> dict:
    return cw_client.get_metric_data(
        MetricDataQueries=[
            dict(
                Id="id1",
                Expression=dedent(sql.strip()),
                Period=60,
                ReturnData=True,
            ),
        ],
        StartTime=five_minutes_ago,
        EndTime=now,
        ScanBy="TimestampAscending",
    )


def use_expression():
    """
    Metric insights doesn't support logic or, so we should use != instead.

    List of queries:

    SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace}, server_id) WHERE server_id = '{stream_name_1}'
    SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace}, server_id) WHERE server_id = '{stream_name_2}'
    SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace}, server_id) WHERE server_id != 'xyz'
    SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace})
    """
    sql = f"SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace}, server_id) WHERE server_id = '{stream_name_1}'"
    res = _use_expression(sql)
    print(sql)
    print_get_metric_data_response(res)

    sql = f"SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace}, server_id) WHERE server_id = '{stream_name_2}'"
    res = _use_expression(sql)
    print(sql)
    print_get_metric_data_response(res)

    sql = f"SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace}, server_id) WHERE server_id != 'xyz'"
    res = _use_expression(sql)
    print(sql)
    print_get_metric_data_response(res)

    sql = f"SELECT AVG({metric_name}) FROM SCHEMA({metric_namespace})"
    res = _use_expression(sql)
    print(sql)
    print_get_metric_data_response(res)


if __name__ == "__main__":
    use_metric_stat()
    use_expression()
