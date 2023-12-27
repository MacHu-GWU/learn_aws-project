Use MFA Protection
==============================================================================


Why MFA
------------------------------------------------------------------------------
MFA 已经成了企业级应用用于进一步保证安全的标准配置. 所以, 为关键的 AWS 登录启用 MFA 是非常有必要的. 这里强调, Root User Access 一定要开启 MFA!!!


How Does MFA Work
------------------------------------------------------------------------------
在 AWS Console 里管理你的登录的页面, 一般会有一个启用 MFA 的选项. 在你第一次启用时就会出现一个 QR code 可以让你用 authenticator app 来扫描. 然后会要你输入两次 MFA token 以确保 AWS 和你的 Authenticator 关联上. 之后你再需要登录就得要输入 MFA token 了.


How to Use MFA to access AWS CLI
------------------------------------------------------------------------------
AWS CLI 是给程序使用的登录方式. 为了防止黑客入侵你的电脑盗取 IAM User 的 AWS CLI Credential (IAM User 的 credential 是长期有效的), 你可以开启 MFA 使得用 IAM User credential + MFA token 才能获得一个临时的 credential 用于登录. 这样你的电脑就算被盗了, 上面的 credential 也很快会失效.

这里列出了用于获得临时 credential 的两种常用方式:

- `aws sts get-session-token --serial-number arn-of-the-mfa-device --token-code code-from-token <https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/get-session-token.html>`_
- `boto3.client("sts").get_session_token(...) <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/get_session_token.html>`_

这两种方式都只能获得 credential, 如果你是给人类使用, 你还需要把这个 credential 放在你的 ``~/.aws/credentials`` 文件中才行并为其 创建一个 profile. 当然这个操作可以自动化.

下面给出了 ``~/.aws/config`` 和 ``~/.aws/credentials`` 的例子:

Sample ``~/.aws/config`` file

.. code-block:: yaml

    [profile my_profile]
    region = us-east-1
    output = json

    [profile my_profile_mfa]
    region = us-east-1
    output = json

Sample ``~/.aws/credentials`` file

.. code-block:: yaml

    [my_profile]
    aws_access_key_id = AAAABBBBCCCC
    aws_secret_access_key = AAAAbbbbCCCCdddd

    [my_profile_mfa]
    aws_access_key_id = AAAABBBBCCCC
    aws_secret_access_key = AAAAbbbbCCCCdddd
    aws_session_token = AAAAbbbbCCCCddddEEEEffffGGGGhhhh

我个人开发了两个小工具来帮助我方便地 MFA:

- `awscli_mate <https://github.com/MacHu-GWU/awscli_mate-project>`_: 一个 interactive 的 CLI 命令行工具. 既可以当一个库来编写 Python 程序, 也可以直接当做 CLI 用.
- `afwf_aws_profile <https://github.com/MacHu-GWU/afwf_awscli_profile-project/blob/main/pyproject.toml>`_: 一个 Mac 专用的 Alfred Workflow. 相当于是 ``awscli_mate`` 的 GUI 版.


Force User to use MFA for AWS CLI
------------------------------------------------------------------------------
有些要求严格的企业会要求所有的 IAM User 都必须用 MFA 登录才能调用大部分的 AWS API. 例如没有 MFA 登录的用户只能列出自己以及为自己配置 MFA (如果自己都进不去, 那就没法自助配置 MFA 了), 而登录后才能够使用大部分的 AWS API. 下面是我曾经为一个企业做的一个方案所用到的 IAM 配置文档.

Reference:

- Using Multi-Factor Authentication (MFA) in AWS: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html
- How do I use an MFA token to authenticate access to my AWS resources through the AWS CLI?: https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/
- Get IAM User of an AWS Profile: https://docs.aws.amazon.com/cli/latest/reference/sts/get-access-key-info.html
- Get AWS Region of an AWS Profile: https://docs.aws.amazon.com/cli/latest/reference/configure/get.html


How to Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create these IAM User Groups.

