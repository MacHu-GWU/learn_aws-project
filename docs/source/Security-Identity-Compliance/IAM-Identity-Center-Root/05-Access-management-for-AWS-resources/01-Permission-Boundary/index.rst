IAM Permission Boundary
==============================================================================


What is Permission Boundary
------------------------------------------------------------------------------
下面这段是官方文档的描述:

    AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries.

简单来说它主要是为了防范 cascade access, 避免一个 IAM Entity 自己没有某些权限, 但是它能创建一些有这些权限的 IAM Entity, 从而间接的获得这些权限. Permission boundary 定义了它能管理的最大权限. 有很多公司的安全规范是要求所有的 IAM Entities 都有 Permission Boundary 的, 这样可以避免一些不必要的风险.

- `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_
