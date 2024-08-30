Glue Crawler With Different DataLake
==============================================================================



CSV
------------------------------------------------------------------------------
.. dropdown:: csv_example_no_partition.py

    .. literalinclude:: ./csv_example_no_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:

.. dropdown:: csv_example_has_partition.py

    .. literalinclude:: ./csv_example_has_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:


Parquet
------------------------------------------------------------------------------
.. dropdown:: parquet_example_no_partition.py

    .. literalinclude:: ./parquet_example_no_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:

.. dropdown:: parquet_example_has_partition.py

    .. literalinclude:: ./parquet_example_has_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:


Delta Lake
------------------------------------------------------------------------------
DeltaLake 社区有一个非常好用的 Python 库 `delta-rs <https://github.com/delta-io/delta-rs>`_, 它是 DeltaLake 的 Rust 原生实现的 Python binding. 它是基于 DeltaLake 3.X 版本的. 我非常喜欢用这个库来将数据写入到 DeltaLake 中.

但我在尝试用 Glue Crawler 来自动从 DeltaLake 的 S3 Location 生成 Glue Table 时遇到了一个问题, 我尝试了所有参数的排列组合, 但 Glue Crawler 依然无法成功生成 Glue Table. 后来经过一天的 Debug, 我找到了这篇 `官方 RePost <https://repost.aws/questions/QUyDYz31OnREGxy7gz2qIeuw/error-internal-service-exception-of-glue-crawler>`_, 里面明确提到了 Glue Crawler 的 DeltaLake 是基于 1.0 的, 它无法识别我用 3.X 版本写入的数据. 所以目前 Glue Crawler 是无法为我的 S3 folder 自动生成 Glue Table 的.

结论就是, 我只能为我的 DeltaLake 手动创建 Glue Table 了. 但是 Glue Table 的参数众多, 我不知道如何设置. 于是我想到了一个办法. 我根据 `Introducing native Delta Lake table support with AWS Glue crawlers <https://aws.amazon.com/blogs/big-data/introducing-native-delta-lake-table-support-with-aws-glue-crawlers/>`_ 这篇博文, 成功用 Crawler 生成了一个 DeltaLake 1.0 的 Glue Table. 这里除了 Schema 的部分, 其实都是 DeltaLake Table 的标准配置. 那么我就可以用纯 Parquet 的 DataLake 让 Crawler 创建一个 Table, 然后查看里面 Partition 的设置, 然后对这个 1.0 的 Glue Table 进行一些 Schema 和 Partition 的修改, 就能得到一个 DeltaLake 3.X 的 Glue Table 了.

这种方式我测试过了, 在有 Upsert 的情况下依然可以查询到最新的数据.

.. dropdown:: succeeded_cralwer_generated_delta_lake_table_without_partition.py

    .. literalinclude:: ./delta_issue/succeeded_cralwer_generated_delta_lake_table_without_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:

.. dropdown:: succeeded_cralwer_generated_parquet_table_partition_details.py

    .. literalinclude:: ./delta_issue/succeeded_cralwer_generated_delta_lake_table_without_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:

.. dropdown:: succeeded_cralwer_generated_parquet_table_with_partition.py

    .. literalinclude:: ./delta_issue/succeeded_cralwer_generated_delta_lake_table_without_partition.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:

下面列出了我的最终解决方案.

.. dropdown:: delta_example_has_partition_manual_create_table.py

    .. literalinclude:: ./delta_issue/delta_example_has_partition_manual_create_table.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:
