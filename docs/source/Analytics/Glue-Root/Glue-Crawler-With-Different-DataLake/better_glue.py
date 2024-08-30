# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from datetime import datetime

import botocore.exceptions

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_glue.client import GlueClient
    from mypy_boto3_glue.type_defs import (
        GetDatabaseResponseTypeDef,
        GetTableResponseTypeDef,
        GetCrawlerResponseTypeDef,
    )


def resolve_kwargs(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


@dataclasses.dataclass
class Database:
    Name: str = dataclasses.field()
    Description: str = dataclasses.field(default=None)
    LocationUri: str = dataclasses.field(default=None)
    Parameters: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    CreateTime: datetime = dataclasses.field(default=None)
    CreateTableDefaultPermissions: T.List[T.Dict[str, T.Any]] = dataclasses.field(
        default_factory=list
    )
    TargetDatabase: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    CatalogId: str = dataclasses.field(default=None)
    FederatedDatabase: T.Dict[str, str] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_get_database_response(
        cls,
        res: "GetDatabaseResponseTypeDef",
    ) -> "Database":
        dct = res["Database"]
        return cls(
            Name=dct["Name"],
            Description=dct.get("Description"),
            LocationUri=dct.get("LocationUri"),
            Parameters=dct.get("Parameters", {}),
            CreateTime=dct.get("CreateTime"),
            CreateTableDefaultPermissions=dct.get("CreateTableDefaultPermissions", []),
            TargetDatabase=dct.get("TargetDatabase", {}),
            CatalogId=dct.get("CatalogId"),
            FederatedDatabase=dct.get("FederatedDatabase", {}),
        )

    @classmethod
    def get(
        cls,
        glue_client: "GlueClient",
        name: str,
        catalog_id: T.Optional[str] = None,
    ) -> T.Optional["Database"]:
        try:
            res = glue_client.get_database(
                **resolve_kwargs(Name=name, CatalogId=catalog_id)
            )
            return cls.from_get_database_response(res)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                return None
            else:  # pragma: no cover
                raise e


@dataclasses.dataclass
class Table:
    Name: str = dataclasses.field()
    DatabaseName: str = dataclasses.field()
    Description: str = dataclasses.field(default=None)
    Owner: str = dataclasses.field(default=None)
    CreateTime: datetime = dataclasses.field(default=None)
    UpdateTime: datetime = dataclasses.field(default=None)
    LastAccessTime: datetime = dataclasses.field(default=None)
    LastAnalyzedTime: datetime = dataclasses.field(default=None)
    Retention: int = dataclasses.field(default=None)
    StorageDescriptor: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)
    PartitionKeys: T.List[T.Dict[str, T.Any]] = dataclasses.field(default_factory=list)
    ViewOriginalText: str = dataclasses.field(default=None)
    ViewExpandedText: str = dataclasses.field(default=None)
    TableType: str = dataclasses.field(default=None)
    Parameters: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    CreatedBy: str = dataclasses.field(default=None)
    IsRegisteredWithLakeFormation: bool = dataclasses.field(default=None)
    TargetTable: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    CatalogId: str = dataclasses.field(default=None)
    VersionId: str = dataclasses.field(default=None)
    FederatedTable: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    ViewDefinition: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    IsMultiDialectView: bool = dataclasses.field(default=None)
    Status: T.Dict[str, str] = dataclasses.field(default_factory=dict)

    @classmethod
    def from_get_table_response(
        cls,
        res: "GetTableResponseTypeDef",
    ) -> "Table":
        dct = res["Table"]
        return cls(
            Name=dct["Name"],
            DatabaseName=dct["DatabaseName"],
            Description=dct.get("Description"),
            Owner=dct.get("Owner"),
            CreateTime=dct.get("CreateTime"),
            UpdateTime=dct.get("UpdateTime"),
            LastAccessTime=dct.get("LastAccessTime"),
            LastAnalyzedTime=dct.get("LastAnalyzedTime"),
            Retention=dct.get("Retention"),
            StorageDescriptor=dct.get("StorageDescriptor", {}),
            PartitionKeys=dct.get("PartitionKeys", []),
            ViewOriginalText=dct.get("ViewOriginalText"),
            ViewExpandedText=dct.get("ViewExpandedText"),
            TableType=dct.get("TableType"),
            Parameters=dct.get("Parameters", {}),
            CreatedBy=dct.get("CreatedBy"),
            IsRegisteredWithLakeFormation=dct.get("IsRegisteredWithLakeFormation"),
            TargetTable=dct.get("TargetTable", {}),
            CatalogId=dct.get("CatalogId"),
            VersionId=dct.get("VersionId"),
            FederatedTable=dct.get("FederatedTable", {}),
            ViewDefinition=dct.get("ViewDefinition", {}),
            IsMultiDialectView=dct.get("IsMultiDialectView"),
            Status=dct.get("Status", {}),
        )

    @classmethod
    def get(
        cls,
        glue_client: "GlueClient",
        database: str,
        name: str,
        catalog_id: T.Optional[str] = None,
        transaction_id: T.Optional[str] = None,
        query_as_of_time: T.Optional[datetime] = None,
        include_status_details: T.Optional[bool] = None,
    ) -> T.Optional["Table"]:
        try:
            res = glue_client.get_table(
                **resolve_kwargs(
                    DatabaseName=database,
                    Name=name,
                    CatalogId=catalog_id,
                    TransactionId=transaction_id,
                    QueryAsOfTime=query_as_of_time,
                    IncludeStatusDetails=include_status_details,
                )
            )
            return cls.from_get_table_response(res)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                return None
            else:  # pragma: no cover
                raise e


