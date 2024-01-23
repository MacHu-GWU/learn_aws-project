What is Redshift Serverless
==============================================================================
Keywords: AWS, Amazon, Redshift, Serverless, sls.


Summary
------------------------------------------------------------------------------
Redshift 是一款非常成功的企业数仓产品. 但是它的价格昂贵, 不适合个人开发者, 也不适合负载快速变化的初创企业. AWS 一直有将传统软件服务 serverless 化的传统, 从早期的 DynamoDB 天生 serverless, 到 RDS 中 Aurora Serverless, 到 OpenSearch Serverless. 终于 AWS Redshift Serverless 在 2022-07 也 Generally Available 了.

为了方便起见, 我们将 Redshift Serverless 简称为 RSSLS.

Reference:

- `What is Amazon Redshift Serverless? <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-whatis.html>`_


.. _redshift-serverless-namespaces-and-workgroups:

What is NameSpaces and Workgroups
------------------------------------------------------------------------------
而只有 Schema / Table / User 等.

在使用 Redshift Cluster 的时候, 我们需要指定 Node 的数量, 以及每个 Node 的配置. 而 RSSLS 不存在 Cluster. 那使用 Redshift Serverless 的时候, 你到底创建了什么呢?

在 RSSLS 中 AWS 将资源抽象为 Namespaces 和 Workgroups. Namespaces 负责对数据相关的资源进行管理的. 而 Workgroup 是负责对计算资源进行管理的, 例如 RPU, VPC 等. 这有点像 Serverless 中最重要的存算分离. Namespaces 负责 "存", 而 Workgroup 负责 "算". 它们各自管理的资源如下:

- Namespaces: schema, tables, users, KMS key.
- Workgroup: RPU, VPC, Security Group.

以下是 AWS 官方文档的说明:

    Namespace is a collection of database objects and users. The storage-related namespace groups together schemas, tables, users, or AWS Key Management Service keys for encrypting data. Storage properties include the database name and password of the admin user, permissions, and encryption and security. Other resources that are grouped under namespaces include datashares, recovery points, and usage limits. You can configure these storage properties using the Amazon Redshift Serverless console, the AWS Command Line Interface, or the Amazon Redshift Serverless APIs for the specific resource.

    Workgroup is a collection of compute resources. The compute-related workgroup groups together compute resources like RPUs, VPC subnet groups, and security groups. Properties for the workgroup include network and security settings. Other resources that are grouped under workgroups include access and usage limits. You can configure these compute properties using the Amazon Redshift Serverless console, the AWS Command Line Interface, or the Amazon Redshift Serverless APIs.

    You can create one or more namespaces and workgroups. A namespace can exist without any workgroup associated with it. Each namespace can have only one workgroup associated with it. Conversely, each workgroup can be associated with only one namespace.

这里比较关键的是, 一个 Namespace 是可以独立于 Workgroup 存在的. 这很好理解, 数据仓库的核心资产是数据. Namespace 负责数据, 数据就像是一个移动硬盘, 你插到任何一台电脑 (计算资源的比喻) 上都能用. 而一个 Namespace 最多关联一个 Workgroup. 而一个 Workgroup 也只能关联一个 Namespace. 这里稍稍跟 移动硬盘 + 电脑 的比喻不一样. 一个电脑可以插多个硬盘, 但这里一个 Workgroup 只能关联一个 namespace (不然对于计算资源的管理就会变得非常复杂).

Ref:

- `Overview of Amazon Redshift Serverless workgroups and namespaces <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-workgroup-namespace.html>`_
- `Amazon Redshift conceptual overview <https://docs.aws.amazon.com/redshift/latest/gsg/getting-started.html>`_: 讲解了 Amazon Redshift 的核心概念.


