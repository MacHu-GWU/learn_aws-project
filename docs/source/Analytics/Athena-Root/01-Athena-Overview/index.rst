.. _aws-athena-overview:

Amazon Athena Overview
==============================================================================
Keywords: AWS, Amazon, Athena, Overview.


Background of Massively Parallel Processing (MPP) SQL Engine
------------------------------------------------------------------------------
在 2005 - 2010 的前云时代, 数据仓库技术开始成为大型企业的基础设施的一部分. 但是数据仓库产品往往价格高昂, 并且由于数据仓库的架构设计既要满足大容量数据存储和更新, 还要满足高性能查询, 它的开销就不太可能大幅下降. 而很多初创企业依然是由数据仓库的需求的, 但由于公司规模和资金限制, 不可能购买昂贵的数据仓库产品. 于是很多企业就开始思考全新的解决方案.

这些方案中, 有一种方案开始脱颖而出. 它的核心原理是用廉价的数据存储来保存数据, 有分析需求的时候用廉价的虚拟机集群来并行查询. 这种方案专注于以查询为目的的数据读取, 而数据的写入则完全交给了开发者自己决定. 由于数据存储非常链接, 而将数据写入到廉价存储的过程本身开销也很小. 相比之下, 数据仓库产品往往需要用昂贵的大型机储存数据, 并且写入数据也需要昂贵的大型机一直在线, 价格自然不菲. 而查询则交给了廉价的虚拟机集群来进行, 由于集群中的机器数量众多, 并且是一个大规模并行系统, 根据算力的需求增加和减少机器也非常容易. 相比之下, 给数据仓库产品添加和减少大型机节点并不容易, 而且价格也很高.

这种方案中最知名的项目是由 Facebook 开发, 在 2013 年捐献给开源社区的 Presto 查询引擎. 后来还出现了基于 Presto 的商业化公司 `PrestoDB <https://prestodb.io/>`_. 又后来 2019 年 Presto 团队中的有些人和 PrestoDB 的商业化理念出现了分歧, 于是另起炉灶开发了一个新项目 `Trino <https://trino.io/>`_, 主打开源精神. 这是后话, 按下不表.


Background of Amazon Athena
------------------------------------------------------------------------------
AWS 最擅长的就是将开源技术部署在自家的云基础设施上, 将其包装成更易用的产品卖给客户. 由于为了使用 Presto 还是需要运维人员配置集群, 安装软件, 连接网络, 维护, 增加, 减少集群中的节点, 企业用户还是需要投入一定的人力和资金才能使用 Presto.

2016 年 11 月, AWS 发布了 Athena. 是一款无需管理基础设施, 就能直接分析位于廉价存储上的数据的产品. 后来基于 Glue Catalog 和 Data Connector, 也能分析位于数据库, 数据仓库中的数据了. 不过它的杀手锏还是分析廉价存储上的数据.

`Athena 的收费模型 <https://aws.amazon.com/athena/pricing/>`_ 是按照它扫描的数据量收费, 不实用的时候不收费. 这就意味着个人开发者无需高昂的成本也能用小型数据集进行原型验证. 对于初创企业来说, 用多少花多少. 无论多大的数据 Athena 都能胜任, 这样就能给初创公司节约非常多的成本. 从长期来看, 投入成本越低, 越易用的产品就越能吸引开发者和用户, 从而形成网络效应, 形成产品的护城河.

本质上, Athena 就是一个或者很多个由 AWS 维护的超大规模 Presto 集群. 这个算力池子很大, 并且能弹性伸缩. 而用户实际上是从 AWS "租" Presto 算力来进行查询分析. 而用户完全无需关心基础设施, 调度等问题, 从而能专注于业务逻辑.


How it Work
------------------------------------------------------------------------------
**Database and Table**

