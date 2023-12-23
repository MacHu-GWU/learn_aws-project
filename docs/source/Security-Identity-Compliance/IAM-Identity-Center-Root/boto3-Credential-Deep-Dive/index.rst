boto3 Credential Deep Dive
==============================================================================
Keywords:


Overview
------------------------------------------------------------------------------
`AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>`_ 是给 Linux 运维设计的命令行程序, 而 `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html>`_ 是 AWS 的 Python SDK. 两者关于鉴权的部分有很多地方都是一样的.

当你深入使用之后, 你会发现这里面其实有很多细节.

- 例如你可能需要使用 "当前" 的 credential, 还可能要 assume 一个其他 AWS account 的 credential.
- 例如在不同的 runtime 下, 例如 Laptop 上, EC2 上, Lambda 中等环境下如何配置 credential.
- 如何使用环境变量来创建 boto session.
- 当环境变量和 ``~/.aws/credentials`` 冲突时到底哪个优先级更高.
- 如何显式的获得一个 boto session 的 Credential, 无论你是用的 IAM User 还是 IAM Role 还是 SSO.
- 如何为很多 AWS 的工具, 例如 AWS CLI, `AWS CDK <https://docs.aws.amazon.com/cdk/v2/guide/home.html>`_, `AWS SAM <https://aws.amazon.com/serverless/sam/>`_, `Terraform <https://www.terraform.io/>`_ 等等配置 credential.

本文详细的研究了这些问题, 希望把底层的工作原理彻底弄清楚, 以便以后使用时随时查阅.


Environment Variables
------------------------------------------------------------------------------
- ``AWS_PROFILE``: 指定使用哪个 local named profile. 如果指定了 ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_SESSION_TOKEN``, 那么显式提供的 credential 会覆盖 ``AWS_PROFILE`` 指定的 credential.
- ``AWS_ACCESS_KEY_ID``: 显式提供的 credential. 如果显式提供了, 则它有最高优先级. 这个 env var 常用于 IAM User 的 credential.
- ``AWS_SECRET_ACCESS_KEY``: 显式提供的 credential. 如果显式提供了, 则它有最高优先级. 这个 env var 常用于 IAM User 的 credential.
- ``AWS_SESSION_TOKEN``: 显式提供的 credential. 如果显式提供了, 则它有最高优先级. 这个 env var 常用于 IAM Role 的 credential.
- ``AWS_REGION`` / ``AWS_DEFAULT_REGION``: ``AWS_REGION`` 会覆盖 ``AWS_DEFAULT_REGION``.

Reference:

- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html


get_credentials vs get_session_token
------------------------------------------------------------------------------
在你创建了一个 ``boto_ses = boto3.session.Session()`` boto session 之后, 有两个跟 credential 相关的 API ``boto_ses.get_credentials()`` 和 ``boto_ses.client("sts").get_session_token()``. 我们这里对它们的功能做一下区分.

`get_credentials <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_credentials>`_ 这个 API 是从本地来 load 你的 credential, **其本身并不会去跟 AWS API 通信**, 仅仅是在本地的 ``${HOME}/.aws`` 文件夹, 环境变量, 或是 ``boto3.session.Session`` 对象的属性中去找. 例如你创建 boto session 的时候只指定了 profile 或是一个 IAM role, 并没有显示给与 credential, 而这个 api 会自动找到并获得最终的 credentials. 下面这个例子可以打印出获得的 credentials 的值.

.. code-block:: python

    import boto3

    boto_ses = boto3.session.Session()
    boto_ses.get_credentials()

    print(cred.access_key)
    print(cred.secret_key)
    print(cred.token)

`get_session_token <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_session_token.html>`_ 这个 API 只有两种用途.

1. 是一个 IAM User 的 IAM Principal 来获取 session token, 用于临时授权.
2. 二是一个 AWS Account 上的资源, 例如 AWS Account, EC2, Lambda, IAM 等获得临时权限.

