Multi Accounts Management Runbook
==============================================================================
Keywords: AWS, Amazon, Organization, Org

在我的项目经历中, 为 5, 6 个公司完成了从 mono-AWS-account 到 AWS Organizational Unit 架构的迁徙. 并且我也为自己的创业公司搭建了 AWS Organizational Unit 架构.

本文是一个 runbook (为了达到某个目的的详细步骤手册). 假设如果我为一个从没有 AWS Account 的公司从零开始搭建 AWS Accounts 架构, 照着本文一步步做就可以完成.


You May Heard About AWS Control Tower
------------------------------------------------------------------------------
`AWS Control Tower <https://aws.amazon.com/controltower/>`_ 是一个用来管理 multi-account AWS environments 的官方工具. 它能自动化实现 AWS 关于账号管理的 best practice, 以及自动收集 account audit log 并汇总, 自动分析扫描你的 security 问题. 对于最终的企业用户, 我还是推荐使用 Control Tower 来管理你的 AWS Accounts. 这个对于每月 AWS 开销在 1w 美元以上的企业当然是有必要的, 但是对于初创企业来说很可能不是必要的. 但本文的目标读者是有一定基础, 但是没有实操经验的开发者, 通过动手操作一次加深理解. 如果你已经是熟练使用 Control Tower 的用户, 说明你已经非常有经验了, 那就不需要看本文了.


1. Create Root AWS Account
------------------------------------------------------------------------------
首先我们需要一个 Root AWS Account 作为你们公司所有跟 AWS 相关操作的最高权限.


1.1 Who Should be Your AWS Account Admin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
首先你需要为你的公司选择一个人作为你们公司 AWS Accounts 的最高权限拥有者. 这包括一个实体的人, 和一个 Email. 通常这个实体的人可能随着人员的离职会变化, 但是这个 Email 应该是一个固定的. 所以假设你们公司叫 ABC group, 你们的 IT 技术的最高负责人是 Tom, 那你不应该用 tom@example.com, 而是专门为你们公司创建一个叫 abc.group.aws.admin@example.com 的邮箱用来做 AWS 管理员. 然后把这个 Email 的所有权给 Tom. 当 Tom 离职的时候需要上交所有权.


1.2 创建 Root Account 以及为 Root User 配置 MFA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
首先, 用管理员邮箱在 https://aws.amazon.com/free 注册一个新的 AWS Account, 期间会要你填很多联系人信息, 以及银行卡信息. 这个 Account 就作为你的 AWS Organizations 的 root account, 也叫 management account. 这个 Account 的目的只有一个, 管理其他的 AWS Account 以及管理 Billing. 一定不要在这个 Account 中掺杂 IT 的功能. 例如收集日志, 监控, CI/CD, Infrastructure 等等都应该在其他 Account 中完成. 这个 Account 的权限最高, 非常敏感, 一定要保护好.

这个时候你登陆是用的 Root user 的 email 和 password 登录的. 这个 Root user 有着 override 后续一切操作的权限. 例如你设置了一些规则禁止对后续创建的 AWS Account 上的一些操作, 这个 Root user 有着可以无视一切禁止操作的权限. **接下来一定要迅速的为这个 Root user 创建 MFA 登录**, 到 IAM 里面 Scan QR code, 在你的手机上设置 MFA. 最好用 Microsoft Authenticator, 能将 MFA 自动备份到云端. 接下来, 除了管理 bill 之类的事情, 不要再用这个 Root user Account 登录了. 这是因为 Root user 的 email 被 hack 了, 并造成了损失, 因为这个 email 是超过了 AWS 的管理范围的, AWS 什么都帮不了你. **正确的管理做法是在 Root Account 上创建一个 IAM User 并授予 Admin 权限**. 这个 IAM User 是可以随时被删除, 重新创建的. 在出现问题的时候我们有能力进行修复并减小损失. 所以下一步就是在 Root Account 上创建一个 IAM User.


1.3 创建 IAM User on Root Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在这一节我们要为 Root Account 创建一个 IAM User, 用于日常管理 AWS Organization 的活动. 建议也为这个 IAM User 配置 MFA.

默认情况下 IAM User 即使有 Admin 权限, 也是无法看到 billing 相关的信息的, 只有每个 Account 的 Root User 有这个权限. 在企业中用 IAM User 编写程序对 billing 信息进行处理是非常有必要的. 你可以参考下面这篇文章显式地给与 IAM User billing 相关的权限.

Reference:

- `How can I troubleshoot access denied errors related to the Billing and Cost Management console? <https://aws.amazon.com/premiumsupport/knowledge-center/iam-billing-access/>`_


2. 用 AWS Organizations 创建 Member Account
------------------------------------------------------------------------------
有了 Root Account 之后, 我们就可以根据你的企业的组织架构, 业务需求搭建 multi-accounts 的架构了. AWS 官方说了, 并不存在一个完美的 multi-accounts 的架构, 需要根据你的实际需求决定, 但总的来说会有一个逻辑. 详情请参考我的另一篇博文 :ref:`organizing-your-aws-environment-using-multiple-accounts`.