``ManageMFA`` - Allow User to Manage their MFA Device:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowUsersToChangePassword",
                "Effect": "Allow",
                "Action": [
                    "iam:ChangePassword",
                    "iam:GetAccountPasswordPolicy",
                    "iam:ListUserPolicies",
                    "iam:GetLoginProfile",
                    "iam:UpdateLoginProfile"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            }
            {
                "Sid": "AllowUsersToCreateDeleteTheirOwnVirtualMFADevices",
                "Effect": "Allow",
                "Action": [
                    "iam:*VirtualMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/${aws:username}"
                ]
            },
            {
                "Sid": "AllowUsersToEnableSyncDisableTheirOwnMFADevices",
                "Effect": "Allow",
                "Action": [
                    "iam:DeactivateMFADevice",
                    "iam:EnableMFADevice",
                    "iam:ListMFADevices",
                    "iam:ResyncMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowUsersToListVirtualMFADevices",
                "Effect": "Allow",
                "Action": [
                    "iam:ListVirtualMFADevices"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/*"
                ]
            },
            {
                "Sid": "AllowUsersToListUsersInConsole",
                "Effect": "Allow",
                "Action": [
                    "iam:ListUsers"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/*"
                ]
            }
        ]
    }

``ForceMFA`` - Force to use MFA for AWS Console and Cli:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowAllUsersToListAccounts",
                "Effect": "Allow",
                "Action": [
                    "iam:ListAccountAliases",
                    "iam:ListUsers"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/*"
                ]
            },
            {
                "Sid": "AllowIndividualUserToSeeTheirAccountInformation",
                "Effect": "Allow",
                "Action": [
                    "iam:ChangePassword",
                    "iam:CreateLoginProfile",
                    "iam:DeleteLoginProfile",
                    "iam:GetAccountPasswordPolicy",
                    "iam:GetAccountSummary",
                    "iam:GetLoginProfile",
                    "iam:UpdateLoginProfile"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowIndividualUserToListTheirMFA",
                "Effect": "Allow",
                "Action": [
                    "iam:ListVirtualMFADevices",
                    "iam:ListMFADevices"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/*",
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "AllowIndividualUserToManageThierMFA",
                "Effect": "Allow",
                "Action": [
                    "iam:CreateVirtualMFADevice",
                    "iam:DeactivateMFADevice",
                    "iam:DeleteVirtualMFADevice",
                    "iam:EnableMFADevice",
                    "iam:ResyncMFADevice"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:mfa/${aws:username}",
                    "arn:aws:iam::111122223333:user/${aws:username}"
                ]
            },
            {
                "Sid": "DoNotAllowAnythingOtherThanAboveUnlessMFAd",
                "Effect": "Deny",
                "NotAction": "iam:*",
                "Resource": "*",
                "Condition": {
                    "Null": {
                        "aws:MultiFactorAuthAge": "true"
                    }
                }
            }
        ]
    }

``ReadOnly`` - Only allow to read / list aws resource:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "autoscaling:Describe*",
                    "cloudformation:DescribeStacks",
                    "cloudformation:DescribeStackEvents",
                    "cloudformation:DescribeStackResources",
                    "cloudformation:GetTemplate",
                    "cloudformation:List*",
                    "cloudtrail:DescribeTrails",
                    "cloudtrail:GetTrailStatus",
                    "cloudwatch:Describe*",
                    "cloudwatch:Get*",
                    "cloudwatch:List*",
                    "directconnect:Describe*",
                    "ec2:Describe*",
                    "elasticloadbalancing:Describe*",
                    "iam:List*",
                    "iam:Get*",
                    "redshift:Describe*",
                    "redshift:ViewQueriesInConsole",
                    "rds:Describe*",
                    "rds:ListTagsForResource",
                    "s3:Get*",
                    "s3:List*",
                    "ses:Get*",
                    "ses:List*",
                    "sns:Get*",
                    "sns:List*",
                    "sqs:GetQueueAttributes",
                    "sqs:ListQueues",
                    "sqs:ReceiveMessage"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }

``Ec2RestrictAccess`` - Don't allow to touch set of EC2 instance:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Condition": {
                    "StringLike": {
                        "ec2:ResourceTag/Name": "Ec2NamePrefix*"
                    }
                },
                "Action": [
                    "ec2:CreateTags",
                    "ec2:DeleteTags",
                    "ec2:StartInstances",
                    "ec2:StopInstances",
                    "ec2:TerminateInstances"
                ],
                "Resource": "arn:aws:ec2:us-east-1:*:instance/*",
                "Effect": "Deny"
            }
        ]
    }


``CreateIamRole`` - Allow to Create IAM Role:

.. code-block:: python

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeIamInstanceProfileAssociations",
                    "iam:AttachGroupPolicy",
                    "iam:AttachRolePolicy",
                    "iam:AttachUserPolicy",
                    "iam:CreatePolicy",
                    "iam:CreateRole",
                    "iam:GetGroupPolicy",
                    "iam:GetPolicy",
                    "iam:GetPolicyVersion",
                    "iam:GetRole",
                    "iam:GetRolePolicy",
                    "iam:GetUserPolicy",
                    "iam:ListAttachedRolePolicies",
                    "iam:ListEntitiesForPolicy",
                    "iam:ListInstanceProfiles",
                    "iam:ListPolicyVersions",
                    "iam:ListRolePolicies",
                    "iam:PassRole"
                ],
                "Resource": "*"
            }
        ]
    }
