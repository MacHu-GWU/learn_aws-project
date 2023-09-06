.. _aws-s3-overview:

Amazon S3 Overview
==============================================================================
Keywords: AWS, Amazon, S3, Overview.


Overview
------------------------------------------------------------------------------
S3 是一个 Object Storage 存储服务, 是 AWS 的王牌存储服务, 也是该领域的行业标杆. 它历史悠久, 功能丰富, 服务稳定, 价格低廉. 互联网中的数据有 1 / 3 被存在了 S3 上, 所以它也被称为互联网的硬盘. 虽然从功能上来说它跟 C 端用户所熟知的网盘服务类似, 但它是一个 Object Storage, 跟主打文件存储的网盘服务有本质的不同.


File Storage, Block Storage and Object Storage
------------------------------------------------------------------------------
本节我们快速的介绍一下行业内的三大存储方式: 文件存储, 块存储 和 对象存储.

- 文件存储: 按照树状结构组织文件. 优点是比较直观易用. 但是它由于底层设计的原因, 存在扩展困难的问题 (可以, 但很难设计一个容量几乎无限的文件系统). 所以为了存储同等大小的数据, 文件存储的成本最高 (参考 AWS EFS)
- 块存储: 把数据分成大小等量的小块 (Block), 然后封装为数据卷 (Volume) 挂载到用户的磁盘上. 例如 AWS EBS 服务中是 16KB. 块存储非常高效, 可靠, 并且容易扩展. 但是块存储成本高昂, 处理元数据通常需要在数据库中进行, 也就多了一层需要维护的东西. 块存储通常作为文件存储的底层虚拟磁盘使用.
- 对象存储: 这是一种扁平的数据结构, 所有的对象都是一个 Key Value Pair. 由于对象存储使用起来不是男直观, 所以通常会提供一个 HTTP API 供用户使用. 它的扩展性极强, 所以成为了公共云的理想之选. 它的缺点是数据一旦写入就成为了一个整体, 无法更改.

Reference:

- `文件存储, 块存储还是对象存储? <https://www.redhat.com/zh/topics/data-storage/file-block-object-storage>`_


How to Learn Amazon S3
------------------------------------------------------------------------------
S3 的官方文档有下面几个部分. 我建议先通读 FAQ, Pricing, 和 Amazon S3 User Guide 中的 What is Amazon S3 这三部分. 这三个部分加起来也不长, 能很快的对 S3 有一个大概的了解. 然后再根据自己的需要深入学习.

- `Amazon S3 FAQs <https://aws.amazon.com/s3/faqs/>`_: 常见问题.
- `Amazon S3 Pricing <https://aws.amazon.com/s3/pricing/>`_: 价格明细.
- `Amazon S3 User Guide <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_: S3 的主文档.
- `Amazon S3 Glacier Developer Guide <https://docs.aws.amazon.com/amazonglacier/latest/dev/introduction.html>`_: S3 Glacier 的主文档.
- `Architecture Center: Storage Best Practices <https://aws.amazon.com/architecture/storage/>`_: 一些关于存储的最佳实践的文章.

我建议直接在你的 AWS Account 里创建一个 S3 bucket, 然后用 Python + `Boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html>`_ 客户端进行编程, 进行创建, 覆写, 删除, 扫描等操作. 通过实践来学习 S3.


S3 Knowledge Graph
------------------------------------------------------------------------------
以下是 S3 的知识图谱, 对所有的知识点进行了一个梳理.

- Storage Class: 不同的存储分类的价格不同, 数据的读写访问速度不同. 例如对冷热数据进行区分能大幅降低成本.
- Storage Management:
    - S3 Lifecycle: 自动化地将 Object 从一种 Storage Class 转移到另一种 Storage Class, 或者彻底删除之.
    - S3 Object Lock: 防止 Object 被意外删除或者覆写. 主要是应对合规性要求和法律风险.
    - S3 Replication: S3 是一个 Regional 的服务, 该功能可以自动化地将 Object 复制到另一个 Region, 以提高可用性.
    - S3 Batch Operations: 用一个 API 来对大量 Object (可以是 billion 级别) 进行操作, 这些操作包括, 复制, invoke lambda, tagging 等.
