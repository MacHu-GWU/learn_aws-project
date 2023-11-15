.. _aws-iam-overview:

Amazon IAM Overview
==============================================================================
Keywords: AWS, IAM, Overview.


What is IAM
------------------------------------------------------------------------------
IAM 是云时代的权限管理的最佳实践. 云时代下所有的访问几乎都是远程的. 而且访问的形式多种多样, 有用户名密码登录, 给人类使用的有界面的 APP, 无界面的程序接口, 给虚拟机和容器等服务器用的权限, 需要身份验证的网站, 和登录服务提供商例如 Google, Facebook, Microsoft AD 整合的第三方登录, 给 Public 用户使用的临时权限, Role based access control (RBAC), attribute based access control (ABAC), 这么多形式数不胜数. 而 IAM 是一个能解决以上所有问题的一个服务.

Reference:

- `What is IAM? <https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html>`_


IAM Concepts
------------------------------------------------------------------------------
Reference:

- `How IAM works <https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html#intro-structure-terms>`_


IAM Knowledge Graph
------------------------------------------------------------------------------
以下是 IAM 的知识图谱, 对所有的知识点进行了一个梳理.

- Concepts: 这里列出了所有重要的概念, 在理解它们之前建议不要深入阅读其他内容.
    - Terms
        - IAM Resource
            - user
            - group
            - role
            - policy
            - identity-provider object
        - IAM Entity
            - user
            - role
        - IAM Identity
        - Principals
        - Human users
        - Workload
    - Principal
    - Request
        - Actions or operations
        - Resources – The AWS resource object upon which the actions or operations are performed.
        - Principal
        - Environment data
        - Resource data
    - Authentication
    - Authorization
    - Actions or operations
    - Resources
- Security best practices and use cases: AWS 自己总结的关于 IAM 的最佳实践和使用场景.
    - Security best practices
    - Root user best practices
    - Business use cases
- IAM Identities: 深入了解如何配置和管理 IAM Identifies, User, Group, Role, Policy.
- Access management for AWS resources: 深入了解如何管理 AWS 资源的访问权限.
- IAM Access Analyzer: 这是一个比较新的服务, 能自动扫描你的 IAM 配置, 发现潜在的安全风险.
