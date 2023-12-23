Deploy Lambda with AWS CDK
==============================================================================
Keywords: Amazon, AWS, Lambda, CDK, Alias, Version


Overview
------------------------------------------------------------------------------
Deploy Lambda 的工具有很多, 有官方的 `SAM (AWS Serverless Application Model) <https://aws.amazon.com/serverless/sam/>`_, `Chalice (Python Serverless Microframework for AWS) <https://github.com/aws/chalice>`_, `AWS CDK <https://aws.amazon.com/cdk/>`_ 等等. 原生的 CDK 可能是受众最广的方法之一. 本文将介绍如何使用 CDK 部署 Lambda.

在使用 CDK 部署 Lambda 进行开发测试很容易, 但一涉及到生产环境的 blue / green, canary deployment, rollback 等操的时候就不那么容易作对了. 本文分享了我在使用 CDK 部署 Lambda 到生产环境中踩过的坑和一些经验.


How Lambda Version and Alias Works in AWS CDK
------------------------------------------------------------------------------
这里有个非常 Tricky 的坑. 在对 production 进行部署的时候, 遵循 blue/green 或是 canary 的最佳实践, 当我们希望每次更新 Lambda 的时候, 如果代码和 Configuration 有变化, 则 publish 一个 new version, 然后将 Alias 指向这个 version. 如果 Configuration 没变化, 则既不 publish version, 也不更新 Alias. 那在 CDK 中要怎么实现呢?

根据直觉, 我们可能会考虑使用 `aws_cdk.aws_lambda.Version <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Version.html>`_ 这一 Construct. 但你会在官方文档看到这样一段话 **"Avoid using this resource directly. ... If you use the Version resource directly, you are responsible for making sure it is invalidated (by changing its logical ID) whenever necessary."** 根据字面意思, 你不应该手动使用这个, 除非你能确保自己 changing logic id. 这是什么意思呢? 我们来看一个例子:

.. code-block:: python

    import aws_cdk as cdk
    import aws_cdk.aws_lambda as lambda_

    class Stack(cdk.Stack):
        def __init__(self, ...)
            self.lbd_func = lambda_.Function(
                self,
                "MyLambdaFunction",
                ...
            )
            self.lbd_version = lambda_.Version(
                self,
                "MyLambdaFunctionVersion",
                ...
                lambda_=self.lbd_func,
                removal_policy=cdk.RemovalPolicy.RETAIN,
            )

凭直觉, 很多人会写出这样的代码. 创建一个指向 lbd_func 的 version, 并且指定 removal_policy = RETAIN, 使得在更新的时候依然保留这个 version (毕竟发布新版本时不保留旧版本就无法回滚了, 失去了版本管理的意义了). **但是你实际操作就会发现, 每次你更新代码的时候, 你的旧 Version 还是被删除了, removal_policy 没有起作用**. 这是为什么呢?

这是因为你定义 ``self.lbd_version`` 的时候给这个 resource 的 logic id 是 ``MyLambdaFunctionVersion``. 当 Version 的内容发生变化时, CDK 在对一个 resource 进行更新时会采用先删除再创建, 或是先创建再删除. 并不存在创建但不删除这一情况, 因为这个操作的本质是 update 而不是 remove, 所以 remove policy 自然不会生效了. 而之所以这个操作被视为 update 是因为 logic id 没有变化. 而要手动实现这一点的正确做法如下 (注意, 该方法只是用来说明原理, 官方有更推荐, 更优雅的实现):

.. code-block:: python

    import aws_cdk as cdk
    import aws_cdk.aws_lambda as lambda_

    class Stack(cdk.Stack):
        def __init__(self, ...)
            self.lbd_func = lambda_.Function(
                self,
                "MyLambdaFunction",
                ...
            )

            # call API to figure out what is the last published version
            # this example won't work, it is just for demonstration
            last_published_version = boto3.client("lambda").list_versions_by_function(...)
            next_version = last_published_version + 1

            self.lbd_version = lambda_.Version(
                self,
                f"MyLambdaFunctionVersion{next_version}",
                ...
                lambda_=self.lbd_func,
                removal_policy=cdk.RemovalPolicy.RETAIN,
            )

这种实现方式的原理正对应了官方文档中的 "you are responsible for making sure it is invalidated (by changing its logical ID) whenever necessary.". 因为这样做每次其实是创建了一个新的 Resource, 因为 logic id 变了. 这时 CDK 才会删除原来的 Resource 同时 retain 旧的 Version, 并创建一个新的 Version. 这里的关键是我们手动计算出了新的 version 数字, 并且用它构建了 logic id.

