.. _redshift-quotas-and-limits:

Redshift Quotas and Limits
==============================================================================
Keywords: AWS, Amazon, Redshift, limit, limits, quota, quotas

注意, 官方的文档随着时间的推移会更新的. 请以官方文档为准.

Reference:

- https://docs.aws.amazon.com/redshift/latest/mgmt/amazon-redshift-limits.html


Quotas for Amazon Redshift objects
------------------------------------------------------------------------------
- 一个 cluster 最多有 128 个 DC2 node
- 一个 cluster 最多有 128 个 DS2 node
- 一个 account 一个 region 所有的 cluster 加起来最多有 200 个 node
- 一个 cluster 中的一个 database 最多有 9,900 个 schema
- COPY command load 的数据一个 row 不能超过 4MB, 所以不要存 large binary, 请用 S3 存 large binary, 然后把 S3 URI 存在 redshift 中.
- 一个 ``large`` node type, single node cluster 最多有 9,900 个 Table. 包括了 table / temp table / view / datashare table.
- 一个 ``xlplus`` node type, multiple node cluster 最多有 20,000 个 Table.
- 后面的 node type 越大, table 的上限越多.


Quotas for Amazon Redshift Serverless objects
------------------------------------------------------------------------------
- Number of databases = 100, 这个不包含通过 data share 创建的 database
- Number of schemas = 9,900. 足够用了, 因为 schema 想当是一个 namespace, 相当于一个 sub-database
- Number of tables = 200,000, 已经跟 Cluster 中的上限打平.
- Timeout for idle or inactive sessions = 1 hour, 给人用的 session 一小时自动登出, 没什么大不了的.
- Timeout for a running query = 86,399 seconds (24 hours), 如果一个 query 超过 1 天, 这不应该是数据仓库来解决的问题.
- Timeout for idle transactions = 6 hours, 一个事务超过 6 小时, 这就不应该是一个事务.
- Number of maximum connections = 2000, 给人用够用了, 给机器用就用 data api 好了, 给机器用的消耗不了多少.
- Number of workgroups = 25, 这个可以要求增加, 肯定够了. 因为一个 workgroup 一般对应这你们公司的一个 role.
- Number of namespaces = 25, 这个可以要求增加, 肯定够了. 因为一个 namespace 下可以创建很多个 database.
- Number of Amazon Redshift roles in a workgroup = 1,000
