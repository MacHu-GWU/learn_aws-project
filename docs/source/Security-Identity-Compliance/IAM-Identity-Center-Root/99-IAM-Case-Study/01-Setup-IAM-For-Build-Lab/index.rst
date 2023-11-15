Case Study - Setup IAM permission For Build Lab
==============================================================================
Keywords: AWS, IAM, Multi Tenant

Tags: :bdg-primary:`Case Study` :bdg-primary:`Security` :bdg-primary:`IAM`


Background
------------------------------------------------------------------------------
在 Solution Architect 的 Business engagement 的过程中, 在 SA 自己的 AWS Account 中给客户做 Solution 的 Demo 只是第一步. 为了进一步帮助客户 build confidence, 往往需要在客户的 AWS 环境中开发和部署这个 Solution. 这个时候 IAM 权限管理就是相当大的挑战, 充满着不确定性. 因为这不像 SA 自己的 AWS Account 上有 Admin 权限, 客户的公司规定无法预测, 而且企业中往往有一个专门的组来管理这些 AWS 权限, 客户参与会议的人员不一定能随心所欲的对 AWS 权限进行配置. 所以我们需要在进入客户的 AWS 环境开发之前, 做好充分准备, 以避免由于没有权限什么都干不了的窘境.


Potential IAM Permission Setup
------------------------------------------------------------------------------
通常无论客户的公司的规定是怎样的, 最终的方案都会是以下方案之一.

1. 给客户的与会人员 Admin 权限 (最简单的方式). 到时候用到什么再临时创建即可.
2. 提前给要用的 AWS Account 配置好一些针对要用到的资源的 Full access 权限, 然后叫一个 Admin 在旁边 Stand by, 随时创建 Ad-hoc role.
3. 我们没有 Admin 在旁边一直 Stand by, 我们仔细计划好所需要的权限, 并提前配置好. 如果出现问题, 就通知 Admin 帮助我们 (会有延迟).
4. 使用 Resource policy 的方式给客户能创建和更改带有某一个特定的 **名字前缀** 的 IAM Role / Policy 资源的 Admin 权限. 这样它们就能在一定的限制下创建任何它们需要的权限了.

至于我们要采纳哪一种方案, 请参考下一节.


Setup IAM Role for Build Lab Decision Tree
------------------------------------------------------------------------------
You can follow the decision tree below to figure out what is the proper method for this activity.

.. raw:: html
    :file: ./setup-iam-role-for-build-lab.drawio.html

Below is a sample IAM policy for method #4. Assume that ``your-common-prefix`` is the common prefix for IAM role / policy we can create freely.

.. code-block:: javascript

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "iam:AttachRolePolicy",
                    "iam:CreatePolicy",
                    "iam:CreatePolicyVersion",
                    "iam:CreateRole",
                    "iam:DeletePolicy",
                    "iam:DeletePolicyVersion",
                    "iam:DeleteRole",
                    "iam:DeleteRolePermissionsBoundary",
                    "iam:DeleteRolePolicy",
                    "iam:DetachRolePolicy",
                    "iam:PassRole",
                    "iam:PutRolePermissionsBoundary",
                    "iam:PutRolePolicy",
                    "iam:SetDefaultPolicyVersion",
                    "iam:UpdateAssumeRolePolicy",
                    "iam:UpdateRole",
                    "iam:UpdateRoleDescription"
                ],
                "Resource": [
                    "arn:aws:iam::111122223333:role/your-common-prefix*",
                    "arn:aws:iam::111122223333:policy/your-common-prefix*"
                ]
            }
        ]
    }
