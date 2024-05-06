Dynamodb Index
==============================================================================
Keywords: AWS, Amazon, DynamoDB


Overview
------------------------------------------------------------------------------
在 DynamoDB 中, 只有用到 hash key, range key 的查询才是高效的. 如果你要根据其他的 attribute 进行条件筛选, 你只能用 Scan + Filter 的 API, 这会导致全表扫描, 对表性能影响较大.

为了支持更灵活的查询模式, 你可以为你的表添加 Secondary Index 以支持所需的查询模式.


GSI and LSI
------------------------------------------------------------------------------
DynamoDB 有两种 Secondary Index, Global secondary index (GSI) 和 Local secondary index (LSI)

下面是 AWS 官方的描述:

    Global secondary index (GSI) - An index with a partition key and a sort key that can be different from those on the base table. A global secondary index is considered "global" because queries on the index can span all of the data in the base table, across all partitions. A global secondary index has no size limitations and has its own provisioned throughput settings for read and write activity that are separate from those of the table.

    Local secondary index (LSI) - An index that has the same partition key as the base table, but a different sort key. A local secondary index is "local" in the sense that every partition of a local secondary index is scoped to a base table partition that has the same partition key value. As a result, the total size of indexed items for any one partition key value can't exceed 10 GB. Also, a local secondary index shares provisioned throughput settings for read and write activity with the table it is indexing.

下面是我的描述:

    - Global Secondary Indexes (GSI): 就是选择一个或者两个 Attribute 分别用作 Hash Key 和 Range Key. 以供特殊的查询模式. 本质上相当于 AWS 在后台帮你维护着一个新的, 只不过这主表更新的时候新表也会自动更行. 但是这个 GSI 中的 Hash Key 和 Range Key 的组合并不像跟 Base Table 一样强制要求是唯一的, 它是可以重复的.
        - 由于 GSI 本质上也是一个表, 它也会有自己的 Partition, 并且额外消耗 RCU/WCU.
        - 在 Table 创建后可以更改.
        - 之所以叫 Global 是因为 GSI 中的数据和 Base Table 是一样的.
    - Local Secondary Indexes (LSI): 就是用原来的 Partition Key, 但是用不同的 Attribute 做 Sort Key. 以供特殊的查询模式.
        - 与 Table 共用 Partition 的 RCU/WCU.
        - 在 Table 创建后不能更改.

    一个 Table 最多能有 20 个 GSI 和 5 个 LSI.


Reference
------------------------------------------------------------------------------
- `Improving data access with secondary indexes <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html>`_
- `General guidelines for secondary indexes in DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-general.html>`_
