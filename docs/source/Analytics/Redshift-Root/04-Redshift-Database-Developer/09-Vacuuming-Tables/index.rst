AWS Redshift Vacuuming Tables
==============================================================================
Keywords: AWS, Amazon, Redshift, Vacuum, Table


Overview
------------------------------------------------------------------------------
Vacuum Table 指的是对 Storage Layer 进行优化. 例如把以前多次写入的小文件重新排序合并成大文件以提高查询效率的操作. 大部分数据仓库系统都有这个步骤. 只不过有的系统把接口给用户用, 有的系统完全自动进行. 在 Redshift 中 Vacumm 默认自动, 你也可以手动运行.

至于决定要不要 Vacuum 主要有下面几个因素:

1. 平均一个 columnar storage file 的大小以及里面的数据条数.
2. 一个 table 中没有被排序的 rows 的百分比.

- `Vacuuming tables <https://docs.aws.amazon.com/redshift/latest/dg/t_Reclaiming_storage_space202.html>`_
