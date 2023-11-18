AWS Systems Manager Parameter Store
==============================================================================
Keywords: AWS, Amazon, System, Systems, SSM, Parameter Store


Overview
------------------------------------------------------------------------------
App 开发和部署的过程中使用配置文件是很常见的模式. 而配置文件中可能会包含一些敏感的信息例如 IP 地址, 密码. 那么如何安全地保存和访问配置数据就是一个很关键的问题.

AWS Parameter Store 是一个 **免费的** 用于管理配置数据的云服务 (Parameter 是参数的意思, 你可以理解为 Config). 简单来说就是你将配置数据储存在 Parameter Store 中, 并用 AWS 来管理权限, 然后你的应用程序可以通过 AWS SDK 来访问这些配置数据.

这里有必要说明一下, AWS Secret Manager 是一个更高级的用于管理敏感数据的服务, 它和 Parameter Store 的核心差异是支持密码自动rotation 以及使用 Resource Policy 来控制访问权限. 对于 90% 的开发情况, Parameter Store 已经足够了.


Managing parameter tiers
------------------------------------------------------------------------------
你创建 Parameter 的时候, 在 API 中你需要指定 tier. AWS parameter store 有两个 tier, 分别是 Standard 和 Advanced.

- Standard: 免费, 最多创建 10k 个, 最大 4kb
- Advanced: 收费 (每个每月 0.05$), 最多创建 100k 个, 最大 8kb

还有一个 tier 叫 Intelligent-Tiering, 它会自动创建 Standard tier, 然后在需要的时候 (Standard tier 的 parameter 数量达到了 10k, 或是大小超过了 4KB) 时候自动转换成 Advanced tier.

Reference:

- `Managing parameter tiers <https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-advanced-parameters.html>`_


Version and Label
------------------------------------------------------------------------------
**Version**

每当你 Update (本质上是 Put) 一个 Parameter 的时候, 他会自动创建一个新的 Version. 而你在 Get Parameter 的时候, 如果没有指定 version, 则默认 get 最新的. 如果指定了 selector, 也就是在 API 中使用了 ``Name="${name}:${version}"`` 这样的形式, 则会 get 指定 version. Version 是从 1, 2, 3, ... 自动递增的, AWS 只会保留最新的 100 个版本. 这里有个小坑, 如果你 Update parameter 的时候其实无论是配置还是 Value 都没有变化, 但是 AWS 还是会为你创建一个新的 Version, 这样在你连续部署实验的时候可能会创建许多无用的 Version, 为了避免这一问题, 我建议使用 `pysecret <https://pypi.org/project/pysecret/>`_ 库, 它能自动检测是否有变化, 如果没有变化则不会 Update.

**Label**

你可以对指定的 Version 使用 ``label_parameter_version`` API 来给指定 Version 一个或多个 labels. 这个 label 说白了跟 Lambda Function 中的 alias 类似, 就是一个指向特定 version 的 人类可读的 pointer. 一个 Label 在一个 Parameter 中的所有不同的 version 中只能 attach 到一个 version, 换言之, 一个 Label 只能指向一个 version. 你如果之前有一个 label 已经 attach 到一个 version 了,  然后你又要 attach 到另一个 version, 那么旧的那个 version 会自动失去这个 label. 类似地, 你可以再 Get Parameter 的时候在 API 使用 ``Name="${name}:${label}"`` 这样的形式来 get 特定 label 的 version.


Parameter Policy
------------------------------------------------------------------------------
Parameter Policy 是一项用来管理 Parameter life cycle 的高阶功能. 只在 Advanced tier 中有效. 注意, 它跟很多其他的 AWS Resource Policy 不同 (例如 S3), 它不是用来管理访问权限的.

它支持三种类型的 Policy:

- Expiration: 管理什么时候自动删除 Parameter.
- ExpirationNotification: 在过期之前的多少天自动发 Notification.
- NoChangeNotification: 在多少天内 Parameter 如果没有发生变化就发送 Notification.

可以看出, 这个的本质其实就是个定时任务, 完全可以用免费的 Standard tier + Lambda Function 来自己实现以及精细化控制. 不过考虑到维护 Lambda 要时间成本, 以及运行 Lambda 要钱 (虽然很少), 还是直接使用 Advance Tier + Parameter Policy 要来的轻松.


Parameter Hierarchies
------------------------------------------------------------------------------
Parameter name 可以用类似于 Linux 路径的 ``/folder1/folder2/folder3/name`` 的形式. 然后 AWS 提供了一个 `get_parameter_by_path <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html>`_ 的 API 可以根据前缀列出所有共享一个前缀的 Parameter, 便于管理.


pysecret Python Library
------------------------------------------------------------------------------
`pysecret <https://pypi.org/project/pysecret/>`_ 是一个能让你用更直观, 更简洁的 API 使用 AWS Parameter Store 的 Python 库. 如果你使用 Python 开发, 那么 pysecret 是一个不错的选择.

具体用法: https://github.com/MacHu-GWU/pysecret-project/blob/master/examples/04-AWS-Parameter-Store.ipynb


Reference
------------------------------------------------------------------------------
- `AWS Systems Manager Parameter Store <https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html>`_
- `AWS System Manager Pricing <https://aws.amazon.com/systems-manager/pricing/>`_
