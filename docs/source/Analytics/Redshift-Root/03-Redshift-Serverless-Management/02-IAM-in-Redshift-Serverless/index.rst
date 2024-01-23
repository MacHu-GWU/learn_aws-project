IAM in Redshift Serverless
==============================================================================
Keywords: AWS, Amazon, Redshift, Serverless, sls.


Granting permissions to Amazon Redshift Serverless
------------------------------------------------------------------------------
如果 RSSLS 需要访问其他 AWS 资源 (例如 Lambda), 那么你需要 Namespace 配置 IAM Role. Workgroup 是没有 IAM Role 的. 这很好理解. Namespace 管理的是底层的数据库, 数据表, User. 当然权限要跟着 Namespace 走了. WorkGroup 更像是一个查询的执行引擎. 你把 Namespace 灵活的插拔到不同的 WorkGroup 上, 这个权限应该是不变的. 而如果你把权限跟着 WorkGroup 走, 岂不是很容易乱套了.

.. note::

    这里的 Principal 是 Amazon Redshift Serverless.

Namespace 的 IAM Role 的 Trusted Entity Document 长这样:

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "redshift.amazonaws.com",
                        "redshift-serverless.amazonaws.com",
                        "sagemaker.amazonaws.com"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


Ref:

- `Identity and access management in Amazon Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-iam.html>`_


Managing access to Amazon Redshift Serverless database objects with database-role permissions
--------------------------------------------------------------------------------------------------
当开发者或是 EC2 Lambda 一类的计算资源调用 API 以一个 Database User 的形式连接到 Redshift 后运行 Query 时, 你希望限定它对 Redshift 对象, 例如 Database, Table 的操作权限 (Select, Update, Delete) 等. 传统做法是管理员用在数据库中创建 User, 并定义这个 User 的权限. 你也可以创建 User Group, 然后把 User 放到这个 Group 中, 然后定义这个 Group 的权限. 然后开发者用 SQL client + host + port + user + password 连接到 Redshift, 然后执行 SQL. 这种方式的缺点你需要把账号密码登信息显式的给开发者, 造成了管理密码的麻烦. 并且随着开发者人数增加, 权限管理复杂, 管理员的工作会变得很多.

AWS 的解决方案是这样的. 管理员在 Redshift Serverless 可以创建一个 Role (不是 IAM Role, 是 DB Role 是一个 DB 对象). 然后定义这个 Role 的权限. 然后你可以创建一个 IAM User (给人用) 或是 Role (给机器用), 然后给这个 Principal 一些例如 ``AmazonRedshiftReadOnlyAccess``, ``sqlworkbench:ListDatabases``, ``sqlworkbench:UpdateConnection`` 的权限. **最重要的**, 给这个 Principal 一个 AWS Resource Tag, key 是 ``RedshiftDbRoles``, 而 Value 则是在 DB 中创建的 Role 的名字. 这样这个 Principal sign in AWS Console 之后, 就可以用 Query Editor sign in. 然后 Query Editor 会自动创建临时的 DB User 以及 Connection, 并且绑定跟 DB Role 一致的权限. 这样做的好处是无需显式的给开发者密码, 并且通过 Tag 来 Match 对应的权限在用户很多的时候能打打减少工作量.

Ref:

- `Managing access to Amazon Redshift Serverless database objects with database-role permissions <https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-iam.html#serverless-iam-credentials-use-case>`_

.. note::

    这里的 Principal 是能 Sign in Console 的开发者, 是人类, 不是 EC2 Lambda 一类的计算资源.
