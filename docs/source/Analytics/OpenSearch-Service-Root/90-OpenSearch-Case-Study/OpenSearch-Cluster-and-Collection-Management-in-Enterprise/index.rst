Case Study - OpenSearch Cluster and Collection Management in Enterprise
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Management

Tags: :bdg-primary:`Case Study` :bdg-primary:`Big Data` :bdg-primary:`Analytics` :bdg-primary:`Search` :bdg-primary:`OpenSearch`


Background
------------------------------------------------------------------------------
ABC Corp (Vanguard) 是一家基金管理公司, 它们是 OpenSearch 的重度用户. 它们的 财务报表数据, 内部的分析文档, 法律文件, Slack 聊天记录, Email 记录, 等很多数据都存在 OpenSearch 中需要进行搜索. 如果将 Schema 类似的文档视为一个 Dataset, ABC 有 200 多个 Dataset. 这些 Dataset 中的数据量, 新数据增量, 以及 Schema 都大不相同. 目前, ABC 公司的 Dataset 的数量和数据量还在不断快速增长中.

目前 ABC 公司使用了一个超大型的 Cluster, 下面有很多个 Index, 然后它们把所有的 Document 都存到这个 Cluster 中的不同的 Index 中.**现在 ABC 公司的搜索服务遇到了很多问题**:

1. 当需要 Scale Cluster 的时候,


1. 由于所有数据都在一个 Cluster 上, OpenSearch Cluster 的 scale 不灵活.
2. 各个 Index 的读写 traffic 不一样, 有的 index 写入压力很大, 有的搜索压力很大. 导致必须为压力最大的 index 来规划 Cluster sizing, 造成了很多浪费.
3. 把 Document 写入 index 的时候是凭人类常识, 将 schema 类似的 document 放在一个 index 中. 这样做由于缺乏设计, 造成了很多 tech debt, 导致这个 index 无法适应新需求.

**所以 ABC 公司考虑重新设计 dataset 和 index 以及 cluster 之间的从属关系. 但是 ABC 公司非常困惑应该按照什么样的原则来重新设计. 所以它们找到了 AWS 希望寻求解决方案**. 而我则是负责这个 Case 的架构师.


Problem Analysis
------------------------------------------------------------------------------
我拿到这个 Case 之后, 通过了几次会议了解了客户的具体需求和关键的技术挑战.

从用户的角度看, 客户实际上最终的需求就是:

1. 当需要 Scale Cluster 的时候, 尽量搜索服务受到影响的时间. 由于目前只有一个巨型 Cluster, 所以一旦 Scale 必然要影响所有的搜索服务.
2. 在确保能满足所有的搜索服务的前提下, 尽量缩减开支. 由于目前只有
3. 当有的搜索服务遭遇突发流量, 导致系统被击穿, 服务不可用的时候, 不影响其他的搜搜服务.
3. 当需要为



**是否应该把多个 Dataset 放到同一个 Index 中**

    由于 OpenSearch 不 enforce schema, 所以你是可以将不同 Schema 的文档放到一个 index 中的. 这种做法是否合理取决于你的数据和应用场景.

**如何合理的 Scale**

对 OpenSearch 的 scale 是以 Cluster 为单位的. 所以我们应该把读写 workload 分布类似的 index 放到一个 Cluster 中.

**如何合理的对 Workload 进行隔离**

由于 OpenSearch 的 系统隔离也是以 Cluster 为单位的, 一个 index 的 traffic 过高会影响在同一个 Cluster 上其他 index 的性能. 所以我们应该将必须要隔离开的 business workload 放在不同的 cluster 中.

