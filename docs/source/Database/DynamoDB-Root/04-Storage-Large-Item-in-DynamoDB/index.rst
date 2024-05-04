Storage Large Item in DynamoDB
==============================================================================
Keywords: aws, amazon, dynamodb

很多时候我们会有用 DynamoDB 来管理大型 binary 数据的需求. 例如文档管理系统, Artifacts 管理系统. 而 DynamoDB 有单个 Item 400KB 的限制. 这种情况下, 根据 AWS 官方文档中的 `Best practices for storing large items and attributes <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-use-s3-too.html>`_ 一文, 你应该将数据存在 S3 上而将 S3 URI 存在 DynamoDB 上. 这种方法听起来简单, 但是在生产实践中有很多细节问题值得商榷. 例如:

1. 写入到 DynamoDB 和 S3 的操作如果有一个失败了怎么处理?
2. 如果 DynamoDB 有多个属性都是 Large Binary, 这必然导致写入 S3 的耗时会比较长, 如何保证它们全部成功或者全部失败?
3. 写入到 S3 的时候应该怎么构建 S3 URI?
4. 在 Update 的时候是否要删除旧的 S3 Object? 长期下来产生的很多没有用的 S3 Object 怎么清理?

本文将详细的讨论这种将数据写入到 S3, 将 S3 URI 存到 DynamoDB 中的正确做法.

Conclusion
------------------------------------------------------------------------------
- 双写一致性: Create / Update 时先写 S3, 再写 DynamoDB, Delete 时先删 DynamoDB 再删 S3.
- S3 Location: 使用 ``s3://bucket/prefix/${partition_key}/${optional_sort_key}/${attribute_name}/${hash_of_the_data}`` 的模式.
- Clean Up: 每个 S3 object 都有一个 update at 的 metadata, 这和 DynamoDB item 的时间一致. 所以我们可以用 DynamoDB export 到 S3 (该操作比较便宜, 并不消耗 RCU, 它是用 bin log 实现的. 请看这篇 `DynamoDB data export to Amazon S3: how it works <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport.HowItWorks.html>`_ 官方文档), 然后用一个 batch 程序去对比 DynamoDB 和 S3 既可. 由于 S3 update 的时间可能比真实的 DynamoDB update 时间要早一点 (取决于写入 S3 的耗时), 所以我们可以把时间回溯个 1 小时, 只对比在这之前的数据既可.


Diagram
------------------------------------------------------------------------------
.. raw:: html
    :file: ./Store-Large-Item-in-DynamoDB.drawio.html


Sample Script
------------------------------------------------------------------------------
.. dropdown:: store_large_item_in_dynamodb.py

    .. literalinclude:: ./store_large_item_in_dynamodb.py
       :language: python
       :linenos:
