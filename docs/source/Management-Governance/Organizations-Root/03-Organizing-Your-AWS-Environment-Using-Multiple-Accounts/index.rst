.. _organizing-your-aws-environment-using-multiple-accounts:

Organizing Your AWS Environment Using Multiple Accounts
==============================================================================
Keywords: AWS, Amazon, Organization, Org


Summary
------------------------------------------------------------------------------
这篇博文是阅读这篇 `同名 AWS Whitepaper <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html>`_ 的笔记. 介绍了在企业中如何正确地管理多个 AWS Accounts.


为什么要用多个 AWS Accounts
------------------------------------------------------------------------------
如果别人有这个疑惑, 要能跟人用人话解释的清楚. 主要有这么几点:

1. Group workloads based on business purpose and ownership: 将云资源按照 business purpose 和 ownership 分组, 以便于管理和审计.
2. Apply distinct security controls by environment: 对于不同的 workload security 的级别是不同的. 例如 prod 和 non prod 的安全级别肯定是不一样的.
3. Constrain access to sensitive data: 对于 data 的安全级别也是不一样的.
4. Promote innovation and agility: 允许开发者在隔离的环境中不受限制的实验一些东西有助于创新. 这里有 sandbox account 和 dev account 两个概念. sandbox account 指的是跟你的业务, data 完全 disconnected 的 account, 通常是可以不受限制的做实验. dev 则是能在受管制的情况下访问一些业务和 data, 同时又有比较大的 freedom 来做实验.
5. Limit scope of impact from adverse events: 隔离风险
6. Support multiple IT operating models: 不同公司有不同的 IT operating model (IT 管理模型), 显然如果只有一个 account 是无法适应复杂多变的需求. 而用多个 accounts 就能灵活的排列组合出你想要的需求了.
7. Manage costs: 管理开支
8. Distribute AWS Service Quotas and API request rate limits: 每个 account 是有 service quotas 的, 对其进行分流可以有效的避免 quota limit 的问题.

Ref:

- https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/benefits-of-using-multiple-aws-accounts.html


一些核心概念
------------------------------------------------------------------------------
这节是了解在企业中如何管理 AWS Accounts 的重点. 要仔细阅读.

有这么一些关键概念啊:

- **AWS Organizations**: 一个能 administer 很多 accounts 的 entity. 通常一个法律和财务上注册的公司就是一个 organization, 底下会有很多部门. 而如果这是一个集团公司, 那么集团下面的公司都可以视为一个个独立的 organization. 而如果这个公司还有子公司, 但是母公司和子公司的关系又没有大到集团公司那种关系, 那么子公司既可以被视为独立的 organization, 也可以归属于母公司的 organization.
- **Organizations management account**: 一个 org 只有一个 management account, 相当于 root account, 里面不跑业务, 而是专门用来管理其他 accounts.
- **Organizations member accounts**: 用来跑具体业务, 同时自己下面没有别的 member 归属自己, 那这就是一个 member account
- **Organizational Units (OU)**: 将多个 member accounts group 到一起的逻辑概念, 每一个 OU 可以按照部门, 项目, 业务等来分组. OU 是 Org tree 上面的一个父节点, 它是 AWS Organizations 里的一个概念, 而不是实体的 AWS Account. 每个 OU 可以有一个 Policy, 这个 Policy 会自动应用到所有的子节点上.

每个 Organization 一般会包含:

- A management account
- Zero or more member accounts
- Zero or more organizational units (OUs)
- Zero or more policies

Ref:

- Core Concept: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/core-concepts.html


Multi-Accounts 架构推荐
------------------------------------------------------------------------------
Design principles for your multi-account strategy:

- Organize based on security and operational needs: 根据安全和业务需求来组织你的 accounts.
- Apply security guardrails to OUs rather than accounts: 把 security policy apply 到 OU 级别而不是 account 级别
- Avoid deep OU hierarchies: 避免特别深的 OU 层级, 尽量使用扁平架构
- Start small and expand as needed: 最开始的规模可以比较小, 随着业务的发展再逐渐扩大
- Avoid deploying workloads to the organization’s management account: 不要用 management account 来部署任何 workload
- Separate production from non-production workloads: 把 production 和 non-production workloads 分离开.
- Assign a single or small set of related workloads to each production account: 把一个或相关的 production workload 放到一个 account 里.
- Use federated access to help simplify managing human access to accounts: 对于第三方 identity provider, 尽量使用 federated (联合) access, 而不是直接把用户加到 AWS account 里. 例如你需要 GitHub Action 来访问 AWS, 你不要为每个需要访问的 Account 创建 IAM user, 而是使用 OpenID connection.
- Use automation to support agility and scale: 所有的这些设置尽量用 automation tool 例如 CloudFormation 来配置而不要手动操作.
- Use multi-factor authentication: 对于关键节点开启 MFA.
- Break glass access: 这个词指的是跳过安全规则直接访问, 指的是用 management account 或 root user 跳过这些规则直接进行某些操作. 在一些极端情况下, 例如 member accounts 中的权限所有者不在了或者彻底丢失, 那么就需要用 management account 或 root user 来进行操作.

**Recommended OUs and accounts**

这里我就直接引用官方文档中的架构图了

.. image:: https://docs.aws.amazon.com/images/whitepapers/latest/organizing-your-aws-environment/images/recommended-ous.png

**Organizing workload-oriented OUs**

这一章的官方文档重点在说一个点, 把你的 prod workload 和 non prod 放在不同的 OU 里然后用 OU 级别的 policy 来管理. 这个我个人认为是很有道理的. 因为这里有两个 hierarchy, 一个是 Team / Line-of-business / App, 也就是这个项目是什么. 还有一个是 workload. 在组织架构上谁先谁后一直以来会争论不休. 通常在 Org chart 上 Team 先, workload 后. 而 AWS OU 的目的是为了方便管理 AWS 权限, 规则. 所以反过来是先 Workload 然后才是 Team. 当然这不是绝对的, 你可以根据自己的情况灵活调整.

Ref:

- `Design principles for your multi-account strategy <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/design-principles-for-your-multi-account-strategy.html>`_: 介绍了一些设计原则. 一旦了解了原则, 就可以在 AWS 推荐的架构基础上进行自定义了.
- `Recommended OUs and accounts <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/recommended-ous-and-accounts.html>`_:  AWS 官方推荐的架构. 基本适用于任何大小, 任何业务的公司. 其中有一个比较重要的就是 Workloads OU, 对应着传统 IT 企业中部署 App 时所经历的不同 阶段 / 环境. 例如 dev / test / prod 等等. 在 AWS 官方文档中的架构图中, 不仅仅是 Workloads OU, Security / Infrastructure / Deployment OU 都多多少少包含了 Workload 的部分. 这个部分会在另一个文档中详细介绍.
- `Organizing workload-oriented OUs <https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/recommended-ous-and-accounts.html>`_: 详细介绍了如何搭建 workload oriented OU.
