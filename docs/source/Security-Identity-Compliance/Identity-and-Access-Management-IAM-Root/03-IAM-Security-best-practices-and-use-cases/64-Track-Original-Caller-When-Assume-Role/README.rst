Track Original Caller When Assume Role
==============================================================================
使用 AWS CloudTrail 来 audit 所有的 AWS API 调用历史记录是企业中常见的需求. 不过这里有一个坑.

当 account-a 上的 IAM User assume 了 account-b 上的 IAM Role 时, cloudtrail 日志中你看到的 ``userIdentity`` 的 arn 是 account-b 上的 IAM Role 的 ARN, 而不是 account-a 上的 IAM User 的 ARN. 而你只有通过 ``accessKeyId`` field 中的值, 并且定位到之前 IAM User console login 或 api authentication 的 cloudtrail event 里的 ``accessKeyId``, 才能找到真正的 caller (也就是 account-a IAM User) 的 arn.

在 2019 年, 我已经做了实验, 并联系 AWS 客服验证了, 目前 cloudtrail 不原生支持完美溯源.

AWS 客服推荐通过用 Cloudtrail Log S3 Put object event trigger 一个 AWS Lambda 对日志进行处理, 然后将 account-a 上的 用户的 ID 和 accessKeyId 连接起来存在 dynamodb 中, 这样才能确保能追溯到原来真正的用户.

现在已经是 2024 年了, 我没有对这点做进一步的验证.
