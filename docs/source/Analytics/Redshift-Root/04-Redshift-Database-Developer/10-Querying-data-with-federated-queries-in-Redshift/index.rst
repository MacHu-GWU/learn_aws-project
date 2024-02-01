Querying data with federated queries in Redshift
==============================================================================
Keywords: AWS, Amazon, Redshift, Federated Query


Overview
------------------------------------------------------------------------------
Federated query 中文是联合查询. 本质上说的是把几个系统中的数据放在一个 Query 中进行. 例如你有一个 Redshift 还有一个 RDS. 你要 Join 两个表. 这就是典型的联合查询的场景. 而如果你只是用 Redshift 查询 RDS 中的数据, 而不和 Redshift 中的数据产生联动, 这只能算是 External Data.

Redshift 允许你创建 Create External Schema, 这个 Schema 本质上和 Glue Catalog 差不多. 然后你就可以用 Schema.Table 的格式指定表, 在一个 SQL 中进行联合查询了. Redshift 会自动分析哪些 SQL 操作适合在 External 系统中做, 哪些操作适合把数据全部 Load 到 Redshift 中的内存后在本地做.

联合查询一般会涉及到一下几个问题:

1. VPC Peering: Redshift 和目标系统可能不在一个 VPC. 需要用 VPC Peering 把网络连起来.
2. Data Type Difference: 不同的系统中的数据类型名字一样, 但是底层可能不兼容.


Reference
------------------------------------------------------------------------------
- `Querying data with federated queries in Amazon Redshift <https://docs.aws.amazon.com/redshift/latest/dg/federated-overview.html>`_