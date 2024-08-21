# -*- coding: utf-8 -*-

import aws_cdk
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct


class MyCDKStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.param_project_name_id = "ParamProjectName"
        self.param_project_name = cdk.CfnParameter(
            self,
            id=self.param_project_name_id,
            type="String",
        )

        self.iam_group = iam.CfnGroup(
            self,
            "IamGroup",
            group_name=cdk.Fn.sub(
                f"${{{self.param_project_name_id}}}-${{AwsRegion}}-group",
                variables={
                    self.param_project_name_id: self.param_project_name.value_as_string,
                    # your IDE may complain about the type hint, but it's fine
                    "AwsRegion": aws_cdk.Aws.REGION,
                },
            ),
        )
