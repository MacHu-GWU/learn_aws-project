AWS Redshift Analyze Tables
==============================================================================
Keywords: AWS, Amazon, Redshift, Analyze, Table


Overview
------------------------------------------------------------------------------
Analyze Table 是对 Table 中的数据进行统计分析, 从而利用这些信息更好的进行 query planning 的操作. Redshift 会自动在后台进行 query planning. 你在 load 了一大堆数据或者 delete 了一大堆数据后你也可以手动进行 Analyze. 另外, 你还可以只选择对某几列会经常参与到 query 中的 columns 进行 Analyze 而不是所有的 column.

要注意 Analyze 的操作是很费资源的, automatic analyze 会自动选择 workload 很轻的时间段进行.

- `Analyzing tables <https://docs.aws.amazon.com/redshift/latest/dg/t_Analyzing_tables.html>`_
