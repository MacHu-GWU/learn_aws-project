# -*- coding: utf-8 -*-

"""
Data model for redshift objects.
"""

import typing as T
import dataclasses
from datetime import datetime


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
        if isinstance(res.get("workgroup", {}), dict):
            res = res["workgroup"]
        if "endpoint" in res:
            endpoint = WorkGroupEndpoint(
                address=res["endpoint"]["address"],
                port=res["endpoint"]["port"],
            )
        else:
            endpoint = None
        return cls(
            workgroupId=res.get("workgroupId"),
            workgroupName=res.get("workgroupName"),
            workgroupVersion=res.get("workgroupVersion"),
            workgroupArn=res.get("workgroupArn"),
            namespaceName=res.get("namespaceName"),
            status=res.get("status"),
            baseCapacity=res.get("baseCapacity"),
            maxCapacity=res.get("maxCapacity"),
            endpoint=endpoint,
        )


@dataclasses.dataclass
class Namespace(BaseModel):
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

    @classmethod
    def from_get_namespace_response(cls, res: dict):
        """
        Ref:

        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_namespace.html
        """
        if isinstance(res.get("namespace", {}), dict):
            res = res["namespace"]
        return cls._from_dict(res)
