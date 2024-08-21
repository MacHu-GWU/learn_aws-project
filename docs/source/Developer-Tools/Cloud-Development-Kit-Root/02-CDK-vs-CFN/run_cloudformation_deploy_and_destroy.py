# -*- coding: utf-8 -*-


from boto_session_manager import BotoSesManager
from learn_cdk.config import aws_profile, stack_name, param_value_project_name, path_cfn
from aws_cloudformation import Parameter, deploy_stack, remove_stack
from app import stack

bsm = BotoSesManager(profile_name=aws_profile)

deploy_stack(
    bsm=bsm,
    stack_name=stack_name,
    template=path_cfn.read_text(),
    parameters=[
        Parameter(
            key=stack.param_project_name_id,
            value=param_value_project_name,
        )
    ],
    include_iam=True,
    include_named_iam=True,
    skip_plan=True,
    skip_prompt=True,
)

# remove_stack(
#     bsm=bsm,
#     stack_name=stack_name,
#     skip_prompt=True,
# )
