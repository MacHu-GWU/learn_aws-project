Case Study - Athena Workload Management for Agriculture Internet of Things Company
========================================================================================
Keywords: AWS, Amazon, Athena, WLM

Tags: :bdg-primary:`Case Study` :bdg-primary:`Big Data` :bdg-primary:`Analytics` :bdg-primary:`Athena`


Background
------------------------------------------------------------------------------
C 公司是一个农业服务公司, 业务包括 Agricultural trading & processing, Supplements 等农业相关服务. 它们在 farm 和 supply chain storage 里安装了很多它们的 sensor 和 IOT 设备. 这些设备由太阳能供电, 通过卫星网络不断地将采集到的数据发送到 Data Lake 中. C 公司的数据科学家们基于 industry knowledge (行业知识) 用 Datalake 中的数据开发了很多算法, 可以计算出很多重要的 business concept metrics. 这些算法被部署在 AWS Lambda 和 Glue 上, 每天不间断滴运行.

在 ETL logic 中 C 公司使用了很多 Athena query 来筛选数据, 简单地处理数据, 以及生成报表. 这些业务用到了很多旧的 SQL, 不适合迁徙到 Spark 中, 而且里面大量用到了 federated query (联合查询, 跨数据源查询), 不适合用 Spark 来做. 由于 ETL Job 的并发量大, 运行频率高, 占用的 Service Quota 长期在 30% - 70% 之间波动.


Technical Challenge
------------------------------------------------------------------------------
目前 C 公司遇到了如下问题:

1. 有的时候数据科学家们进行探索性实验时, 由于没有经验, 写出来不够优化的 query, 导致大量占用 Quota 并影响到了成熟稳定的那些 ETL Job.
2. 有的 ETL Job 需要扫描的数据较多, 有的需要扫描的数据少, 有的运行时间长, 有的运行时间短. 总体来说扫描的数据量比较容易预估, 但是并发量不好预估. 所以经常会出现 ETL Job 中的 Athena query 阻塞的情况.

现在客户的 ETL Job 已经经常受到影响而导致较大的数据延迟, 甚至是 failure. 客户希望能解决这些问题, 保证成熟业务能稳定运行, 但又给数据科学家自由度来进行探索性分析.

所以, 客户寻求资深 大数据架构师 来帮助他们解决这些问题.


How do I solve Technical Challenge
------------------------------------------------------------------------------
1. 经过我的分析, 我认为问题的根源是它们的 query 欠缺管理. 导致不同目的, 不同特性 (characteristic) 的 query 都混在一起.
2. 我认为 Athena Workgroup management 功能可以解决这一问题.
    - 我创建了 5 个 workgroup, 分别是: predictable, fast query, long query, exploratory, ad-hoc.
    - predictable: 成熟, 可预估, 稳定的 query. 根据计算出的 quota, 设定了 1 hour workgroup data usage limit, 并额外再给了 10% 的 buffer.
    - fast query: 能快速完成的 query, 设定了 per query data usage limit 并且没有给 buffer. 因为 fast query 就算失败了, 重试的代价也不大.
    - long query: 需要较长时间运行的 query, 根据计算出的 quota, 设定了 1 day workgroup data usage limit, 并额外再给了 100% 的 buffer 来确保能够运行成功.
    - exploratory: 探索性实验的 query, 根据计算出会影响生产环境的阈值, 按照阈值的 70% 设定了 1 hour workgroup data usage limit, 如果超过了这个限制那么就给 query 发送者发邮件警告.
    - ad-hoc: 这个 workgroup 的 data usage limit 设的很低. 由管理员和脚本管理, 在需要的时候增加 quota 临时运行一些 query.
3. 并且我还设置了一个 Lambda function 定期去 CloudWatch log metrics 去查 metrics, 如果因为我们设定的 quota 不合理而导致资源就快用尽, 则自动给管理员发邮件警告.
4. 既然现在有了 5 个 workgroup, 我们就要对应地为用户配置权限. 我们收回了所有人默认的可以使用任何 workgroup 的权限, 然后创建了 5 个对应的 IAM Policy. 谁需要这些权限就给谁 attach Policy.


Non Technical Challenge
------------------------------------------------------------------------------
1. 跟我对接的客户的头是 VP of Data Analytics, 他比较懂业务, 但并不是很懂具体有哪些 ETL Job. 所以一开始我只能发现 ETL Job failure 了很多, 而他也无法给我提供有效信息帮我定位问题.
2. 我对他们给的 deal 其实并不满意, 我 negotiate 了, 但是客户没有这个 budget. 可是我也不想放弃这个客户, 因为我认为我的技能还能不断地给他们的数据系统带来价值.


How do I solve None Technical Challenge
------------------------------------------------------------------------------
1. 我用思维导图的方式引导这个 VP, 让他知道可能存在的 bottle neck, 然后针对它懂的领域, 业务问题进行提问 (从结果出发, 问他为什么收集这些传感器数据, 为什么要计算这些 business concept metrics, 不计算的话会导致什么不良后果, 一步步问), 从业务的角度来说估计哪些 ETL Job 会比较重要, 哪些 ETL Job 的负载较高, 哪些 ETL Job 比较难以预估. 从而最终得到了一个有许多 detail 的 big picture. 下一步只要他帮我对接具体的 engineer 确认这些信息即可.
2. 我跟客户签合同的时候约定了由我来负责具体的开发, 我甚至在之前的价格上给他们还打了 30% 的折扣, 并且将工期从 3 个月缩小到了 2 个月. 因为这个项目的本质是 management, 以及长期的 monitoring, alarm 和 dynamic optimization. 既然有长期的 monitoring, 我知道他们以后必然还要找我. 而我给他们把活干的又快又好, 还少收他们钱, 这样能取得他们的信任, 从而获得更多的 contract. 结果因为我在做项目的过程中对他们的 ETL Job 更熟悉了, 果然他们又有 ETL Pipeline 的需求就又找到我来设计了.


Result
------------------------------------------------------------------------------
C 公司 Result:

- 所有的重要的 ETL Job 都没有再因为 Athena 出现过问题.
- 对于需要长时间运行的 Query, 也几乎没有出现过问题, 避免了昂贵的重试代价.
- 它们的数据科学家能更有信心地进行探索性实验, 而无需担心自己影响了生产环境中的 ETL Job.
- 我帮他们准备了给 SVP 汇报的 PPT 和 demo, 演示很成功, 它们的 SVP 很高兴.

BMT Result:

- 这个项目在 2 个月内为 BMT 带来了 $100,000 的收入.
- 项目结束后 3 个月我又跟他们签了一个 ETL Pipeline & Orchestration 的项目.


Reference
------------------------------------------------------------------------------
- `Athena Workgroup Management <https://docs.aws.amazon.com/athena/latest/ug/workload-management.html>`_