- Access management and security:
    - S3 Block Public Access: 防止公网公众访问你的 Bucket. 该功能默认是开启的.
    - AWS Identity and Access Management (IAM): 用于管理 AWS 上的 Principal 来访问 S3. 可以定义 "谁", 在什么 "情况下 (例如 IP 地址网段)" 能对 "什么资源 (包括 bucket, 文件夹, object 等)" 进行 "什么操作 (例如读写, 删除, 修改 tag 等)". 这套规则是给 Principal, 也就是访问 S3 的人或机器用的.
    - Bucket policies: 和 IAM 类似, 但是是给 S3 Bucket 用的, 也是 Resource Policy 中的一种.
    - Amazon S3 access points: 可以创建一个专用的 Endpoint (具有公网 IP 和 URL 的网络设备) 来将你的 S3 中的 Object 共享给受信用户. 你可以在 Access Point 中定义受信用户的 VPC 或 IP 网段. 该功能本质上是为了解决共享 S3 Bucket 的时候通常要修改 Bucket Policy, 而 Bucket Policy 有 20KB 大小的限制问题. 而你可以创建多达 10,000 个 Access Point, 如果你申请增加 Quota, 你可以创建更多 Access Point.
    - Access control lists (ACLs): ACL 是传统的权限管理方式, 它是一个 XML 文档. 官方推荐尽量使用 IAM + Bucket Policy, 它比 ACL 更易用, 功能更多. 只有特殊需求的情况下会用到 ACL.
    - S3 Object Ownership: 每个对象都有 Ownership, 这个 Ownership 就可以作为 Bucket Policy 中的一部分作为访问数据的条件. 同时你也可以转移 Ownership. 默认情况下创建 S3 Bucket 的人就是 Owner, 里面的 Object 都默认属于这个 Bucket Owner.
    - IAM Access Analyzer for S3: 这是一个可以分析对你的 S3 的访问进行分析的工具, 并自动给出建议或者当有可疑的访问的时候进行报警.
- Data Processing:
    - S3 Object Lambda: 在用户 Get, Head, List 的时候 (Put 不行), 你可以用一个 Lambda 自动对数据进行一定的处理之后再返回. 例如你可以对数据进行一定的扫描和检查以防止给用户返回了敏感数据. 你还可以自动将图片进行裁剪或格式转换的处理等. 这个功能主要是为了让你对 "读" 操作进行自定义处理.
    - Event notifications: 当对象被创建 (包括 Put), 删除, 或者 ACL 发生变更等 Write 操作发生时, 可以自动发送 Event 到各种 Target. 然后你就可以 Subscribe 这些 Event 来对数据进行处理. 例如当文件被上传到一个 Bucket 后, 你自动触发 Lambda 对文件进行格式转换, 写入数据库等操作. 这个功能主要是为了让你对 "写" 操作进行自定义处理.
- Storage logging and monitoring:
    - Amazon CloudWatch metrics for Amazon S3: 你可以用 CloudWatch 对每天 S3 的读写访问操作, 数据量进行监控.
    - AWS CloudTrail: 所有对 S3 的 API 操作日志都可以用 CloudTrail 来捕获, 然后存为 JSON 文件供你分析.
    - Server access logging: 这是针对对 S3 Bucket 进行的 API 操作的 log (CloudTrail log 会包括对 Object 操作), 主要是用于安全相关的审查.
    - AWS Trusted Advisor
- Analytics and insights
    - Amazon S3 Storage Lens: 对多个 AWS Account, Region, Bucket, Prefix 中的 metrics 数据进行聚合, 用 Dashboard 来展示, 以便你能更好地了解你的数据.
    - Storage Class Analysis: 分析你的 Object life cycle, 从而更好地决定哪些数据应该放在哪种 Storage Class 中.
    - S3 Inventory with Inventory reports: 这是一个自动扫描你的 S3 并生成一个 inventory 报告的功能.
- Strong consistency: S3 能确保 Strong read-after-write consistency. 也就是说, 你在写入一个 Object 后, 立刻读取这个 Object, 你能读到最新的数据.

What's Next
------------------------------------------------------------------------------
todo
