Cloud Migration Strategy Overview
==============================================================================
Keywords:


Cloud Migration Strategy
------------------------------------------------------------------------------
基本上有以下几种迁徙模式:

1. Rehost (life and shift), 对服务器的硬盘做 比特级 的复制, 然后再云上运行.
2. Replatform (lift-tinker-and-shift), 换一个平台, 例如将数据库从自家数据中心的虚拟机上迁徙到 AWS RDS 上.
3. Repurchasing, 购买新的产品, 例如抛弃过去的 CMS 员工管理系统, 使用 Salesforce.
4. Refactoring / Rearchitect, 重新设计架构, 例如从 monolithic 模式迁徙到 microservice 模式.
5. Retire
6. Retain


How to Migrate
------------------------------------------------------------------------------
按照 AWS 官方的说法, 一个 AWS Cloud Migration 的项目大约可以分为三步 Asset, Mobilize, Migrate and modernize. 简单来说:

- Asset 就是清点你已有的资源的清单, 计划要把哪些东西 migrate 到云上.
- Mobilize 就是准备工作, 例如创建 AWS 账号, 创建被 migrate 之后的资源环境, 例如你要 migrate database 就要创建 AWS RDS 并测试
- Migrate and modernize 就是迁徙工作的执行, 例如切断目前的业务流量, 然后迁徙数据, 测试通过后将业务流量切换到云上.


Assess
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At the start of your journey, you assess your organization’s current readiness for operating in the cloud. Most importantly, you want to identify the desired business outcomes and develop the business case for migration.

Our tools help you assess your on-premises resources and build a right-sized and optimized cost projection for running applications in AWS.

**Services and programs**

**Optimization and Licensing Assessment**

When you are evaluating options for migrating to the cloud or reducing licensing costs, you can take advantage of an AWS Optimization and Licensing Assessment (AWS OLA) to save on third-party licensing costs and run your resources more efficiently. AWS OLA is a free program for new and existing customers to assess and optimize current on-premises and cloud environments, based on actual resource utilization, third-party licensing, and application dependencies.

**Migration Evaluator**

Migration Evaluator delivers accurate data-driven recommendations to right-size and right-cost compute. Our predictive analytics provide insights on an ongoing basis to ensure that you are always running each application in the best place, with the right software and at the lowest TCO—even as your environment, cloud options, and prices change. Migration Evaluator helps you build a clear business case to accelerate your migration planning.

**AWS Migration Acceleration Program**

The AWS Migration Acceleration Program (MAP) is a comprehensive and proven cloud migration program based upon AWS’s experience migrating thousands of enterprise customers to the cloud.  MAP provides tools that reduce costs and automate and accelerate execution, tailored training approaches and content, expertise from Partners in the AWS Partner Network, a global partner community, and AWS investment.  Specialized workload support is available for Mainframe, Windows, storage, VMware Cloud on AWS, SAP, databases, and Amazon Connect.


Mobilize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As part of the mobilize phase, you create a migration plan and refine your business case. You address gaps in your organization’s readiness that were uncovered in the assess phase, with a focus on building your baseline environment (the “landing zone”), driving operational readiness, and developing cloud skills.

A strong migration plan starts with a deeper understanding of the interdependencies between applications, and evaluates migration strategies to meet your business case objectives. One critical aspect of developing your migration strategy is to collect application portfolio data and rationalize applications using the seven common migration strategies: relocate, rehost, replatform, refactor, repurchase, retire, or retain.

Not every decision in a migration can be automated, but our tools help you make easier and better decisions.

**Services**

**AWS Application Discovery Service**

    AWS Application Discovery Service helps you plan migration projects by gathering information about your on-premises data centers. AWS Application Discovery Service collects and presents configuration, usage, and behavior data from your servers to help you better understand your workloads.

**AWS Migration Hub**

    AWS Migration Hub automates the planning and tracking of application migrations across multiple AWS and partner tools, allowing you to choose the migration tools that best fit your needs.

