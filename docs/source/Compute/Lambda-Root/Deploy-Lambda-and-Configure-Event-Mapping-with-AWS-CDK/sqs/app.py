# -*- coding: utf-8 -*-

from pathlib import Path

from boto_session_manager import BotoSesManager

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sqs as sqs
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda_event_sources as event_source
from constructs import Construct


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        project_name: str,
        **kwargs,
    ) -> None:
        project_name_slug = project_name.replace("_", "-")
        super().__init__(scope, id=id, stack_name=project_name_slug, **kwargs)

        self.iam_role_for_lbd = iam.Role(
            self,
            "IamRoleForLambda",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name=f"{project_name}-{cdk.Aws.REGION}-lambda-role",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("PowerUserAccess")
            ],
        )

        # SQS is declared in the same stack
        self.sqs_queue_name = f"{project_name}-queue"
        self.sqs_queue = sqs.Queue(
            self,
            "SQSQueue",
            queue_name=self.sqs_queue_name,
        )

        self.lbd_func_1 = lambda_.Function(
            self,
            "LambdaFunction1",
            function_name=f"{project_name}-1",
            code=lambda_.Code.from_asset(f"{dir_lambda_app}"),
            handler=f"lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            memory_size=128,
            timeout=cdk.Duration.seconds(3),
            role=self.iam_role_for_lbd,
        )

        self.sqs_event_source_1 = event_source.SqsEventSource(
            queue=self.sqs_queue,
            batch_size=10,
            enabled=True,
        )
        self.lbd_func_1.add_event_source(self.sqs_event_source_1)

        # SQS is declared in another stack
        self.lbd_func_2 = lambda_.Function(
            self,
            "LambdaFunction2",
            function_name=f"{project_name}-2",
            code=lambda_.Code.from_asset(f"{dir_lambda_app}"),
            handler=f"lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_10,
            memory_size=128,
            timeout=cdk.Duration.seconds(3),
            role=self.iam_role_for_lbd,
        )

        sqs_queue = sqs.Queue.from_queue_arn(
            self,
            "SQSQueueInterface",
            queue_arn=f"arn:aws:sqs:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:{self.sqs_queue_name}",
        )
        self.sqs_event_source_2 = event_source.SqsEventSource(
            queue=sqs_queue,
            batch_size=10,
            enabled=True,
        )
        self.lbd_func_2.add_event_source(self.sqs_event_source_2)


# ------------------------------------------------------------------------------
# Config
aws_profile = "bmt_app_dev_us_east_1"
project_name = "lbd_cdk_event_demo-sqs"
# ------------------------------------------------------------------------------

dir_workspace = Path(__file__).absolute().parent
dir_lambda_app = dir_workspace.joinpath("lambda_app")
bsm = BotoSesManager(profile_name=aws_profile)

app = cdk.App()
stack = Stack(app, "MyApp", project_name=project_name)

if __name__ == "__main__":
    app.synth()
