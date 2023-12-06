Amazon Kinesis Data Streams - Kinesis Producer Library KPL
==============================================================================
Keywords: AWS, Amazon, Kinesis, Data Stream,.


Overview
------------------------------------------------------------------------------
KPL 本质上是编程语言实现的客户端 SDK 程序. 到 2023-12-01 为止, 它原生由 Java 实现, 然后由于 MultiLanguageDaemon 的模式 (其他语言调用 Java 暴漏出的接口) (目前只有 Java), 能让用户更容易的编写 Producer 程序.


Advantages of Using KPL over AWS SDK (Put Record)
-------------------------------------------------------------------------------

1. 性能更好, 单台机器 1K + Record /s 的写入性能.
2. 自带 Retry 机制.
3. 使用了 Batch, 先将 Record 写入 Buffer, 再一次性发给 Stream, 从而提高写入性能.
4. 允许方便地自定义 Monitor Event, 并将其发送到 CloudWatch.
5. 异步架构, 由于使用了 Buffer, 当你使用 KPL 执行 Put Record 时, 并不会堵塞 Producer Client 程序.


When to Use KPL When to use AWS SDK (Put Record)
-------------------------------------------------------------------------------
When to NOT USE KPL:

1. 如果不允许 Consumer 接受 Record 的时候有 Delay. 因为 KPL 使用了异步架构, 而且 Record 先打入 Buffer 再 Batch 发送, 所以不能用 KPL


KPL Key Concepts
-------------------------------------------------------------------------------
Records:

- KPL Records: 一条 Blob 数据
- Kinesis Data Stream Records: 一个特殊的 Record 数据结构, 包括了 Partition Key, Sequence Number, Blob of Data

Batching:

Batching 指对多个 Items (Records) 执行同一个 Action. KPL 支持两种不同的 Batching 模式:

- Collection: 将多个本应用 PutRecord API 提交的 Record 写入到 Buffer, 然后集中用一个 PutRecords API 批量提交, 以节约多个 Record 分别使用 API 所需要的网络延迟.
- Aggregation: 将多个小 KPL Record 合并成一个大 Record 再提交. 在 Consume 的时候先将它们分拆成小的 Record 后再消费.


Reference
------------------------------------------------------------------------------
- https://docs.aws.amazon.com/streams/latest/dev/developing-producers-with-kpl.html
