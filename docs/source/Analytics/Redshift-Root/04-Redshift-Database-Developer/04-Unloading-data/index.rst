Unloading Data from Redshift
==============================================================================
Keywords: AWS, Amazon, Redshift, Unload

如果你的 Query 的结果可能非常大, 那么你在 SQL client 中遍历超大结果的过程中如果出错了, 那么你就得再运行一次 Query 了. 为了避免这一情况, 建议使用 Unload 命令异步将结果写入到 S3, 然后你再想怎么读就怎么读.


Unloading data to Amazon S3
------------------------------------------------------------------------------
默认情况下你的 SQL client 发送了一个 query, Redshift 会在每个 Slice 上执行这些 query, 然后这些分布在每个 Slice 上的 result 会以并行的方式返回. (特殊情况是你指定了 sort by 排序, 那么这些数据会被汇总到一个 node 上进行排序后再返回)

如果你想把数据结果 dump 到 S3, 你可以使用 ``UNLOAD`` 命令将 query 的结果写入到 S3. 具体的写入行为可以通过参数控制, 比如写成什么数据格式, 是一个大文件还是多个小文件. 数据在 S3 上会被 Server side encryption 加密.


Python Library
------------------------------------------------------------------------------
由于这个需求太过于常见, 所以我想自己写一个简单的模块, 将 SQL 查询和从 S3 读取结果封装成极简 API. 我现在还没有完成.


Reference
------------------------------------------------------------------------------
- `Unloading data <https://docs.aws.amazon.com/redshift/latest/dg/c_unloading_data.html>`_
