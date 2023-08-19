.. _aws-athena-ctas:

Creating a Table from Query Result (CTAS)
==============================================================================
Keywords: AWS, Amazon, Athena.

Create Table AS (CTAS) 这个功能可以让你为 SELECT 查询的结果创建一个 Table, 从而方便地进行后续的 Subquery. 它相当于将中间结果缓存下来了, 这是一个非常实用的功能. 跟 View 相比, View 不会将中间结果写入到任何地方, 而 CTAS 会将中间结果写入到 S3 中. 除此之外 CTAS 功能也可以用来做 ETL, 这就很牛逼了.

不过 CTAS 有一些限制, 其中下面几条比较重要:

1. 如果你的 CTAS 在创建表的时候用的 SELECT 语句有 ORDER BY, 那么最终写入到 S3 的 row 的顺序可能不是你指定的 ORDER BY 的顺序. 这个是 SQL 标准规定的, 不是 Athena 的问题. 如果你需要获得 ORDER BY 的数据, 从新读一下这个新创建的 Table 再加上 ORDER By 即可.
2. 如果你的 CTAS query 既有 partitioning 又有 bucketing, 那么这个 query 最多支持 100 个 partition (也就是要 partition 的 column 的值最多有 100 个不同的值)

Reference:

- `Creating a table from query results (CTAS) <https://docs.aws.amazon.com/athena/latest/ug/ctas.html>`_
- `Examples of CTAS queries <https://docs.aws.amazon.com/athena/latest/ug/ctas-examples.html>`_
- `Using CTAS and INSERT INTO for ETL and data analysis <https://docs.aws.amazon.com/athena/latest/ug/ctas-insert-into-etl.html>`_
