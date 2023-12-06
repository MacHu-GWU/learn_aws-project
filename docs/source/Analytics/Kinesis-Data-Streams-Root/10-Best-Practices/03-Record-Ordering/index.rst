Amazon Kinesis Data Streams - Record Ordering
==============================================================================
Keywords: AWS, Amazon, Kinesis, Data Stream, Best Practice

作为流数据系统, 能按照写入顺序读取数据在很多场景下是必须的. Kinesis 提供了 Shard 级别的顺序严格一致性. 这跟 Kafka 中的 Partition 是一样的.

举例来说, 你用 PutRecords API 写数据的时候, 每个 record 最终到哪个 Shard 上是由 Partition key 决定的. 而你用 `GetRecords API <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_records.html>`_ 获取数据时, 你得先用 `GetShardIterator <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/get_shard_iterator.html>`_ 获得特定 Shard 的 iterator (iterator 和 Kafka 中的 Offset 是一样的概念) 才能从 Shard 上拉数据. 如果你有 3 条数据 r1, r2, r3 你需要确保消费它们的时候也是严格按照这个顺序消费, 那么这 3 条数据的 partition key 必须一样, 这样他们才会落到同一个 Shard 上.

拿电商系统的数据汇总 Stream 举例, 用户下单以后, 你需要先检查库存, 然后处理支付, 然后生成确认订单, 然后处理包装物流. 这几个步骤每一步都会生成一个 Record, 你处理这几个 Record 的顺序肯定不能乱. 那么你可以用 order_id 作为这几个 Record 共同的 partition key 即可.
