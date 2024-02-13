AWS CDK - StepFunctions Task
==============================================================================
Keywords: Amazon, AWS, CDK, Step Function, Task


Overview
------------------------------------------------------------------------------
Airflow 的那种用来定义 Orchestration Workload 逻辑的链式 API 非常受欢迎. AWS StepFunction 一直以来都想在易用性上追赶 Airflow. AWS 内部有一个 WDK (Workflow Development Kit) 项目, 直到 2023 年下旬, 它的底层组件, 才在 AWS CDK 中以 AWS StepFunctions Task 的形式发布. 本质上这个 Task 就是一个类, 类似于 Airflow 中的 Task 定义. 然后你可以用 ``task1.next(task2).next(task3)`` 这样的链式语法把 Task 代码中的定义连接起来.


Examples
------------------------------------------------------------------------------
我创建了几个用于快速上手这种新型 API 风格的例子. 请参考下面的源代码. 每一个类都是一个 Stack, 每个 Stack 里只有一个 State Machine.

.. dropdown:: learn_stepfunctions_task/stacks.py

    .. literalinclude:: ./learn_stepfunctions_task/stacks.py
       :language: python
       :linenos:


Reference
------------------------------------------------------------------------------
- `Tasks for AWS Step Functions <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_stepfunctions_tasks/README.html>`_
