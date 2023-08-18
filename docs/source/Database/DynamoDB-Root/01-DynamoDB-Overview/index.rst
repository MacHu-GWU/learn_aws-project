Amazon DynamoDB Overview
==============================================================================
Keywords: aws, amazon, dynamodb

Amazon Dynamo
------------------------------------------------------------------------------


How to Learn Amazon DynamoDB
------------------------------------------------------------------------------
DynamoDB 是 NoSQL 数据库中的一种, 也是商业化非常成功的产品之一. 如果你是第一次接触 DynamoDB, 大概率和你之前的经验关系不大. 我建议先精读 DynamoDB 的官方文档中的第一节 What is Amazon DynamoDB, 了解它的设计理念, 独特的 Hash Key, Range Key, GSI Index 的设计, 和传统的关系数据库的区别. 非常不推荐在没有搞懂 DynamoDB 的设计理念之前就进行

- `What is Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html>`_: DynamoDB 的主文档.
- `Amazon DynamoDB FAQ <https://aws.amazon.com/dynamodb/pricing/>`_
- `Amazon DynamoDB pricing <https://aws.amazon.com/dynamodb/pricing/>`_
- `Amazon DynamoDB paper <https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>`_
- `PynamoDB, DynamoDB ORM in Python <https://github.com/pynamodb/PynamoDB>`_

- `Amazon Redshift Documentation <https://docs.aws.amazon.com/redshift/index.html>`_: Redshift 的文档总站.
- `Amazon Redshift FAQ <https://aws.amazon.com/redshift/faqs/>`_: 关于 FAQ.
- `Amazon Redshift Pricing <https://aws.amazon.com/redshift/pricing/>`_: 关于价格.
- `Amazon Redshift Getting Start Guide <https://docs.aws.amazon.com/redshift/latest/gsg/new-user-serverless.html>`_: 快速上手的文档, 适合第一次使用的用户. 有了基本的了解之后, 可以看 Amazon Redshift Management Guide 和 Amazon Redshift Database Developer Guide 两个详细文档了.
- `Amazon Redshift Management Guide <https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html>`_: 主要介绍了管理 Redshift 的知识, 例如创建, 维护, 备份, 删除 Redshift 等. 如果涉及到使用 Redshift 进行开发, 可以参考 Amazon Redshift Database Developer Guide.
- `Amazon Redshift Database Developer Guide <https://docs.aws.amazon.com/redshift/latest/dg/welcome.html>`_: 这个主要是给负责 CRUD 的 data engineer 的文档, 主要介绍了如何创建表, SQL 的功能等跟数据相关的内容. 而关于 Redshift 的维护和管理, 可以参考 Amazon Redshift Management Guide.

我建议直接在你的 AWS Account 里创建一个 Redshift serverless, 然后用 Dbeaver 作为 SQL Client, 用 Python 中的 redshift-connector, psycopg2-binary, sqlalchemy, sqlalchemy-redshift, awswrangler 等库来创建表格, 写入数据, 进行查询等操作来学习.




Amazon DynamoDB Knowledge Graph
------------------------------------------------------------------------------
- Core Concepts: Table, Item, Attributes, Index (GSI, LSI)
- DynamoDB Architecture:
- Read Consistency: Eventual, Strong, Global table eventual consistency
- Read / Write Capacity Mode:
- Partition Key and Sort Key
- Data Types in DynamoDB
- Data Modeling
    - One to One
    - One to Many
    - Many to Many
- DynamoDB development in Python
    - Declare DynamoDB table in CloudFormation or AWS CDK
    - Manage table, index
    - Insert, Update, Get, Scan, Query, Delete items. Single action and batch action.
    - Transaction.
- DynamoDB Streams: kinesis stream and dynamodb stream
- DynamoDB Backup
- DynamoDB Point-in-time-Recovery (PITR)
- Integrating with Redshift: load data from dynamodb into Redshift
- Integrating with EMR
- Integrating with S3: import and export
- Security
    - Data Protection
    - IAM access Management: table management permission, CRUD permission
    - VPC Endpoint
- Monitoring
- Best Practice
    - NoSQL design
    - Deletion protection
    - The DynamoDB Well-Architected Lens
    - Partition key design
    - Sort key design
    - Secondary indexes
    - Large items
    - Time series data
    - Many-to-many relationships
    - Hybrid DynamoDB–RDBMS
    - Relational modeling
    - Querying and scanning
    - Table design
    - Global table design
    - Control plane
