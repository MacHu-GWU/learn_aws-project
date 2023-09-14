Optimizing Amazon S3 performance
==============================================================================
Keywords: AWS, Amazon, S3

.. note::

    因为 S3 是根据 key 的 prefix 来决定具体是哪台服务器处理这个请求的, 所有早期官方推荐给 prefix 加 random hash 来分散请求. 2018 年 7 月起, `这个公告 <https://aws.amazon.com/about-aws/whats-new/2018/07/amazon-s3-announces-increased-request-rate-performance/>`_ 说了, 这种优化已经不在需要了.


Performance Guidelines for Amazon S3
------------------------------------------------------------------------------
- Measure Performance: 建议测量你用来对 S3 读写的机器 (EC2, Lambda) 的 IO 速度.
- Scale Storage Connections Horizontally: S3 是个超大型分布式系统, 你用多个机器同时对 S3 进行读写, 让每个机器都跑满贷款, 放心, S3 扛得住.
- Use Byte-Range Fetches: 你可以用 byte range 来获取一个大型文件中的一小部分.
- Retry Requests for Latency-Sensitive Applications: 如果你的应用对延迟敏感, 例如你知道你一个 read 大概率在 1 秒内结束, 你可以激进一点, 如果超过 1 秒还没结束, 肯定是因为什么别的原因导致的, 不如直接重试, 这样大概率会在 1 秒内结束. 放心, S3 扛得住.
- Combine Amazon S3 (Storage) and Amazon EC2 (Compute) in the Same AWS Region: 计算和存储在一个 Region 速度会比较快.
- Use Amazon S3 Transfer Acceleration to Minimize Latency Caused by Distance: 这是一个 S3 的功能, 其本质是用 CloudFront 的全球网络, 使用内网将数据从 S3 拷贝到离你近的地方, 然后再给你的客户端.
- Use the Latest Version of the AWS SDKs: 没什么说的.


Performance Design Patterns for Amazon S3
------------------------------------------------------------------------------
- Using Caching for Frequently Accessed Content
- Timeouts and Retries for Latency-Sensitive Applications
- Horizontal Scaling and Request Parallelization for High Throughput
- Using Amazon S3 Transfer Acceleration to Accelerate Geographically Disparate Data Transfers
