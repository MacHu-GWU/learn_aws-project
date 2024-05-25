.. _use-dynamodb-for-status-tracking:

Status Tracking
==============================================================================


Overview
------------------------------------------------------------------------------
在我的职业生涯中, 我发现在运行 Business Critical Task 的时候, 往往会有如下痛点:

1. 在运行 Business Critical Task 的时候, 我们通常希望能够 Track 一个 Task 的状态, 例如查看 Task 是处于 pending, 还是 in_progress, 还是 failed, 还是 succeeded 等等.
2. 如果 Task 失败了, 我们则希望重试.
3. 由于是 Business Critical, 我们还会希望确保整个任务的执行是幂等的, 换言之如果我们定义了一个 Python 函数来执行这个任务, 无论我们是在一台机器上按顺序运行很多次, 还是我们在多台机器上同时运行很多次, 我们希望最终结果都跟我们只运行了一次是一样的. 这就会涉及到解决多个 Worker 同时尝试去做一个 Task 的情况的问题.
4. 我们希望能够自动的打上 Trace 和 Error Log, 以便于我们后续的 Debug.
5. 能够对许多 Task 进行筛序, 查询. 例如查找处在过去 30 天内失败的 Task, 以便于我们之后重试.

这里第三条是最难实现的, 特别是在高并发, 分布式的情况下.

这种需求在实践中往往是用一个支持行锁和 Transaction 的 Relational Database 来实现的, 也有人会用 Redis 来实现. 但这两者都有一定的问题. Relational Database 的并发性能在高并发的情况下往往不够, 而 Redis 中的数据不容易持久化, 并且 Redis 也不支持高性能条件过滤查询.

在我的职业生涯中, 我发现 Amazon DynamoDB 这款云原生的 Key Value Store 恰好是解决这一问题的最佳选择. DynamoDB 支持低延迟高并发, 超强的自动扩容能力, 查询能力完全能满足这个 Use Case, 并且完全无需管理任何基础设施就可使用. 于是在我的职业生涯中有 10 多个项目都使用了 DynamoDB 来做 Business Critical Task 的 Status Tracking 系统. 为了更方便使用, 我在我的开源项目 `pynamodb_mate <https://github.com/MacHu-GWU/pynamodb_mate-project>`_ 中 (一个自带了许多高级功能的 DynamoDB ORM 框架), 我实现了这个功能并提供了一套优雅的 API.

本文希望能详细的说说我的实现思路, 涉及的概念, 业务流程.


Concepts
------------------------------------------------------------------------------
为了更方便理解, 我们设定一个应用场景. 我们假设我们是 Amazon.com 电商平台, 一个用户的订单会经过 "已下订单 -> 确认收款 -> 进行物流发货 -> 货物送达 -> 用户确认完成订单" 这样一个流程. 于是我们希望 Track 每一个订单在这个流程中的状态.

- **Task**: 每个我们希望追踪状态的任务. 每个任务都有一个唯一的 task_id.
- **Status**: 每个任务的状态, 每个任务的生命周期都会经过 pending -> in_progress -> failed/succeeded/ignored 这样一个流程. pending 表示已经准备好随时执行了, in_progress 表示正在执行, failed 表示执行失败, succeeded 表示执行成功, ignored 表示由于失败重试了太多次被忽略. 我不允许在这个流程中添加任何其他的状态码. 因为这个生命周期所对应的是一个幂等操作, 如果你在 in_progress 中还有其他的中间状态操作, 我们以一共 2 步为例. 此时你应该将这 2 步分拆成两个生命周期, 第一个步骤的 succeeded 的状态码应该和第二个步骤的 pending 的状态码相等. 这样做的原因是一旦你有其他的中间状态操作, 那么你的幂等将无法保证, 所以必须要将其分拆成两个步骤.
- **Use Case**: 在 DynamoDB 中, 我们通常会用一个表来做很多关系数据库中需要多个表做的事情. 在这篇文章里, 我们会把属于完全不同类型的 Task 都放在同一个表中. 而这些不同的 Task 可能会有相同的状态码, 例如我们都用 0 表示 pending. 那么我们就需要一个字段将这些 Task 却分开, 这个字段就是 use_case_id. 我们会保证在一个 use_case_id 下的所有 task_id 都是唯一的.
- **Execution Context (ctx)**: 我们在程序设计中, 用到了 Python 中的 Context Manager 来开始一个任务的生命周期, 并且根据这个任务的执行结果, 成功, 失败 来自动的对数据库中的状态进行更新. 这个 Execution Context 就是一个执行任务的生命周期中的所有上下文数据的容器.
- **Execution**: 一次尝试执行任务的过程. 也就是上面提到过很多次的任务的 "生命周期".


Implementation
------------------------------------------------------------------------------
我用 Python 为例. 实现这个的关键就是首先在执行业务逻辑之前, 先去 DynamoDB 中获取锁, 然后把你的业务逻辑用 try, except 包裹起来. 如果成功了则更新 status 字段, 失败了也更新 status 字段, 不过还要将 retry + 1. 如果失败了多次, 则将 status 更新为 ignored. 最后无论成功还是失败, 都要释放锁. 这个锁是有失效时间的, 这样做是为了防止由于程序直接挂掉 (比如拔电源) 导致无法释放锁.


Solution
------------------------------------------------------------------------------
我开发了一个开源库 `pynamodb_mate <https://github.com/MacHu-GWU/pynamodb_mate-project>`_ 使得你用很少的代码就能实现这个功能. 详情请参考 `Enable status tracking for business critical application using Amazon DynamoDB <https://pynamodb-mate.readthedocs.io/en/latest/search.html?q=status+tracking&check_keywords=yes&area=default>`_ 这篇文档.
