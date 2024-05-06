.. _dynamodb-transaction:

Dynamodb Transaction
==============================================================================
Keywords: AWS, Amazon, DynamoDB, Transaction, Transactions

Reference:

- `Managing Complex Workflows with DynamoDB Transactions <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html>`_: AWS 官方文档中对 Transaction 的详细介绍.


Overview
------------------------------------------------------------------------------
和 SQL 中的 Transaction (事务) 类似, 你可以把多个 CRUD 操作打包在一起, 要么全部成功, 要么全部不成功. 这也是数据 Strong Consistency 的基础. 在银行等业务中非常重要. Transaction 的 Read 和 Write 比普通 Read 和 Write 的价格高. 详情请参考 :ref:`dynamodb_rru_wru`.

Dynamodb 支持两种 Transaction:

- ``TransactWriteItems``: Transaction Write API 支持将多个 Put, Update, Delete, ConditionCheck 打包在一起.
    - Limitation: 最多把 25 个 write action 打包在一起, 被操作的 item 数最多是 25 个. 这些 items 的大小总和不能超过 4MB. 这些操作可以跨 Table, 但是这些 Table 必须要在同一个 AWS Account 下以及同一个 Region 下.
- ``TransactGetItems``: Transaction Read API 支持将多个 Get 打包在一起.
    - Limitation: 最多把 25 个 get action 打包在一起, 被操作的 item 数最多是 25 个. 这些 items 的大小总和不能超过 4MB. 这些操作可以跨 Table, 但是这些 Table 必须要在同一个 AWS Account 下以及同一个 Region 下. (和 Write 差不多)

FAQ:

- Q: Transaction 可以跨 Table 吗?
- A: 可以, 例如你可以将对多个 Table 的 Update 的 event 打包.
- Q: Transaction 无法做到什么?
- A: 不能跨对 global table 进行跨 region.

在仔细研究了 DynamoDB Transaction 的文档之后, 我有这么几点印象:

1. 分布式数据库做 Transaction 一直是业界难题. MongoDB 花了大约 9 年时间才做出来一个可用的 Transaction (MongoDB 2009-08 发布, 2018-06 开始支持 Transaction). Amazon DynamoDB 花了接近 7 年 (DynamoDB 2012-01-18 发布, 2018-11-27 开始支持 Transaction).
2. 一个 Database 是否能在关键业务中使用的一个关键因素就是是不是能保证 Transaction. 对于大多数 NoSQL 来说, 之所以不适合关键业务的原因都是因为不支持 Transaction. 而 DynamoDB 做到了, 使得它成为了关键业务的商业数据库的几个首要选项之一.
3. DAX 是一个 DynamoDB 用内存对数据库性能加速的功能. 通常传统方案是用 Redis 来做缓存, 但是使用 Redis 就要考虑更新的时候双写一致性问题, 在 Transaction 内如何保持数据库和缓存一致, 等等很多麻烦的问题. 而 DynamoDB DAX 完全支持 Transaction, 你就跟正常使用一样, 就能获得缓存的高性能, 同时保证 Transaction 的一致性. 这是一个非常普遍而难以解决的痛点, 客户会非常愿意为这个功能买单.


Idempotency Write Action (幂等)
------------------------------------------------------------------------------
幂等是一个非常重要的概念, 意思是如果一个操作你成功连续做几次的效果和做一次的效果是一样的, 这就叫幂等. 比如 Insert 不是幂等, Set Value 和 Get Value 都是幂等.

在做 ``TransactWriteItems`` 时, 你可以用一个 ``client Token`` 来确保你的重复操作是幂等的. 不过这个 Token 只有 10 分钟的实效. 在 10 分钟以内同一个 Token 的操作只会被执行一次, 而同一个 Token 在 10 分钟后会启用一个新的操作. 而如果你两个 ``TransactionWriteItems`` 的具体操作不一样, 却给了同一个 Token, 那么客户端会报错 ``IdempotentParameterMismatch``.


