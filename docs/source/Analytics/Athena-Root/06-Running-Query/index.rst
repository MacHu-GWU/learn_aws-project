Running Query
==============================================================================
Keywords: AWS, Amazon, Athena.


知识点
------------------------------------------------------------------------------
- Viewing query plans:
    - `Understanding Athena EXPLAIN statement results <https://docs.aws.amazon.com/athena/latest/ug/athena-explain-statement-understanding.html>`_: 理解 explain statement result 的内容.
- Query results and recent queries: 可以在 Console 中查看最近的 query 的结果 (也可以用 API 来查看). 因为本质上每一个 query 都有一个 id, 而结果就储存在指定的 S3 bucket 中, 所以你可以无需重新运行 query 就能查看结果, 只不过 Athena Console 自带了这个功能.

Reusing query results
------------------------------------------------------------------------------
这是 Athena 2022 年 11 月发布的新功能. 你在运行 Query 的时候可以打开 result cache. 这个 cache 最短能有 1 分钟, 最长能有 7 天. 只要在打开了 result cache 的状态下执行的查询, 你的 SQL 结果就会被缓存, 从而你下次运行同样的结果时就能自动使用之前的结果, 当然也就不收费.

而如果你运行的新 Query 中包含了之前已经被缓存的查询, 例如你把之前的查询结果作为 subquery, 同样 Athena 也会自动走缓存. 这个功能类似于之前的 Creating a Table from Query Result (CTAS) 和 View 的概念, 只不过 CTAS 要把结果 dump 到 S3 并创建新表, 你如果之后不用了还要将其删除. 而 View 则是相当于一个子查询, 还是要执行扫描来获得这个子查询的结果. 所以该功能是一个非常好的补充, 有助于企业提高查询性能并大幅减少开销.

而 Athena 是如何知道是否要用缓存的呢? 这取决于你的 Query 是不是 deterministic 的, 也就是说如果数据不变, Query 不变, 结果是不是 100% 不变. 例如如果你用了 LIMIT, 那么结果的顺序可能是不一样的, 结果就不会被缓存, 因为它是一个分布式系统. 而如果你用了 LIMIT + ORDER BY, 那么结果肯定是一样的, 也就会被缓存下来.


Viewing query stats
------------------------------------------------------------------------------
你可以再 Console 内查看每个已经完成的 Query 的 Statistics, 例如扫描了多少数据, 扫描了多少行, 输出了多少数据, 多少行. querying, planning, execution, service processing 分别用了多长时间, 有助于你理解你的 Query.


Working with views
------------------------------------------------------------------------------
View 是数据库领域很常见的概念, 它本质就是一个虚拟的表, 它的内容是一个对实体表进行查询的结果. 你每次查询 View 的时候本质上会将 View 作为一个子查询. 这里不多赘述了.


Using saved queries
------------------------------------------------------------------------------
你可以在 Console 中 (或者用 API) 创建 saved query (也叫 named query). 说白了就是将你的 SQL 保存下来, 并给他个名字.


Using parameterized queries
------------------------------------------------------------------------------
Query 是可以带 parameter 的, 你可以先写一个具体的 Query, 然后把值用 ``?`` 替换掉即可. 然后再运行该 Query 的时候把参数按照位置指定即可. 注意, 它不支持 keyword parameter.

当然, 这个 parameter 是有一些限制的, 例如你只能把值放在 WHERE 里面. 如果你要对 Select 中的内容也要参数化, 建议你使用 ORM 框架例如 Sqlalchemy.

如果你是用 Console 运行 Query, 那么它检测到 ? 之后就会弹出对话框让你输入 Parameter. 而如果你是用 API 来运行 Query, 那么在 API Request 中就要指定 Parameter


Querying S3 Glacier
------------------------------------------------------------------------------


Handling schema updates
------------------------------------------------------------------------------


Querying arrays
------------------------------------------------------------------------------
对 Array 的查询是用 SQL 进行大数据分析的常见难点. 你主要需要熟悉很多对 Array 进行操作的函数. 详情请参考官方文档 `Querying arrays <https://docs.aws.amazon.com/athena/latest/ug/querying-arrays.html>`_


Querying geospatial data
------------------------------------------------------------------------------
Athena 还支持地理数据的查询, 例如判断点到点的距离, 点是否在多边形内等. 你主要需要了解 Athena 所能处理的数据格式, 以及熟悉很多对 geospatial 的函数. 详情请参考官方文档 `Querying geospatial data <https://docs.aws.amazon.com/athena/latest/ug/querying-geospatial-data.html>`_


Querying JSON
------------------------------------------------------------------------------
对 JSON 这种嵌套式的数据结构的查询是用 SQL 进行大数据分析的常见难点. 你主要需要熟悉很多对 JSON 进行操作的函数. 详情请参考官方文档 `Querying JSON <https://docs.aws.amazon.com/athena/latest/ug/querying-JSON.html>`_


Using ML with Athena
------------------------------------------------------------------------------
在大数据查询引擎中使用 ML 是一个 2020 年以后比较热的话题, 很多厂商也都在跟进. 这个功能的本质是在 SQL 引擎中自定义一个函数, 这个函数真正调用的是一个外部的服务, 例如 AWS Lambda. 这个自定义的函数也叫做 UDF (User Defined Function). 详情请看下一节.


Querying with UDFs
------------------------------------------------------------------------------
UDF 是 Athena 的一个功能, 它允许你自定义一个函数, 并用 AWS Lambda 作为后端实现. 定义 UDF 的语法就像是这个样子:

.. code-block:: sql

    USING EXTERNAL FUNCTION UDF_name(variable1 data_type[, variable2 data_type][,...])
    RETURNS data_type
    LAMBDA 'lambda_function_name_or_ARN'
    [, EXTERNAL FUNCTION UDF_name2(variable1 data_type[, variable2 data_type][,...])
    RETURNS data_type
    LAMBDA 'lambda_function_name_or_ARN'[,...]]
    SELECT  [...] UDF_name(expression) [, UDF_name2(expression)] [...]

详情请查看 `Querying with user defined functions<https://docs.aws.amazon.com/athena/latest/ug/querying-udf.html>`_

Querying across regions
------------------------------------------------------------------------------


Querying AWS Glue Data Catalog
------------------------------------------------------------------------------


Querying AWS service logs
------------------------------------------------------------------------------
AWS 很多 Service 都是自带日志系统的. 例如 ELB 的 Log, VPC Log, CloudTrail Log 等等. 如果一个公司希望对这些数据进行审计和分析, 通常都是要为这些 Log 所在的 S3 location 创建 Glue Catalog Table, 然后才能进行查询. 而这一步你需要对 Log 的文件格式了如指掌才能正确地创建 Table. 现在这些 Service 都有一个按钮, 能一键自动创建 Table, 让后你就可以直接开始查询了, 大大简化了工作量.


Querying web server logs
------------------------------------------------------------------------------


Reference
------------------------------------------------------------------------------
- `Running SQL queries using Amazon Athena <https://docs.aws.amazon.com/athena/latest/ug/querying-athena-tables.html>`_