如果目前的 IAM Principal 已经是一个用 token 创建的 session 了 (换言之这个 boto session 是由 #1 #2 所创建的), 则无法再次使用这个 API.

出于安全考虑, access_key, secret_key pair 合在一起是一个长期的 credential, 不适合直接使用. 为了安全 AWS 最终的鉴权都是用时效较短的 session + token 进行的, 前面的 credential 都是用来 authentication, 证明你是谁, 然后获取 token 来进行 authorization, 证明你有什么权限.

下面这个例子先用 IAM User 创建一个 session, 然后临时获得一套 token, 你可以用这套 token 创建一个新的 boto session, 用于后续的操作. 为了安全考虑, 这套 token 一般过期时间较短.

.. code-block:: python

    import boto3

    boto_ses = boto3.session.Session() # this is an IAM User

    res = boto_ses.client("sts").get_session_token()
    print(res["Credentials"]["AccessKeyId"])
    print(res["Credentials"]["SecretAccessKey"])
    print(res["Credentials"]["SessionToken"])


Test Script
------------------------------------------------------------------------------
下面我们用一个脚本来对各种情况进行测试, 深入研究不同情况下 ``get_credentials`` 和 ``get_session_token`` API 的行为. 在后面我们将实验条件和结果进行了总结.

.. literalinclude:: ./boto3_credential_deep_dive.py
   :language: python
   :linenos:


get_credentials - Default Profile
------------------------------------------------------------------------------
使用本地的 default AWS Profile. 是一个 IAM User.

结果:

    返回 access key 和 secret key, 没有 token


get_credentials - IAM User Profile
------------------------------------------------------------------------------
使用本地的 named AWS Profile. 是一个 IAM User.

结果:

    跟 "Default Profile" 的情形一样.


get_credentials - IAM Role Profile
------------------------------------------------------------------------------
使用本地的 named AWS Profile, 是一个需要被 IAM User (source profile) 来 assume 的 IAM Role.

.. code-block:: ini

    [profile assume_role_profile]
    region = us-east-1
    output = json
    role_arn = arn:aws:iam::123456789012:role/my_role_name
    source_profile = the_source_profile

结果:

    返回 access key 和 secret key, 以及 token. 跟用 source profile 创建 boto session, 然后调用 ``sts.assume_role()`` API 返回的 credential 一样.


get_credentials - SSO Profile
------------------------------------------------------------------------------
使用 SSO 登录后所创建的 AWS Profile.

结果:

    跟 "IAM Role Profile" 的情形一样.


get_credentials - EC2
------------------------------------------------------------------------------
在一个有 IAM Profile 的 EC2 Instance 上运行. (Lambda, ECS, Glue 以及任何能给给 IAM Role 的 runtime 都是一样的)

结果:

    返回 access key 和 secret key, 以及 token. 跟用 source profile 创建 boto session, 然后调用 ``sts.assume_role()`` API 返回的 credential 一样. 这个 principal 是一个 assumed role.


get_session_token - Default Profile
------------------------------------------------------------------------------
使用本地的 default AWS Profile. 是一个 IAM User.

结果:

    返回 access key 和 secret key 和 token, access key 跟原本的 IAM User 的不一样, 因为它是一个临时创建的 identity, 不是原来的 IAM User principal 了. 你可以用这些 credential 创建一个新的 boto session, 它跟原本的 IAM User 有着相同的权限.


get_session_token - IAM User Profile
------------------------------------------------------------------------------
使用本地的 named AWS Profile. 是一个 IAM User.

结果:

    跟 "Default Profile" 的情形一样.


get_session_token - IAM Role Profile
------------------------------------------------------------------------------
使用本地的 named AWS Profile, 是一个需要被 IAM User (source profile) 来 assume 的 IAM Role.

.. code-block:: ini

    [profile assume_role_profile]
    region = us-east-1
    output = json
    role_arn = arn:aws:iam::123456789012:role/my_role_name
    source_profile = the_source_profile

结果:

    根据官方文档 ``get_session_token`` API 是给 IAM User 或 AWS Account 来获取 session token, 用于临时授权. IAM Role 不能调用这个 API.


get_session_token - SSO Profile
------------------------------------------------------------------------------
使用 SSO 登录后所创建的 AWS Profile.

结果:

    跟 "IAM Role Profile" 的情形一样.


get_session_token - EC2
------------------------------------------------------------------------------
在一个有 IAM Profile 的 EC2 Instance 上运行. (Lambda, ECS, Glue 以及任何能给给 IAM Role 的 runtime 都是一样的)

结果:

    跟 "IAM Role Profile" 的情形一样.
