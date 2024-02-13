# -*- coding: utf-8 -*-

import aws_cdk as cdk
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as sfn_tasks

from constructs import Construct


class MySfnTaskStack1(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            state_machine_name=f"my-first-sfn-task-state-machine",
            definition=sfn.Chain.start(sfn.Pass(self, "PassState")),
        )
