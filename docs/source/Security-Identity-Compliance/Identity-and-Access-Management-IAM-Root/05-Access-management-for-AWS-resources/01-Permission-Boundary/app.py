#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup necessary resources
"""

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct

from aws_console_url.api import AWSConsole
from boto_session_manager import BotoSesManager


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: "Construct",
        construct_id: str,
        prefix: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.prefix = prefix

        self.iam_group_name = f"{prefix}_iam_group"
        self.iam_group_policy_name = f"{self.iam_group_name}_policy"
        self.iam_permission_boundary_policy_name = (
            f"{self.prefix}_iam_permission_boundary_policy"
        )

        self.iam_user_name = f"{prefix}_iam_user"

        # Create Resources
        self.create_permission_boundary_policy()
        self.create_group()
        self.create_user()

    def create_permission_boundary_policy(self):
        self.pb_statement_1 = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "iam:AddRoleToInstanceProfile",
                "iam:AttachRolePolicy",
                "iam:ChangePassword",
                "iam:CreateAccessKey",
                "iam:CreateInstanceProfile",
                "iam:CreatePolicy",
                "iam:CreatePolicyVersion",
                "iam:CreateServiceLinkedRole",
                "iam:CreateVirtualMFADevice",
                "iam:DeactivateMFADevice",
                "iam:DeleteAccessKey",
                "iam:DeleteInstanceProfile",
                "iam:DeletePolicy",
                "iam:DeletePolicyVersion",
                "iam:DeleteRole",
                "iam:DeleteRolePermissionsBoundary",
                "iam:DeleteRolePolicy",
                "iam:DetachRolePolicy",
                "iam:EnableMFADevice",
                "iam:GetAccessKeyLastUsed",
                "iam:GetAccountName",
                "iam:GetAccountPasswordPolicy",
                "iam:GetAccountSummary",
                "iam:GetContextKeysForCustomPolicy",
                "iam:GetGroup",
                "iam:GetGroupPolicy",
                "iam:GetInstanceProfile",
                "iam:GetLoginProfile",
                "iam:GetMFADevice",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:GetUser",
                "iam:GetUserPolicy",
                "iam:ListAccessKeys",
                "iam:ListAccountAliases",
                "iam:ListAttachedGroupPolicies",
                "iam:ListAttachedRolePolicies",
                "iam:ListAttachedUserPolicies",
                "iam:ListCloudFrontPublicKeys",
                "iam:ListEntitiesForPolicy",
                "iam:ListGroupPolicies",
                "iam:ListGroups",
                "iam:ListGroupsForUser",
                "iam:ListInstanceProfiles",
                "iam:ListInstanceProfilesForRole",
                "iam:ListInstanceProfileTags",
                "iam:ListMFADevices",
                "iam:ListMFADeviceTags",
                "iam:ListOpenIDConnectProviders",
                "iam:ListOpenIDConnectProviderTags",
                "iam:ListPolicies",
                "iam:ListPoliciesGrantingServiceAccess",
                "iam:ListPolicyTags",
                "iam:ListPolicyVersions",
                "iam:ListRolePolicies",
                "iam:ListRoles",
                "iam:ListRoleTags",
                "iam:ListSAMLProviders",
                "iam:ListSAMLProviderTags",
                "iam:ListServerCertificates",
                "iam:ListServerCertificateTags",
                "iam:ListServiceSpecificCredentials",
                "iam:ListSigningCertificates",
                "iam:ListSSHPublicKeys",
                "iam:ListSTSRegionalEndpointsStatus",
                "iam:ListUserPolicies",
                "iam:ListUsers",
                "iam:ListUserTags",
                "iam:ListVirtualMFADevices",
                "iam:PassRole",
                "iam:PutRolePermissionsBoundary",
                "iam:SimulateCustomPolicy",
                "iam:SimulatePrincipalPolicy",
                "iam:TagInstanceProfile",
                "iam:TagPolicy",
                "iam:TagRole",
                "iam:UntagInstanceProfile",
                "iam:UntagPolicy",
                "iam:UntagRole",
                "iam:UpdateAccessKey",
                "iam:UpdateAssumeRolePolicy",
                "iam:UpdateRoleDescription",
            ],
            resources=["*"],
        )
        # 这个 Permission boundary statement 要求当用户 Create Role 时, 也必须
        # attach 这个 permission boundary policy
        self.pb_statement_2 = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "iam:CreateRole",
                "iam:PutRolePolicy",
            ],
            resources=[f"arn:aws:iam::{cdk.Aws.ACCOUNT_ID}:role/*"],
            conditions={
                "StringEquals": {
                    "iam:PermissionsBoundary": f"arn:aws:iam::{cdk.Aws.ACCOUNT_ID}:policy/{self.iam_permission_boundary_policy_name}",
                }
            },
        )
        self.pb_policy = iam.ManagedPolicy(
            self,
            id="IamPermissionBoundaryPolicy",
            managed_policy_name=self.iam_permission_boundary_policy_name,
            document=iam.PolicyDocument(
                statements=[
                    self.pb_statement_1,
                    self.pb_statement_2,
                ],
            ),
        )

    def create_group(self):
        """
        Create an IAM Group.
        """
        # 显式给 IAM Group S3 权限, 但是由于 Permission Boundary Policy 的限制,
        # 这个权限是不生效的
        self.s3_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:*",
            ],
            resources=["arn:aws:s3:::*"],
        )
        self.group_inline_policy = iam.Policy(
            self,
            id="IamGroupPolicy",
            policy_name=self.iam_group_policy_name,
            statements=[
                self.pb_statement_1,
                self.pb_statement_2,
                self.s3_statement,
            ],
        )
        self.group = iam.Group(
            self,
            id="IamGroup",
            group_name=self.iam_group_name,
        )
        self.group.attach_inline_policy(self.group_inline_policy)

    def create_user(self):
        self.user = iam.User(
            self,
            "IamUser",
            user_name=self.iam_user_name,
            permissions_boundary=self.pb_policy,
        )
        self.user.add_to_group(self.group)

        self.access_key = iam.AccessKey(
            self,
            "IamUserAccessKey",
            user=self.user,
        )
        self.out_access_key = cdk.CfnOutput(
            self,
            "OutputIamUserAccessKey",
            value=self.access_key.access_key_id,
            description="Iam User Access Key",
        )
        self.out_secret_key = cdk.CfnOutput(
            self,
            "OutputIamUserSecretKey",
            value=self.access_key.secret_access_key.unsafe_unwrap(),
            description="Iam User Secret Key",
        )


app = cdk.App()

aws_profile = "bmt_app_dev_us_east_1"
prefix = "iam_pb_example_1"

stack_name = prefix.replace("_", "-")
stack = Stack(
    scope=app,
    construct_id=stack_name,
    prefix=prefix,
)

bsm = BotoSesManager(profile_name=aws_profile)
aws_console = AWSConsole.from_bsm(bsm=bsm)


def print_url():
    # fmt: off
    print(f"IAM Permission Boundary Policy: {aws_console.iam.get_policy(stack.iam_permission_boundary_policy_name)}")
    print(f"IAM Group: {aws_console.iam.get_user_group(stack.iam_group_name)}")
    print(f"IAM User: {aws_console.iam.get_user(stack.iam_user_name)}")
    # fmt: on


if __name__ == "__main__":
    print_url()
    app.synth()