**如何跨 Index 和 Cluster 搜索**

    当 Dataset 分散到 Index 和 Cluster 之后, OpenSearch 官方支持的一些特性能帮我们解决跨 Index 和 Cluster 的问题.

    - Multi Search: https://opensearch.org/docs/latest/api-reference/multi-search/
    - Cross-cluster search in Amazon OpenSearch Service (Serverless Collection 还不支持这一功能): https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cross-cluster-search.html

    除此之外, 我们还可以自己用 AWS Lambda 或者 ECS Task 搭建一个 Coordinator + Worker 的架构, 来将跨 Index 和 Cluster 的搜索分散到不同的 Worker 上然后让 Coordinator 进行汇总.



是一个漏洞扫描产品. 它能扫描你在 AWS 云上的资源的漏洞, 并生成实时 (数据从产生到显示到面板上的延迟不超过 5-10 分钟) 监控面板, 报表数据, 以及列出漏洞的详情以及修复方法.

它在全球有 5000 多家企业客户. Rapid7 主要使用 Redshift 来储存扫描数据. 平均下来, 每天会产生 2.5 Trillion 行数据, 大约压缩后有 50 GB. 它们的客户在各自的 SAAS 平台上只能看到自己的数据. 这是一个典型的多租户的 Use Case. 此外, 它们有些大客户还有将多个 Team 拥有的不同的 Rapid7 账户下的数据合并到一个 Dashboard 上的需求, 要求能对账户的排列组合进行灵活的配置.

目前 Rapid7 的 Redshift 是用了一个 database, 并为每个客户的表都加了客户名的前缀, 每个客户有 10 张表. 现在集群遇到了一些问题. 例如:

1. 数据延迟随着客户的增加以及数据量的增加越来越慢了, 已经经常出现超过 10 分钟的数据延迟的情况. 在随机出现的 Peak 时候会更慢 (超过 30 分钟), 而 Peak 的时候恰恰是 Security 更容易出问题的时候, 这样的数据延迟会影响它们的客户信任.
2. 它们的客户群还在快速增长, 而目前 5000 个客户已经占用了 5000 * 10 张表了. 而 Redshift 一个 Cluster 最多有 200000 张表 (hard limit), 它们担心现有架构无法支撑未来的增长.
3. 它们客户要求的能对账户的排列组合进行灵活的配置这个需求 Rapid7 在现有架构上不知道如何实现. 这样会导致 Rapid7 的客户需求无法被满足.

所以, 客户寻求资深 Redshift 架构师来帮助他们解决这些问题.


Technical Challenge
------------------------------------------------------------------------------
以上的问题可以被总结为以下几个技术问题:

1. 现在 5000 个企业客户总共平均每秒钟产生 30 million 行数据, 如何设计表结构以应付高频率大量的写入. 总体的扫描数据从被生成出来到可以再 Redshift 中被查询的延迟要在 5 - 10 分钟. 这里还有个情况根据客户的 App 遇到的随机事件写入的时候会有 peak, 并且 peak 的时间段是不确定的, 但是 peak 时的写入量会是平时的 10 倍左右.
2. 对于 95% 的查询, 响应时间要在 5 秒以内. 因为 95% 的查询都是在 Dashboard 上展示指标. 而对于另外 5% 可能耗时较长的查询, 也要能在可接受的时间内完成.
3. 能满足每秒钟 15 个并行查询, 今后的要求可能会更高. 因为目前 5000 个用户平均每 5 分钟查询一次. 这也就是 5000 / 300 ~= 17 个并行查询, 实际没有这么多.
4. 对于不同的用户要能做到数据隔离. 不能允许一个用户在看自己的 dashboard 的时候看到了其他用户的数据的情况.
5. 有的大客户有多个账号, 它们想要能对不同的账号灵活的排列组合并将数据汇总.


