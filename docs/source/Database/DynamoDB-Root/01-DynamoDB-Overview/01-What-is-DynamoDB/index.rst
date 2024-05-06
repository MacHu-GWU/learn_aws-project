.. _what-is-dynamodb:

What is DynamoDB
==============================================================================
Keywords: AWS, Amazon, DynamoDB.

本文是我的 DynamoDB 文档的第一篇, 简略的介绍了 DynamoDB, 让人有一个基本概念.


Key Characteristics
------------------------------------------------------------------------------
我们用几个关键字来描述一下 DynamoDB 的特征.

- NoSQL: 在 DynamoDB 中没有 Schema 的概念. 只有 Hash key 和 Range key 是必须要有的以及需要预先定义, 其他的 field 都不需要定义就可以使用.
- Key Value: DynamoDB 是一个 Key Value 数据库. 这并不是说 DynamoDB 不能批量读写, 只是说按照 Key 来读写是最有效率的方式.
- Serverless: 你无需管理任何服务器就可以使用 DynamoDB, 并且你无需进行任何运维, 扩容等工作. 大部分的数据库运维工作都是自动的.
- Data Modeling: 由于是 NoSQL, 为你的 Application 进行数据建模的方式跟传统的 RDBMS 有很大的不同. 这里先不展开讲.


DynamoDB API (Connect to DynamoDB)
------------------------------------------------------------------------------
传统的关系数据库通常都是通过 http 协议, 数据用 TSL 加密, 通过一个长得像 URL 的 Endpoint (其实是 URI), 用 host, port, database, username, password 来连接到数据库. 这个连接会长期存在直到数据库杀死它, 或是客户端主动选择关闭. 而为了提高性能, 数据库和客户端都会在内存中维护一个连接池, 以便复用, 减少创建连接的开销.

而 DynamoDB 作为云原生服务, 不存在数据库连接的概念. 整个 API 都是 Stateless 的. 完全是通过 Https Request 与 DynamoDB 进行通信. 这个 HTTPS 的 API 也就是俗称的 Low Level API, 详细的语法文档可以参考这里 `DynamoDB Low-level API <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html>`_.

而 AWS SDK 提供了封装更好的 API. 在 Python 中你可以用 boto3 来对 DynamoDB 进行 读/写/更新/删除 等操作. 主要使用 JSON 作为数据传递的接口.

在 Python 社区还有个封装的更好的 API, 由开源 Python 库 `Pynamodb <https://pynamodb.readthedocs.io/en/latest/>`_ 提供. 这个库相当于 SQL 世界中的 ORM, 允许用 Class 来定义数据模型, 使得代码量更少, 人类更好理解.


DynamoDB Permission
------------------------------------------------------------------------------
关于鉴权, DynamoDB 没有 Username Password 的概念, 完全是用 AWS 原生的权限管理系统 IAM Role 来验证你是否有权限对某个 Table / Index 进行某种操作. 由于使用了 IAM Role, 你可以对客户端权限做更精细的控制.


DynamoDB Table, Item, Attribute and Index
------------------------------------------------------------------------------
由于是 NoSQL, 在 DynamoDB 中没有传统的数据库中 Database 的概念, 也没有 View 的概念. DynamoDB 里的跟数据库相关的核心概念有:

1. Table: 就是一个表. 由于 NoSQL 中不推荐做多表 JOIN, 联合查询, 所以在 DynamoDB 中的数据是以表为单位隔离的.
2. Item: 就是一个 Database Record, 只不过它没有 Schema, 可以是任何 JSON.
3. Attribute: 由于没有 Schema, 一个 Item 可以有任意数量的 Attribute, 并且这些 Attribute 在不同的 Item 中可以不一样.
4. Index: 和传统数据库一样, DynamoDB 也可以为一个 Attribute 创建 Index, 使得查询更加高效.


DynamoDB Partition Key and Sort Key
------------------------------------------------------------------------------
Partition Key (又叫 PK, Hash Key), Sort Key (又叫 SK, Range Key) 是 DynamoDB 中核心中的核心概念. 这里的 PK 有点像传统数据库中的 Primary Key, 但又很不一样. 由于 DynamoDB 是一个大型分布式系统, PK 决定了这个流量由哪个 Node 处理. 而 SK 则像是一个排序索引使得 DynamoDB 能很快定位到这个 Item.

