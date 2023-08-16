Exponential Backoff
==============================================================================
`Exponential Backoff <https://en.wikipedia.org/wiki/Exponential_backoff>`_ 是一个反馈系统中的算法. 说的是一个系统有 Event 可以触发 Response 的, 如果连续进来许多个相同 Event, 我们不希望为所有的 Event 都返回 Response, 这样会占用大量系统资源. 而是使用 指数轮训 的方式, 让每两次返回 Response 的间隔越来越长. 举例来说, 前 1 秒内最多返回一个 Response, 1 - 2 秒内最多返回 1 个, 2 - 4 秒内最多返回 1 个, 4 - 8 秒内最多返回 1 个, 依次按 2 的倍数递增, 然后超过 3600 秒则刷新整个过程. 这里只是一个例子, 其中的间隔, 倍数, 刷新时间都可以自定义.

在 AWS 的很多服务中都有这种机制, 常常用于异常处理, 错误重试. 例如如果一个 Lambda Function Async Call fail 了, 你重试的次数如果是 3. 那么第一次可能要等 1 秒, 第二次要等 10 秒, 第三次可能要等 30 秒.

这种机制在软件工程里非常常用, 但是你自己实现这种机制却不是那么的容易. 所以这里我给出了一种 Python 实现, 可以在多个项目中复用.

.. literalinclude:: ./exponential_backoff_implementation_using_amazon_dynamodb.py
   :language: python
   :linenos:
