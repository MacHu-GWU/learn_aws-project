# -*- coding: utf-8 -*-

import uuid
import time
import random
from datetime import datetime, timezone

import pynamodb_mate.api as pm
from boto_session_manager import BotoSesManager


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


tb_name = "incremental_export_poc-measurement"


class Measurement(pm.Model):
    class Meta:
        table_name = tb_name
        region = "us-east-1"
        billing_mode = pm.constants.PAY_PER_REQUEST_BILLING_MODE

    id = pm.UnicodeAttribute(hash_key=True, default=lambda: str(uuid.uuid4()))
    time = pm.UTCDateTimeAttribute(null=False, default=get_utc_now)
    value = pm.NumberAttribute(null=False)


Measurement.create_table(wait=True)

aws_profile = "bmt_app_dev_us_east_1"
bsm = BotoSesManager(profile_name=aws_profile)


def turn_on_pitr():
    bsm.dynamodb_client.update_continuous_backups(
        TableName=tb_name,
        PointInTimeRecoverySpecification={
            "PointInTimeRecoveryEnabled": True,
        },
    )


def gen_data():
    while 1:
        time.sleep(random.randint(500, 1500) / 1000)
        Measurement(
            value=random.randint(1, 100),
        ).save()


if __name__ == "__main__":
    turn_on_pitr()
    gen_data()