你创建表的时候必须要制定一个 PK. 同时你可以指定一个 SK 也可以不指定. 如果你的表只有 PK 那么这就完完全全是一个类似 Redis 的 Key-Value Store 了. PK 就是你的 Primary Key. 而如果你的表既有 PK 又有 SK, 那么两者合起来构成一个 Compound Key, 唯一确定一个 Item, 换言之它们合起来构成一个 Primary Key.


DynamoDB Write
------------------------------------------------------------------------------
在 DynamoDB 中的 Write 操作包括: Create, Update, Delete. 只要是对数据发生了变更, 就是 Write 操作.

- Create: 这里的 Create 更像是 Put 操作, 它会把你定义的 JSON 完全覆写到 Item 中. 这个操作不存在 Partial Update. 如果你要批量写入请用 Batch Create.
- Update: 有两种 Update 模式. 一种是你指定 PK (或者以及 SK), 然后对 Attribute 进行更新. 一种是你指定 Filter 对所有满足该条件的 Item 的 Attribute 进行更新, 这也是所谓的批量 Update. Item 一旦被创建, 你无法更新 PK 和 SK.
- Delete: 和 Update 类似, 有根据 PK (或者以及 SK) 删除 Item, 和指定 Filter 进行批量删除两种模式.

这三种操作都有 单个 Item 和 Batch 两种模式. 单个 Item 的模式很好理解, 这里重点说一下 Batch 模式.

Batch 的本质是将多个 Action Push 到一个 Buffer 中, 然后以 25 个 Action 为一批批量执行. (25 是 Batch 的上限) 要注意的是 **一个 Batch 中的多个 Actions 的执行顺序是无法保证的, 完全可能生效的顺序和你请求的顺序不一致. 如果你要严格保证一致, 请使用 Transaction**


DynamoDB Read
------------------------------------------------------------------------------
DynamoDB 有三种查询模式:

1. get item: 直接根据 PK (或是以及 SK) 定位到某一个 Item.
2. query: 利用 hash key, range key, 或是用 secondary index 索引进行查询. **这是 DynamoDB 推荐的查询方式, 比较有效率, 可以利用索引, 避免全表扫描**.
3. scan: 对全表进行扫描, 支持用 Filter 进行条件判断筛选. 查询速度慢 (因为要全表扫描), 如果非必要不推荐.


DynamoDB Data Modeling
------------------------------------------------------------------------------
请特别注意, 设计表时, 列名称不要和 Reserved Keyword 冲突, 这里是所有 DynamoDB 保留关键字的列表: https://docs.aws.amazon.com/amazonDynamoDB/latest/developerguide/ReservedWords.html


DynamoDB Ops
------------------------------------------------------------------------------
DynamoDB 是云原生数据库. 创建一个表只需要 3-5 秒. 备份和恢复也都是秒级的.


DynamoDB Pricing
------------------------------------------------------------------------------
DynamoDB 的收费有 On-Demand (Pay as you go) 和 Provisioned 两种模式. 这里有个核心概念 RRU (Read Request Unit) 用来统计你的读操作读了多少数据, 和 WRU (Write Request Unit) 用来统计你的写操作写了多少数据. 这两个概念都是你的 Capacity (用量). On-Demand 就是你随便用, 它会自动扩容, 然后根据你用了多少付钱. Provisioned 就是你设定一个每秒 RRU 和 WRU 的上限, 你的读写不超过这个上限. 如果你一直跑满了 RRU 和 WRU, 那么它会比 On-Demand 更便宜, 你还可以跟 Amazon 签一个 Contract, 说我预付款多少钱买指定数量的 Capacity, 这个价格比 Provisioned 会更加优惠.


Reference
------------------------------------------------------------------------------
- `What is Amazon DynamoDB <https://docs.aws.amazon.com/amazonDynamoDB/latest/developerguide/Introduction.html>`_
