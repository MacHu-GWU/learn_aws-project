# -*- coding: utf-8 -*-

import random
from app import bsm, stack

bsm.sns_client.publish(
    TopicArn=f"arn:aws:sns:{bsm.aws_region}:{bsm.aws_account_id}:{stack.sns_topic_name}",
    Message=f"random number = {random.randint(1, 100)}",
)
