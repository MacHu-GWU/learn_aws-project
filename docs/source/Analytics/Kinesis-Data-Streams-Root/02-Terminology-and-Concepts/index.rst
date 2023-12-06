Amazon Kinesis Data Streams - Terminology and Concepts
==============================================================================
Keywords: AWS, Amazon, Kinesis, Data Stream, Concept.


Concepts
------------------------------------------------------------------------------
- Kinesis Data Stream: 相当于一个 Kafka 的 Topic, 你写入数据的时候都是写入到这个 Data Stream 里面的.
- Shard: 相当于一个 Kafka 的 Partition
- Data Record: 相当于一个 Kafka 的 Message, 一条被 binary encode 之后的数据.
- Capacity Mode: 有两种模式, 一种是 on-demand, AWS 自动扩容, 一种是 provisioned, 你自己指定 Shard 的数量并自己 scale.
- Retention Period: 数据在 shard 上保留多久.
- Producer: 数据生产者. Producer 写入数据的时候不指定 Shard, Data Stream 自己根据 Partition key 决定写入到哪个 Shard. 通常 Producer 有以下两种方式来写入数据
    - PutRecords API: Synchronous, immediately available after captured, need manually implement retry, batch.
    - Kinesis Producer Library (Java): Asynchronous, High Performance (high concurrence), but with larger delay
- Consumer: 数据消费者. 读取的时候需要指定 Shard 以及 ShardIterator (Kafka 中的 Offset 对等的概念)
- Amazon Kinesis Data Streams Application: 一般是一个消费者集群.
- Partition Key: 每个 data record 都必须有 partition key, 你可以手动指定, 也可以指定算法由某个 key 计算而来. 这个 partition key 会被 hash 之后用 consistent hash 算法来决定写入到哪个 Shard.
- Sequence Number: 每个 record 在 shard 内都有一个唯一的 sequence number 用于决定 record 的顺序.
- KPL (Kinesis Producer Library): AWS 官方提供的 Java SDK, 用于高性能异步写入. 也提供了 Python 的 binding (Python 库里面没有业务逻辑, 只是调用 Java 接口). 简单来说, 它额外提供了这些功能:
    - Async PutRecords: 异步, 提高性能.
    - Collection: 将多个 Record 打入 Buffer 后再用 Batch PutRecords 发送, 减少 PutRecord API 调用次数, 从而提高性能.
    - Aggregation / Batch: 将多个 Record 进行 Aggregation, 合并成一个 Record, 然后一起发送. 避免每个 Record 太小, 无法充分利用带宽..
- KCL (Kinesis Consumer Library): AWS 官方提供的 Java SDK, 用于稳定可靠的消费数据, 并提供重试, 容错, 记录消费状态等高级功能. 同样也提供 Python 的 binding.
- Server-Side Encryption: 默认情况下所有写入 Kinesis 的数据都是加密的.

Reference:

- https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html


FAQ
------------------------------------------------------------------------------
本节是 Kinesis 官方 FAQ 中比较重要的部分的节选和解读.

- Q: Does on-demand mode scale both up and down?
- A: YES

- Q: Can I switch between on-demand and provisioned mode?
- A: YES:

- Q: Is the order of what consumer received is same as the order produced?
- A: Yes, It provides ordering of records, as well as the ability to read and/or replay records in the same order to multiple Amazon Kinesis Applications

Reference: https://aws.amazon.com/kinesis/data-streams/faqs/
