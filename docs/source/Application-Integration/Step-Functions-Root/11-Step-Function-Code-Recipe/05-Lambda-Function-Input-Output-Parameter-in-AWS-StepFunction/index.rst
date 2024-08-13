AWS Step Functions - Lambda Function Input Output Parameter
==============================================================================
Keywords: AWS Step Function, StepFunction, SFN, State Machine, StateMachine, Lambda

在 AWS StepFunction 的编排中, Lambda Function 通常是最为常用的组成部分. 而同一个 Lambda Function, 我们可能会有多种使用方法. 下面我们以一个简单的对 S3 object 进行处理的 Lambda Function 为例, 它只是返回这个 Object 的 size (in bytes).

这个业务的核心逻辑是:

.. code-block:: python

    import boto3

    s3_client = boto3.client("s3")

    def main(bucket: str, key: str) -> int:
        return s3_client.get_object(Bucket=bucket, Key=key)["ContentLength"]

为了方便测试, 我们往往用 Request Response 的方式直接对 Lambda Function 发起请求, 并给与核心逻辑所需要的参数. 这种方式可以确保 LBD 的核心功能运转正常.

另一种常见的运行 Lambda Function 的方式是由 Event 触发.

而如果用 SFN 运行 LBD, 由多种方式传递参数. 最常见的是用前一个 Step 将核心逻辑所需的参数传递给 LBD. 但我们这里要说两种更加高级的方式:

1. 在 SFN Input 的 Payload 里用一个 key, value, 其中 value 是一个 dict, 里面包含了核心的参数. 这种方式只适用于 LBD 的参数在开始 SFN 的时候就已经确定下来了. 如果这个参数需要基于一些中间态的计算结果, 那么这种方式就不适用了.
2. 用 SFN execution id 作为一个唯一的 id, 把这个 execution 相关的 data 都存在一个 S3 object 中. 这个 exec data 本质上是一个 JSON, 所有的中间计算步骤都可以对这个 JSON 进行读写. 然后约定一个规定, 每个 step 的输入数据放在哪个 key 下. 然后所有的 LBD 的输入参数都只包含这个 SFN exec id, 然后去 S3 里拿数据. 这样完全跳过了 SFN 的限制,

下面我给出了上面提到的所有方式的代码实现, 以及提供了一个能兼容所有模式的 Lambda Function 的代码.

.. dropdown:: lbd1_request_response.py

    .. literalinclude:: ./lbd1_request_response.py
       :language: python
       :linenos:

.. dropdown:: lbd2_event_triggered.py

    .. literalinclude:: ./lbd2_event_triggered.py
       :language: python
       :linenos:

.. dropdown:: lbd3_sfn_input_object.py

    .. literalinclude:: ./lbd3_sfn_input_object.py
       :language: python
       :linenos:

.. dropdown:: lbd3_sfn_input_object_sfn_def.json

    .. literalinclude:: ./lbd3_sfn_input_object_sfn_def.json
       :language: python
       :linenos:

.. dropdown:: lbd3_sfn_input_object_test.py

    .. literalinclude:: ./lbd3_sfn_input_object_test.py
       :language: python
       :linenos:

.. dropdown:: lbd4_sfn_exec_arn.py

    .. literalinclude:: ./lbd4_sfn_exec_arn.py
       :language: python
       :linenos:

.. dropdown:: lbd4_sfn_exec_arn_sfn_def.json

    .. literalinclude:: ./lbd4_sfn_exec_arn_sfn_def.json
       :language: python
       :linenos:

.. dropdown:: lbd4_sfn_exec_arn_test.py

    .. literalinclude:: ./lbd4_sfn_exec_arn_test.py
       :language: python
       :linenos:

.. dropdown:: lbd5_universal.py

    .. literalinclude:: ./lbd5_universal.py
       :language: python
       :linenos:

.. dropdown:: lbd5_universal_test.py

    .. literalinclude:: ./lbd5_universal_test.py
       :language: python
       :linenos:
