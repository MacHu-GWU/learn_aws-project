.. _aws-redshift-overview:

Amazon Redshift Overview
==============================================================================
Keywords: AWS, Amazon, Redshift, Overview.


Background (Short Data Warehouse History)
------------------------------------------------------------------------------
在关系数据库最辉煌的 2000 - 2010 时代, 商用的 Oracle, IBM DB 2, Microsoft MSSQL, 开源的 MySQL, PostgresSQL 百家争鸣. 不过由于互联网爆发式的增长, 对大数据进行分析的需求也越来越大, 用传统关系数据库做分析就变得越来越难了, 只有 Oracle, DB2, MSSQL 这些商用数据库还能挺住, 但是价格也是高的吓人.

Google 在 2003 - 2006 年的三篇 GFS, MapReduce 和 Bigtable 三篇论文, 开启了大数据时代, 于是大数据系统 Hadoop 开始发展, 但是它本质上是一个技术, 一套软件, 并不是一个产品. 虽然后面有 Cloudera 公司将其商业化, 但是这个是数据仓库发展史中的一个引子, 我们不再深挖.

`Google 在 2011 年 11月 正式发布了 Big Query <https://en.wikipedia.org/wiki/BigQuery>`_ 一款云原生的数据仓库产品. 该产品从头到尾都是 Google 自研. 不过 Google 的产品都是一如既往的高冷, 技术很牛, 但是不接地气. 技术实力不强的客户上手不易.

之后亚马逊快马加鞭跟上, 基于 Postgres 修改而来研发了 AWS Redshift, `并于 2013 年 2 月发布 <https://en.wikipedia.org/wiki/Amazon_Redshift>`_ . 它也是一款云原生 OLAP 数据仓库产品. 亚马逊的产品贯彻了客户之上的理念, 一切围绕客户服务, 导致 Redshift 的易用性, 还有许多终端客户需要的额外功能, 例如权限管理, 算力管理等, 使得 Redshift 大火. 据说, 该产品是 AWS 内部盈利能力连续多年增长速度最快的产品.

以上两家都是巨头之间在数据仓库领域的布局, 在此期间, 2012 年, 两名 Oracle 公司的大牛离职, 创办了 Snowflake 公司. 它的理念是做云中立 (可以在任何云上部署) 的数据仓库产品. 同时它也是一款纯 SAAS 的产品, 按照用户的用量收费, 无需自己部署和安装任何软件, 所有工具都是用户 subscribe 后登录即可用. Snowflake 于 `2014 年 10 月正式发布了 Snowflake <https://en.wikipedia.org/wiki/Snowflake_Inc.>`_ 并于 2020 年 IPO 上市, 创造了当时最大的 IPO.

微软的 Azure 发力比较晚, `在 2019 年 11 月才发布了自家的云原生数据仓库产品 Azure Synapse Analytics <https://azure.microsoft.com/en-in/products/synapse-analytics>`_.

总结下来 Redshift 算是数仓产品的第一梯队, 并且背靠 AWS 庞大的生态空间, 是企业选择数仓产品的首要考虑对象之一.

Reference:

- 数据仓库发展史: https://cloud.tencent.com/developer/article/2109058
November 2011.
- Snowflake vs AWS vs Azure: Top 8 Unique Differences: https://hevodata.com/learn/snowflake-vs-aws-vs-azure/


Overview
------------------------------------------------------------------------------
作为数据仓库 Redshift 支持秒级对 PB 级数据进行查询. 支持丰富的数据格式, 查询函数, 以及和其他 AWS 服务紧密结合, 还能支持在 Redshift 中进行 ML 计算.

作为一款产品 Redshift 提供了丰富的管理功能, 方便用户对权限, 数据访问, 算力, 用量进行管理.

为了满足数据安全和合规的需要 Redshift 还支持多种数据加密方式, 以及权限管理方式. 所有的数据库操作和 API 操作都有日志记录用于审计.

Amazon Redshift 有两种部署模式:

- **Provisioned Cluster 模式**. 你通过简单的几下点击启动集群, 自己监控系统指标, 并且根据情况添加, 减少节点.
- **Redshift Serverless**. 2022 年 7 月 AWS 发布了 Redshift Serverless, 用户只需要指定一个最小 RPU (Redshift Processing Unit) 和最大 RPU, 在这之间 Redshift 会自动根据需要 Scale Up / Down, 大大的减少了管理工作. 而且你放在那里不用就不花钱, 只有你运行 SQL 的时候才会花钱, 非常适合初创企业.


How to Learn Amazon Redshift
------------------------------------------------------------------------------
Redshift 的官方文档有下面几个部分. 我建议先通读 FAQ, Pricing, Getting Start Guide 这三部分. 这三个部分加起来也不长, 能很快的对 Redshift 有一个大概的了解. 然后再根据自己的需要深入学习. 如果你主要是运维管理, 那么就精读 Management Guide. 如果你主要是数据开发写 CRUD 和 SQL, 那么就精读 Management Guide.

- `Amazon Redshift Documentation <https://docs.aws.amazon.com/redshift/index.html>`_: Redshift 的文档总站.
- `Amazon Redshift FAQ <https://aws.amazon.com/redshift/faqs/>`_: 关于 FAQ.
- `Amazon Redshift Pricing <https://aws.amazon.com/redshift/pricing/>`_: 关于价格.
- `Amazon Redshift Getting Start Guide <https://docs.aws.amazon.com/redshift/latest/gsg/new-user-serverless.html>`_: 快速上手的文档, 适合第一次使用的用户. 有了基本的了解之后, 可以看 Amazon Redshift Management Guide 和 Amazon Redshift Database Developer Guide 两个详细文档了.
- `Amazon Redshift Management Guide <https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html>`_: 主要介绍了管理 Redshift 的知识, 例如创建, 维护, 备份, 删除 Redshift 等. 如果涉及到使用 Redshift 进行开发, 可以参考 Amazon Redshift Database Developer Guide.
- `Amazon Redshift Database Developer Guide <https://docs.aws.amazon.com/redshift/latest/dg/welcome.html>`_: 这个主要是给负责 CRUD 的 data engineer 的文档, 主要介绍了如何创建表, SQL 的功能等跟数据相关的内容. 而关于 Redshift 的维护和管理, 可以参考 Amazon Redshift Management Guide.

我建议直接在你的 AWS Account 里创建一个 Redshift serverless, 然后用 Dbeaver 作为 SQL Client, 用 Python 中的 redshift-connector, psycopg2-binary, sqlalchemy, sqlalchemy-redshift, awswrangler 等库来创建表格, 写入数据, 进行查询等操作来学习.


Redshift Knowledge Graph
------------------------------------------------------------------------------
以下是 Redshift 的知识图谱, 对所有的知识点进行了一个梳理.

- Management:
    - Cluster Mode:
        - Concepts:
            - Node and Cluster.
        - Create Cluster:
            - 如何创建 Cluster.
            - Cluster 的网络配置方式, 如何选择 VPC, Subnet, Security Group, Public Subnet 还是 Private Subnet, 是否 Public Accessible.
        - Connect to Cluster:
            - 如何使用 Query Editor 来执行 SQL.
            - 如何使用 SQL Client 软件 (例如 Dbeaver) 来连接到 Cluster (Username Password 和 IAM 两种方式).
            - 如何使用 Python Driver (例如 psycopg2, redshift-connector, sqlalchemy, sqlalchemy-redshift 等) 连接到 Cluster (Username Password 和 IAM 两种方式).
            - 如何使用 Data API 来执行 SQL.
        - Manage Cluster:
            - 如何管理 Cluster 中的 User, User Group, User Permission, Username, Password 等.
            - 如何用 Snapshot 备份和恢复 Cluster.
            - 如何用 Snapshot 复制 Cluster.
            - Resizing a Cluster (Scale up and down)
            - 如何用 Usage limit 来管理使用情况. 主要是用来控制成本, 例如防止 Amazon Redshift Spectrum 用太多产生不必要的账单.
            - 如何用 Workload Management (WLM) 来管理各个用户组分别能占用多少计算资源, 查询的最长运行限制, 扫描的数据量的限制等.
            - 如何用 Redshift-managed VPC endpoints 来管理 Cross Account VPC Access.
        - Security:
            - Data Protection, 如何保护你的数据.
                - Data Encryption, 如何加密你的数据, at rest 和 in transit.
                - Data Tokenization, 如何对数据进行脱敏.
                - Internet traffic privacy.
            - IAM access management.
                - 使用 IAM 来管理对 Redshift Cluster 进行管理的权限.
                - 使用 IAM 来管理对 Redshift API 的管理权限 (特别是 data api).
                - 给 Redshift Cluster 添加 IAM Role, 使得 Redshift 可以访问其他 AWS 服务, 例如 S3, Lambda, SageMaker 等.
            - Logging and monitoring.
                - 如何使用 CloudWatch 来监控 Redshift Cluster 的运行状态, 例如 CPU 和 Memory 的使用情况, 数据量的大小, 读写的 IOPS 的流量大小.
                - 如何使用 Audit Logging 来记录对 Redshift Cluster 的操作情况. 例如登录, 执行 Query 等. 你可以将这些 Log dump 到 S3 以供分析.
                - 如何使用 CloudTrail 来监控 Redshift API 的调用情况.
            - Compliance validation.
        - Cost:
            - 理解 Cluster 模式下的账单构成.
    - Serverless Mode:
        - Concepts:
            - Serverless 和 Cluster 架构的主要区别.
            - 理解 Namespace, Workgroup, RPU, Managed Storage 这些概念.
        - Create Namespace and Workgroup:
            - 如何创建 Workgroup, 同时创建新的 Namespace 或将 Workgroup 添加到已有的 Namespace 中.
            - Workgroup 的网络配置方式, 如何选择 VPC, Subnet, Security Group, Public Subnet 还是 Private Subnet, 是否 Public Accessible.
        - Connect to Redshift Serverless:
            - 如何使用 Query Editor 来执行 SQL.
            - 如何使用 SQL Client 软件 (例如 Dbeaver) 来连接到 Cluster (Username Password 和 IAM 两种方式).
            - 如何使用 Python Driver (例如 psycopg2, redshift-connector, sqlalchemy, sqlalchemy-redshift 等) 连接到 Cluster (Username Password 和 IAM 两种方式).
            - 如何使用 Data API 来执行 SQL.
        - Manage Namespace:
        - Manage Workgroup:
            - 如何管理 Redshift Serverless 中的 User, User Group, User Permission, Username, Password 等.
            - Managing usage limits, query limits, and other administrative tasks
        - Security:
            - Data Protection, 如何保护你的数据. 这部分和 Redshift Cluster 模式一样.
            - IAM access management.
                - 使用 IAM 来管理对 Redshift Serverless 进行管理的权限.
                - 使用 IAM 来管理对 Redshift API 的管理权限 (特别是 data api).
                - 给 Redshift Serverless 添加 IAM Role, 使得 Redshift 可以访问其他 AWS 服务, 例如 S3, Lambda, SageMaker 等.
            - Logging and monitoring. 这部分和 Redshift Cluster 模式一样.
            - Compliance validation. 这部分和 Redshift Cluster 模式一样.
        - Monitoring queries and workloads with Amazon Redshift Serverless
        - Working with snapshots and recovery points
            - Restore a serverless snapshot to a serverless namespace.
            - Restore a serverless snapshot to a provisioned cluster.
            - Restore a provisioned cluster snapshot to a serverless namespace.
        - Data Sharing:
            - Data Sharing within AWS Account, or across regions
            - Data Sharing across AWS Accounts, or across regions
        - Cost:
            - 理解 Serverless 模式下的账单构成. 主要由 RPU 部分和 Managed Storage 部分构成.
