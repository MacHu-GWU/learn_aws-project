.. _aws-opensearch-scaling-opensearch-cluster:

Scaling OpenSearch Cluster
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Cluster, Scaling

TODO: 这篇文档还未完成, 我只是把我能想到的点都写在这里, 以后慢慢改.


Overview
------------------------------------------------------------------------------
通常说到 Scaling 的时候包含两种情况, Scaling Up 和 Scaling Down. 大部分的情况是 Scaling Up, 少数情况需要 Scaling Down. 在 Scaling 的过程中最重要的因素是 Node, Shard 和 内存. 我建议先精读 :ref:`aws-opensearch-sizing-opensearch-cluster`, 了解这几个概念对性能的影响之后再来读本文.

我们先谈 Scaling Up 的情况. 通常之所以需要 Scaling Up 是因为 Cluster 的内存空间满了, 无法增加更多的 Document. 或是一个 Index 的性能达到了瓶颈, 查询速度越来越慢了.

我们再谈 Scaling Down 的情况. 通常之所以需要 Scaling Down 是因为 Cluster 上的内存空间富余太多, 不需要那么多 Node.

本文详细的探讨了针对不同的情况下所需要采取的 Scaling 策略.


Scale Up for an Index
------------------------------------------------------------------------------
情况:

    随着业务的扩张, 有一个 Index 的的查询请求的并发在不断增加, 并且数据量也越来越多. 我们发现查询速度越来越慢. 我们发现所有的 Shard 的内存已经接近 50G 的上限.

目标:

    如何使得业务在不断扩张的过程中, 能应付不断增加的并发量, 并且能让查询速度保持在一个常量附近?

问题分析:

    1. 由于数据在不断增加, 我们肯定是要增加 Shard 的数量的, 使得每个 Shard 上的内存低于 50G.
    2. 由于查询请求的并发也在不断增加, 所以我们还需要增加 Replica Shard 来应付读操作.
    3. 注意, 你无法修改已经存在的 Index 的 Shard 数量. 你只能创建一个新的 Index 并设定更多的 Shard, 然后做 Re-index.
    4. 注意, 在做 Re-index 的过程中, 最好要将 Source Index 设为 Read-only. 不然 Source Index 依然会接受 Write request 导致最后的 Target Index 和 Source Index 中的数据不一致.
    5. 注意, 在做 Re-index 的过程中, 会占据 Source Index 的资源, 从而导致 Source Index 的响应速度变慢. 不过这个只针对 Main Replica, 其他的 Replica 还是可以服务于查询请求.
    6. 注意, 你可以给已经存在的 Index 增加 Replica Shard. 但是这个改变需要在下一个 Maintenance window 之后才能生效. Maintenance window 期间 Cluster 会短暂地变得不可用 (几十秒到几分钟不等).
    7. 注, 以上信息都是基于 AWS OpenSearch 的官方文档.

解决方案:

    1. 本解决方案是建立在 App 是允许一定时间的 Downtime 用来做升级, Migration 等操作的. 例如每周日的半夜 (周一的凌晨) 允许 15 分钟的停机时间. 我们假设每周都有一个 Maintenance window 可供我们进行 Scale up.
    2. 将数据写入到 OpenSearch 的 ETL Pipeline 有 buffer 机制. 使得我们能暂时切断写操作一段时间, 将期间本应写入的数据放在 buffer 中, 然后再恢复写操作之后 catch up.
    3. 当 Shard 中的内存接近 80% 上限时候将 Index 中的 Shard 数量翻倍 (翻倍后的使用量是 40% 上限). 并且做 Reindex, 这个在 System downtime 的时候做 (不需要停机). 只需要暂时切断写操作, 然后执行 Re-Index, 最后将请求切换到新的 Index 既可. 这个操作需要 Application code 做适配. 在 App code 里的 index name 需要到一个专门的服务上去获取. 而这个服务则会监控 Re-Index 的进度, 并且在完成后进行切换.
    4. 当 Shard 中的内存还比较充裕, 但是读请求太多导致延迟增加的时候, 我们可以增加 Replica Shard. 然后再 Maintenance window 之后生效.
    5. 以上操作都会增加 Shard 的数量. 请进行操作之前计算 Node 的数量是否能支持修改后的 Shard 数量. 如果不行, 请先 Scale Up Cluster.


