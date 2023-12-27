.. _implement-assume-role-correctly:

Implement Assume Role Correctly
==============================================================================
在 AWS 的最佳实践中, 是不推荐为管理员以外的人创建 IAM User 的. 而是推荐用 Assumed Role 来管理 cross account 的权限. 创建一个可以被 Assumed 的 IAM Role 时要制定指定谁可以 Assume 这个 Role. 这里有一些常见的操作可能会导致安全隐患. 本文来介绍一下这些常见错误以及正确的做法.

假设你需要用在 ``aws-account-a`` 上的 IAM User Assume ``aws-account-b`` 上的 IAM Role, 有两种方式可以控制这一权限.

1. 为 IAM User ``arn:aws:iam::aws-account-a:user/alice`` 添加 inline policy. 指定他可以 Assume 的 Role.

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": [
                    "arn:aws:iam::aws-account-b:role/my-assumed-role"
                ]
            }
        ]
    }

2. 为 IAM Role ``arn:aws:iam::aws-account-b:role/my-assumed-role`` 的 trusted entity 指定 Principal. 指定谁可以 Assume 这个 Role. 在 ``Principal`` 里你可以用 ``arn:aws:iam::aws-account-a:root`` 来给允许来自于 ``aws-account-a`` 下的所有 Group, User, Role 的访问. 也可以用 ``arn:aws:iam::aws-account-a:group/...``, ``arn:aws:iam::aws-account-a:user/...``, ``arn:aws:iam::aws-account-a:role/...`` 这样的形式显式指定 **谁** 可以 assume 这个 Role. 根据 `这篇官方文档 <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns>`_, root 常用于 Resource Based Policy, 例如 S3 Bucket Policy. 我们这里是 Assume Role, 不是一个 Resource Based Policy, 所以一般不要用 root 作为 principal.

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam::aws-account-a:user/alice"
                    ]
                },
                "Action": "sts:AssumeRole",
                "Condition": {}
            }
        ]
    }

3. 注意不要给在 ``aws-account-b`` 上用于 assume 的 role 任何 IAM Management 权限 (CloudFormation 除外, 但你也要用 resource regex 来进行限制). 因为这样可能会导致 A assume 了 B 上的一个 role, 然后用这个 role 修改 IAM 权限给自己更多的权限, 这样就可以跳过 B 上的 role 的权限限制从而可以进行破坏了. 这个事情可以用 Permission Boundary 来实现.

Reference:

- `Using IAM roles
 <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_
- `How do I assume an IAM role using the AWS CLI? <https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/>`_
- `cross_aws_account_iam_role <https://github.com/MacHu-GWU/cross_aws_account_iam_role-project>`_: Python library - Setup cross AWS account IAM permission made easy