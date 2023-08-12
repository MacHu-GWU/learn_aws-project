Manage Redshift Cluster - Workload Management WLM
==============================================================================
Keywords: AWS, Amazon, Redshift, Workload Management, WLM


What is Workload Management (WLM)
------------------------------------------------------------------------------
WLM 是 Redshift 的一个功能. 它解决了同时执行多个 Query 时相互竞争计算资源时的问题. 它可以防止一个查询占用了所有计算资源导致其他的查询全部失败. 你可以启用自动 WLM, 也可以手动精细化管理 WLM.

.. note::

    WLM 功能在 Redshift Serverless 中不存在. 因为 Redshift Serverless 能自动 Scale up down, 所有的 Query 都会有足够的资源执行, 不存在需要用 WLM 来隔离 Query 的需求. 和 WLM 类似地, 在 Redshift Serverless 中可以为 Workgroup 设置 usage limit 来限制一个资源使用的上限, 还能设置 query limit 来限制每个 query 的执行时间, CPU 用量等.


How does WLM Work
------------------------------------------------------------------------------
WLM 的本质是通过将 **Query (workload)** 分配给不同的 **Queue (队列)**. 然后通过对 Queue 的配置来限制里面的 Query 所占用的资源.

**Auto WLM**

在自动 WLM 管理模式下, 每个 Queue 会有不同的 Priority. Priority 高的 Queue 中的 Query 会先被执行.

**Manual WLM**

在手动 WLM 管理模式下, 每个 Queue 还可以限制执行 Query 所消耗的计算资源:

- 最多同时进行的 Query 数量, Number of Query Tasks (slots)
- 每个 Query 最多能占用多少内存, Query Working Memory (mem)
- 每个 Query 最长能执行多久, Max Execution Time (max_time)

当 Query 超过了 Queue 中定义的限制时, 根据 Query 的分类, 例如是 INSERT / Update / Delete, 还是 UNLOAD, COPY, 有着不同的处理方式, 例如是直接 cancel, 还是继续执行, 还是等待重试. 这样就做到了让分配到不同的 Queue 中的 Query 不会互相影响.

**Assign Query to Which Queue**

而至于一个 Query 要被分配到哪个 Queue 是由 **User Group** 和 **Query Group** 决定的. 这点在 Auto 和 Manual 模式下都是一样的. Queue 的定义还包含了 ``user_group_wild_card`` 和 ``query_group_wild_card`` 两个字段, 可以用通配符来根据 User Group 和 Query Group 来匹配 Queue. 简单来说, 当一个 Query 被执行的时候, 会先看它有没有 Query Group, 有则优先按照 Query Group 来匹配 queue. 如果没有 Query Group 则看 Query 是哪个 User 发起的, 然后根据它属于哪个 User Group 来匹配 Queue. 详情请参考 `WLM queue assignment rules <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-queue-assignment-rules.html>`_ 官方文档.


How to Configure Auto WLM
------------------------------------------------------------------------------
对 WLM 的配置是通过修改 Parameter Group 来实现的. Redshift Cluster 本质上是一个数据库集群. 和 RDS 类似, Redshift Cluster 也有 Parameter Group. 其中有一个 ``wlm_json_configuration`` 设置可以用 JSON 来定义 WLM. 详情请查看 `Configuring queue priority <https://docs.aws.amazon.com/redshift/latest/dg/query-priority.html#concurrency-scaling-queues>`_ 官方文档.

除此之外关于 Auto WLM 还有 ``Concurrency scaling mode``, ``Query monitoring rules`` 两个知识点. 这里不展开说, 详情请查看官方文档.


How to Configure Manual WLM
------------------------------------------------------------------------------
和 Configure Auto WML 类似, 也是通过修改 Parameter Group 来实现的. 详情请查看 `Tutorial: Configuring manual workload management (WLM) queues <https://docs.aws.amazon.com/redshift/latest/dg/tutorial-configuring-workload-management.html>`_ 官方文档.


