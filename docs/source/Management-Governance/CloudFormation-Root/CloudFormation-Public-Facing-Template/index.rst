CloudFormation Public Facing Template
==============================================================================
Keywords: AWS, Amazon, CloudFormation

如果你是一个企业, 出售部署在 AWS 上的 Solution, 那么最佳的部署方式就是用 CloudFormation. 你可以把你的 CloudFormation Template 放在一个 Public Facing 的 S3 bucket 上, 然后把下面的 URL 放在你的公司网站上, 用户一点就自动打开 CloudFormation 的 Console 来部署你的 Solution 了. 这个页面是 Create 的第一步, 第二步就是填写参数.

这里有这么几个参数:

- aws_region: 用户要把这个 solution 部署到哪个 region
- stack_name: 用户创建的 stack 的名字
- s3_bucket: 你的 CFN 的 S3 bucket
- s3_key: 你的 CFN 的 S3 Key

.. code-block::

    https://{aws_region}.console.aws.amazon.com/cloudformation/home?region={aws_region}#/stacks/create?stackName={stack_name}&templateURL=https://{s3_bucket}.s3.amazonaws.com/{s3_key}

更高阶的做法是直接跳过第一步, 直接到填参数的页面. 参数的默认值用 ``&param_{ParameterName}={ParamaterValue}`` 的形式放在 URL 里. 这个 URL 的格式是这样的:

.. code-block::

    https://{aws_region}.console.aws.amazon.com/cloudformation/home?region={aws_region}#/stacks/create/review?stackName={stack_name}&templateURL=https://{s3_bucket}.s3.amazonaws.com/{s3_key}&param_MyParameterName=MyParameterValue

Reference:

- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stacks-quick-create-links.html
