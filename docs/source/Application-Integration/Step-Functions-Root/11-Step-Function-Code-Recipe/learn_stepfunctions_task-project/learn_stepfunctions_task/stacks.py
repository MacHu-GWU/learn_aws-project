# -*- coding: utf-8 -*-

import aws_cdk as cdk
import aws_cdk.aws_lambda as aws_lambda
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
        """
        Basic stepfunctions_tasks example.
        """
        super().__init__(scope, construct_id, **kwargs)

        self.state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            state_machine_name=f"sfn-task-1",
            definition=sfn.Chain.start(sfn.Pass(self, "PassState")),
        )


class MySfnTaskStack2(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        """
        Invoke Lambda Function.
        """
        super().__init__(scope, construct_id, **kwargs)

        task1 = sfn.Pass(self, "Task 1")
        task2 = sfn_tasks.LambdaInvoke(
            self,
            "Task 2",
            lambda_function=aws_lambda.Function.from_function_name(
                self,
                "SfnTaskTest1",
                function_name="sfn_tasks_test_1",
            ),
        )
        definition = task1.next(task2)

        self.state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            state_machine_name=f"sfn-task-2",
            definition_body=sfn.DefinitionBody.from_chainable(definition),
        )


class MySfnTaskStack3(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        """
        Use chain syntax to write state machine workflow

        Task 1 -> Task 2 ->
            if: job succeeded -> job succeeded task
            elif: job failed -> job failed task
            else: wait 1 sec
        """
        super().__init__(scope, construct_id, **kwargs)

        # task 1
        task1 = sfn.Pass(self, "Task 1")

        # task 2
        # status = "succeeded"
        status = "failed"
        # status = "running"
        task2 = sfn.Pass(self, "Task 2", result=sfn.Result.from_object({"status": status}))

        # choice
        job_complete_choice = sfn.Choice(self, "Job Complete?")

        succeeded_condition = sfn.Condition.string_equals("$.status", "succeeded")
        failed_condition = sfn.Condition.string_equals("$.status", "failed")

        job_succeeded_task = sfn.Pass(self, "Job Succeeded Task")
        job_failed_task = sfn.Pass(self, "Job Failed Task")

        # fmt: off
        definition = (
            task1
            .next(task2)
            .next(
                job_complete_choice
                .when(succeeded_condition, job_succeeded_task.next(sfn.Succeed(self, "Job Succeeded")))
                .when(failed_condition, job_failed_task.next(sfn.Fail(self, "Job Failed")))
                .otherwise(sfn.Fail(self, "Unknown Status"))
            )
        )
        # fmt: on

        self.state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            state_machine_name=f"sfn-task-3",
            definition_body=sfn.DefinitionBody.from_chainable(definition),
        )
