.. _aws-opensearch-ingestion-overview:

AWS OpenSearch Ingestion Overview
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Serverless.

Reference:

- `Amazon OpenSearch Ingestion Pipeline <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ingestion.html>`_
- `First Release <https://aws.amazon.com/about-aws/whats-new/2023/04/amazon-opensearch-service-ingestion/>`_


What is OpenSearch Ingestion
------------------------------------------------------------------------------
OpenSearch Ingestion 是一个运行在服务器端的全托管的 Ingestion Pipeline. 它把 ETL Pipeline 抽象成了 Source, Processor, Sink 三个部分允许你用 YAML 或 JSON 配置文件进行简单定义, 既可实现持续不断的 Ingestion. 它把常见的 ETL Pipeline 中需要的: Buffer, CheckPoint, Scaling 等组件全部搞定封装好了. 你只需要定义好核心的 Transformation 逻辑既可 (甚至不需要 Transformation). 并且由于它运行在服务端, 所以 Index 的速度远远快于你自己用 BULK API 进行 Index (这个我怀疑它走的不是 Rest API 而是底层的服务).


Why Not Direct Ingest with Bulk API
------------------------------------------------------------------------------
前面说了 OpenSearch Ingestion 把常见的 ETL Pipeline 中需要的: Buffer, CheckPoint, Scaling 等组件全部搞定封装好了. 那我们来看看, 如果不用 Ingestion Pipeline, 情况是怎样的.

**Buffer**

为了方便说明, 我们来考虑这个常见的场景. 你有 10 个 GB 的数据需要 Index. 而你的 OpenSearch 的节点数最多支持每秒 Index 50 MB 的数据. 而你如果使用多个 Lambda Function, 完全可以并行每秒读取 1G 的数据, IO 的速度远远快于 Index 的数据. 而更要命的是这个每秒 Index 50 MB 的指标往往是测很多次测出来的, 并且随着网络, 数据结构的变化而变化, 只是个大概, 是不靠谱的. 所以你必须要有某种机制, 确保 Index 的速度保持稳定, 并且这个速度还要能够动态调节. 如果速度太快, 错误率高, 那么就慢一点, 如果错误率一直是 0%, 就适当提高一点.

**CheckPoint**

而且就算你按照每秒 Index 50MB 去调用 Bulk API, 但还是有可能会有一部分数据发因为网络或服务器的原因会发生错误. 所以, 使用某种容错机制是必须的. 而这种容错机制往往需要你用 DynamoDB, Redis 这种 Metadata store 来保证 Exact once delivery.

**Scaling**

由于 OpenSearch 是个分布式系统, 你完全可以进行分布式 Index, 这就需要一个调度机制和增加减少 Worker 的机制了.


Why OpenSearch Ingestion is Fast
------------------------------------------------------------------------------
为了方便说明, 我们来考虑这个经典的情况. 用户有一堆 JSON 数据文件在 S3 上 (几百个把), 每个文件大约 1W 多条数据. 假设我们不需要 Transformation, 直接进行 Index 就可以了.

在传统 Index 的情况下, 假设我们用的 Lambda Function 需要经过这么几步 (Lambda Function 跟 S3 通信速度极快, 肯定比你的 Web 服务器通信速度快):

1. 从 S3 中把数据读到 Lambda Function 中的内存中, 转换成 JSON 的形式.
2. Lambda 把 JSON 通过 OS Rest API 发送到 OS.
3. OS 的 API 收到 JSON, 开始解析, 并进行 Index.

而在 Ingestion 的场景下, 这个步骤就成了:

1. 从 S3 中把数据读到 Ingestion 的 Buffer 中.
2. 直接用 OS 的底层服务进行 Index.

看起来两者一样, 其实在 IO 上差别很大. 这里最关键的点是:

1. Ingestion 本身是跟 OS 的服务器部署到一起的, Ingestion 和 OS 的通信速度是极快的, 要比 Lambda 通过 API 跟 OS 通信要快得多.
2. 这里有 Lambda Function 把 S3 数据读成 JSON, 发出去, 然后收到 JSON 再解析成需要的格式的过程, 一共有 2 次 Seder, 和 2 次网络通信, 而 Ingestion 则是直接把 S3 的数据读到 Index, 本质上只有一次 Seder 和 网络 IO.


What is the Best Ingestion Architecture with OpenSearch Ingestion
------------------------------------------------------------------------------


OpenSearch Ingestion Pitfalls
------------------------------------------------------------------------------
我在使用 OpenSearch Ingestion 的过程中发现有这么几个小坑:

- 使用 S3 作为 Source 的时候, 如果 S3 Filter Prefix 中有特殊字符, 例如等号 (等号在 Hive partition 中很常见的), 那么无法正确识别并触发 S3 Event. 这是因为 S3 Filter Prefix 是 Literal 的, 这个 Prefix 的字符串不支持 Escape. 所以这个 Prefix 中是不能有除了 +, -, _ 以外的特殊字符的. 例如你如果想要让 Prefix 为 ``data/year=2021/``, 那么建议你让 Prefix 设为 ``data/year-2021/``, 然后让你的数据写入到这个目录下, 来为 Prefix 妥协. 还有一个常见的错误是 S3 Filter 的 suffix, 他也是 Literal 的. 比如你只想要 JSON 文件来 trigger event, 那么 Suffix 就要是 ``.json`` 而不能是 ``*.json``.
- 使用 S3 作为 Source 并使用 SQS 作为 Notification Channel 的时候, 每次修改 Event Notification Configuration 之后 S3 会自动给 SQS 发送一个 Test Event. 这个 Event 是无法被 Ingestion Pipeline 所处理的, 所以你修改这个 Event 之后最好要用 Lambda 之类的东西删掉这个 Event.
- 使用 S3 作为 Source 并使用 Parquet 作为 codec 数据文件格式时, 对于 ``array<str>`` 这一类的列表是无法直接识别的 (会将其解析为 element<...> 这种形式), 你只有用 Processor 对其进行处理之后才能正确 Index, 不然这些数据都会导致 Ingestion 失败. 所以能应对各种各样的数据结构, 还是使用跟 Document 的形式更像的 NDJSON 格式 (在 codec 中是 newline) 用来进行 Ingestion 要更稳定.
