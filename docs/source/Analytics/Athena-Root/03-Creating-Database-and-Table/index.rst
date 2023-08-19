Creating Database and Table
==============================================================================
Keywords: AWS, Amazon, Athena.


Creating Table
------------------------------------------------------------------------------
我们知道 Athena 需要基于 AWS Glue Catalog 才能让查询引擎知道去哪里读取数据, 以及怎样解析数据. 所以我们首先要创建 Glue Catalog Database 和 Glue Table. 其中 Database 非常好创建, 几乎没有什么配置选项. 而 Table 则比较复杂. Table 的本质是一个 HIVE Table (virtual table, metadata only), 我们需要指定数据的存储位置, 数据格式, 序列化, 反序列化工具, 以及数据的分区等信息.

有下面几种方法可以创建 Table:

1. 在 Athena Console 的 Query Editor 中, 点击 Create Table 按钮可以用用户友好的 GUI 来创建 Table. 这种方法特别适合于数据在 S3 上的情况, 同时这也是 Athena 90% 的应用场景.
2. 在 Glue Console 里手动创建 Table. 这属于 Glue 服务的内容, 这里不展开说.
3. 用 Glue Crawler 自动创建 Table. 它的本质是扫描你的数据源中的数据, 并进行随机采样, 分析出你的表结构. 这属于 Glue 服务的内容, 这里不展开说.
4. 用 DDL (Data Declaration Language) 来创建 Table. 它的本质就是写 SQL, 不过你要对 HIVE 的 DDL 语言有一定的了解. Athena DDL 是基于 HIVE DDL 的方言, 99% 的地方都一样. 你可以参考下面的链接详细学习 Athena DDL 语言.

Reference:

- `Creating tables in Athena <https://docs.aws.amazon.com/athena/latest/ug/creating-tables.html>`_
- `DDL statements <https://docs.aws.amazon.com/athena/latest/ug/ddl-reference.html>`_: DDL 语言手册速查.
- `Supported SerDes and data formats <https://docs.aws.amazon.com/athena/latest/ug/supported-serdes.html>`_: 序列化和反序列化的文档, 数据读取参数, 比如设置 CSV 的 delimiter, 是否有 header 等.
- `JSON SerDe <https://docs.aws.amazon.com/athena/latest/ug/json-serde.html>`_: 对于 JSON 中的 array, struct 等数据结构的处理方法详解.
