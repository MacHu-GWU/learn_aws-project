Amazon IAM Concepts
==============================================================================
Keywords: AWS, IAM, Concept, Concepts

`How IAM works <https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html#intro-structure-terms>`_ 这篇官方文档详细的介绍了 IAM 中的所有概念. 本文对这篇文档进行了提炼和简化, 以便于理解和记忆.


Terms
------------------------------------------------------------------------------
- IAM Resource: IAM 服务下的 AWS 资源.
    - user: 代表一个给人类使用, 可以登录的用户, 每个 user 会 attach policy 以定义他们的权限.
    - group: 代表用户的组, 每个 group 会 attach policy 以定义他们的权限. 所有在这个 group 下的 user 会继承这个 group 的权限.
    - role: 代表一个给机器使用的 role. 每个 role 会 attach policy 以定义他们的权限.
    - policy: 详细定义了权限, 用类似 JSON 文档的语法来描述 谁, 可以对什么, 做什么.
    - identity-provider object
- IAM Entity: IAM 服务下可以进行 auth 这个动作的一个实体.
    - user: 上面说过了
    - role: 上面说过了
- IAM Identity

.. image:: https://docs.aws.amazon.com/images/IAM/latest/UserGuide/images/iam-terms-2.png

- Principals: "谁, 可以对什么, 做什么" 里的 "谁". 可以是一个 User, 一个 Role, 一个 Account.
- Human users
- Workload


Principal
------------------------------------------------------------------------------
"谁, 可以对什么, 做什么" 里的 "谁". 可以是一个 User, 一个 Role, 一个 Account.


Request
------------------------------------------------------------------------------
"谁, 可以对什么, 做什么" 里的 "做什么" 发生时, 本质上是对 AWS 发起一个 API request.

- Actions or operations
- Resources
- Principal
- Environment data: 关于这个 "谁" 的一些 metadata, 例如 IP 地址, user agent, 当前时间等.
- Resource data: 关于这个 "可以对什么" 里的 "什么" 的一些 metadata, 例如 tag.


Authentication
------------------------------------------------------------------------------
验证身份, 证明发起请求的这个 Principal 是 "谁".


Authorization
------------------------------------------------------------------------------
验证权限, 检查这个 Principal 是否有某个权限做某件事.


Actions or operations
------------------------------------------------------------------------------
这个 Request 的动作会有一个唯一的 ID, 例如 ``s3:PutObject``.


Resources
------------------------------------------------------------------------------
"谁, 可以对什么, 做什么" 里的 "可以对什么" 里的 "什么".


Additional Concepts
------------------------------------------------------------------------------
- `Permission Boundary <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_: 是一个高级应用, 作用于 IAM User 和 IAM Role, 决定了这个用户的最大权限. 如果没有这个设定, 例如 IAM User 如果被禁止删除 S3, 但是允许创建 IAM, 那么这个用户可以创建一个可以删除 S3 的 Role 然后删除之. 这个叫做 Cascade Update. 设置了 Permission Boundary 可以避免这种情况.
- `Resource Policy <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html>`_: 比如 S3, SQS, Glue Catalog 等资源都可以设置 Resource 级别的 Policy 作为 IAM 的补充. 简单来说 IAM 决定了用户可以做哪些事, Resource Policy 决定了哪些用户可以对自己做哪些事.
- `Organization Service Control Policy (SCP) <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html>`_: 是一个组织对整个账户进行的限制. 你可以理解为一个对 Account 中所有的 IAM entity 生效的 permission boundary.
- `Session Policy <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session>`_: 你在创建一个 Session 的时候可以指定它的 Policy. 这个 Policy 必须比创建 Session 时的权限要小. 这有助于你用一个 Role 创建很多 session 给第三方使用.
- `Access Control List (ACL) <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_acl>`_: 它和 Resource Policy 很类似, 主要是 attach 在 resource 上用白名单黑名单, 正则匹配来决定谁可以访问自己, 能进行什么操作. 只不过 ACL 一般是 XML, 而不是 JSON.


Summary
------------------------------------------------------------------------------
对于权限管理来说, 最核心的就是三个东西 "Principal", "Resource", "Action", 分别对应了 "谁, 可以对什么, 做什么".

在 IAM 中, Principal 可以是 Account, User, Role. Resource 可以是任何 AWS 资源, Action 会有一个具体的 Id, 例如 ``s3:PutObject``. 而 Action 是可以被 Allow 和 Deny. IAM 的本质就是对这三个东西的排列组合.

除此之外, 还有一些其他概念例如 IAM Permission Boundary, Organizations SCP, Session Policy, Resource Policy, ACL 都会决定最终的权限. 不过只要我们对核心的三个概念有了深刻的理解, 理解这些概念如何能决定最终权限是非常容易的.
