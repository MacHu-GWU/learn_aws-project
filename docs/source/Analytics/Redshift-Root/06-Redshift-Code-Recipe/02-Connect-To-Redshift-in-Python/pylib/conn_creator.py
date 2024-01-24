# -*- coding: utf-8 -*-

import typing as T
import redshift_connector

# sqlalchemy is optional
try:
    import sqlalchemy as sa
except ImportError:  # pragma: no cover
    pass

from .model import WorkGroup, Namespace, Cluster

if T.TYPE_CHECKING:  # pragma: no cover
    import boto3


def get_database_by_workgroup(
    redshift_serverless_client,
    workgroup_name: str,
) -> T.Tuple[str, WorkGroup, Namespace]:
    """
    Get the database of the namespace associated with the workgroup.
    """
    res = redshift_serverless_client.get_workgroup(workgroupName=workgroup_name)
    workgroup = WorkGroup.from_get_workgroup_response(res)
    res = redshift_serverless_client.get_namespace(
        namespaceName=workgroup.namespaceName
    )
    namespace = Namespace.from_get_namespace_response(res)
    database = namespace.dbName
    return database, workgroup, namespace


def create_connect_for_serverless_using_iam(
    boto_ses: "boto3.session.Session",
    workgroup_name: str,
) -> redshift_connector.Connection:
    """
    Create connection for Redshift serverless using IAM.

    :param boto_ses: boto3 session object.
    :param workgroup_name: serverless workgroup name.
    """
    rs_sls_client = boto_ses.client("redshift-serverless")
    database, _, _ = get_database_by_workgroup(rs_sls_client, workgroup_name)
    kwargs = dict(
        iam=True,
        database=database,
        is_serverless=True,
        serverless_work_group=workgroup_name,
    )
    if boto_ses.profile_name is None or boto_ses.profile_name == "default":
        pass
    else:
        kwargs["profile"] = boto_ses.profile_name
    return redshift_connector.connect(**kwargs)


def create_sqlalchemy_engine_for_serverless_using_iam(
    boto_ses: "boto3.session.Session",
    workgroup_name: str,
    duration: int = 900,
) -> "sa.engine.Engine":
    """
    Create sqlalchemy engine for Redshift serverless using IAM.

    :param boto_ses: boto3 session object.
    :param workgroup_name: serverless workgroup name.
    :param duration: credential duration in seconds.
    """
    rs_sls_client = boto_ses.client("redshift-serverless")
    database, workgroup, namespace = get_database_by_workgroup(
        rs_sls_client,
        workgroup_name,
    )
    res = rs_sls_client.get_credentials(
        dbName=database,
        workgroupName=workgroup_name,
        durationSeconds=duration,
    )
    username = res["dbUser"]
    password = res["dbPassword"]
    username = username.replace(":", "%3A")  # url encode the : character
    conn_str = (
        f"redshift+psycopg2://{username}:{password}"
        f"@{workgroup.endpoint.address}:{workgroup.endpoint.port}/{database}"
    )
    return sa.create_engine(conn_str)


def get_database_by_cluster_id(
    redshift_client,
    cluster_id: str,
) -> T.Tuple[str, Cluster]:
    """
    Get the database of the namespace associated with the workgroup.
    """
    res = redshift_client.describe_clusters(ClusterIdentifier=cluster_id)
    cluster = Cluster.from_describe_clusters_response(res)
    database = cluster.DBName
    return database, cluster


def create_connect_for_cluster_using_iam(
    boto_ses: "boto3.session.Session",
    cluster_id: str,
) -> redshift_connector.Connection:
    """
    Create connection for Redshift Cluster using IAM.

    :param boto_ses: boto3 session object.
    :param cluster_id: Redshift cluster id.
    """
    rs_client = boto_ses.client("redshift")
    database, _ = get_database_by_cluster_id(rs_client, cluster_id)
    kwargs = dict(
        iam=True,
        db_user="awsuser",
        database=database,
        is_serverless=False,
        cluster_identifier=cluster_id,
    )
    if boto_ses.profile_name is None or boto_ses.profile_name == "default":
        pass
    else:
        kwargs["profile"] = boto_ses.profile_name
    return redshift_connector.connect(**kwargs)


def create_sqlalchemy_engine_for_cluster_using_iam(
    boto_ses: "boto3.session.Session",
    cluster_id: str,
    duration: int = 900,
) -> "sa.engine.Engine":
    """
    Create sqlalchemy engine for Redshift cluster using IAM.

    :param boto_ses: boto3 session object.
    :param cluster_id: Redshift cluster_id
    :param duration: credential duration in seconds.
    """
    rs_client = boto_ses.client("redshift")
    database, cluster = get_database_by_cluster_id(rs_client, cluster_id)
    res = rs_client.get_cluster_credentials_with_iam(
        DbName=database,
        ClusterIdentifier=cluster_id,
        DurationSeconds=duration,
    )
    username = res["DbUser"]
    password = res["DbPassword"]
    username = username.replace(":", "%3A")  # url encode the : character
    conn_str = (
        f"redshift+psycopg2://{username}:{password}"
        f"@{cluster.Endpoint.Address}:{cluster.Endpoint.Port}/{database}"
    )
    return sa.create_engine(conn_str)
