IAM Permission Boundary
==============================================================================
Keywords: AWS, IAM


What is Permission Boundary
------------------------------------------------------------------------------
下面这段是官方文档的描述:

    AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries.

简单来说它主要是为了防范 cascade access, 避免一个 IAM Entity 自己没有某些权限, 但是它能创建一些有这些权限的 IAM Entity, 从而间接的获得这些权限. Permission boundary 定义了它能管理的最大权限. 有很多公司的安全规范是要求所有的 IAM Entities 都有 Permission Boundary 的, 这样可以避免一些不必要的风险.

- `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_


Permission Boundary How it Works Explained
------------------------------------------------------------------------------
下面我来介绍一下 Permission Boundary 到底是如何工作的. 我们现在已经知道 Permission Boundary 的主要作用是, 防止某一个 IAM Principle 当他自己没有一些特定的权限的时候, 但如果这个 Principle 拥有 Create IAM Role 的权限, 那么他有可能就会通过创建一个新的 IAM Role 并且给 IAM Role更大的权限, 然后他去 Assume 这个 Role, 使得他间接的去获得那些他本不应该拥有的权限. 那么在这种情况下, 我们可以用 Permission Boundary 来阻止他.

现在我们快速的回顾一下 Permission Boundary 的基本原理. 你不管 IAM Principle 他自己的 Permission 有多少, 他的 Permission 永远是他的其他的 Permission 以及 Permission Boundary 的交集, 也就是把它合并在一起, 共同的部分. 如果 Permission Boundary 中没有某个权限但是 IAM Principle 本身有, 那么它依然不能做这件事.

现在我们考虑一个简单的例子, 一个 IAM User 有创建 IAM Role 的权限, 但是没有 S3 的权限. 我们要防止它操作 S3.

首先，我们需要了解一个常见的错误：在给用户配置 Permission Boundary 后，虽然可以限制其直接操作 S3，但当用户创建一个 role 时，Permission Boundary 并不会自动限制这个新创建的 role 的权限. 也就是说，如果用户创建了一个允许操作 S3 的 role 并自行 assume，该用户就能绕过原本对 S3 的访问限制. 这显然是不符合安全要求的.

为避免这种情况，Permission Boundary 必须不仅适用于用户本身，还需要应用到用户创建的每个 IAM role 上，才能有效限制权限扩展. 然而，如何强制要求用户在创建 role 时应用特定的 Permission Boundary 呢？

这就需要在用户的 Permission Boundary 中加入一个 Condition 条件，确保在执行 CreateRole 和 PutRolePolicy 操作时附加指定的 Permission Boundary. 具体来说，该条件要求当用户创建 role 时，必须将其自身的 Permission Boundary 绑定到新创建的 role 上，只有这样才能确保权限限制有效.

在这种设置下，用户在创建 role 时，如果没有将指定的 Permission Boundary 绑定到新创建的 role 上，就无法成功创建该 role，自然也无法 assume 它. 因此，关键在于，若要限制某个 IAM Principal 的权限范围，需要通过 Permission Boundary 强制其在创建新的 role 时附加特定的 Permission Boundary，从而防止权限提升. 这是实现安全控制的核心.

注意事项:

- 在使用 Permission Boundary 时候一定不能给 ``iam:DeleteRolePermissionsBoundary`` 这个权限, 不然用户可以创建后删除 Permission Boundary, 这个机制就形同虚设了.


Permission Boundary Example
------------------------------------------------------------------------------
- `app.py <https://github.com/MacHu-GWU/learn_aws-project/blob/main/docs/source/Security-Identity-Compliance/Identity-and-Access-Management-IAM-Root/05-Access-management-for-AWS-resources/01-Permission-Boundary/app.py>`_
- `example1.py <https://github.com/MacHu-GWU/learn_aws-project/blob/main/docs/source/Security-Identity-Compliance/Identity-and-Access-Management-IAM-Root/05-Access-management-for-AWS-resources/01-Permission-Boundary/example1.py>`_
