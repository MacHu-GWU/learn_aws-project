Connect To Redshift in Python
==============================================================================
Keywords: AWS, Amazon, Redshift, Connect


How it Works
------------------------------------------------------------------------------
首先我们来了解一下用 Python 跟 Redshift 通信的原理.

首先我们回顾一下用 GUI 工具, 连接到数据库的原理. 我们以 DBeaver (免费的数据库 GUI) 为例. 一般对于不同的数据库你需要一个 Driver, Driver 定义了跟特定数据库通信的接口. 而 Redshift 本质上是一个数据库, 它当然也需要一个 Driver. 如果你用 DBeaver 连接 Redshift, 你会看到提示让你下载 Driver.

我们再来看用 Python 连接到数据库的原理. Python 中有一个标准, `PEP 249 – Python Database API Specification v2.0 <https://peps.python.org/pep-0249/>`_, 如果你要用 Python 实现一个数据库 Driver, 你就必须符合这个标准. 这使得不同的数据库的 Driver 的 API 接口都是类似的. 而 Redshift 是一个数据库, 当然 Redshift Python Driver 也得符合这个标准.

AWS 官方维护着一个叫 `redshift_connector <https://pypi.org/project/redshift-connector/>`_ 的 Python 库. 这个库就是官方的 Redshift Driver. 你看到的任何第三方库, 例如 awswrangler, sqlalchemy-redshift, 本质上都是对 redshift-connector 所创建的 connection 的封装.


Use Username Password or IAM
------------------------------------------------------------------------------
AWS 提供了两种鉴权方式:

1. 在数据库中创建 Database User (以及 password), 然后用 host, port, database, user, pass 的方式创建 DBApi2.0 connection.
2. 使用 IAM Role, 本质上是用你的 IAM Principal 创建临时的 User / Pass (过一段时间后会失效), 然后创建 DBApi2.0 connection. 有这么几个 API 可以获得临时的 credential:
    - `redshift_client.get_cluster_credentials <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_cluster_credentials.html>`_: 这是给 Provisioned cluster 模式用的. 这个 API 需要显式创建一个临时的 DB user / password.
    - `redshift_client.get_cluster_credentials_with_iam <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/get_cluster_credentials_with_iam.html>`_: 这是给  Provisioned cluster 模式用的, 你无法指定 DB user, user 是跟你的 IAM Principal 1:1 绑定的.
    - `redshift_serverless_client.get_credentials <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/client/get_credentials.html>`_: 这是给 Serverless 模式用的, 你无法指定 DB user, user 是跟你的 IAM Principal 1:1 绑定的.

在 Redshift 产品早期, 你只能用 #1. 这就涉及到你需要用 Secret Manager 来保存密码并定期用 Lambda Rotate. 这比较的麻烦. 目前 (2024 年) 基本上你可以无脑使用 #2 的方式. 临时的 Credential 永远会更安全. 不过要注意的是 #2 用的是临时 Credential, 最大持续时间是 1 小时. 对于长时间运行的 App 你可能需要 Refresh Credential. 不过这个很好实现.


Redshift Data API
------------------------------------------------------------------------------
Data API 是云原生产品的一大优势. AWS 允许你用 Rest API 异步执行 Query, 而无需创建连接. 这种做法超级超级方便. 非常适合用来写长期运行的 App 程序, 或是将其封装为 App 给最终用户使用.

- `Redshift Data API boto3 document <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-data.html>`_


Trouble Shoot
------------------------------------------------------------------------------
1. 注意你的 Cluster 或 WorkGroup 的 Security Group 白名单里有你的 IP 地址.
2. 如果你的网络不是在 VPC 中的, 注意你的 Cluster 是否开启了 Public Access.


Sample Code
------------------------------------------------------------------------------
这里我把用多种方法连接到 Redshift 并进行简单的 CRUD 操作的代码封装成了一个简单的库, 方便以后调用.

- `pylib <https://github.com/MacHu-GWU/learn_aws-project/tree/main/docs/source/Analytics/Redshift-Root/06-Redshift-Code-Recipe/02-Connect-To-Redshift-in-Python/pylib>`_

.. dropdown:: test_create_connect_for_serverless_using_iam.py

    .. literalinclude:: ./test_create_connect_for_serverless_using_iam.py
       :language: python
       :linenos:

.. dropdown:: test_create_sqlalchemy_engine_for_serverless_using_iam.py

    .. literalinclude:: ./test_create_sqlalchemy_engine_for_serverless_using_iam.py
       :language: python
       :linenos:

.. dropdown:: test_create_connect_for_cluster_using_iam.py

    .. literalinclude:: ./test_create_connect_for_cluster_using_iam.py
       :language: python
       :linenos:

.. dropdown:: test_create_sqlalchemy_engine_for_cluster_using_iam.py

    .. literalinclude:: ./test_create_sqlalchemy_engine_for_cluster_using_iam.py
       :language: python
       :linenos:

.. dropdown:: test_work_with_awswrangler.py

    .. literalinclude:: ./test_work_with_awswrangler.py
       :language: python
       :linenos:
