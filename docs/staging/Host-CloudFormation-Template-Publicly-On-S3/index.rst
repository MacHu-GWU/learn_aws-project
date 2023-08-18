Host CloudFormation Template Publicly On S3
==============================================================================


介绍
------------------------------------------------------------------------------
CloudFormation 是非常强大的 IAC 工具. 你可以将成熟的, 参数化的 CloudFormation Template (CFT) 打包成易用的用户产品, 让你的用户无需安装任何工具, 只需要一个浏览器和几下点击就能使用你的 CFT.

这里有一个例子, `AWS Neptune 图数据库官方将用于启动数据库集群的 CFT Host 在了一个 Public S3 Bucket <https://docs.aws.amazon.com/neptune/latest/userguide/get-started-cfn-create.html>`_ 上, 然后用户点击链接即可跳转到 AWS CloudFormation Console 并使用该 CFT, 用户只需要填入参数即可. 这个 URL 的格式是 ``https://${aws_region}.console.aws.amazon.com/cloudformation/home?region=${aws_region}#/stacks/create?stackName=${stack_name}&templateURL=https://${bucket}.s3.amazonaws.com/v2/${key}``. 其中 ``${aws_region}`` 是用户想要部署到的 AWS Region, ``${stack_name}`` 是用户想要给这个 CFT 起的名字, ``${bucket}`` 是存放 CFT 的 S3 Bucket 名字, ``${key}`` 是 CFT 的文件名.


用 CFT 来 Deliver
------------------------------------------------------------------------------
你可以将 CFT Host 在 Public 的 S3 Bucket 上, 然后用上一节介绍的链接格式给用户点击使用 CFT. 你还可以启用 Requester Pay, IP based Bucket Policy, IAM Bucket Policy 来限制特定的人访问, 以及防止 DDOS 攻击造成大量 Bill.

这是一件潜力无限的事情. 例如你可以用 CFT 来 deliver 你的产品. 这样你就无需为 delivery 搭建专用的软件, 而是用 CFT 这种轻量的方式. 例如, 你可以要用户点击链接使用你的 CFT, 并且让用户在启动 CFT 的时候输入它购买你的服务时你给他的 Token. 你的 CFT 里在开始阶段会在用户的 AWS Account 中创建 Lambda Function, 然后你的 CFT 会把这个 Token 发给 Lambda Function, 这个 Lambda Function 就可以做几乎任何自定义的事情. 例如, 你给用户的产品需要一个 API Key, 而这个 API Key 在部署 CFT 的时候用户并不知道, 这个 Lambda Function 可以把 Token 传递给你公司 SAAS 平台的 API 服务来鉴权, 并返回一个 API Key. 然后用户才能继续后续的部署. 由于 CFT 里面可以在运行到一半时调用 Lambda Function, 你几乎可以做到任何事.


Reference
------------------------------------------------------------------------------
- `AWS Lambda-backed custom resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources-lambda.html>`_