How do I solve Technical Challenge
------------------------------------------------------------------------------
1. 首先经过我的分析, 我认为所有的需求的核心是 Data Modeling. 这是实现数据隔离以及高效查询的关键. 现有的基于分表的方式不是长久之计. 于是我调研了 Multi tenant 用例的常用数据模型, Pool Model, Silo Model 和 Bridge Model. 这里我简单解释一下, pool model 就是将不同 tenant 的数据放在一个 table 里, 用一个字段 tenant 来标记 owner. model silo 则是给每个 tenant 一个单独的 database, 也就是不同 tenant 在物理意义上的隔离. bridge model 则是介于两者之间, 所有的 tenant 都在一个 database 下, 但给每个 tenant 一个单独的 schema, 每个 schema 中的表的结构都类似. 我详细比较了几种方法:
    - 首先我们要满足数据隔离, 因为这是没得商量的需求, 所以我们从隔离级别最高的 silo 开始评估.
    - 首先排除 silo, 因为 redshift 只支持最多 60 个 database (hard limit), 这样算下来就要 5000 / 60 ~= 84 个 redshift cluster, 这会让运维变得非常麻烦.
    - 其次考虑了 bridge model, Redshift 支持一个 database 9900 个 schema (hard limit), 也就是最多支持 9900 个 tenant, 未来可能会有问题. 好处是这样每个 tenant 的表都不大, 查询的速度比较快. 但是在写入数据的时候每个 tenant 需要单独 commit, 这样导致写入过于频繁, 大量占用资源, 会影响其他 tenant 的查询.
    - 最后考虑了 pool model, 这样做可以支持几乎无限数量的 tenant. 并且写入数据时可以在写入前把多个 tenant 的数据 merge 成大批量数据进行 bulk insert, 写入性能较高. 但是需要对大表进行合理的设计才能保证查询性能.
    - 最终我决定使用 pool model, 这样能满足不断增长的 tenant 数量, 以及写入性能的要求. 我有信心能通过合理的设计来保证查询性能.
2. 为了保证数据写入性能, 我做了以下几点:
    - 我认为要最大化利用 pool model 的优势, 来将来自于不同 tenant 的写入聚合成较大的数据块再写入. 我用 AWS Lambda 对进来的数据进行扫描, 然后根据数据文件的大小将大大小小的数据分组, 确保每一组的总大小差不多. 然后为每一组创建一个 manifest 文件然后用 COPY Command 来并行写入数据 (一个 manifest 中的多个文件是并行写入的), 这样就大幅提高了写入吞吐量.
    - 我发现 Rapid7 并没有对它们的数据进行极致的优化, 我认为还有很多的优化空间. 我为每个字段选择了最优的压缩算法, 例如我对 tenant_id 字段用整数对实际值进行了映射 (Byte-dict 只支持 256 种以下的情况, 而我们有 5000+ tenant), 对 event_time 字段使用了 Delta compression, 对一些 measurement 字段使用了 run length 来压缩, 因为这些字段在时间序列上很长一段时间都保持不变.
3. 为了保证查询性能, 我调研了如何通过选择合理的 sort key. 因为在查询数据的时候, 通常在 where 中会包含两个字段 ``tenant_id = 'a1b2c3'`` 和 ``event_time BETWEEN ...`` 我比较了以下四种方案, 并且测量了 benchmark, 最终决定使用 ``(tenant_id, event_time)`` 方案. 因为 tenant_id 是第一个 filter 优先级, 并且很可能会用于 JOIN, 所以放在第一位. event_time 也是一个常用的 filter, 放在第二位. 这样可以保证查询性能.
    - tenant_id
    - event_time
    - (tenant_id, event_time)
    - (event_time, tenant_id)
4. 以上的设计已经能满足 95% 的查询在 5 秒以内完成, 而对于 5% 的查询, 我启用了 Concurrency Scaling (是 Redshift 的一个 feature) 使得能够在需要额外计算资源做复杂度较高的查询时自动启用额外计算资源来保证任务能够尽快完成. 为此我帮客户做了 Workload Management 的配置, 定义了什么 Query 要交给 Concurrency Scaling 来执行. 并且 Concurrency Scaling 还能提高繁忙时期的 COPY Command 的写入性能.
5. 为了进一步的提升查询性能, 我还提出了一些额外方案, 例如:
    - 用 materialized view table 来提升查询性能, 缓存中间态的数据表.
    - 为 dashboard 的查询设计了智能化的缓存, 并对 redshift 进行了优化从而能检测到何时需要 expire 缓存, 提高了一些常用操作的响应时间, 例如刷新.
