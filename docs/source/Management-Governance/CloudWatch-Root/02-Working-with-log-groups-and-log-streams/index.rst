Working with log groups and log streams
==============================================================================
Keywords: AWS, Amazon, CloudWatch, CW, Log Group Stream


Create and Update Log Group and Stream
------------------------------------------------------------------------------
对 Log group 的管理非常简单, 它只有 `create_log_group <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/create_log_group.html>`_ 和配置 Retention policy `put_retention_policy <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/put_retention_policy.html>`_ 两个操作.

对 Log stream 的管理更简单了, 压根没有其他参数.

下面是一个帮助你管理 Group 和 Stream 的模块. 比原生 API 的提升是加入了处理在 Create 时 Group 已经存在, 或是 Delete 的时 Group 不存在的情况. 并且提供了一个对 Log event 的数据模型抽象.

.. literalinclude:: ./recipe.py
   :language: python
   :linenos:


Put Log Events
------------------------------------------------------------------------------
我们可以用 put_log_events 的 API 来将 Log 打到 CloudWatch. 默认情况下这个 API 有两个限制:

1. 每个 batch (一次 API) 的数据量不得超过 1MB.
2. 对于 US East (N. Virginia), US West (Oregon), and Europe (Ireland), 一个 account / region 每秒最多 1500 Transaction, 对于其他 region 则是每秒 800 次.

下面给出了一段利用前面的模块写的往 Log Stream 里打 Log 的代码.

.. literalinclude:: ./working_with_log_groups_and_log_streams.py
   :language: python
   :linenos:
