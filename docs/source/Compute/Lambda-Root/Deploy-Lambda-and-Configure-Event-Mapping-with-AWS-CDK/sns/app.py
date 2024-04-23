# -*- coding: utf-8 -*-

from pathlib import Path

from boto_session_manager import BotoSesManager

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as sns_subscription
import aws_cdk.aws_lambda as lambda_
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

        self.sns_topic_name = f"{project_name}-topic"
        self.sns_topic = sns.Topic(
            self,
            "SNSTopic",
            topic_name=self.sns_topic_name,
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

        self.sns_topic.add_subscription(
            sns_subscription.LambdaSubscription(self.lbd_func_1)
        )

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

        sns_topic = sns.Topic.from_topic_arn(
            self,
            "SNSTopicInterface",
            topic_arn=f"arn:aws:sns:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:{self.sns_topic_name}",
        )
        sns_topic.add_subscription(sns_subscription.LambdaSubscription(self.lbd_func_2))


# ------------------------------------------------------------------------------
# Config
aws_profile = "bmt_app_dev_us_east_1"
project_name = "lbd_cdk_event_demo-sns"
# ------------------------------------------------------------------------------

dir_workspace = Path(__file__).absolute().parent
dir_lambda_app = dir_workspace.joinpath("lambda_app")
bsm = BotoSesManager(profile_name=aws_profile)

app = cdk.App()
stack = Stack(app, "MyApp", project_name=project_name)

if __name__ == "__main__":
    app.synth()
