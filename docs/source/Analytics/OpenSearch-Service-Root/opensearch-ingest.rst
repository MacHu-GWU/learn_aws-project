我在使用 OpenSearch Ingestion 的过程中发现有这么几个小坑:

- 使用 S3 作为 Source 的时候, 如果 S3 Filter Prefix 中有特殊字符, 例如等号 (等号在 Hive partition 中很常见的), 那么无法正确识别并触发 S3 Event. 这是因为 S3 Filter Prefix 是 Literal 的, 这个 Prefix 的字符串不支持 Escape. 所以这个 Prefix 中是不能有除了 +, -, _ 以外的特殊字符的. 例如你如果想要让 Prefix 为 ``data/year=2021/``, 那么建议你让 Prefix 设为 ``data/year-2021/``, 然后让你的数据写入到这个目录下, 来为 Prefix 妥协. 还有一个常见的错误是 S3 Filter 的 suffix, 他也是 Literal 的. 比如你只想要 JSON 文件来 trigger event, 那么 Suffix 就要是 ``.json`` 而不能是 ``*.json``.
- 使用 S3 作为 Source 并使用 SQS 作为 Notification Channel 的时候, 每次修改 Event Notification Configuration 之后 S3 会自动给 SQS 发送一个 Test Event. 这个 Event 是无法被 Ingestion Pipeline 所处理的, 所以你修改这个 Event 之后最好要用 Lambda 之类的东西删掉这个 Event.
- 使用 S3 作为 Source 并使用 Parquet 作为 codec 数据文件格式时, 对于 ``array<str>`` 这一类的列表是无法直接识别的 (会将其解析为 element<...> 这种形式), 你只有用 Processor 对其进行处理之后才能正确 Index, 不然这些数据都会导致 Ingestion 失败. 所以能应对各种各样的数据结构, 还是使用跟 Document 的形式更像的 NDJSON 格式 (在 codec 中是 newline) 用来进行 Ingestion 要更稳定.
