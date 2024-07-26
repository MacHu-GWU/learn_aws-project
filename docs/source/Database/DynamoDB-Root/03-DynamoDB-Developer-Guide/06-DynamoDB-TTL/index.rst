DynamoDB Time to Live (TTL)
==============================================================================
Keywords: AWS, Amazon, DynamoDB

DynamoDB 的 Time to Live (TTL) 功能可以自动删除过期的项目. 它的价值在当 Item 过期后, DynamoDB 会自动删除 Item, 而不需要应用程序来删除, 也不消耗 WCU. 这个功能是不花钱的.

- 你需要指定一个 Attribute 作为 TimeToLive 的 expiration time, 凡是当前时间大于这个值的 item 都视为过期数据.
- 过期的数据不会被立刻删除, 而是会在几天内 (一般是 3 天内) 被 AWS 自动删除.
- 在还没有被删除之前你依然可以 get, put, update, delete.
- 你在 Scan 和 Query 的时候默认还是会扫到这些过期数据, 你需要在 query 中指定 filter condition 来过滤掉这些数据. AWS 不会自动帮你过滤这些数据.

下面我们给出了一个示例:

.. dropdown:: test_dynamodb_ttl.py

    .. literalinclude:: ./test_dynamodb_ttl.py
       :language: python
       :linenos:


Reference
------------------------------------------------------------------------------
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_time_to_live.html
https://pynamodb.readthedocs.io/en/stable/api.html#pynamodb.attributes.TTLAttribute