2.1 设计你的 Multi-Accounts 架构
------------------------------------------------------------------------------
Multi-Accounts 架构取决于根据你的业务需求和企业规模. 本文的架构着眼一个极简的架构.

我建议至少创建下面这些 Account 和 OU. 这个设计满足了一个初创企业能在生产环境中部署 App, 并且遵循了最佳实践, 并且可以在 expand 的时候无需破坏目前的拓扑结构::

    root (ROOT)
    |-- root (Account) 这个就是前面创建的 root (management) account
    |-- infra (OU)
        |-- infra (Account) 用于管理 infrastructure as code, 这个 account 也是 delegated cloudformation stackset admin. 凡是需要自动部署到所有 Account 的资源, 例如 common s3 bucket, audit trail 等, 都是通过这个 Account 中的 cloudformation stackset 来实现的.
    |-- sandbox (OU)
        |-- sandbox1 (Account) 用于隔离测试一些功能, 测试完成后就可以关掉了.
    |-- deployments (OU)
        |-- deploy-devops (Account) 用于 Host 所有的 Git 代码, CI/CD, Configuration, Deployment Artifacts 资源.
    |-- app (OU), 本质上是 workload OU 的一种.
        |-- app-dev (Account) 用于 app 开发工作. 开发者开发 App 时进行测试的环境.
        |-- app-prd (Account) 用于运行 app 的 production workload.

这个架构没有包括专门的 Audit, Security OU. 这些 OU 在合规要求高的行业和大企业中是必须得, 但对于初创企业来说, 这些 OU 可以在后续的发展中再添加.


2.2 Naming Convention
------------------------------------------------------------------------------
我建议按照一定的 naming convention 组织你的 AWS Account 相关的资源. 下面我们假设你们公司叫 ABC group, 简称 ``abc``. 你们的 Root Account 的 email 是 ``abc@example.com``.

- **AWS Account Alias**: 每个 AWS Account 可以有一个 alias, 这个 alias 是你的 login url 的一部分, 并且能在很多 API 中避免你暴漏 AWS Account ID (虽然 Acc ID 并不是敏感信息, 但是还是有一些攻击手段可以靠这个, 所以还是尽量避免暴漏). 建议在所有的 AWS Account Alias 都遵循这个 format ``${org_name}-${ou_name}-${workload_name(optional)}``. 例如 root account 就可以叫 ``abc-admin``, 例如专门用于部署 infrastructure 的 account 就可以叫 ``abc-infra``. 例如某个 App 的 dev 环境的 account 就可以叫 ``abc-app-dev``.
- **Root User Email for Member Account**: 在使用 AWS Organization Account 创建 member account 的时候会要你输入 Email 作为 root user. 由于我们是使用 Organization 来管理 accounts, 这个 root user 显然要是 root account 的 root user email. 但是一个 email 只能 associate 一个 Account. 那该怎么办呢? 答案是使用 email alias, 现代 email 系统都允许在 email 的 ``@`` 前面加 ``+`` 跟着一串字符作为 email alias. 所有在加号后面的字符都会被忽略并且 email 都会被 forward 到你的主 email 中. 所以你用 AWS Organizations 创建 Account 时用的 email 应该是 ``${root_user_email}+${account_alias}@example.com`` 例如你的 ``abc-app-dev`` Root user email 就应该是 ``abc+abc-app-dev@example.com``.


2.3 使用 AWS Organizations 创建 Member Account
------------------------------------------------------------------------------
先进入 AWS Organizations Console 里的 `Add an AWS Account <https://us-east-1.console.aws.amazon.com/organizations/v2/home/accounts/add/create>`_ 界面, 这个界面既可以创建一个新的 AWS Account 并自动添加到你的 AWS Org 中, 或是邀请一个已经存在的 AWS Account 加入到你的 AWS Org 中 (常用于刚开始用 AWS 的时候没有使用 AWS Organizations 的情况)

- AWS account name: 使用上一节介绍的 ``${org_name}-${ou_name}-${workload_name(optional)}`` 格式, 例如 ``abc-app-dev``.
- Email address of the account's owner: 使用上一节介绍的 ``${root_user_email}+${account_alias}@example.com`` 格式, 例如 ``abc+abc-app-dev@example.com``.
- IAM role name: 这个 Role 是用于给 Admin account 来 assume member account 的 Admin role 用的, 这个最好使用默认的 ``OrganizationAccountAccessRole``.

以上操作也可以使用在 Root Account 上的 IAM User 通过 `boto3.client("organizations").create_account(..) <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations/client/create_account.html>`_ 来进行.

接下来就可以用 Admin account 来 access member account 了, 请参考下面两篇官方文档.

Reference:

- After I use AWS Organizations to create a member account, how do I access that account?: https://aws.amazon.com/premiumsupport/knowledge-center/organizations-member-account-access/
- Accessing and administering the member accounts in your organization: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html


3. Configure Member Account
------------------------------------------------------------------------------
现在我们已经有了很多 Member Account 了, 我们需要对这些 Account 进行配置. 例如:

1. 配置 OU Policy 来限制每个 Account 的权限.
2. 为每个 Account 部署一些必要的资源.

TODO: 这部分内容还没写完.
