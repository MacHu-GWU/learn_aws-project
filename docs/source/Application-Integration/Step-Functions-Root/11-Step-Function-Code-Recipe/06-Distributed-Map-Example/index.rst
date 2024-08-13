AWS Step Functions - Distributed Map Example
==============================================================================
Keywords: AWS Step Function, StepFunction, SFN, State Machine, StateMachine, Lambda

早期 AWS Step Function 的 Map 并行处理只有 inline 模式. 这种并发模式指的是这个并发是在一个同一个 scheduler 的子进程中调度的. 类似于你一个机器上 fork 了一个 thread. 所以这种模式的并发不可能做的很高, 所以它有 40 个 concurrency 的限制.

而在 2022-12-01, `AWS 发布了 Distributed Map <https://aws.amazon.com/blogs/aws/step-functions-distributed-map-a-serverless-solution-for-large-scale-parallel-data-processing/#:~:text=The%20new%20distributed%20map%20state,Storage%20Service%20(Amazon%20S3).>`_ 功能, 它允许同时并发 10,000 个子任务. 这种模式的底层是用的 sub step function workflow execution 的模式来实现的, 所以作为一个分布式系统, 它的并发是可以做的很高的.


Item Sources
------------------------------------------------------------------------------
给每个子任务指定参数的方式有很多种:

1. State Input: 上一步返回的结果就是一个 List of Dictionary. 里面每个 Dictionary 就是一个子任务的参数, List 中元素的个数就是并发数.
2. Amazon S3 - S3 Object List: 把某个 S3 prefix 下的所有 object 作为输入, 每个 object 都有是一个 JSON, 里面是子任务的参数.
3. Amazon S3 - Json File in S3: 把 List of Dictionary 用 JSON 序列化保存在 S3 object 中. 然后 Step Function 到这个 S3 object 中去读数据.
4. Amazon S3 - CSV File in S3: 跟 Json File in S3 类似, 唯一的区别是文件格式是 CSV.
5. Amazon S3 - S3 Inventory: 跟 S3 Object List 类似, 不过是在一个指定的 Manifest File (一个 S3 Object) 中去读所有文件的列表, 这个 Manifest File 是一个 Json Line 文件, 每一行是一条数据. 注意, 每一行只是包含了每个子任务的参数所在的 S3 object 的 uri, 并不包含参数数据本身.

我个人最喜欢 #3, 因为它简单, 直观, 灵活 (适用于各种复杂的参数列表). 只有在数据量巨大的时候才会用到 #5.



Amazon S3 Json File in S3 Example
------------------------------------------------------------------------------
这里给出了一个具体的例子.

这里的关键是 sfn_def 中的这个部分, 指定了 Map 要从哪里读参数::

    "Parameters": {
      "Bucket.$": "$.map_input_s3_bucket",
      "Key.$": "$.map_input_s3_key"
    }

以及 Lambda Function 的 input 是直接从 state input 过来的.

SFN 的定义

.. dropdown:: sfn_def.json

    .. literalinclude:: ./sfn_def.json
       :language: javascript
       :linenos:

Lambda 的源码

.. dropdown:: lbd.py

    .. literalinclude:: ./lbd.py
       :language: python
       :linenos:

测试代码

.. dropdown:: sfn_test.py

    .. literalinclude:: ./sfn_test.py
       :language: python
       :linenos:
