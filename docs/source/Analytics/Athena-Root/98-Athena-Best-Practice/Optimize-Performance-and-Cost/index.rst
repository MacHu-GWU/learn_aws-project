Optimize Athena Performance and Cost
==============================================================================
Keywords: AWS, Amazon, Athena.

这篇文档是对 AWS 官方博客上的 "Top 10 Performance Tuning Tips for Amazon Athena" (链接在文末) 这篇文章的精读.


Partition (分区) 和 Bucketing (分桶)
------------------------------------------------------------------------------
Partition (分区) 和 Bucketing (分桶) 是两种将数据分区的技术. 两者都是为了在分布式的查询引擎中提高性能, 减少被扫描的数据, 提高查询的速度.

.. note::

    这里的 bucketing 指的并不是 S3 Bucket 中的 Bucket, 而是一种逻辑概念.

首先我们要明白一个概念 **Cardinality** (Number of element in a set). 它指的是一个字段中, 不同的值的个数. 比如你有 10 年的 1 亿条电商购买数据. year 字段可能只有 10 种可能, month 只有 12 种, day 只有 31 种. 那么这几个字段都是 ``Low Cardinality`` 的. 而对于 OrderId, 可能有千万个购买行为, 那么就有几千万个不同的 OrderId, 那么这个字段就是 高 ``High Cardinality`` 的.

.. note::

    字段是指二维表数据中的 Column, 或者 Json 中的 Key.

Partition 常用于 ``Low Cardinality`` 的字段. 常用于年月日时间这一类查询中常用 Range ( ``start <= time <= end``) 进行过滤的字段. 在 S3 Bucket 中的实现表现为使用不同的 S3 Key prefix. 在文件系统中表现为使用不同的文件夹. 这样使得查询时能少扫描一些数据.

Bucketing 常用于 ``High Cardinality`` 的字段. 常用于 OrderId 这一类人类不可读, 但是机器可读的 Id 类型的字段. 常用于我们指定具体的值 或者进行 Join 的查询 (``OrderId = "f90a9d8fb3671f8f4a488585461b6144"``). 在 S3 Bucket 中的实现表现为使用不同的 S3 Key prefix. 在文件系统中表现为使用不同的文件夹. 其原理是指定比如 256 个桶, 然后将 ``OrderId`` 进行 hash 后除以 256 取余然后放在不同的桶中. 这样在查询具体订单的相关信息时时能够快速的定位到具体的桶中, 使得只扫描很少的数据. 并且在做 Join 的时候, 所有的相关数据都会被放到桶一个桶中, 所以 JOIN 的效率会高.

在同时使用 Partition 和 Bucketing 时, S3 Key 的 pattern 长这样: ``s3://my-bucket/order-dataset/year=2010/month=01/day=15/001/data.parquet`` ... ``s3://my-bucket/order-dataset/year=2010/month=01/day=15/256/data.parquet``. ...


Compression and Splittable file
------------------------------------------------------------------------------
**Compression**

首先, Athena 是按照扫描的数据收费的, 那么压缩后的文件体积更小, 显然你的 cost 也更低. 但是它的代价就是读取数据后还要解压缩, 不过对于 Athena 引擎来说, 它需要将数据从 S3 读到内存中, 读取更小的数据+解压缩 和 读取大数据+没有压缩, 相比, 前者反而更快, 因为读取是网络 IO, 而解压缩是 CPU 计算, 网络 IO 比 CPU 计算慢了几个数量级, 所以这样做是值得的. 并且对于 Parquet 这样的列示存储而言, 有的查询例如查询某个字段的值等于特定的值来说, 甚至都不需要进行解压缩就可以直接查询. 总之对数据进行压缩是值得的.

**Splittable file**

对于 Athena 查询引擎而言, 有的文件例如 CSV 和 JSON 是不可分割的, 也就不支持并行读. 而 Parquet 支持并行读. 所以用 Splittable 的格式可以增加查询性能.


Optimize file sizes
------------------------------------------------------------------------------
很多用过电脑的人都知道对大量小文件进行操作要比对一个大文件进行操作要慢得多. 这是因为对每个小文件操作都要经过操作系统 IO, 并且读取过程也不是顺序读取. 在云上数据仓库中也是一样. 最佳实践推荐让数据文件保持 128MB ~ 512MB 之间的查询效率会比较高 (对于很多支持 upsert 的框架例如 Hudi 来说, 因为每个 update 都是对整个文件的 full replacement, 所以 hudi 需要对其进行平衡, 保持文件不大不小, 一般会在 64MB ~ 128MB 之间, 这里不展开说)

