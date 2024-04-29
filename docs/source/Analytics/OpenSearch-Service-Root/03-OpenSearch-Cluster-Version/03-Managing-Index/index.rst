Manging Index
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Cluster, Manage, Index


Overview
------------------------------------------------------------------------------
Index 是 OpenSearch 中跟 RDBMS 中的 Table 对等的概念. 也是除了 DB 运维之外的数据库或者 App 管理人员最常管理的对象.


Reference:

- https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managing-indices.html


UltraWarm storage for Amazon OpenSearch Service
------------------------------------------------------------------------------
通常情况下索引是放在 Data Node 中的内存中的, 然后数据是放在 Data Node 上的磁盘中的. 这个磁盘的 Storage Tier 属于 Hot data, 可读可写. 而对于只读数据, UltraWarm storage 可以提供更低的成本.

UltraWarm 本质上是一个特殊设计的 EC2 Instance (Data Node). 你需要给你的 Cluster 添加这些 UltraWarm Node.

关于数据从 Hot data 到 Ultra Warm storage tier 之间的迁徙, 这里我们只列出一些应用场景, 但不展开讨论了.

1. 把已有的 Index 迁徙到 UltraWarm storage tier 中, 以节省成本.
2. 把已有的 UltraWarm storage tier 中的 Index 迁徙到 Hot data 中, 让它重新变得可写入.


Cold storage for Amazon OpenSearch Service
------------------------------------------------------------------------------
Code storage 是另一种用于数据归档的 Storage Tier. 它的特点是比 UltraWarm 成本更低.

Code storage 的本质是 UltraWarm node 上的一个功能, 你先要开启 UltraWarm 才能使用这个功能. 它允许用户通过一个 timestamp 的 field 筛选出自动被迁徙到 Code storage 中的 document 并完成自动迁徙.

但是 Code storage 中的数据是无法被实时查询到的, 你如果要查询, 你需要把 Code Storage 重新 attach 回 UltraWarm Node 上.


OR1 storage for Amazon OpenSearch Service
------------------------------------------------------------------------------
OR1 是一个专门为 OpenSearch 设计的 EC2 Instance. 它吸取了 UltraWarm 和 Cold storage 的经验, 在底层能将数据储存在 S3 中以降低成本, 同时也能提供实时查询的能力. 这使得为了达到同样的性能, 成本可以降低 30% 左右. 这个功能你只能在创建 Domain 的时候开启. 你无法在已有的 Domain 上开启这个功能.


Index State Management in Amazon OpenSearch Service
------------------------------------------------------------------------------
TODO (这个很重要, 以后补)

Summarizing indexes in Amazon OpenSearch Service with index rollup
------------------------------------------------------------------------------
Rollup 是一种能将历史数据进行汇总聚合分析, 将统计数据写入到一个新的 Index 上, 并从原始的 Index 中删除原始文档, 从而能大幅降低储存成本的功能. 这个 Rollup 本质上是一个 Fully managed Cron Job. 通常你需要用一个 Lambda function 或者定时任务来实现这一功能, 但是 OpenSearch 可以帮你自动完成这种 Job.


Transforming indexes in Amazon OpenSearch Service
------------------------------------------------------------------------------
Transform 是一种能根据自定义的数据的查询, 把结果写入到一个新的 Index 作为一个 view 的功能. 这相当于数据库系统中的 Materialized view (普通的 view 需要临时 run query, materialized view 是将结果写入到新的表中). 通常你需要用一个 Lambda function 或者定时任务来实现这一功能, 但是 OpenSearch 可以帮你自动完成这种 Job.


Cross-cluster replication for Amazon OpenSearch Service
------------------------------------------------------------------------------
这个主要是给 Disaster Recovery 设计的. 你可以把一个 OpenSearch Cluster 跨账号, 跨区域滴复制到另一个 OpenSearch Cluster 中从而实现两地灾备.


Migrating Amazon OpenSearch Service indexes using remote reindex
------------------------------------------------------------------------------
Remote index 是一个为了数据迁徙而设计的一个单项数据同步的工具. 你可以在不中断服务的情况下从其他的 OpenSearch 或者 ElasticSearch index 把数据迁徙到新的 OpenSearch 中. 本质上它就是一个专门为 OpenSearch 设计的 AWS DMS 服务, 只不过运行在 OpenSearch Cluster 之上的一个程序.


Managing time-series data in Amazon OpenSearch Service with data streams
------------------------------------------------------------------------------
Time series index 是一种 OpenSearch index type. 对于 Times series index 通常你都需要手动管理 rollover (跟前面的 rollup 类似, 都是自动迁徙旧数据到新的 Index 中), 只不过 AWS OpenSearch 把这一步骤自动化了, 你无需额外维护任何 Computational resource 例如 Lambda 之类的. 然后你查询的时候还需要用不同的 index 进行冷热数据查询的切换.

而 data streams 功能则是不仅自动化了 rollover, 并且提供一个抽象, 使得你只需要再这个抽象的 index 中查询, query engine 会自动管理后台的这些 index 切换以及数据汇总. 我个人觉得这一功能非常牛逼.
