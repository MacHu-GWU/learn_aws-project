AWS Step Functions - Pricing
==============================================================================
Keywords: AWS, Amazon, Step Function, SFN, Price.


Overview
------------------------------------------------------------------------------
Step Functions 是一个 Serverless 无服务器的服务. Serverless 产品主打的就是一个按照使用量收费. Step Functions 的 Pricing Model 很有特点, 它不按照运行的总时间收费, 也不按照底层消耗的资源收费 (因为所有的计算都不发生在 Step Function 中, 这跟 Airflow 有本质的不同), **而是按照 Transition 的次数收费 (对 Standard Workflow 而言)**. 这非常有意思, 因为调度系统的核心功能是调度. 诚然有很多人会用一个 shell script 脚本加一堆等待, 异常处理来做调度. 但这样做的本质是将运算放在一个容器中进行, 本质还是运算. 对于复杂的调度任务运行时间很长. 作为用户而言, 用户是不希望为调度所产生的等待时间而买单的. 例如你隔 1 小时就运行一次 Lambda Function, 你会希望为等待的那 1 个小时付费吗? 但是对于 Step Functions 而言, 你只需要为状态转移的次数付费, 这就是 Serverless 的魅力所在.

注意, 对于 Express Workflow 而言, 它是按照运行时间收费的.


Pricing
------------------------------------------------------------------------------
- Standard: $0.025 per 1000 transition. 可见对于 long polling 的 workflow, 每次 wait 的间隔应该尽量长一点, 这样可以减少 transition 的次数.
- Express: 可以看出, 它跟 Lambda Function 的收费类似. 可能它的底层实现就是就是一个自带异常处理的 Lambda Function.
    - Request:
        - $1.00 per 1M requests
        - $0.000001 per request
    - Duration:
        - $0.00001667 per GB-Second ($0.0600 per GB-hour) for the first 1,000 hours GB-hours
        - $0.00000833 per GB-Second ($0.0300 per GB hour) for the next 4,000 hours GB-hours
        - $0.00000456 per GB-Second ($0.01642 per GB-hour) beyond that


Reference
------------------------------------------------------------------------------
- `AWS Step Functions Pricing <https://aws.amazon.com/step-functions/pricing/>`_