**Migration partner solutions**

    Enterprises migrating to AWS require expertise, tools, and alignment of business and IT strategy. Many organizations can accelerate their migration and time to results through partnership. The AWS Partner Competency Program has validated that the partners below have demonstrated that they can help enterprise customers migrate applications and legacy infrastructure to AWS.

**AWS Landing Zone**

    AWS Landing Zone solution helps you set up a secure, multi-account AWS environment based on AWS best practices. Before you start to migrate first few applications, Landing Zone solution helps set-up your initial security baseline for your core accounts and resources.

**AWS Control Tower**

    AWS Control Tower helps setup an automated landing zone, which is a well-architected, multi-account AWS environment. You can use Control Tower to manage your AWS environment during and after the migration. During the application migration process, Control Tower dashboards provide continuous visibility into your AWS environment.


Migrate and modernize
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
During the migrate and modernize phase, each application is designed, migrated, and validated. Leverage the services below through our migration specialists, with one of our migration competency partners, or on your own to start the process of moving applications and data to AWS.

**Services for migrating and modernizing**

**AWS Migration Hub**

    AWS Migration Hub is the one destination for cloud migration and modernization, giving you the tools you need to accelerate and simplify your journey with AWS. Perhaps you’re making the case for cloud within your organization, or creating a data-driven inventory of existing IT assets. Maybe you’re planning, running, and tracking a portfolio of applications migrating to AWS. Or you might be modernizing applications already running on AWS. In all of these cases, Migration Hub can help with your cloud transformation journey.

**AWS Application Migration Service**

    AWS Application Migration Service (AWS MGN) simplifies and expedites migration from physical, virtual, and cloud infrastructure. AWS MGN keeps your source servers up to date on AWS using continuous, block-level data replication. During replication, your applications continue to run in your source environment without downtime or performance impact. You can use the same automated process to migrate a wide range of applications and databases, including SAP, Oracle, and Microsoft SQL Server. After a minimal cutover window, your migrated servers run natively on AWS.

**AWS Database Migration Service**

AWS Database Migration Service (DMS) can migrate your data to and from most widely used commercial and open-source databases. AWS DMS supports homogeneous migrations such as Oracle to Oracle, as well as heterogeneous migrations between different database platforms, such as Oracle or Microsoft SQL Server to Amazon Aurora. You can use AWS DMS to continuously replicate your data with high availability and consolidate databases into a petabyte-scale data warehouse by streaming data to Amazon Redshift and Amazon S3. Learn more about AWS data transfer services.

**VMware Cloud on AWS**

VMware Cloud on AWS (VMC) allows you to quickly relocate hundreds of applications virtualized on vSphere to the AWS Cloud in just days and to maintain consistent operations with your VMware Cloud Foundation-based environments. VMware Cloud on AWS enables seamless bi-directional application migration with consistent policies by using vSphere vMotion between your on-premises data center and the AWS Cloud without converting or re-architecting any workload.

**AWS Marketplace**

    AWS Marketplace is a curated digital catalog that helps you reduce costs by not over-purchasing with an in-perpetuity license. You can find, buy, deploy, and manage third-party software and services to build solutions for your business.

**AWS Managed Services**

    AWS Managed Services (AMS) operates AWS on your behalf, providing a production-ready enterprise operating model, on-going cost optimization, and day-to-day infrastructure management. AMS takes responsibility for operating your cloud environment post migration, such as analyzing alerts and responding to incidents, enabling your internal resources to focus on the more strategic areas of your business. AWS Managed Services automates common activities, such as change requests, monitoring, patch management, security, and backup services, and provides full-lifecycle services to provision, run, and support your infrastructure.


Migrate Execution Strategy
------------------------------------------------------------------------------
上一节我们介绍了 Migration 的 三步 Asset, Mobilize, Migrate and modernize. 其中第三步的执行是变数最多的, 也是最复杂的. 我们需要根据不同的应用场景, 选择不同的执行策略. 下面我们来详细讨论一下这个问题.

首先我们要考虑这么几件事:

1. 我们执行迁徙的时候, 业务是否可以暂停?
    - 如果可以, 暂停的窗口期有多长?
    - 如果不行, 业务的流量的统计特征是什么?