6. 为了保证用户数据隔离, 我开发了一个 middleware 用于创建包含有合适的 ``WHERE tenant_id = 'a1b2c3'`` 的查询, 并且使用了 ORM 框架以预防 SQL 注入. 在执行查询之前, 使用 SAAS 平台登录的 token 获取对应的 tenant_id 并最终生成 SQL 进行查询.
7. 为了解决拥有多个账号的用户想要灵活的对账号数据进行聚合的需求, 我设计了一张额外的表 tenant_group 用于记录 tenant_id 和 tenant_group_id 之间的对应关系, 用户只需要把想要聚合的账号给放到一个 tenant_group 下即可. 默认情况下每个 tenant_id 都会有一个自动创建的独立的 tenant_group. 然后进行一些简单的 JOIN 就能够实现基于 tenant_group 的数据隔离.


Non Technical Challenge
------------------------------------------------------------------------------
1. 跟我对接的客户的头是 chief product officer (CPO), 这个 CPO 刚上岗 2 个月, 他只能从产品的角度理解遇到的困难的表象, 但由于对后台系统不够熟悉, 无法给我提供更精确的信息帮我找到底层原因.
2. 我在设计方案的时候, 客户无法给我权限直接访问它们的 Production Redshift Cluster, 这样我就很难验证我的设计能在这么高的压力下依然能正常工作.



How do I solve None Technical Challenge
------------------------------------------------------------------------------
1. 我用选择题的方式提问引导 CPO, 在没有足够信息的情况下, 让他知道可能有哪些原因. 然后引导他帮我找到合适的人员对接. 我在对接之后将搜集到的信息和结论用可视化和浅显易懂的方式呈现给他. 这样也建立了客户信任.
2. 虽然出于数据安全的原因, 我无法利用他们的生产数据. 但我用技术手段模拟了和他们生产数据相同的流量 (用 StepFunction orchestrator + Lambda function worker). 由于我已经获取了他们的信任, 他们也增加了 budget, 供我创建更多的资源来模拟生产数据.


Result
------------------------------------------------------------------------------
Rapid7 Result:

- 总体的数据延迟重新回到了 5-10 分钟以内. 并且该架构设计能确保在数据量是现有的 10 倍的情况下依然能保证 5-10 分钟的数据延迟.
- 总体查询性能更快了, 能允许更高的并发量, 用户体验更好了.
- 可以轻松应对无法预测的 peak 写入流量和查询请求, 减少了 complain ticket 的数量, 提高了 customer satisfaction.
- 尽快满足了大客户的需求, 加强了大客户对他们的信任, 锁定了非常客观的利润.

BMT Result:

- 这个项目在 3 个月内为 BMT 带来了 $250,000 的收入.
- 收获了对方 Rapid7 CPO 的信任. 他们还在告诉发展期, 需要发布更多创新的产品. 他们的新 CPO 在新加入的这段时期也获得了很多来自于 BMT 的帮助, 他们希望将 BMT 作为他们的长期合作伙伴.


Reference
------------------------------------------------------------------------------
- `How Rapid7 built multi-tenant analytics with Amazon Redshift using near-real-time datasets <https://aws.amazon.com/blogs/big-data/how-rapid7-built-multi-tenant-analytics-with-amazon-redshift-using-near-real-time-datasets/>`_: Rapid7公司是如何实现 Multi tenant 近实时数据分析的.
- `Implementing multi-tenant patterns in Amazon Redshift using data sharing <https://aws.amazon.com/blogs/big-data/implementing-multi-tenant-patterns-in-amazon-redshift-using-data-sharing/>`_: 详细介绍了如何使用 Redshift Data Sharing 实现 Multi tenant.
