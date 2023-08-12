.. _aws-overview:

Amazon Web Service Overview
==============================================================================
Keywords: AWS, Amazon Web Service, Overview

AWS 是世界上市场份额最大的云服务供应商 (到 2023 年为止还是这样). 云计算也是未来的趋势, 许多传统的计算机硬件软件行业都在云时代以一种全新的方式重新被实现.

云基础设施中最基础的三大类服务包括: 计算类 (Compute), 存储类 (Storage) 和 网络类 (Networking). 所有的其他服务可以说都是基于这三大类服务之构建的.

AWS 的计算服务的王牌有 EC2 (虚拟机服务), 存储服务的王牌有 S3 (对象存储), 网络服务的王牌有 VPC (虚拟私有网络). 在此之上, 数据库, 容器, 分布式计算, 数据分析, 运维和持续集成, 机器学习, 网站服务器 等所有的服务都是在这 3 大类基础设施的基础上实现的.

除此之外还有一些服务是用来管理云上资源的. 例如 IAM 可以对所有的云上资源进行细致化的管理. AWS Organization 可以用来管理多个 AWS Accounts 等.

建议在学习 AWS 技术的时候, 先从 S3 开始学习存储 (最简单直观), 从 EC2 和 Lambda 开始学习计算 (最实用, 应用范围广), 从 VPC 开始学习网络 (IT 行业的通识基本功), 然后再慢慢扩展知识:

- 对于数据领域的人可以学习 Database 系列和 Analytics 系列的服务.
- 对于 App 开发者可以学习 Application Integration 系列和 Developer Tools 系列的服务.
- 对于机器学习领域的人可以学习 Machine Learning 系列的服务.
- 对于运维人员可以学习 Management Governance 系列和 Developer Tools 系列.
- 对于网络工程师可以学习 Networking Content Delivery 系列, 对于安全工程师可以学习 Security Identity Compliance 系列.

Reference:

- `AWS vs Azure vs Google Cloud Market Share 2019: What the Latest Data Shows <https://www.parkmycloud.com/blog/aws-vs-azure-vs-google-cloud-market-share/>`_: 这篇博文比较了目前三大云提供商 AWS, Azure, Google Cloud Platform 的市场份额.
- `AWS vs Azure vs GCP: Comparing The Big 3 Cloud Platforms <https://www.bmc.com/blogs/aws-vs-azure-vs-google-cloud-platforms/>`_: 这篇博文从多个维度比较了三大云服务提供商.
- `What's the Difference Between AWS vs. Azure vs. Google Cloud? <https://www.coursera.org/articles/aws-vs-azure-vs-google-cloud>`_: 这篇博文从多个维度比较了三大云服务提供商.