Scale Up for a Cluster
------------------------------------------------------------------------------
情况:

    随着业务的扩张, 我们会需要存更多的 document 以及创建更多的 Index. 但是 Cluster 上无法增加更多的 Shard 了, 并且 Shard 的内存使用量已经逼近 50G 上限了

目标:

    如何让 Cluster 应付业务不断扩张的需求, 存更多的 document, 创建更多的 Index, 而不影响整体的性能?

问题分析:

    TODO

解决方案:

    TODO


AI Answer
------------------------------------------------------------------------------
Question::

    I am an Data Architect. I am exploring Amazon OpenSearch Service Cluster version. I am interested to know how does scaling up working in OpenSearch.

    I read from the official document that user can add nodes to OpenSearch cluster. In my understanding, if I have a very hot index receiving increasing read traffic, adding nodes doesn't solve the problem. What I need is actually adding shards. If feel like adding nodes can have extract computational resources for new index, but not useful for existing index.

    I want to hear your advice to see how could I scale opensearch cluster to adapt increasing read traffic on certain index.

Answer::

    You're correct that adding nodes to an Amazon OpenSearch Service cluster does not automatically solve the problem of a hot index receiving increasing read traffic. Adding nodes can provide additional computational resources and improve the overall capacity of the cluster, but it doesn't directly address the issue of distributing the load for a specific index.

    To scale an OpenSearch cluster to handle increasing read traffic on a particular index, you have a few options:

    1. Increase the number of shards for the hot index:
       - By increasing the number of shards, you can distribute the data and read load across more shards.
       - However, keep in mind that you cannot change the number of shards for an existing index once it's created. You would need to create a new index with the desired number of shards and reindex the data from the old index to the new one.
       - When creating a new index, carefully consider the number of shards based on your expected data volume and query patterns.

    2. Leverage replica shards:
       - Replica shards are copies of the primary shards and can help distribute the read load across multiple nodes.
       - Increasing the number of replica shards for the hot index can improve read performance by allowing more nodes to handle read requests in parallel.
       - You can dynamically adjust the number of replica shards for an existing index using the OpenSearch API.

    3. Optimize query performance:
       - Analyze and optimize your query patterns to ensure efficient querying on the hot index.
       - Use appropriate indexing techniques, such as creating relevant mappings and analyzers, to improve query performance.
       - Leverage caching mechanisms, such as query result caching or shard request caching, to reduce the load on the cluster for frequently executed queries.

    4. Implement index lifecycle management (ILM):
       - Use ILM to automatically manage the lifecycle of your indices based on predefined policies.
       - You can configure ILM to automatically roll over indices based on criteria like index size or time, which can help distribute the load across multiple indices.
       - ILM can also help with managing replica shards and optimizing indices for better performance.

    5. Consider data partitioning and index design:
       - If your hot index contains a large amount of data, consider partitioning the data into multiple indices based on a logical partition key (e.g., time-based partitioning).
       - By distributing the data across multiple indices, you can spread the read load and improve query performance.
       - Design your index structure and mappings to align with your query patterns and data access requirements.

    It's important to monitor your OpenSearch cluster's performance metrics, such as CPU utilization, memory usage, and query latency, to identify bottlenecks and make informed decisions about scaling. OpenSearch provides various monitoring and alerting features to help you track cluster health and performance.

    Remember that scaling is an iterative process, and you may need to combine multiple approaches based on your specific use case and requirements. It's recommended to test and validate any changes in a non-production environment before applying them to your production cluster.
