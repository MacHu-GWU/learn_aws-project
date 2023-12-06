Amazon Kinesis Data Streams - Kinesis Consumer Library KCL
==============================================================================
Keywords: AWS, Amazon, Kinesis, Data Stream,.


Using a Lease Table to Track the Shards
------------------------------------------------------------------------------
在 Consumer 端, 如果你使用的是官方的 Kinesis Consumer Library (或者叫 Kinesis Client Library), 它会用一个 DynamoDB Table 来 track 你 consume 到哪里了. 这很好理解, 一个 Consumer 的进程是可能会挂掉的, 所以我们需要一个中心化的存储能记录它消费到哪里了 (ShardIterator 到哪里了, 和 Kafka 中的 Offset 一个概念). KCL 会使用一个 Table Name 等于 Application Name 的 Dynamodb Table 来 Track Application State. 关于这个 Table 的 Schema, 建议参考官方文档.

**Throughput**:

如果你看到 Kinesis Throughout Exception 时, 大概率是 DynamoDB 读写速度达到上限了 (默认情况下是 10 write read per seconds). 你得注意你的 DynamoDB 的 WCU 和 RCU 和 Kinesis Stream 是否匹配.

Reference:

- `Using a Lease Table to Track the Shards Processed by the KCL Consumer Application <https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html#shared-throughput-kcl-consumers-leasetable>`_