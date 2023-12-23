# -*- coding: utf-8 -*-

import typing as T
import uuid
from pathlib import Path

from boto_session_manager import BotoSesManager
from aws_lambda_version_and_alias import get_alias_routing_config

import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
from constructs import Construct

dir_workspace = Path(__file__).absolute().parent
dir_lambda_app = dir_workspace.joinpath("lambda_app")
bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
canary_increments = [30, 70]


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        stack_name: str,
        func_name: str,
        md5: str,
        is_canary: bool,
        version1: T.Optional[T.Union[str, int]] = None,
        version2: T.Optional[T.Union[str, int]] = None,
        version2_weight: T.Optional[float] = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, id=id, stack_name=stack_name, **kwargs)

        self.lbd_func_name = func_name
        self.alias_name = "LIVE"
        self.lbd_func = lambda_.Function(
            self,
            "LambdaFunction",
            function_name=self.lbd_func_name,
            code=lambda_.Code.from_asset(f"{dir_lambda_app}"),
            handler=f"lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            memory_size=128,
            timeout=cdk.Duration.seconds(3),
            environment={
                "MD5": md5,
            },
            current_version_options=lambda_.VersionOptions(
                removal_policy=cdk.RemovalPolicy.RETAIN,
                retry_attempts=1,
            ),
        )

        if version1 is None:
            if is_canary:
                self.create_alias_for_canary()
            else:
                self.create_alias_for_blue_green()
        else:
            self.create_alias_manually(
                version1=version1,
                version2=version2,
                version2_weight=version2_weight,
            )

    def create_alias_for_blue_green(self):
        print("using blue green deployment")
        self.lbd_func_alias = lambda_.Alias(
            self,
            "AliasLive",
            alias_name=self.alias_name,
            version=self.lbd_func.current_version,
        )

    def _ref_version(self, vx: str, version: str) -> lambda_.Version:
        return lambda_.Version.from_version_arn(
            self,
            f"LambdaVersion{vx}ForLive-{self.lbd_func_name}",
            version_arn=f"arn:aws:lambda:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:function:{self.lbd_func_name}:{version}",
        )

    def create_alias_for_canary(self):
        """ """
        print("using canary deployment")
        rc = get_alias_routing_config(
            bsm.lambda_client,
            self.lbd_func_name,
            self.alias_name,
        )
        print(f"current routing config: {rc}")
        if rc is None:
            print("alias not found, create a new alias")
            self.lbd_func_alias = lambda_.Alias(
                self,
                "AliasLive",
                alias_name=self.alias_name,
                version=self.lbd_func.current_version,
            )
        elif bool(rc.version2_weight) is False:  # version2 could be None or 0
            print(
                "current route config only has one version! "
                f"new version 1 = {rc.version1} + 1, "
                f"new version 2 = {rc.version1}"
            )
            self.lbd_func_alias = lambda_.Alias(
                self,
                "AliasLive",
                alias_name=self.alias_name,
                version=self.lbd_func.current_version,
                additional_versions=[
                    lambda_.VersionWeight(
                        version=self._ref_version("2", rc.version1),
                        weight=round((100 - canary_increments[0]) / 100, 2),
                    )
                ],
            )
        else:
            print(
                "current route config has two version, "
                "gradually increase the weight of version1 to 100%"
            )
            for threshold in canary_increments:
                if rc.version1_weight < threshold:
                    self.lbd_func_alias = lambda_.Alias(
                        self,
                        "AliasLive",
                        alias_name=self.alias_name,
                        version=self._ref_version("1", rc.version1),
                        additional_versions=[
                            lambda_.VersionWeight(
                                version=self._ref_version("2", rc.version2),
                                weight=round((100 - threshold) / 100, 2),
                            )
                        ],
                    )
                    return
            self.lbd_func_alias = lambda_.Alias(
                self,
                "AliasLive",
                alias_name=self.alias_name,
                version=lambda_.Version.from_version_arn(
                    self,
                    f"LambdaVersion1ForLive-{self.lbd_func_name}",
                    version_arn=f"arn:aws:lambda:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:function:{self.lbd_func_name}:{rc.version1}",
                ),
            )

    def create_alias_manually(
        self,
        version1: T.Union[str, int],
        version2: T.Optional[T.Union[str, int]] = None,
        version2_weight: T.Optional[float] = None,
    ):
        print("configure routing manually")
        kwargs = {"version": self._ref_version("1", str(version1))}
        if version2 is not None:
            kwargs["additional_versions"] = [
                lambda_.VersionWeight(
                    version=self._ref_version("2", str(version2)),
                    weight=version2_weight,
                )
            ]
        self.lbd_func_alias = lambda_.Alias(
            self,
            "AliasLive",
            alias_name=self.alias_name,
            **kwargs,
        )


app = cdk.App()

stack = Stack(
    app,
    "MyApp",
    stack_name="deploy-lambda-with-aws-cdk-test",
    func_name="deploy_lambda_with_aws_cdk_test",
    md5=uuid.uuid4().hex,  # use random value to force new version
    # md5="a1b2", # manually specify md5 env var
    # is_canary=False, # use blue / green
    is_canary=True,  # use canary
    # version1=None, # rollback to specific version
    # version2=None, # rollback to specific version
    # version2_weight=None, # rollback to specific version
)

app.synth()
