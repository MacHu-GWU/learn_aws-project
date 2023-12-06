.. _aws-kinesis-data-streams-overview:

Amazon Kinesis Data Streams Overview
==============================================================================
Keywords: AWS, Amazon, Kinesis, Data Stream, Overview.


Background (Short Data Warehouse History)
------------------------------------------------------------------------------
由 Linkedin 公司开发并捐献给 Apache 软件基金会开源的的 Kafka 是流数据处理的事实标准. 虽然其背后的商业公司 Confluence 以及很多第三方公司也推出了全托管的 Kafka 集群产品, 但是跟云时代主打的 Pay as you go (用多少付多少钱), 以及自动 Scale up/down 相比, 运维成本还是不小的.

Kafka 是 2011 年 1 月的推出的产品. 而 AWS 在 2013 年 11 月推出了 Kinesis Data Stream, 完全对标 Kafka, 主打一个 0 运维, 云原生, Pay as you go. 这对于开发者以及初创公司而言, 1 秒钟就能用上跟 Kafka 体验一致的流数据产品, 极大的提高了开发效率, 并降低了运维成本. 这是非常大的进步.


Overview
------------------------------------------------------------------------------



How to Learn Amazon Kinesis Data Streams
------------------------------------------------------------------------------
- `Amazon Kinesis Data Stream Developer Documentation <https://docs.aws.amazon.com/streams/latest/dev/introduction.html>`_: 开发者文档总站.
- `Amazon Kinesis Data Stream FAQ <https://aws.amazon.com/kinesis/data-streams/faqs/>`_: 关于 FAQ.
- `Amazon Kinesis Data Stream Pricing <https://aws.amazon.com/kinesis/data-streams/pricing/>`_: 关于价格.

我建议直接在你的 AWS Account 里创建一个最小的 Kinesis stream, 然后用 Python 作为 Client, 写两个程序分别扮演 producer / consumer 进行实验.


Amazon Kinesis Data Streams Knowledge Graph
------------------------------------------------------------------------------
以下是 Kinesis Data Streams 的知识图谱, 对所有的知识点进行了一个梳理.

- Terminology and Concepts:
- Manage Streams:
    - Capacity Mode: on-demand (自动扩容) 和 provisioned (手动扩容) 两种模式.
    - Re-sharding a Stream: 对一个 stream 中的 shard 的数量进行管理.
    - Changing the Data Retention Period
- Writing to Data Stream
- Reading from Data Stream:
    - Developing Custom Consumers with Shared Throughput
    - Developing Custom Consumers with Dedicated Throughput (Enhanced Fan-Out): 通常属于同一个 shard 的所有的 consumer 共享一个总的数据读取上限. 而这一功能能单独为一个 consumer 分配一个独立的读取上限.
- KPL (Kinesis Producer Library)
- KCL (Kinesis Client / Consumer Library)


What's Next
------------------------------------------------------------------------------
todo
