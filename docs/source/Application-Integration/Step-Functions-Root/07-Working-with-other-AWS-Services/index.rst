AWS Step Functions - Working with other AWS Services
==============================================================================
Keywords: AWS, Amazon, Step Function, SFN


Overview
------------------------------------------------------------------------------
通常使用 AWS StepFunction 的用户的需要被调度的计算单元通常都是在 AWS 跑着的服务, 例如 Lambda 之类的. 当然你可以用 AWS 调用外部服务, 只要这个外部服务有两个 API, 一是 start, 二是 get status (running, succeeded, failed), 但是这种 integration 就比较复杂了.


如何用 SFN 来调用 AWS 服务?
------------------------------------------------------------------------------
总的来说调用 AWS 服务或 API 的方式有这么三种方法:

1. 用 Lambda 包装一层, 在 Lambda 的代码中调用 API, 然后用 SFN 调度 Lambda.
2. 用 `AWS SDK Service Integrations <https://docs.aws.amazon.com/step-functions/latest/dg/supported-services-awssdk.html>`_ 调用 AWS 服务. 本质上是直接调用 AWS 的原生 API. 基本上你在 Boto3 Python SDK 中的参数原封不动的输入成 JSON 就行.
3. 用 `Optimized integrations <https://docs.aws.amazon.com/step-functions/latest/dg/connect-supported-services.html>`_, 这是 Step Function 对一些常用的 AWS 服务进行了优化后的调用模式. 例如一些只能异步执行的服务, 例如 AWS Glue Job, 你可以原生执行 Sync 模式而无需自己实现 Poll Job (Transition 可是要钱的, 并且无论这个 Job 花费多长时间你都不需要为时间付费). 又或是一些数据的服务, 例如 DynamoDB, 可以直接输入 key, 返回数据而无需写 Code.

总结下来, #1 很万能, 而且很清晰, 你本地代码怎么写就怎么用, 但是多了部署 Lambda 的步骤. 最灵活, 最强大, 但是也最麻烦. #2 比较万能, 但是你得 figure out 正确的 syntax 和行为, 只能在 Step Function 里调试. #3 最简单, 但是也最局限, 不是所有的 AWS 服务都支持, 不过也支持 90% 的常用计算服务了.

我个人喜欢优先考虑 #3, 然后考虑 #2, 实在不行了再用 #1.


Call third-party APIs
------------------------------------------------------------------------------
HTTP Task 是一种用 HTTP 协议调度外部的系统的方式. 调用的时候你主要要提供提供三个参数:

1. endpoint, 一个 URL
2. authentication, 通过 `eventbridge connection <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_Connection.html>`_ 来储存鉴权方式. 你不应该将敏感信息用 step function input 传递, 因为这会被打到 cloudwatch log 里. 相比之下, 如果被调用方是 AWS 服务, 你的权限是通过 IAM 来管理的.
3. payload: 你要传递的数据.

Reference:

- `Call third-party APIs <https://docs.aws.amazon.com/step-functions/latest/dg/connect-third-party-apis.html>`_


Wait for a Callback with the Task Token
------------------------------------------------------------------------------
这是一种比较高级的用法. 这个 Callback Task Token 主要是为了解决在 Orchestration 的过程中, 有些 Task 并不是 AWS 所管理的服务, 对于这种外部服务的 Async 调用, 你无法让 StepFunction 去 Poll 它们的状态, 因为外部服务不是 AWS 所能管理的范畴. AWS 提供的方法是在调用这些外部 Task 的时候, 发一个 Token 给 Task, 然后 StepFunction 就一直等, 直到它收到这个 Token 才会继续进行下一步. 也就是说你的外部的 Task 需要负责在运行成功或者失败之后, 调用 API 给 StepFunction 提交一个 Token, 然后 StepFunction 才会继续运行 (transit 到下一步). 这种让 Task Executor 主动推送的方式要比让 Scheduler 去轮询的性能要好的多, 避免了频繁的状态查询, 也根本无需实现状态查询. 不过代价就是你依赖于外部服务的实现, 如果外部服务本身出了问题, 很可能会导致你的 StepFunction 一直等待下去. 所以一旦你要使用这种模式, 就需要给 State Machine 加上 Timeout.

补充一点, 其实这本身就是 AWS StepFunction 原生的跟其他 Service Integrate 的方式, 只不过 AWS 封装了一层, 让你感觉不到, 从而提高开发体验罢了.

- `Wait for a Callback with the Task Token <https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token>`_
