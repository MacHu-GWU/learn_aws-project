Designing Table
==============================================================================
Keywords: AWS, Amazon, Redshift, Design Table


Choose sort key
------------------------------------------------------------------------------
关于 sort key 的介绍请参考 :ref:`redshift-sort-key`

首先要知道的是 Redshift 是基于列式存储的. Redshift 在将数据存储到磁盘上时, 会基于 Sort Key 在磁盘上顺序写入. 这相当于时候每个 Table 都有个默认的 sorted index column. 同时 Redshift 由于使用了列式存储, RDBMS 中的那些 index 根本就没有必要, 所以在 Redshift 中没有 Index. 查询性能的优化主要取决于 Sort Key, Distribution Key.

官方文档推荐用以下几个原则来决定哪个 Column 成为 Sort Key:

- 如果有 datetime column, 并且最近的数据查询的更为频繁, 则果断选择时间列为 sort key.
- 如果你的 query 会有很多 range query, 选择在 query 中被使用最多的列作为 sort key.
- 如果你频繁的要 join table, 那么把 join ON column 的列同时作为 sort key 和 distribution key.

Reference:

- `Choose the best sort key <https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-sort-key.html>`_


Choose Distribution Key and Style
------------------------------------------------------------------------------
关于 Distribution key 的介绍请参考 :ref:`redshift-distribution-key`

首先要知道的是 Redshift 是一个分布式系统. 数据需要根据 distribution key 来决定由哪个节点来处理这个数据.

官方文档推荐用以下几个原则来决定哪个 Column 成为 Distribution Key

1. Distribute the fact table and one dimension table on their common columns.

    Your fact table can have only one distribution key. Any tables that join on another key aren't collocated with the fact table. Choose one dimension to collocate based on how frequently it is joined and the size of the joining rows. Designate both the dimension table's primary key and the fact table's corresponding foreign key as the DISTKEY.

2. Choose the largest dimension based on the size of the filtered dataset.

    Only the rows that are used in the join need to be distributed, so consider the size of the dataset after filtering, not the size of the table.

3. Choose a column with high cardinality in the filtered result set.

    If you distribute a sales table on a date column, for example, you should probably get fairly even data distribution, unless most of your sales are seasonal. However, if you commonly use a range-restricted predicate to filter for a narrow date period, most of the filtered rows occur on a limited set of slices and the query workload is skewed.

4. Change some dimension tables to use ALL distribution.

    If a dimension table cannot be collocated with the fact table or other important joining tables, you can improve query performance significantly by distributing the entire table to all of the nodes. Using ALL distribution multiplies storage space requirements and increases load times and maintenance operations, so you should weigh all factors before choosing ALL distribution.

Reference:

- `Choose the best distribution style <https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-best-dist-key.html>`_


Choose Best Columnar Compression
------------------------------------------------------------------------------
关于 Distribution key 的介绍请参考 :ref:`redshift-column-compression`.