Create the WLM_QUEUE_STATE_VW view
------------------------------------------------------------------------------
Parameter Group 中于 WLM 相关的配置可以再一些系统表中被访问到. 为了更清晰的理解 Queue 的行为, AWS 推荐创建一个 ``WLM_QUEUE_STATE_VW`` 的 View, 它的本质是对相关的几个系统表进行 SELECT, 然后汇总成一个表. 详情请参考 `Create the WLM_QUEUE_STATE_VW view <https://docs.aws.amazon.com/redshift/latest/dg/tutorial-wlm-understanding-default-processing.html#tutorial-wlm-create-queue-state-view>`_.


Concurrency Scaling
------------------------------------------------------------------------------
Concurrency Scaling 是 Redshift 中的一项功能. 允许在不添加节点的情况下, 应对高并发的读写操作. 而你只需要为这些临时 Scale Out 的计算资源实际计算的时间付费. 但这个功能要求你的主节点的机器必须是某些特定的实例, 例如为应对高并发读操作需要 ``dc2.8xlarge, ds2.8xlarge, dc2.large, ds2.xlarge, ra3.xlplus, ra3.4xlarge, or ra3.16xlarge``, 为应对高并发写操作需要 ``ra3.xlplus, ra3.4xlarge, or ra3.16xlarge``.


Short Query Acceleration
------------------------------------------------------------------------------
Short Query Acceleration 是 Redshift 中的一项功能. Redshift 能通过机器学习分析你的 Query 预测它的用时. 如果 Query 的用时比较短 (1 ~ 20) 秒, 那么这种 Query 就叫做 Short Query (SQ). Redshift 会划分一部分专用计算资源用来运行 SQ. 这些 SQ 不会被发送到 Queue 中执行. 而且 Redshift 会优先执行这些 SQ 以尽快返回结果. 这个机制配合 WLM 一起, 能够平衡用户希望能频繁地运行消耗资源较小的短查询, 也能保证消耗资源较大的长查询不会阻塞整个集群. 而 AWS 推荐 Queue 一般是为长查询服务的, 建议每个 Queue 最多同时进行的 Query 数量不要超过 15 个.

.. note::

    这个功能是默认开启的, 也是 AWS 所推荐的. 如果你足够了解并有足够的信息, 你可以在 Parameter 中将其关闭.


Conclusion
------------------------------------------------------------------------------
总结下来 WLM 虽然是 Cluster 模式独有的功能. 但其实 Serverless 中类似的机制也借鉴了 WLM 中的设计. 作为一款云原生数据仓库, 提供更精细化的管理工具能更好的解决不同的终端用户的形形色色的需求, 也是一个数据仓库产品成熟的标志.


Reference
------------------------------------------------------------------------------
- `Introduce Workload management <https://docs.aws.amazon.com/redshift/latest/dg/c_workload_mngmt_classification.html>`_: 介绍 WLM 的概念.
- `Configuring workload management <https://docs.aws.amazon.com/redshift/latest/mgmt/workload-mgmt-config.html>`_: 如何配置 WLM.
- `Implementing workload management <https://docs.aws.amazon.com/redshift/latest/dg/cm-c-implementing-workload-management.html>`_: 如何实现 WLM.
- `Implementing automatic WLM <https://docs.aws.amazon.com/redshift/latest/dg/automatic-wlm.html>`_: 介绍了如何实现自动 WLM.
- `WLM query queue hopping <https://docs.aws.amazon.com/redshift/latest/dg/wlm-queue-hopping.html>`_: 介绍了在 Manual WLM 模式下, 当 Query 超过了 WLM 所限制的资源时, 会如何处理.
- `Understanding the default queue processing behavior <https://docs.aws.amazon.com/redshift/latest/dg/tutorial-wlm-understanding-default-processing.html>`_: WLM 的系统表的字段解释, 也说明了 Queue 的定义中的各种属性的含义.