2. 我们要迁徙的系统是否有可以独立拆分出去的组件, 例如 App 和 Middleware 可以分开迁徙吗?
3. 我们要迁徙的系统是否可以在内部分片? 例如一个 Database 就是必须要作为一个整体迁徙的. 而如果我们的系统是一个存储数据的系统, 我们是可以把数据按照 hash 分片, 一部分一部分的迁徙.
4. 迁徙的系统如果作为一个整体, 从外部看有哪些外部系统依赖这个系统运行? 如果有很多外部系统, 我们还要负责给外部系统提供技术支持, 帮助他们从旧系统切换到新系统上.


Examples
------------------------------------------------------------------------------


Server Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
应用场景:

    我们有很多 Linux 服务器在机房运行, 希望将他们迁移到 AWS 上.

执行方案:

    一般用 lift and shift, 将镜像和配置文件打包, 然后迁徙到 AWS EC2 上. 如果不允许停机, 则可以先迁徙但是不启用, 然后用软切换进行切换. 有很多工具例如 CloudEndure 可以帮助我们进行这个过程.


Database Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
应用场景:

    数据库迁徙, 我们希望将他们迁徙到 AWS 上. 这个数据库是我们的 App 后台数据库, 我们不希望 App 在迁徙后受到影响.

执行方案:

    1. 将数据库 dump 成文件, 然后导入到 AWS RDS 上.
    2. 把 App 代码复制一份, 更新数据库连接, 用 AWS RDS 进行测试.
    3. 更新 App 代码, 将数据库连接参数化, 并在代码层实现自动切换.

    这时候就有两种情况, 可以停机和不可以停机两种.

    如果可以停机:

    1. 将数据库 dump, 以及导入到 AWS RDS 的这个过程自动化, 并进行演习, 确保这个过程能在停机窗口内完成.
    2. 停机 -> 执行自动化迁徙 -> 进行数据库连接自动切换 -> 上线

    如果不可以停机:

    1. 用 AWS DMS 服务将数据不断同步到 AWS RDS 上, 检测数据时延, 和数据一致性. 假设时延大约在 1 分钟左右.
    2. 将读请求指向 AWS RDS, 写请求指向旧数据库.
    3. 然后暂停 1 分钟时间的写请求, 然后讲写请求也指向新 AWS RDS, 再恢复写请求.

    值得注意的是针对不可以停机情况下的解决方案, 在很多非 Database Migration 的场景下的思路是一样的. 都是:

    1. Near real-time data sync (let's say latency is 1 minute)
    2. redirect read access to new system
    3. cut off write access, wait 1 minute
    4. redirect write access to new system
    5. recover write access.


App Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
这可能涉及到容器化或者微服务化. 我们暂时不展开讨论.


Data Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
执行方案:

    总体策略和 Database Migration 一样.

    如果可以停机:

    - 先停机, 然后迁徙拷贝数据, 然后恢复.
    - 如果数据量很大, 无法保证在停机窗口内迁徙完, 那么可以将数据分为冷热数据, 存量数据提前迁徙, 然后在停机窗口内只迁徙增量数据.

    如果不可以停机:

    - 则需要实现数据同步策略. 然后先将读请求指向新系统, 然后暂时停止写请求并等待数据同步彻底完成, 再将写请求也指向新系统, 最后恢复写请求.


Infrastructure Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Network Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Software Repurchasing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- SVN -> CodeCommit
- Jenkins -> CodeBuild / CodePipeline
- Self hosted Kafka -> MSK
- Self hosted message queue -> SQS


Reference
------------------------------------------------------------------------------
- `6 Strategies for Migrating Applications to the Cloud <https://aws.amazon.com/blogs/enterprise-strategy/6-strategies-for-migrating-applications-to-the-cloud/>`_: 这是一篇比较早期的介绍上云策略的官方博文, 至今依然有参考意义.
- `How to migrate <https://aws.amazon.com/cloud-migration/how-to-migrate/>`_: 这是 AWS 官方的迁徙指南的入口, 介绍了一些迁徙的工具和服务.
