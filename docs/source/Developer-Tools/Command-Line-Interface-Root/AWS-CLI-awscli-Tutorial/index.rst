.. _aws-cli-tutorial:

AWS CLI Tutorial
==============================================================================
Keywords: aws cli


AWS CLI V1 vs V2
------------------------------------------------------------------------------
AWSCLI 早期是用 Python 写的并以一个 Python 包的形式存在 所以你需要安装 Python 然后 ``pip install awscli``. 而 V2 增加了很多新的功能, 其中最主要的是 auto-complete 以及 sso 登录. 而且 V2 是以一个独立的安装包形式存在, 它里面自带一个 Python 而不需要额外安装 Python 了.

我建议全面使用 V2 在日常工作中取代 V1.


Install or update the latest version of the AWS CLI
------------------------------------------------------------------------------
首先我们需要安装. 如果是 V1, 那么就在 Python 中 ``pip install awscli`` 即可. 而对于 V2, 则是参考 `官方文档 Install or update the latest version of the AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>`_ 的说明要么从系统级的包管理安装, 要么下载安装包安装.

**具体安装步骤**

- 安装 `aws cli version 2 <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>`_.
    - Linux: 请参考官方文档
    - MacOS: 用官方推荐的方式的好处是它把所有需要的依赖打包成 MacOS Package 了, 你删除也好删, 对全部用户有效. 不过你也可以到 GitHub 上 https://github.com/aws/aws-cli/tree/v2, 这个 v2 的 branch 下 pull Python 源码, 然后 pip install. 这样的好处是可以指定安装到哪个 Python 环境下.


Configure AWS CLI
------------------------------------------------------------------------------
本节内容来自于这篇 `官方文档 Configuration and credential file settings <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>`_.

安装完成之后, 你可以用 ``aws configure`` 命令来启动一个 wizard, 然后按照提示输入信息来进行配置, 也可以直接编辑 ``~/.aws/config`` 和 ``~/.aws/credentials`` 文件来进行配置. 对于新手建议用 ``aws configure`` 而我个人喜欢直接来进行配置以获得更好的控制.

- ``~/.aws/config``: 主要是配置不同的 AWS Profile.
- ``~/.aws/credentials``: 主要解决的是 credentials 相关的信息, 比如 ACCESS KEY, SESSION TOKEN 等.

**Configuration settings and precedence**

由于 AWS CLI 会从多个地方读取参数, 主要是哪些权限的参数, 当一个参数在多个地方同时存在时, 会按照如下的顺序优先使用靠前的值. 例如我们在输入 ``aws s3 ls`` 的时候, 并没有显式指定任何权限, 那么 cli 会按如下顺序搜索权限:

1. Common line option, such as ``--profile``
2. Environment Variable
3. CLI credential file: ``~/.aws/credentials``
4. CLI config file: ``~/.aws/config``
5. Container Credential: ECS IAM Role
6. Instance Profile Credential: EC2 IAM Role

**Reference**

- Environment variables to configure the AWS CLI, 可用的 环境变量: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
- Using an IAM role in the AWS CLI, 在 aws cli 中使用 IAM Role 而不是 IAM User: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html
- CLI Configuration: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html


AWS Single Sign On
------------------------------------------------------------------------------
**为什么在用 SSO 的企业中使用 AWS API 需要额外的配置?**

在大型企业中, 使用 AWS Account 的方式会和个人用户有很大不同. 企业雇员都有一个 邮箱 和 密码, 这套密码通常是由 Active Directory 提供的 (微软的一个企业雇员账号管理解决方案, 历史有 30 多年了). AWS Account 支持用企业的 账户登陆, 这样就可以让企业用户只用一套密码登陆所有系统了. 免除了管理多套密码的麻烦.

如果你要登录 AWS Console, 通常是登录企业的 SSO portal, 然后选择 AWS Account 进入.

但如果你需要使用 CLI 或是 API, 由于你每次登陆 AWS Account 后是用的一个随机生成的 IAM Role 以及临时的 Token, 企业是不会为你创建 IAM User 以及创建 Access Key Pair 的. 这就需要一些额外的步骤来解决这一问题.

**AWS 推荐的解决方案**

AWS 推荐安装 aws cli version 2 (pip install 的是 V1, 没有我们需要的 sso sign in 的功能). 之后你可以对其用 ``aws configure sso`` 进行简要配置, 输入企业的 SSO portal 的 URL. 然后为其创建一个 profile. 每次需要使用 AWS API 之前, 就可以用 ``aws sso login --profile ${your_profile_name}`` 登录, 此时会自动打开浏览器, 然后你用浏览器登录, CLI 会自动获得这个临时的 token 并对其进行缓存到 ``~/.aws/sso/cache`` 目录下. 之后你这个 profile 在一定时间内就是可使用的状态了.

下面给出了几个例子:

``~/.aws/config``

.. code-block:: yaml

    [profile my_profile]
    sso_start_url = https://yourcompanydomain.awsapps.com/start#/
    sso_region = us-east-1
    sso_account_id = 111122223333
    sso_role_name = my_role
    region = us-east-1
    output = json

``~/.aws/credentials``

.. code-block:: yaml

    [my_profile] # no need to put any content

Sample cli command: ``aws sso login --profile my_profile``.