如果你每次扫描的文件数量超过了 1000 个, 那么就推荐你考虑进行 compaction (合并).


Use Columnar data store generation
------------------------------------------------------------------------------
使用列示存储的查询性能显然更高, 好处多多, 这里不展开说了. 一般选用 Parquet 或 ORC 都行. 一般如果你的计算框架是 Spark 就用 Parquet, 如果是 Hive 就用 ORC.


Use ``Limit`` clause with ``Order By``
------------------------------------------------------------------------------
由于 Order by 要对数据排序, 而对数据在扫描过程中排序的主要技术是 堆排序, 如果你只需要返回最高或者最低的几个数据, 那么用 LIMIT 的话就可以大大减少需要扫描的数据, 从而大幅提高性能.


Join Large table on the Left Small table on the right
------------------------------------------------------------------------------
在做 JOIN 的时候, 把大表放在左边, 小表放在右边性能比较好 (好个 20% 左右). 因为一般右边的表是 lookup table, 显然放在右边的表越小越好. 对于 SQL 数据库中的查询引擎来说这个优化不是很必要, 因为引擎会自动分析出哪个表大, 哪个表小.



``GROUP BY`` highest cardinality column first, low cardinality column last
------------------------------------------------------------------------------
用多个字段组合成的 compound key 进行 group by 分组的时候, 先对 high cardinality 的字段分组, 再对 low cardinality 的字段分组, 性能会比较高. 这个也很好理解, 先对高 cardinality 的字段分组能使得后面的每个小组比较小, 再对 low cadinality 的字段分组就比较快了.


Use regexp_like instead of ``LIKE`` if multiple token used
------------------------------------------------------------------------------


Use approx_distinct(my_column) instead of COUNT(DISTINCT my_column) if the exact number doesn't matter
------------------------------------------------------------------------------
如果你的 COUNT DISTINCT query 只是需要知道大概有多少个, 具体的值有个 1% 的误差也关系不大, 那么你就可以用 approx_distinct 来近似. 其原理主要是 HyperLogLog 算法.


Only include the columns that you need
------------------------------------------------------------------------------
如果你用的是列示存储, 显然只包含你需要的 columns 会比 SELECT * 要少扫描很多数据. 这里不再赘述.


Optimizing Partition Processing using partition projection
------------------------------------------------------------------------------
如果你的表有超级多有层级的 Partition (百万级), 那么你可以考虑使用 Partition Projection 来优化. 它的原理是 Partition 本身只是 HIVE Table 中的一条记录, 而你的每个查询如果包含了 Partition 的字段, 就先要扫描所有的 Partition 找到哪些 Partition 中的数据文件会包含你的数据. 而 Partition metadata 数据本身是没有索引的, 所以当 Partition 多起来的时候这一步就会比较慢.

而 Partition Projection 的本质就是给 Partition metadata 加索引, 从而大大提高定位到最终你的数据文件的速度. 这件事的本质就是把数据用 Partition 的方式聚类成文件, 每个文件都被放在一个 Partition 下, 而你又对 Partition 本身进行了索引, 自然就能很轻松地定位到这些文件了, 从而让原本的要扫描 N 行的复杂度, 降低到了 Log(Log(N)) 级别.

你可以参考这篇官方文档 `Setting up partition projection <https://docs.aws.amazon.com/athena/latest/ug/partition-projection-setting-up.html>`_, 给 Glue Catalog Table 添加一些 properties 就可以启用 Partition Projection.


Speed up queries producing large result sets using UNLOAD
------------------------------------------------------------------------------
默认情况下 Athena Result 的结果会被写入到 CSV 文件中, 而 CSV 只支持单线程顺序写入. Athena 支持 UNLOAD 命令, 能将查询结果用其他格式, 例如 Parquet, 并行地写入到 S3. 这样不仅能提高写入速度, 还能提高读取速度. 详情请参考我写的 :ref:`aws-athena-write-query-results-in-parquet` 这篇博文.


Reference
------------------------------------------------------------------------------
- `Top 10 Performance Tuning Tips for Amazon Athena <https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/>`_

Storage

- Partition your data
- Bucket your data
- Use Compression
- Optimize file sizes
- Optimize columnar data store generation

Query tuning

- Optimize ORDER BY
- Optimize joins
- Optimize GROUP BY
- Use approximate functions
- Only include the columns that you need