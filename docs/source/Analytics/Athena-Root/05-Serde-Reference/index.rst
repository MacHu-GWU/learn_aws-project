Serde Reference
==============================================================================
Keywords: AWS, Amazon, Athena.


Overview
------------------------------------------------------------------------------
SerDe 是 serialization 和 deserialization 的简称, 也就是序列化和反序列化. 常用语从各种数据格式中读取数据. 通常有两个地方会用到 SerDe:

1. 在你写 DDL 定义 Catalog Table Schema 的时通常会需要定义用哪个 Seder 库来解析数据.
2. 在你写 Query 的时候可以指定用 Seder 来序列化数据.


Reference
------------------------------------------------------------------------------
- SerDe reference: https://docs.aws.amazon.com/athena/latest/ug/serde-reference.html