**好了, 我们来看看前面提到的 "更加优雅的方法是什么"**. 通常我们不会单独使用 Version, 而是将其和 Alias 一起使用. 你当然可以创建一个 ``aws_cdk.aws_lambda.Alias <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Alias.html>`_, 并将其指向 ``self.lbd_version``. 但是官方提供了更优雅的方法:

.. code-block:: python

    import aws_cdk as cdk
    import aws_cdk.aws_lambda as lambda_

    class Stack(cdk.Stack):
        def __init__(self, ...)
            self.lbd_func = lambda_.Function(
                self,
                "MyLambdaFunction",
                current_version_options=lambda_.VersionOptions(
                    removal_policy=cdk.RemovalPolicy.RETAIN,
                    retry_attempts=1,
                ),
                ...
            )

            self.lbd_func_alias = lambda_.Alias(
                self,
                "AliasLive",
                alias_name="LIVE",
                version=self.lbd_func.current_version,
            )

在这个方法里的关键是指定了 ``current_version_options``, 它定义了每当你引用 ``self.lbd_func.current_version`` 这个 property 属性时, 如何自动创建 Version. 我们规定了每次创建新的 Version 的时候 retain 旧 Version. 其实这一个属性就等效于上面的例子中的一堆代码. 然后我们定义了一个 Alias, 引用了这个被自动创建的新 Version.


Deploy Lambda Version and Alias with AWS CDK
------------------------------------------------------------------------------
Version 和 Alias 是实现 Blue / Green deployment, Canary deployment, Version Rollback 等功能的核心. 这里我们不对其进行介绍, 我们假设你已经充分了解了它的原理. 我们重点介绍如何使用 CDK 来实现用 Version 和 Alias 来进行版本管理.

首先我们要明确需求. 通常我们会将 app 按顺序发布到多个 environment (环境) 中进行充分测试后最后再到 production. 而在不同的环境下我们的部署策略可能是不同的. 我们假设有四个环境, sbx (sandbox), tst (test), stg (staging), prd (production), 其中 sbx 用于开发, tst 用于端到端测试, stg 用于使用和 prd 一样的数据进行测试, prd 用于生产. 下面是我们的部署策略的简化版本, 用于描述我们的目标. 这里面还有很多具体细节, 之后再详细解释:

1. **💻 Dev 设置**: 在 sbx, tst, 我们的主要目的是确保最新的代码能够正常运行, 所以我们会部署最新的代码到 $LATEST, 并且不发布新版本. 因为 sbx, tst 中的代码变更频率极高, 没有必要每次占用存储空间发布新版本, 就用 $LATEST 就好. 而 LIVE alias 也指向 $LATEST.
2. **🚀 Production 设置**: 在 stg, prd, 我们的主要目的是在 stg 中复现 prd 的情况, 而 prd 的 LIVE alias 一般不会指向 $LATEST, 因为 $LATEST 是 mutable 的, 所以我们一般会指向一个 immutable 的 version. 所以 stg 中的情况也要跟 prd 进行同步. 不过我们会保留手动修改 ALIAS 指向历史版本.

**💻 Dev 设置**

在 Dev 模式下, 我们的默认都是使用最新代码部署, 也就是每次都 publish 都不创建 Version, 而 Alias 则是将指向 $LATEST. 而如果我们真的要 debug 一个历史版本, sbx, tst 环境是不保存历史版本的, 我们要么直接在 stg 中修改 Alias 指向旧版本然后进行 debug. 要么切换回历史版本所属的 Git Tag (这个 git tag 一般等于软件的 semantic version, 在部署的时候会一并保存在 environment variable 中), 然后拉一个 release branch 将其部署到 sbx, tst 中进行 debug.

**🚀 Production 设置**

在实际操作中, 我们的 API 通常会这么设计:

1. 自动化部署: 该 API 无需手动指定版本, 而是根据一定的规则自动计算出需不需要 publish version, alias 该怎么变化. 而这个规则取决于用户想要用 blue / green 还是 canary. 该 API 适用于日常发布.
2. 手动指定: 该 API 可以允许用户指定 version1, version2 (optional), version2_weight (optional). 该 API 适用于版本回滚.

我们这里重点说一下 **自动化部署** 的规则. 这里我们假设是发布了新版本的情况 (lambda code 或 configuration 有变化的情况), 如果没有变化则既不会 publish version 也不需要更新 alias.

如果是 **🔵🟢 blue / green 部署**, 这种情况比较简单. 创建新版本, 并让 Alias 指向新版本即可.

如果是 **🐤 canary 部署**, 这种情况比较复杂. 首先我们要了解一个概念. 一个 Alias 如果只指向一个版本, 则视为 stable. 而如果同时指向两个版本, 则视为 transition, 处于过渡期. 这里我们定义一个 ``canary_increments`` 的概念, 它是一个整数数组, 例如 ``[25, 50, 75]``. 它的意思是当发布新版本时, 先只给新版本 25% 的流量, 然后增加到 50%, 75% 最后才给全部流量. 下面我们分情况讨论:

1. 目前 Alias 都不存在. 那么直接创建新 Version 并将 Alias 指向这个 Version.
2. 目前 Alias 存在, 且 stable. 那么这是一个新版本的发布, 则创建新 Version 并将 Alias 指向这个 Version.
3. 目前 Alias 存在, 处于 transition 状态. 那么这是一个流量增加的过程. 我们根据 ``canary_increments`` 的定义, 如果目前流量小于 25% 则提升到 25%, 小于 25% ~ 50% 则提升到 50%, 超过 75% 则提升到 100%.

对于 **手动指定** 的情况就没什么好说的, 通常这不涉及到创建新版本, 只是修改 Alias 的指向即可.

下面我们给出了一个简化后的我在生产环境在用的例子.

.. literalinclude:: app.py
   :language: python
   :linenos:

下面的 bash command 是我用来创建虚拟环境, 安装依赖, 执行部署所用的命令.

.. code-block:: bash

    # create virtualenv
    virtualenv -p python3.10 .venv

    # activate virtualenv
    source .venv/bin/activate

    # install dependencies
    pip install -r requirements.txt

    # deploy
    python cdk_deploy.py

    # delete
    python cdk_delete.py
