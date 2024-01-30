# -*- coding: utf-8 -*-

"""
Improve the original redshift data api.
"""

import typing as T

import botocore.exceptions

from .waiter import Waiter


def run_sql(
    rs_data_client,
    database: str,
    sql: str,
    cluster_id: T.Optional[str] = None,
    workgroup_name: T.Optional[str] = None,
    statement_name: T.Optional[str] = None,
    parameters: T.Optional[T.Dict[str, str]] = None,
    db_user: T.Optional[str] = None,
    secret_arn: T.Optional[str] = None,
    with_event: T.Optional[bool] = None,
    client_token: T.Optional[str] = None,
    delay: int = 1,
    timeout: int = 10,
    max_items: int = 1000,
    no_result: bool = False,
):
    """
    Run redshift SQL statement using Data API and get the results. It will
    run ``execute_statement`` API to run the SQL asynchronously, then do a
    long polling to check the status of the SQL execution using``describe_statement``
    API. Once the SQL execution is finished, it will run ``get_statement_result``
    API to get the result.

    In other words, this function is a human-friendly wrapper of the Data API.

    :param rs_data_client: boto3.client("redshift-data") object
    :param database: database name.
    :param sql: SQL statement you want to execute.
    :param cluster_id: cluster id. this is for Redshift provisioned cluster only.
    :param workgroup_name: workgroup name. this is for Redshift serverless only.
    :param statement_name: statement name. a human-friendly name you want to give
        to this SQL statement.
    :param delay: how many seconds to wait between each long polling.
    :param timeout: how many seconds to wait before timeout.
    :param max_items: maximum number of items to return (not 100% sure what
        the "items" refers to, I guess it refers to rows).
    :param no_result: some SQL statement doesn't return any result, for
        example, ``CREATE TABLE``, ``DELETE TABLE``. If this is True,
        then it will only wait the status to reach FINISHED, but won't run
        ``get_statement_result`` API.

    Reference:

    - execute_statement: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/execute_statement.html
    - describe_statement: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/describe_statement.html
    - get_statement_result: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data/client/get_statement_result.html

    :return: a tuple of (columns, rows) # todo, also return the column type
    """
    # --------------------------------------------------------------------------
    # execute_statement
    # --------------------------------------------------------------------------
    # process arguments
    kwargs = dict(
        Database=database,
        Sql=sql,
    )
    if cluster_id is not None:
        kwargs["ClusterIdentifier"] = cluster_id
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    if parameters:
        kwargs["Parameters"] = [dict(name=k, value=v) for k, v in parameters.items()]
    if statement_name is not None:
        kwargs["StatementName"] = statement_name
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if with_event is not None:
        kwargs["WithEvent"] = with_event
    if client_token is not None:
        kwargs["ClientToken"] = client_token

    res = rs_data_client.execute_statement(**kwargs)
    id = res["Id"]

    # --------------------------------------------------------------------------
    # describe_statement, wait for the status to reach FINISHED
    # --------------------------------------------------------------------------
    for _ in Waiter(delays=delay, timeout=timeout, verbose=False):
        try:
            res = rs_data_client.describe_statement(Id=id)
            status = res["Status"]
            if status == "FINISHED":
                break
            # still pending
            elif status in ["SUBMITTED", "PICKED", "STARTED"]:
                continue
            # raise exception when failed
            elif status in ["FAILED", "ABORTED"]:
                raise RuntimeError(f"reached status {status!r}")
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                continue
            else:
                raise e

    # --------------------------------------------------------------------------
    # get_statement_result
    # --------------------------------------------------------------------------
    if no_result:
        return None, None

    paginator = rs_data_client.get_paginator("get_statement_result")
    response_iterator = paginator.paginate(
        Id=id,
        PaginationConfig=dict(
            MaxItems=max_items,
        ),
    )
    rows = list()
    for res in response_iterator:
        # get result data
        for _row in res["Records"]:
            row = list()
            for field in _row:
                k, v = list(field.items())[0]
                if k == "isNull":
                    if v:
                        row.append(None)
                    else:
                        raise ValueError("I never see this before!")
                else:
                    row.append(v)
            rows.append(row)

    # get column information
    # todo: also get column type information so that we can use it to create pandas dataframe properly
    columns = list()
    for dct in res["ColumnMetadata"]:
        # todo: hard to decide which column naming convention to use
        # columns.append(
        #     "{}.{}.{}".format(
        #         dct["schemaName"],
        #         dct["tableName"],
        #         dct["name"],
        #     )
        # )
        columns.append(dct["label"])
    # rprint(columns, rows) # for debug only
    return columns, rows
