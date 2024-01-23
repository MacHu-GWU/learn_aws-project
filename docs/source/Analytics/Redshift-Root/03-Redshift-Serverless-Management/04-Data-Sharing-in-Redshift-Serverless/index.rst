Data Sharing in Redshift Serverless
==============================================================================
Keywords: AWS, Amazon, Redshift, Serverless, sls.

在数据库或数据仓库的世界中, 当我们提到 Data Share 一般指的是在不复制数据的情况下, 允许 "其他人" (也可以是机器, 下面用专业术语 Consumer 来指代) 访问你的数据. 但是这里有几个点有必要说明一下:

1. 为 "Consumer" 创建一个 User 并且给他们连接信息, **这不叫 Data Share**. 这根 DB Owner 自己连接到数据库没有本质区别.
2. "Consumer" 查询不应该占用 Owner 的计算资源, "Consumer" 自己应该为自己的查询计算资源付费. 不然你一分享, 人家就用大量的 Query 把你的服务器弄垮了.

AWS Redshift Serverless Data Share 的 "Consumer" 可以是一个 AWS Account, 也可以是另一个 Namespace (需要有自己对应的 Workgroup). 并且 Consumer 可以是一个 Cluster, 不一定必须是 Redshift Serverless Namespace. 并且可以位于不同的 Region (会产生额外费用)

我们这里假设有两个 AWS Account, A 和 B. A 有一个 Redshift Serverless 的 Namespace, 想要分享给 B. 下面列出了详细步骤:

1. A 的管理员进入到 Namespace Console -> Data Share.
2. 点击 Connect. 你得先 Connect 之后才能操作.
3. 选择 Create Data Share, 配置好你要 Share 哪些 Schema, 哪些 Table, UDF 等, 分享给谁 (在本例中是另一个 AWS Account) 以及 Publish 到哪里 (这里有个 Publish 到 Data Exchange 说的是你公开卖你的数据的情况)
4. 然后是 B 的管理员进入到 Redshift Console 中. 进入到自己的 Namespace -> Data Share 中, 然后在 ``Datashares from other namespaces and AWS accounts`` 中找到 A 分享的 Namespace. 然后为这个分享的 Namespace 创建一个新的 Database (虚拟的, 不是实体的).
5. 然后就可以在 B 的 Namespace 中使用 A 的数据了. 就跟使用 B 自己的 Database 一样, 只不过计算资源时 B 中的 Workgroup. 所以不会影响到 A 的查询性能.

Ref:

- `Data sharing in Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-datasharing.html>`_: Data Share 的官方文档, 是一个简要的介绍.
- `Managing data sharing using the console <https://docs.aws.amazon.com/redshift/latest/dg/getting-started-datashare-console.html>`_: 作为管理员, 或是 Consumer 使用 Data Share 功能的详细步骤.
- `Considerations when using data sharing in Amazon Redshift <https://docs.aws.amazon.com/redshift/latest/dg/considerations.html>`_: 一些考量和限制.