@dataclasses.dataclass
class Crawler:
    Name: str = dataclasses.field()
    Role: str = dataclasses.field()
    Targets: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)
    DatabaseName: str = dataclasses.field(default=None)
    Description: str = dataclasses.field(default=None)
    Classifiers: T.List[str] = dataclasses.field(default_factory=list)
    RecrawlPolicy: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    SchemaChangePolicy: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    LineageConfiguration: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    State: str = dataclasses.field(default=None)
    TablePrefix: str = dataclasses.field(default=None)
    Schedule: T.Dict[str, str] = dataclasses.field(default_factory=dict)
    CrawlElapsedTime: int = dataclasses.field(default=None)
    CreationTime: datetime = dataclasses.field(default=None)
    LastUpdated: datetime = dataclasses.field(default=None)
    LastCrawl: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)
    Version: int = dataclasses.field(default=None)
    Configuration: str = dataclasses.field(default=None)
    CrawlerSecurityConfiguration: str = dataclasses.field(default=None)
    LakeFormationConfiguration: T.Dict[str, T.Any] = dataclasses.field(
        default_factory=dict
    )

    @classmethod
    def from_get_crawler_response(
        cls,
        res: "GetCrawlerResponseTypeDef",
    ) -> "Crawler":
        dct = res["Crawler"]
        return cls(
            Name=dct["Name"],
            Role=dct["Role"],
            Targets=dct.get("Targets", {}),
            DatabaseName=dct.get("DatabaseName"),
            Description=dct.get("Description"),
            Classifiers=dct.get("Classifiers", []),
            RecrawlPolicy=dct.get("RecrawlPolicy", {}),
            SchemaChangePolicy=dct.get("SchemaChangePolicy", {}),
            LineageConfiguration=dct.get("LineageConfiguration", {}),
            State=dct.get("State"),
            TablePrefix=dct.get("TablePrefix"),
            Schedule=dct.get("Schedule", {}),
            CrawlElapsedTime=dct.get("CrawlElapsedTime"),
            CreationTime=dct.get("CreationTime"),
            LastUpdated=dct.get("LastUpdated"),
            LastCrawl=dct.get("LastCrawl", {}),
            Version=dct.get("Version"),
            Configuration=dct.get("Configuration"),
            CrawlerSecurityConfiguration=dct.get("CrawlerSecurityConfiguration"),
            LakeFormationConfiguration=dct.get("LakeFormationConfiguration", {}),
        )

    @classmethod
    def get(
        cls,
        glue_client: "GlueClient",
        name: str,
    ) -> T.Optional["Crawler"]:
        try:
            res = glue_client.get_crawler(Name=name)
            return cls.from_get_crawler_response(res)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                return None
            else:  # pragma: no cover
                raise e

    def is_ready(self) -> bool:
        return self.State == "READY"

    def is_running(self) -> bool:
        return self.State == "RUNNING"

    def is_stopping(self) -> bool:
        return self.State == "STOPPING"
