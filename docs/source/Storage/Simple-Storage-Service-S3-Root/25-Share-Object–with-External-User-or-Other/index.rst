Share Object with External User or Other
==============================================================================
Keywords: AWS, Amazon, S3

**情况 1: 用户只访问 object 里的 content, 而不需要 S3 API access.**

方法 1: 使用 pre-signed URL

用 SDK 可以为 Object 创建一个 Pre-signed URL, 并设置失效时间 (最多 7 天). 这是唯一的能控制失效时间的分享方式, 并且还能 track 是谁访问了你的数据. Bucket Policy 并不能自动设置过期时间.

方法 2: 使用 CloudFront 的 Signed URL

它的本质和 S3 类似, 只不过这个 URL 对应的是位于 CloudFront 上的 S3 object 的副本.

**情况 2: 用户需要用 S3 API 或 Console 访问你的 S3 bucket**

方法 1: IAM Role + Bucket Policy

给用户配置 IAM Role (通常是 cross account) 允许访问该 Bucket, 同时给 Bucket 添加 bucket policy, 显式允许前面指定的 IAM Role 访问. 这样的弊端是如果用户数量非常多 (几千个), 就不容易配置了.

**情况 3: 你负责存储, 允许你的用户读数据**

这种情况常见于你是 Data vendor 的情况, 这时一般会使用 requeter pay 的 bucket, 也就是谁用谁付钱. 你还可以用 AWS Marketplace Data Exchange 来发布和卖你的数据.

**情况 4: 用户只需要对你的数据进行统计, 或聚合分析, 而无需知道具体数据**

例如你允许运行 GROUP BY 的 query, 但不允许用 ``SELECT * FROM ... LIMIT 10``

`AWS Clean Room <https://docs.aws.amazon.com/clean-rooms/>`_ 是专门为这种情况设计的一个服务.


Reference
------------------------------------------------------------------------------
- `Sharing objects with presigned URLs <https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html>`_
- `Using Requester Pays buckets for storage transfers and usage <https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html>`_
- `Share Your AWS S3 Private Content With Others, Without Making It Public <https://dev.to/idrisrampurawala/share-your-aws-s3-private-content-with-others-without-making-it-public-4k59>`_
- `AWS CloudFront Using signed URLs <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-urls.html>`_
