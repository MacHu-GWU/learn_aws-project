Kinesis Root
==============================================================================

.. image:: /_static/aws-icons/arch/Analytics/Amazon-Kinesis_64_5x.png
    :width: 128px

Kinesis 是 AWS 的 Serverless (无服务器), 专注于解决实时流数据处理的服务. 对标的开源项目是 Apache Kafka. 它相当于一个点击可用 (秒级), 自动缩容扩容, 无需管理服务器, 按用量收费的 Kafka.

Kinesis 有三个子组件:

- :ref:`Kinesis Data Stream <aws-kinesis-data-streams-root>`: 数据流中间件, Producer 将数据 put records 发送给 Data Stream, Data Stream 将流数据分 Partition, 按顺序 保存, 供后续的 Consumer 消费. Kinesis Data Stream Shard 相当于 Kafka 的 Partition.
- :ref:`Kinesis Data Firehose <aws-kinesis-data-firehose-root>` (也叫 Delivery Stream): 数据传输中间件, 相当于一个无需维护的 consumer, 专注于将数据流从 A 传输给 B. 这个 A 通常是 Kinesis Data Stream, 也可以作为一个管党允许 Direct Put. B 则可以是任何系统, 其中很多 AWS 系统例如 S3, Cloudwatch, Dynamodb, OpenSearch, Redshift 都和 Kinesis Delivery Stream 原生紧密结合, 无需写任何的数据 input / output 接口. 如果有自定义逻辑, 则数据可以被 buffer 成小数据, 传输给 AWS Lambda 进行处理.
- :ref:`Kinesis Data Analytics <aws-kinesis-data-analytics-root>`: 用 Flink 作为 Data Stream 的后续, 提供实时数据分析, 比如按时间聚合计算平均值, 统计实时总数, 等.

建议点击链接前往子页面查看更多信息.
