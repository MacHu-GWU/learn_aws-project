Redshift Data API
==============================================================================
Keywords: AWS, Amazon, Redshift, Data API


Overview
------------------------------------------------------------------------------
Redshift Data API 是 AWS 下的一个服务. 对, 没错, 它居然不是一个功能, 而是一个服务. 它是一套 Rest API 能允许用户使用 AWS CLI 权限直接运行 SQL, 而无需创建数据库连接, 也不没有什么你的网络必须位于同一个 VPC 的要求. 等于是 AWS 帮你部署了一台免费的堡垒机, 然后让你免费用. 这个功能和 AWS RDS Aurora Data API 一样, 非常好用!

在本文中我们对 Data API 进行了测试. 主要是想验证除了能运行 Query, 是不是 Load data, 以及一些 DDL 语句例如 Create Table, Drop Table 之类的是不是也能用 Data API. 这里直接放结论, 对, 可以, 凡是你能运行的 SQL 都可以通过 Data API 使用.


Considerations
------------------------------------------------------------------------------
使用 Data API 前你需要知道会有如下考量.

- 同一时间最多有 200 个 query 处于正在执行中的状态.
- query result 最多不超过 100MB. 毕竟结果是要用 HTTP Response 返回的, 不可能太大. 太大的结果请用 UNLOAD.
- query statement 的大小不得超过 100KB. 这个可能性很小.
- query results 在 24 小时后就会自动删除.


Data API Use Case
------------------------------------------------------------------------------
什么情况下使用 Data API 比较好呢?

1. 进行探索性实验. 由于 Data API 设置简单, 适合用于在编程语言中运行 SQL. 如果你只是需要随便写写 SQL, 那么 AWS Console 里的 Query Editor. 而如果你是把 SQL 的输入输出结果做成 Python Code, 那么 Data API 就是一个很好的选择.
2. 在 EC2, Lambda, ECS, Step Function 等计算环境中对 Redshift 进行查询. 并且是你预计查询总时间不会太长 (小于 5 分钟) 的情况下. 如果你的查询总时间可能会很长, 那么建议用 Step Function 来进行长轮询. 因为在 EC2, Lambda, ECS 中做长轮询, 等待的时间也是要计费的. 而 Step Function 是按照 transition 计费.
3. 在 ETL job 中运行一些 LOAD 的命令.

简而言之, 对于高频率, 但是查询时间不长的 Query 用 Data API 进行编程是非常便利的.


VPN Endpoint
------------------------------------------------------------------------------
Data API 是一个 service, 你从客户端发起的请求默认是走公网到达 public facing 的 AWS 的 API 服务器, 然后获得数据的. 这个 Data API 跟 DynamoDB 的 API 可以说是一模一样的. 而类似的, 在企业中就会有让客户端和 API 通信之间的信道不走公网的需求. 这个时候就需要用到 VPN Endpoint 了.

Reference:

- `Connecting to Amazon Redshift using an interface VPC endpoint <https://docs.aws.amazon.com/redshift/latest/mgmt/security-private-link.html>`_: 如何为 Redshift 配置 VPN Endpoint 的文档.


The AWS Redshift Helper Library
------------------------------------------------------------------------------
使用 Data API 运行 SQL 主要有三个步骤:

- execute_statement: 异步执行 SQL
- describe_statement: 获取执行的状态, 可能还在 pending 或者正在运行, 或者失败了, 或者成功了. 你在 execute statement 之后要用这个 API 进行长轮询, 这样可以把异步的 API 变成同步的.
- get_statement_result: 获取执行结果. 包括 metadata 和数据两部分. 因为数据量可能很大, 所以这个 API 是一个 paginator.

我写了一个 Python 库, 把这三个步骤绑定到了一个函数中, 使得开发者可以轻松的像平时用 DB API 进行数据库编程一样轻松的用 Data API 编写程序.

Sample Usage:

.. dropdown:: test_redshift_data_api.py

    .. literalinclude:: ./test_redshift_data_api.py
       :language: python
       :linenos:


Reference
------------------------------------------------------------------------------
- `Using the Amazon Redshift Data API <https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html>`_
