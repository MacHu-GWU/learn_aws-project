AWS Step Functions - Quick Start
==============================================================================
Keywords: AWS, Amazon, Step Function, SFN


Concept
------------------------------------------------------------------------------
学一门新技术时, 最重要的就是了解其中的概念. 下面是 Step Function 的核心概念.

- **Action**: 一个具体的计算动作, 比如 "运行一个 Lambda Function", "发送一条消息到 SNS Topic" 这些都是 Action, 每个 Action 有它自己的 Input Output 的接口数据模型.
- **State**: 一个状态, 是对一个 Action 的封装. 也是编排的最小单位. State 本身也有 Input Output, 而 State Input/Output 和 Action Input/Output 之间是可以进行一些简单的数据处理的.
- **Transition**: 从一个状态转移到另一个状态.
- **Workflow**: 将所有的 State 用 Transition 组织到一起的一个图, 有一个确定的开始, 以及多个结束. 也是我们编排的重点.
- **State Machine**: 一个 AWS StepFunction Console 中的 Resource, 里面包含了 Workflow Definition, IAM Role, Tag 等等. 是对 Workflow 的一个封装. 你可以 Execute State Machine, 并用图形化界面查看执行状态和结果.
- **Choice Rule**: 实际上就是一系列逻辑判断的组合, 来根据判断结果决定下一步做什么.
- **Logic Flow**: 这其实不是 Step Function 中的概念, 而是通用的概念. 其实就是一个图论中的 "图", 里面有 链条, 并行, 分叉, 条件判断 等等元素. SFN 支持
    - **Parallel**: 并行的执行多个子 workflow. 这些子 workflow 相互独立, 并且都有明确的结束节点. 相当于你枚举了每个并行的通道.
    - **Map**: 并行执行多个子 workflow, 不过这些 workflow 是同一个, 只不过拥有不同的输入参数. 常用于大规模并发.
    - **Choice**: 根据输入进行条件判断.

可以看出 Step Function 的本质就是把各种 Action 封装成一个 State (和 Airflow 中的 Task 是等价概念), 然后用 Logic Flow 对其进行编排.


Amazon State Language
------------------------------------------------------------------------------
Step Functions 的 Workflow definition 是用 JSON 语言定义的. 当然, 手写 JSON 很难. 一般开发者都是使用 Visual Editor 或是 `CDK stepfunctions_ task <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_stepfunctions_tasks.html>`_ 来生成 JSON. 但是了解底层的 JSON 结构是对我们学习非常有帮助的.

这个 JSON 语言的 Spec 叫做 Amazon State Language (ASL), 下面我们学习如何精准的定义一个 Workflow.

以下两个文档包含了基本上所有需要的资料.

- https://states-language.net/spec.html
- https://docs.aws.amazon.com/step-functions/latest/dg/concepts-states.html

ASL 中一共有 8 种不同的 State:

- Task: 一个包含具体的 Action 的任务, 也就是你的业务逻辑, 有输入输出, 有异常处理. 这是最常用的 State.
- Parallel: 并行执行多个子 workflow. 这些子 workflow 相互独立, 并且都有明确的结束节点.
- Map: 用不同的参数并行执行同一个子 workflow.
- Choice: 根据条件判断, 执行不同的逻辑分支.
- Pass: 通常用于输入输出的参数处理, 不执行任务, 只处理数据.
- Wait: 等待一段时间, 或是等待直到某个时间点.
- Succeed: 标记为成功, 并结束.
- Fail: 标记为失败, 并结束.

对于不同的 State 你能做的事情也不同. 例如 Task, Parallel, Map, Pass, Wait 都必须要么结束, 要么有下一个节点. 而 Choice 则没有结束和下一个节点的概念, 因为它的逻辑分支本质上就是一个个的 Task, 这些 Task 有结束和下一个就可以了, Choice 本身是不需要的.

下面这个图可能是最重要的图, 列出了不同的 State 都能做什么事.

.. image:: ./state.png

由于 AWS 提供了低代码的 `Workflow Studio <https://docs.aws.amazon.com/step-functions/latest/dg/workflow-studio.html>`_. 我建议先用 GUI 搭建一个简单的 Workflow, 将它跑通, 然后再阅读 JSON 代码, 结合 ASL 文档学习, 这样效率比较高. 下面是 Workflow Studio 的界面.

.. image:: ./workflow.png


Input Output Data Handling
------------------------------------------------------------------------------
我们把这个问题简称为 IO.

如果你认真读了 Concept, 你会知道 Action 和 State 虽然非常相似, 但是它们有各自的 Input Output. 而所谓的 IO 就是进行 State Input -> Action Input, 以及 Action Output -> State Input 的转换. ASL 提供了 5 种 IO 的处理方式:

- InputPath:  取 State Input 的一个 JSON Node 作为 Action Input, 适合简单的情况
- Parameters: 用 Payload Template 语法从 State Input 中提取 Action Input, 适合复杂的情况
- ResultSelector: 用 Payload Template 语法从 Action Output 中提取 State Output, 适合复杂的情况
- ResultPath: 直接把 State Input 和 Action Output 合并成一个大 JSON 输出. 常见于把整个 Workflow 的后续的 State 掌握之前所有的 Input Output 的信息的情况
- OutputPath: 去 Action Output 的一个 JSON Node 作为 State Output, 适合简单的情况

下面这张官方图很好的解释了整个流程:

.. image:: https://docs.aws.amazon.com/step-functions/latest/dg/images/input-output-processing.png

这个问题我们先不展开讲, 有兴趣可以先读文档.


Error Handling
------------------------------------------------------------------------------
这里的 Error Handling 主要说的是 Task State. 因为你在执行非业务逻辑的那些 State 是不容易出错的, 而错误往往是发生在业务逻辑中. Task State 支持 Error Handling. 你可以用 Error Code 来决定, 在出了什么错误的情况下, 进行 Retry. 或者决定如何对错误信息进行处理, 例如你可以选择报错或者忽略. 或是将错误数据传递给下 State 来专门处理 Error Data. 用 Python 的逻辑来说就是:

.. code-block:: python

    try:
        run_task_state(...)
    except SomeError:
        run_catch_logic(...)

只不过 ``run_task_state`` 和 ``run_catch_logic`` 是两个实际的 Task 而已.


My First Workflow
------------------------------------------------------------------------------
我推荐使用下面的 Workflow 体验一下 SFN 的功能. 它只有一步, Invoke 一个 Lambda Function.

.. image:: ./example.png

Lambda Function 的代码是这样的:

.. code-block:: python

    import json

    def lambda_handler(event, context):
        print("event:")
        print(json.dumps(event))
        return event


What's Next
------------------------------------------------------------------------------
至此, 你已经有动手实践的经验了, 你可以开始学习更多的内容了.
