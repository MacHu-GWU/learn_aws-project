How to Learn Amazon DynamoDB
==============================================================================
Keywords: AWS, Amazon, DynamoDB.

在读完 :ref:`what-is-dynamodb` 后, 如果想要深入学习 DynamoDB, 就可以参考这篇文档了解到那列


Where to Find Learning Resource
------------------------------------------------------------------------------
DynamoDB 是 NoSQL 数据库中的一种, 也是商业化非常成功的产品之一. 如果你是第一次接触 DynamoDB, 大概率和你之前的经验关系不大. 我建议先精读 DynamoDB 的官方文档中的第一节 What is Amazon DynamoDB, 了解它的设计理念, 独特的 Hash Key, Range Key, GSI Index 的设计, 和传统的关系数据库的区别. 非常不推荐在没有搞懂 DynamoDB 的设计理念之前就进行

- `What is Amazon DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html>`_: DynamoDB 的主文档.
- `Amazon DynamoDB FAQ <https://aws.amazon.com/dynamodb/pricing/>`_
- `Amazon DynamoDB pricing <https://aws.amazon.com/dynamodb/pricing/>`_
- `Amazon DynamoDB paper <https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html>`_
- `PynamoDB, DynamoDB ORM in Python <https://github.com/pynamodb/PynamoDB>`_
- `DynamoDB Guide <https://www.DynamoDBguide.com>`_: 一个第三方写的书.

我建议直接在你的 AWS Account 里创建一个 DynamoDB Table, 并选择 On-Demand 模式, 然后用 Python boto3 作为 Client 进行学习. 由于是 On-Demand 模式下 DynamoDB 是按使用量收费, 用来学习的所产生的流量不会超过 1 美金, 所以非常划算.


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
