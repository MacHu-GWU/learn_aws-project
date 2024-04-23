# -*- coding: utf-8 -*-

import uuid
import random
from app import bsm, stack

bsm.sqs_client.send_message_batch(
    QueueUrl=f"https://sqs.{bsm.aws_region}.amazonaws.com/{bsm.aws_account_id}/{stack.sqs_queue_name}",
    Entries=[
        {
            "Id": uuid.uuid4().hex,
            "MessageBody": f"Message {random.randint(1,100)}",
        }
        for i in range(1, 1 + 10)
    ],
)
