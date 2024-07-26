# -*- coding: utf-8 -*-

import time
from datetime import datetime, timezone, timedelta

import pynamodb_mate.api as pm
from boto_session_manager import BotoSesManager


class Measurement(pm.Model):
    """
    我们假设我们的应用场景是用传感器不断地采集测量数据.

    - series: 是一个传感器的唯一标识.
    - time: 是测量数据的时间戳.
    - expire_at: 是测量数据的过期时间, 比如我们可以设定测量之后只保留 30 天的数据.
    """

    class Meta:
        table_name = "dynamodb-ttl-poc-measurement"
        region = "us-east-1"
        billing_mode = pm.constants.PAY_PER_REQUEST_BILLING_MODE

    series = pm.UnicodeAttribute(hash_key=True)
    time = pm.UTCDateTimeAttribute(range_key=True)
    # 只要定义了一个 TTL attribute (实际上是一个 UTCDateTimeAttribute)，在创建 Table 的时候就会自动启用 TTL 功能
    expire_at = pm.TTLAttribute()


bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
with bsm.awscli():
    Measurement._connection = None
    # 在第一次创建 table 的时候, 会自动打开 ttl 功能
    if Measurement.exists() is False:
        Measurement.create_table(wait=True)


class EC2Usage(Measurement):
    """
    这个 DynamoDB table 只是扩展了 :class:`Measurement` 类, 添加了一些额外的属性.
    """

    cpu_usage = pm.NumberAttribute()
    memory_usage = pm.NumberAttribute()


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


# 清空已有的数据
EC2Usage.delete_all()

# 插入一条数据
ec2_inst_id = "i-1a2b3c"

measurement_time = get_utc_now()
ec2_usage = EC2Usage(
    series=ec2_inst_id,
    time=measurement_time,
    expire_at=measurement_time + timedelta(seconds=5),
    cpu_usage=0.1,
    memory_usage=0.2,
)
ec2_usage.save()

# 每秒查询一次数据, 从第 6 次开始, 就不会再查询到数据了
for i in range(1, 1 + 10):
    time.sleep(1)
    now = get_utc_now()
    print(f"at {i}th second")
    ec2_usage_list = EC2Usage.iter_query(
        ec2_inst_id,
        filter_condition=EC2Usage.expire_at >= now,  # 用 filter 来过滤掉已经过期的数据
    ).all()
    print(f"  {ec2_usage_list = }")
