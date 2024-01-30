# -*- coding: utf-8 -*-

"""
Data model for redshift objects.
"""

import typing as T
import dataclasses
from datetime import datetime

import botocore.exceptions


@dataclasses.dataclass
class BaseModel:
    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def _from_dict(cls, data: dict):
        """
        The ``data`` may have more keys than the fields of the class.
        """
        kwargs = dict()
        for field in dataclasses.fields(cls):
            if field.name in data:
                kwargs[field.name] = data[field.name]
        return cls(**kwargs)


@dataclasses.dataclass
class WorkGroupEndpoint(BaseModel):
    address: str = dataclasses.field()
    port: int = dataclasses.field()


@dataclasses.dataclass
class WorkGroup(BaseModel):
    """
    WorkGroup object.
    """
    # fmt: off
    workgroupId: T.Optional[str] = dataclasses.field(default=None)
    workgroupName: T.Optional[str] = dataclasses.field(default=None)
    workgroupVersion: T.Optional[str] = dataclasses.field(default=None)
    workgroupArn: T.Optional[str] = dataclasses.field(default=None)
    namespaceName: T.Optional[str] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    baseCapacity: T.Optional[int] = dataclasses.field(default=None)
    maxCapacity: T.Optional[int] = dataclasses.field(default=None)
    endpoint: T.Optional[WorkGroupEndpoint] = dataclasses.field(default=None)
    creationDate: T.Optional[datetime] = dataclasses.field(default=None)
    crossAccountVpcs: T.Optional[T.List[str]] = dataclasses.field(default=None)
    customDomainCertificateArn: T.Optional[str] = dataclasses.field(default=None)
    customDomainCertificateExpiryTime: T.Optional[datetime] = dataclasses.field(default=None)
    customDomainName: T.Optional[str] = dataclasses.field(default=None)
    patchVersion: T.Optional[str] = dataclasses.field(default=None)
    port: T.Optional[int] = dataclasses.field(default=None)
    publiclyAccessible: T.Optional[bool] = dataclasses.field(default=None)
    securityGroupIds: T.Optional[T.List[str]] = dataclasses.field(default=None)
    subnetIds: T.Optional[T.List[str]] = dataclasses.field(default=None)
    # fmt: on

    @classmethod
    def from_get_workgroup_response(cls, res: dict):
        """
        Ref:

        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_workgroup.html
        """
        if "workgroup" in res and "workgroupName" not in res:
            data = res["workgroup"]
        else:
            data = res

        if "endpoint" in data:
            endpoint = WorkGroupEndpoint(
                address=data["endpoint"]["address"],
                port=data["endpoint"]["port"],
            )
        else:
            endpoint = None

        data["endpoint"] = endpoint
        return cls._from_dict(data)

    @classmethod
    def from_name(cls, rs_sls_client, name: str) -> T.Optional["WorkGroup"]:
        try:
            res = rs_sls_client.get_workgroup(workgroupName=name)
            return cls.from_get_workgroup_response(res["workgroup"])
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                return None
            else:  # pragma: no cover
                raise e


@dataclasses.dataclass
class Namespace(BaseModel):
    """
    Namespace object.
    """
    # fmt: off
    namespaceArn: T.Optional[str] = dataclasses.field(default=None)
    namespaceId: T.Optional[str] = dataclasses.field(default=None)
    namespaceName: T.Optional[str] = dataclasses.field(default=None)
    status: T.Optional[str] = dataclasses.field(default=None)
    dbName: T.Optional[str] = dataclasses.field(default=None)
    adminPasswordSecretArn: T.Optional[str] = dataclasses.field(default=None)
    adminPasswordSecretKmsKeyId: T.Optional[str] = dataclasses.field(default=None)
    adminUsername: T.Optional[str] = dataclasses.field(default=None)
    creationDate: T.Optional[datetime] = dataclasses.field(default=None)
    defaultIamRoleArn: T.Optional[str] = dataclasses.field(default=None)
    iamRoles: T.Optional[T.List[str]] = dataclasses.field(default=None)
    kmsKeyId: T.Optional[str] = dataclasses.field(default=None)
    logExports: T.Optional[T.List[str]] = dataclasses.field(default=None)
    # fmt: on

    @classmethod
    def from_get_namespace_response(cls, res: dict):
        """
        Ref:

        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_namespace.html
        """
        if "namespace" in res and "namespaceName" not in res:
            data = res["namespace"]
        else:
            data = res
        return cls._from_dict(data)

    @classmethod
    def from_name(cls, rs_sls_client, name: str) -> T.Optional["Namespace"]:
        try:
            res = rs_sls_client.get_namespace(namespaceName=name)
            return cls.from_get_namespace_response(res["namespace"])
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                return None
            else:  # pragma: no cover
                raise e


@dataclasses.dataclass
class ClusterEndpoint(BaseModel):
    Address: str = dataclasses.field()
    Port: int = dataclasses.field()


