Why User Assume Role for Multiple AWS Account
==============================================================================
For big Organization, **it is always a bad idea to maintain multiple IAM User in different AWS Account representing the same Person**. Because it makes it harder to track activity / cost did by the same person, and also managing multiple sensitive credential may greatly increase the probability of leaking. In addition, assume-role makes it easy to switch between multiple AWS Account, instead of typing credentials.


如何为 Cross Account Access 创建一个 Assume Role
------------------------------------------------------------------------------
**注意** 本节摘抄于官方文档, 只是用来学习和快速了解. 该设置不适合于生产环境. 最佳实践请参考 :ref:`implement-assume-role-correctly` 这篇文档.

1. 创建一个 IAM Role, 在 Select type of trusted entity 中选择 Another AWS Account, 并填入你当前的 AWS Account Id (12位数字)
2. Attach 对应的 Policy, 这些 Policy 会成为你想模拟的 IAM User 的 Policy.
3. 给这个 IAM Role 一个名字, 里面最好包含 Assume Role, 以表示其功能.
4. 在 Console 的右上角点击自己的 Account, 选择 Switch Role, 填入你的 AWS Account Id 和 Policy Name (你刚才起的名字). 此时你在 Console 中的权限就跟 Assume Role 中的一样了.
5. 如果要切换回来, 在 Console 右上角点击自己的 Account, 选择 back to xxx 即可.
6. 如果要使用 CLI, 请参考官方文档 https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html, 简单来说就是将你的 ``$HOME/.aws/credentials`` 文件修改成如下样子, 然后在你的 Cli 中加上 ``--profile my_iam_user_assume_role`` 选项, 或是在 SDK 中加上 ``boto3.Session(profile_name="my_iam_user_assume_role")`` 即可::

    [original_iam_user_profile]
    aws_access_key_id = AAAAAAAAAAAAAAAAAAAA
    aws_secret_access_key = AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

    [my_iam_user_assume_role]
    role_arn = arn:aws:iam::123456789012:role/my-assume-role
    source_profile = original_iam_user_profile


FAQ
------------------------------------------------------------------------------
- Q: 为什么要禁止 IAM User 创建其他 IAM User?
- A: 因为作为公司, 公司需要管理用户创建 IAM User 的行为, 并使用 IAM User 来追踪用户的使用行为. 如果允许用户自行创建其他的 IAM User, 那么公司就很难追踪这些新创建的 IAM User. 这叫做 preventing cascade creation.

- Q: 如果我需要使用其他的 IAM User 进行测试该怎么做? 我可能需要同时使用 Console 和 Cli. 比如我需要使用一个 Machine User 进行项目的 Deploy, 我需要知道这个 Machine User 所需要的最小权限是什么, 所以我需要一个 IAM User 进行测试.
- A: 你可以使用 Assume Role 的方式, 创建一个 IAM Role, 用来模拟 IAM User 的权限, 然后在 Console 和 Cli 中 Assume 这个 Role 进行测试.

- Q: 使用 Assume Role 的好处?
- A: 不用频繁的登录切换 IAM User, 减少管理 ACCESS KEY 的麻烦.