Redshift Important Concepts
==============================================================================
Keywords: AWS, Amazon, Redshift, Concept


.. _redshift-sort-key:

Sort Key
------------------------------------------------------------------------------
简单来说在当数据被写入到 Redshift 的时候, 在单个节点上 RS 会按照 Sort Key 对其进行排序. 这样在查询的时候能极大程度上提高性能, 过滤掉大部分数据.

`Redshift 内部的列式存储使用 1MB 作为 block size <https://docs.aws.amazon.com/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html>`_, 每个 block 中的 Sort Key 的最大值和最小值是作为 metadata 储存的. 这使得 Redshift 可以快速跳过很多无关 block, 定位到查询结果需要的 data 上.

Redshift 在创建表时如果没有指定 Sort key, 它会先将所有的 row 在磁盘上顺序存储. 当你 run 了很多 query 以后 redshift 会分析 query 的频率, 找出哪个 column 作为 sort key 能最大程度增加 performance, 然后对 table 自动指定 Sort key, 然后数据进行重新排序. 期间不影响使用.

在创建表时, 你还可以指定一个或者多个 column 作为 sort key. 这里有两种情况 COMPOUND sort key 和 INTERLEAVED sort key. 举例来说, 如果指定了 col_a, col_b 为 sort key. 我们用 va, vb 来表示一个 row 中两个 column 的值. COMPOUND sort key 会按照指定 sort key 的顺序, 先对 va 排序, va 一致的时候再根据 vb 进行排序. 而 INTERLEAVED sort key 对所有的 column 采用相同的权重. 从查询优化的角度来说, COMPOUND sort key 可以增加 JOIN, GROUP BY, ORDER BY 的性能, 或是用到 partition by / order by 的 window function. 而 INTERLEAVED sort key 适合特别大的 fact table 中有很多个 sort key column 彼此之间没什么相关性, 并往往单独用在不同的 query 中的情况.

Reference

- `Choose the best sort key <https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-sort-key.html>`_
- `Working with sort keys <https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html>`_


.. _redshift-distribution-key:

Distribution Key and Style
------------------------------------------------------------------------------
在 Redshift 的架构中, 一个 Cluster 有多个节点, 一个 Node 就是一个有单独 CPU 内存 磁盘的机器, 通常是虚拟机. 一个 Slice 则对应着 ElasticSearch 中的 Shard 的概念, 通常对应着一个 CPU 核心, 有时候也会有多个 Slice 对应一个 CPU 核心的情况. 这个 CPU 核心是我的一个比喻, 并不是 Redshift 真的是这样实现的. 对于一个 Table 中的数据, **有且只有一个** Column 会被指定为 Distribution key, 用于决定一个 Row 的数据最终由哪个 Node 和哪个 Slice 负责处理.

**Distribution Style**

Redshift 有多种 Distribution Style:

- **Key**: 就是根据 distribution key 计算出一个 hash, 用这个 hash 决定具体由哪个 node 哪个 slice 处理. 这是最常用的情形. 通常用于比如 cardinality 很高的列, 比如几百万条 order id.
- **Even**: 就是 round robin, 系统维护一个全局序号, 不断从 0 ~ (N-1) 循环, N = node * slices per node. 这常用于一个 Table 并不会被用于 JOIN 的情形.
- **All**: 每个数据在所有的 Node 都有一个副本. 该方式主要用于提高用小的 dimension table 做 join 时的性能. 比如你有个 business code, 只有 200 多个值, 你经常需要做 join 以获得人类可读的对 business code 的解释, 那么这个表就适合用 All.
- **Auto**: 让 redshift 自动决定, 在数据量小时用 All, 随着数据增加变成 Even.

**Viewing distribution styles**

你可以以下的 SQL 语句获得每个表的 distribution key.

.. code-block:: SQL

    select "schema", "table", diststyle from SVV_TABLE_INFO

其中 distribution style code 的含义对应如下::

    0	EVEN
    1	KEY
    8	ALL
    10	AUTO (ALL)
    11	AUTO (EVEN)
    12	AUTO (KEY)

Reference:

- `Choose the best distribution style <https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-best-dist-key.html>`_
- `Working with data distribution styles <https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html>`_
- `Distribution styles <https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html>`_
- `Viewing distribution styles <https://docs.aws.amazon.com/redshift/latest/dg/viewing-distribution-styles.html>`_


Columnar Storage
------------------------------------------------------------------------------
列式存储已经被讲烂了, 这里不赘述了. 唯一有必要知道的是 Redshift 的 Block Size 是 1 MB.

Reference:

- `Columnar storage <https://docs.aws.amazon.com/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html>`_

.. _redshift-column-compression:

Column Compression
------------------------------------------------------------------------------
由于 Redshift 在存储层使用了 column 列存储, 所以对不同的数据类型做压缩优化可以节约大量磁盘, 大部分的情况下提高性能, 少部分的情况下牺牲一点点性能.

**Compression Encoding**

下面我们列出了 Redshift 所支持的压缩编码, 以及它们的应用场景.

**AZ64 encoding**

    一种针对整数的编码, 官方没有发布算法解释, 其原理不详 (网上有人深入研究了 AZ64 https://www.redshiftresearchproject.org/white_papers/downloads/az64_encoding.pdf, 你可以参考一下), 不仅能减少磁盘空间占用, 还能提升查询性能

**Byte-dictionary encoding**

    对于 Enum 数据 (不同的 unique 值的总数小于 256) 适用的字典存储. 由于 1 bytes = 8 bit, 所以最多支持 256 个不同的值.

**Delta encoding**

    适合于递增递减的步长不大的数据, 比如 datetime 的类型. 它只保存与前一个值相比的 delta 值.

LZO encoding

    是一种致力于解压缩快的压缩算法, 适合于 CHAR / VARCHAR 数据类型. 如果该字符串 column 需要大量参与到 WHERE, 那么就不太合适. 该编码适合于只存不查的 column

Mostly encoding

    简单来说就是说比如一个 column 中的值的整个范围需要用到 8 bytes, 但大部分的值只需要用到 4 bytes, 那么就可以将大部分的只需要 4 bytes 的值用 4 bytes 编码.

Run length encoding

    简单来说如果一个 column 中的值的 cardinality 很低, 比如只有 10. 那么大概率出现连续多个 row 的这个 column 的值会是一样的. 比如一个 color 的列只有 10 个 color, 那么就可以用 4 个 blue, 5 个 red 这样的方式节约存储空间. 该方法不推荐用在 sort key 上, 这会导致非常大的性能浪费.

Text255 and Text32k encodings

    简单来说就是字典, 把出现频率较高的 word, 照字典编码成整数. 该方式只适合西方语系的语言, 不适合中文日文, 因为中文日文最小单位 token 本身占用的比特就不多, 不适合压缩.

Zstandard encoding

    Facebook 2016 年开源的通用型压缩算法, 对整数, 字符串压缩效果都很好, 压缩解压都快, 压缩率也高. 适合作为通用压缩算法. 但在整数类型上的压缩效率要全面差于 AZ64.

总结

    Byte-dictionary, Delta, Text255, Run length, Mostly 都有独特的应用场景, 基本上没有异议.

    其他情况下对于整数类型基本可以无脑上 AZ64. 对于中等长度复杂字符串可以无脑上 Zstandard, 而对于只存不查的大量字符串则适合 LZO.

Reference:

- `Working with column compression <https://docs.aws.amazon.com/redshift/latest/dg/t_Compressing_data_on_disk.html>`_