在 RDBMS 系统中, 要使用 SQL 前你需要定义 Database, Table. 而在 Athena 中其中 Database 仅仅是一个逻辑概念, 是 Table 的集合. 每个 AWS Account 下有一个内置的 Database. 而每一个 Table 对应的其实是一堆描述你的 Dataset 的 metadata. 包括了你的数据储存在哪里 (location), 数据格式是什么 (format), 数据二维组织结构是怎样的 (schema), 如何对其进行反序列化, 也就是将其读取到内存 (serde), 有哪些人可以访问这个数据 (access), 数据量有多少, 有多少个文件 (statistics), 有没有 partition key 可以利用以避免全量扫描 (partition / index).

AWS Glue Catalog 是 AWS 基于 Hadoop Hive 标准开发的中心化 Metadata Store, 你为定义的 Database / Table 又被叫做 Glue Database, Glue Table. 有了这些定义, Presto 就知道如何在你的 Dataset 上执行 SQL 查询了.

**SQL 查询引擎原理**

这本质上是 Presto 的内容, 不过这里我们就简单描述一下. 当你运行一个 SQL 的时候, Presto 的调度器 (Coordinator) 就会把你的 SQL 发给查询优化器 (Optimizor). 查询优化器就会根据你的 Glue Table 的信息, 分析应该怎么去执行这条 SQL. 然后调度器就会把查询按照 Partition 分发给许多 Worker 节点去执行, 然后执行的结果由调度器汇总, 最后返回给你.


How to Learn Amazon Athena
------------------------------------------------------------------------------
我建议先通读 FAQ, Pricing, What is Amazon Athena 这三部分. 这三个部分加起来也不长, 能很快的对 Athena 有一个大概的了解.

- `Amazon Athena FAQ <https://aws.amazon.com/athena/faqs/>`_
- `Amazon Athena Pricing <https://aws.amazon.com/athena/pricing/>`_
- `What is Amazon Athena <https://docs.aws.amazon.com/athena/latest/ug/what-is.html>`_

然后再根据自己的需要精读官方文档. 由于 Athena 需要依赖于 Glue Catalog Table 才能工作, 所以也要学习如何为 S3 上的 CSV 数据创建一个最简单的 Glue Catalog Table. 接下来就可以深入学习 Athena 的 SQL 语法了 (本质是 Presto SQL).

- `Amazon Athena Documentation <https://docs.aws.amazon.com/athena/latest/ug/what-is.html>`_
- `Getting started with the AWS Glue Data Catalog <https://docs.aws.amazon.com/glue/latest/dg/start-data-catalog.html>`_
- `SQL Reference for Athena <https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html>`_

接下来就可以开始基于 Athena 学习如何构建一些应用了. 其中 AWS 官方博客上有很多精品文章. 其中这篇 Top 10 Performance Tuning Tips for Amazon Athena 属于必读.

- `AWS Big Data Blog - Amazon Athena <https://aws.amazon.com/blogs/big-data/tag/amazon-athena/>`_
- `Top 10 Performance Tuning Tips for Amazon Athena <https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/>`_

在进行开发的过程中, Python 库 `pyathena <https://pypi.org/project/pyathena/>`_ 是一个非常优秀的工具, 可以让你在 Python 中使用 Athena. 此外, 还有如下扩展包以及 `awswrangler <https://aws-sdk-pandas.readthedocs.io/en/stable/index.html>`_ 也很好用.

- ``pip install PyAthena[SQLAlchemy]``: SQLAlchemy integration
- ``pip install PyAthena[Pandas]``: Pandas integration
- ``pip install PyAthena[Arrow]``: Apache Arrow integration
- ``pip install PyAthena[fastparquet]``: fastparquet integration
- `awswrangler.athena.read_sql_query <https://aws-sdk-pandas.readthedocs.io/en/stable/stubs/awswrangler.athena.read_sql_query.html>`_: Execute any SQL query on AWS Athena and return the results as a Pandas DataFrame.


Athena Knowledge Graph
------------------------------------------------------------------------------
以下是 Athena 的知识图谱, 对所有的知识点进行了一个梳理.

- Understand database, table, and catalog


What's Next
------------------------------------------------------------------------------
todo