- Database Developer
    - Concept:
        - sort key
        - distribution style
        - columnar storage
        - column compression
    - Designing Table
        - 如何选择最佳的 sort key.
        - 如何选择最佳的 best distribution style. 有 dist key, ALL, Auto 三种模式.
        - 如何选择最佳的 columnar compression.
    - Load Data (把数据写入 Redshift)
        - 用 SQL 写入大量数据
        - 从 S3 批量读数据
    - Unload Data (把数据从 Redshift 弄出来)
        - 把查询结果 unload 到 S3
    - User defined function, (自定义函数, 甚至能用 SQL, Python 和 Lambda)
    - Stored procedure, 存储过程 (PG 的传统)
    - Materialized views, 解决复杂查询的结果作为一个 Materialized view 储存起来.
    - Querying spatial data, 对空间地理数据进行查询
    - Querying data with federated queries in Amazon Redshift, 使用联合查询来查询位于 RDS 上的数据. 并且能把一些 Transformation 的工作放在 Redshift 上做以提高性能.
    - Querying external data using Amazon Redshift Spectrum, 对 S3 中的数据进行查询而无需将数据 load 到 redshift 中. 本质跟 Athena 类似.
    - Using HyperLogLog sketches in Amazon Redshift, 使用 HyperLogLog 函数来进行近似计数.
    - Querying data across databases, 跨数据库进行查询
    - Sharing data across clusters in Amazon Redshift, 在 Redshift Cluster 之间分享数据 (无需同步数据)
    - Ingesting and querying semistructured data in Amazon Redshift, 对半结构化数据进行查询, 主要是 JSON.
    - Using machine learning in Amazon Redshift, 在 Redshift 中使用机器学习.
    - Tuning query performance, 查询性能优化.
        - 了解 Redshift Query plan 是如何工作的.
        - 学习官方推荐的 Query analysis workflow, 按照这个流程去优化你的 Query.
    - Implementing workload management.
    - Managing database security, 主要是基于 User, Group 的权限管理.
    - SQL Reference, Redshift 中的 SQL 方言以及特殊函数.
        - SQL Command
        - SQL Function
        - SQL Data Type
        - Condition
        - Expression
    - System tables and views reference, 系统表和视图有哪些, 都有什么用.
    - Configuration reference, 一些常用的, 需要运行 SQL 命令, 对 Redshift 进行的配置的工作的实现方法的速查.


What's Next
------------------------------------------------------------------------------
todo