Redshift Serverless Pricing
------------------------------------------------------------------------------
简单来说, 跟 Cluster 模式的 Redshift 放在那里就收钱相比, Redshift Serverless 是只按你运行 Query (包括 Insert / Update) 的时长收费, 精确到秒. 也就是说, 你的 Redshift Serverless 可以一直存在, 但是你不运行任何 Query 的时候, 你是不用付钱的. 但是你的存在 Redshift 上的数据无论你有没有运行 Query, 都是要收费的. 但是作为数据分析的仓库的成本而言, 运算成本一般远远高于存储.

- Redshift Processing Units: $0.36 per RPU hour
- Amazon Redshift managed storage pricing: $0.024 per GB / Month
- 注意, Redshift 最小的 RPU 是 8, 最大是 512, 一个 RPU 大约是 16G 内存, 你 scale 的时候也会以 8 为单位的增加减少. 并且 8, 16, 24 RPU 能 handle 大约 128 TB 的数据. 超过 128 TB 数据就要用 32 RPU 了. 换算过来大约是 1 个 RPU 能处理 128 / 16 = 8 TB 的数据量 (这条参考自 `Understanding Amazon Redshift Serverless capacity <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html#serverless-rpu-capacity>`_).

这里我们把 On-Demand Cluster 的价格也列出来作为对比. 最小的 Plan 是用 ``dc2.large``, 1 台, 2 vCPU, 15GB 的实例. 价格是 $0.25 / Hour, 也就是 0.25 * 24 * 30 = $180 一个月. 当然你可以用 Pause 的功能暂时停止来节约成本. 可以看出, ``dc2.large`` 和一个 RPU 的大小差不多.

这里我们来看两个案例:

案例 1:

你用 Redshift serverless 进行实验性质的开发, 假设你用最小的 8 RPU, 每天实际运行 Query 的时间大约 1 小时, 你的数据集是 1GB. 那么你的开销是:

- 计算成本: 0.36 * 8 = $2.88 / 天 = $86.4 / 月
- 存储成本: 0.024 * 1 = $0.024 / 月

这就比你用最小的 On-Demand Cluster 的价格 ($180 / 月) 要划算多了. 并且你在 query 的时候用的是 8 个 RPU. 而 On-Demand Cluster 只有 1 个 ``dc2.large`` 的实例. 你的 query 速度会快很多.

案例 2:

你用 Redshift serverless 每天从 7AM - 7PM (包括 7PM), 每小时运行一个耗时 10 分钟的 Query 来统计每天的指标, 也就是每天运行 13 次. 你的数据量大约是 100 TB, 需要 24 个 RPU. 那么你每月的开销是:

- 计算成本: 0.36 (RPU / Hour 单价) * 24 (24 个 RPU) * 30 (一个月 30 天) * 13 (每天运行 13 次) * 600 (每次 600秒) / 3600 (换算为小时) = 0.36 * 24 * 30 * 13 * 600 / 3600 = $561.6 / 月. 存 100 TB 的数据, 这还是挺划算的.

这个我们就不计算 On-Demand Cluster 了, 如果你 24 小时开的话价格肯定远远高于这个. 而如果你要用 Pause 的功能, 你就要额外花费精力运行自动化脚本在每次 query 前启动 Cluster, 运行完之后关闭 Cluster. 这个人力, 开发, 维护成本也是要考虑的.

Reference:

- `Amazon Redshift pricing <https://aws.amazon.com/redshift/pricing/>`_
- `Billing for Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-billing.html>`_


Reference
------------------------------------------------------------------------------
- Amazon Redshift Serverless: https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html
- Amazon Redshift Serverless is now generally available (2022-07): https://aws.amazon.com/about-aws/whats-new/2022/07/amazon-redshift-serverless-generally-available/


- Amazon Redshift Serverless Technical Overview Deck: https://aws.highspot.com/items/62a8d0a5282f1e220bf892bb?lfrm=srp.4
- Amazon Redshift Serverless - First Call Deck: https://aws.highspot.com/items/62ccc8244585166b17aa16a1?lfrm=srp.2