Isolation Levels for DynamoDB Transactions (隔离等级)
------------------------------------------------------------------------------
**SERIALIZABLE**

Serializable isolation 保证了多个并发操作能按照顺序执行, 前一个不执行完后一个不会执行.

There is serializable isolation between the following types of operation:

- Between any transactional operation and any standard write operation (PutItem, UpdateItem, or DeleteItem).
- Between any transactional operation and any standard read operation (GetItem).
- Between a TransactWriteItems operation and a TransactGetItems operation.

简单来说, Batch Write / Read 内部的 item 不能被 Serializable.

**READ-COMMITTED**

Read-committed 保证了你读到的数据一定是 Committed 的数据. 例如你的 Read 需要一定时间返回, 而这段时间里有 Transaction Write commit 了你要读的数据, 返回的将会是 committed 的数据, 而不是你 Read request 被接受到的瞬间的数据版本.

**Operation Summary**

这里有个表列出了哪些操作分别用的什么样的 Isolation::

    +-------------------------------+-------------------+
    | Operation                     | Isolation Level   |
    +-------------------------------+-------------------+
    | DeleteItem                    | Serializable      |
    +-------------------------------+-------------------+
    | PutItem                       | Serializable      |
    +-------------------------------+-------------------+
    | UpdateItem                    | Serializable      |
    +-------------------------------+-------------------+
    | GetItem                       | Serializable      |
    +-------------------------------+-------------------+
    | BatchGetItem                  | Read-committed*   |
    +-------------------------------+-------------------+
    | BatchWriteItem                | NOT Serializable* |
    +-------------------------------+-------------------+
    | Query                         | Read-committed    |
    +-------------------------------+-------------------+
    | Scan                          | Read-committed    |
    +-------------------------------+-------------------+
    | Other transactional operation | Serializable      |
    +-------------------------------+-------------------+


Transaction Conflict Handling in DynamoDB (事务冲突)
------------------------------------------------------------------------------
简单来说如果两个 Transaction 对同一个 Item Update, 那么两个都会 failed.


Using transactional APIs in DynamoDB Accelerator (DAX)
------------------------------------------------------------------------------
由于 DAX 本质上是一个在 DynamoDB 外安排的纯内存 Key Value 缓存, 相当于是 AWS 帮你管理了一个 Redis. 所以在启用了 DAX 的时候使用 Transaction 的时候会


Capacity management for transactions
------------------------------------------------------------------------------
在 :ref:`dynamodb-pricing` 一章你会注意到 Transaction 的读写都会小号额外的 RRU, WRU. 这是因为 Transaction 的底层实现是要对 Item 上锁, 然后再写之前要额外有几次读确保数据在 Transaction 的生命周期内没有被修改.


Best Practices for Transactions (最佳实践)
------------------------------------------------------------------------------
Consider the following recommended practices when using DynamoDB transactions.

- Enable automatic scaling on your tables, or ensure that you have provisioned enough throughput capacity to perform the two read or write operations for every item in your transaction.
- If you are not using an AWS provided SDK, include a ClientRequestToken attribute when you make a TransactWriteItems call to ensure that the request is idempotent.
- Don't group operations together in a transaction if it's not necessary. For example, if a single transaction with 10 operations can be broken up into multiple transactions without compromising the application correctness, we recommend splitting up the transaction. Simpler transactions improve throughput and are more likely to succeed.
- Multiple transactions updating the same items simultaneously can cause conflicts that cancel the transactions. We recommend following DynamoDB best practices for data modeling to minimize such conflicts.
- If a set of attributes is often updated across multiple items as part of a single transaction, consider grouping the attributes into a single item to reduce the scope of the transaction.
- Avoid using transactions for ingesting data in bulk. For bulk writes, it is better to use BatchWriteItem.


Using transactional APIs with global tables
------------------------------------------------------------------------------
DynamoDB 只能保证 Transaction 在发起它的那个 Region 是强一致的.