@dataclasses.dataclass
class Cluster(BaseModel):
    # fmt: off
    ClusterIdentifier: T.Optional[str] = dataclasses.field(default=None)
    NodeType: T.Optional[str] = dataclasses.field(default=None)
    ClusterStatus: T.Optional[str] = dataclasses.field(default=None)
    ClusterAvailabilityStatus: T.Optional[str] = dataclasses.field(default=None)
    ModifyStatus: T.Optional[str] = dataclasses.field(default=None)
    MasterUsername: T.Optional[str] = dataclasses.field(default=None)
    DBName: T.Optional[str] = dataclasses.field(default=None)
    Endpoint: T.Optional[ClusterEndpoint] = dataclasses.field(default=None)
    ClusterCreateTime: T.Optional[datetime] = dataclasses.field(default=None)
    AutomatedSnapshotRetentionPeriod: T.Optional[int] = dataclasses.field(default=None)
    ManualSnapshotRetentionPeriod: T.Optional[int] = dataclasses.field(default=None)
    ClusterSecurityGroups: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    VpcSecurityGroups: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    ClusterParameterGroups: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    ClusterSubnetGroupName: T.Optional[str] = dataclasses.field(default=None)
    VpcId: T.Optional[str] = dataclasses.field(default=None)
    AvailabilityZone: T.Optional[str] = dataclasses.field(default=None)
    PreferredMaintenanceWindow: T.Optional[str] = dataclasses.field(default=None)
    PendingModifiedValues: T.Optional[dict] = dataclasses.field(default=None)
    ClusterVersion: T.Optional[str] = dataclasses.field(default=None)
    AllowVersionUpgrade: T.Optional[bool] = dataclasses.field(default=None)
    NumberOfNodes: T.Optional[int] = dataclasses.field(default=None)
    PubliclyAccessible: T.Optional[bool] = dataclasses.field(default=None)
    Encrypted: T.Optional[bool] = dataclasses.field(default=None)
    RestoreStatus: T.Optional[dict] = dataclasses.field(default=None)
    DataTransferProgress: T.Optional[dict] = dataclasses.field(default=None)
    HsmStatus: T.Optional[dict] = dataclasses.field(default=None)
    ClusterSnapshotCopyStatus: T.Optional[dict] = dataclasses.field(default=None)
    ClusterPublicKey: T.Optional[str] = dataclasses.field(default=None)
    ClusterNodes: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    ElasticIpStatus: T.Optional[dict] = dataclasses.field(default=None)
    ClusterRevisionNumber: T.Optional[str] = dataclasses.field(default=None)
    Tags: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    KmsKeyId: T.Optional[str] = dataclasses.field(default=None)
    EnhancedVpcRouting: T.Optional[bool] = dataclasses.field(default=None)
    IamRoles: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    PendingActions: T.Optional[T.List[str]] = dataclasses.field(default=None)
    MaintenanceTrackName: T.Optional[str] = dataclasses.field(default=None)
    ElasticResizeNumberOfNodeOptions: T.Optional[str] = dataclasses.field(default=None)
    DeferredMaintenanceWindows: T.Optional[T.List[dict]] = dataclasses.field(default=None)
    SnapshotScheduleIdentifier: T.Optional[str] = dataclasses.field(default=None)
    SnapshotScheduleState: T.Optional[str] = dataclasses.field(default=None)
    ExpectedNextSnapshotScheduleTime: T.Optional[datetime] = dataclasses.field(default=None)
    ExpectedNextSnapshotScheduleTimeStatus: T.Optional[str] = dataclasses.field(default=None)
    NextMaintenanceWindowStartTime: T.Optional[datetime] = dataclasses.field(default=None)
    ResizeInfo: T.Optional[dict] = dataclasses.field(default=None)
    AvailabilityZoneRelocationStatus: T.Optional[str] = dataclasses.field(default=None)
    ClusterNamespaceArn: T.Optional[str] = dataclasses.field(default=None)
    TotalStorageCapacityInMegaBytes: T.Optional[int] = dataclasses.field(default=None)
    AquaConfiguration: T.Optional[dict] = dataclasses.field(default=None)
    DefaultIamRoleArn: T.Optional[str] = dataclasses.field(default=None)
    ReservedNodeExchangeStatus: T.Optional[dict] = dataclasses.field(default=None)
    CustomDomainName: T.Optional[str] = dataclasses.field(default=None)
    CustomDomainCertificateArn: T.Optional[str] = dataclasses.field(default=None)
    CustomDomainCertificateExpiryDate: T.Optional[datetime] = dataclasses.field(default=None)
    MasterPasswordSecretArn: T.Optional[str] = dataclasses.field(default=None)
    MasterPasswordSecretKmsKeyId: T.Optional[str] = dataclasses.field(default=None)
    IpAddressType: T.Optional[str] = dataclasses.field(default=None)
    MultiAZ: T.Optional[str] = dataclasses.field(default=None)
    MultiAZSecondary: T.Optional[dict] = dataclasses.field(default=None)
    # fmt: on

    @classmethod
    def from_describe_clusters_response(cls, res: dict):
        """
        Ref:

        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_clusters.html
        """
        if "Clusters" in res and "ClusterIdentifier" not in res:
            _clusters = res["Clusters"]
            if len(_clusters):
                data = _clusters[0]
            else:
                raise ValueError("Clusters is empty")
        else:
            data = res

        if "Endpoint" in data:
            Endpoint = ClusterEndpoint(
                Address=data["Endpoint"]["Address"],
                Port=data["Endpoint"]["Port"],
            )
        else:
            Endpoint = None

        data["Endpoint"] = Endpoint
        return cls._from_dict(data)

    @classmethod
    def from_cluster_id(
        cls,
        rs_client,
        cluster_id: str,
    ) -> T.Optional["Cluster"]:
        try:
            res = rs_client.describe_clusters(
                ClusterIdentifier=cluster_id,
            )
            return cls.from_describe_clusters_response(res["Clusters"][0])
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ClusterNotFoundFault":
                return None
            else:  # pragma: no cover
                raise e
