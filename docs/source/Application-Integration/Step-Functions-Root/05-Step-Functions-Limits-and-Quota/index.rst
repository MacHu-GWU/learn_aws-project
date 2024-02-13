AWS Step Functions - Limits and Quota
==============================================================================
Keywords: AWS, Amazon, Step Function, SFN, Limit, Quota.

这里我们只列出几个比较重要的 Limit 和 Quota:

- Maximum execution time:
    - Standard: 1 年
    - Express: 5 分钟
- Execution history retention time:
    - Standard: 90 天
    - Express: 由于底层是 CloudWatch Log, 所以是无限.
- Maximum number of registered state machines: 10000, 可以提升到最高 25000.
- Maximum request size: 1MB. 这个 payload 那怕是对 map task 也够大了.
- Maximum open executions per account: 每个 region 同时最多有 1M 个正在执行的 Execution.


Reference
------------------------------------------------------------------------------
- `AWS Step Functions Quota <https://docs.aws.amazon.com/step-functions/latest/dg/limits-overview.html>`_
