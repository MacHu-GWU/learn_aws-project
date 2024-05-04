# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime, timezone

import moto
import pynamodb_mate as pm
from s3pathlib import S3Path, context
from boto_session_manager import BotoSesManager


def get_md5(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def get_s3_key(
    pk,
    sk,
    attr: str,
    value: bytes,
    prefix: str = "",
) -> str:
    s3path = S3Path(f"s3://my-bucket").joinpath(prefix).joinpath(f"pk={pk}")
    if sk is not None:
        s3path = s3path.joinpath(f"sk={sk}")
    fingerprint = get_md5(value)
    s3path = s3path.joinpath(f"attr={attr}", f"hash={fingerprint}")
    return s3path.key


aws_region = "us-east-1"


class Model(pm.Model):
    class Meta:
        table_name = "test"
        region = aws_region
        billing_mode = pm.PAY_PER_REQUEST_BILLING_MODE

    pk = pm.UnicodeAttribute(hash_key=True)
    update_at = pm.UTCDateTimeAttribute()
    html = pm.UnicodeAttribute()
    image = pm.UnicodeAttribute()


mock_dynamodb = moto.mock_dynamodb()
mock_s3 = moto.mock_s3()
mock_dynamodb.start()
mock_s3.start()

bsm = BotoSesManager(region_name=aws_region)
context.attach_boto_session(boto_ses=bsm.boto_ses)

bucket = "my-bucket"
bsm.s3_client.create_bucket(Bucket=bucket)

Model.create_table(wait=True)

# ------------------------------------------------------------------------------
# Create item
# ------------------------------------------------------------------------------
print("--- Create Item ---")
utc_now = get_utc_now()

pk = "id-1"
html = "<b>Hello Alice</b>"
html_data = html.encode("utf-8")
image = "this is image one".encode("utf-8")
image_data = image

html_s3_key = get_s3_key(pk=pk, sk=None, attr=Model.html.attr_name, value=html_data)
image_s3_key = get_s3_key(pk=pk, sk=None, attr=Model.image.attr_name, value=image_data)

print("Create S3 ...")
s3path_html = S3Path(f"s3://{bucket}/{html_s3_key}")
s3path_html.write_bytes(
    html_data,
    metadata={
        "pk": pk,
        "attr": Model.html.attr_name,
        "update_at": utc_now.isoformat(),
    },
)

s3path_image = S3Path(f"s3://{bucket}/{image_s3_key}")
s3path_image.write_bytes(
    image_data,
    metadata={
        "pk": pk,
        "attr": Model.image.attr_name,
        "update_at": utc_now.isoformat(),
    },
)

print("Create DynamoDB ...")
model = Model(pk=pk, update_at=utc_now, html=s3path_html.uri, image=s3path_image.uri)
model.save()

# ------------------------------------------------------------------------------
# Get item
# ------------------------------------------------------------------------------
print("--- Get Item ---")
model = Model.get(pk)
html = S3Path(model.html).read_bytes().decode("utf-8")
image = S3Path(model.image).read_bytes()
print(f"{html = }")
print(f"{image = }")

# ------------------------------------------------------------------------------
# Inspect S3 Bucket
# ------------------------------------------------------------------------------
print("--- Inspect S3 Bucket ---")
for s3path in S3Path(bucket).iter_objects():
    print(s3path.uri)

# ------------------------------------------------------------------------------
# Update item
# ------------------------------------------------------------------------------
print("--- Update Item ---")
model = Model.get(pk)

utc_now = get_utc_now()

html = "<b>Hello Bob</b>"
html_data = html.encode("utf-8")
image = "this is image two".encode("utf-8")
image_data = image

# get existing s3 object location, we may need to delete them if update success
s3path_existing_html = S3Path(model.html)
s3path_existing_image = S3Path(model.image)

html_s3_key = get_s3_key(pk=pk, sk=None, attr=Model.html.attr_name, value=html_data)
image_s3_key = get_s3_key(pk=pk, sk=None, attr=Model.image.attr_name, value=image_data)
s3path_html = S3Path(f"s3://{bucket}/{html_s3_key}")
s3path_image = S3Path(f"s3://{bucket}/{image_s3_key}")

print("Put S3 ...")
s3path_html.write_bytes(
    html_data,
    metadata={
        "pk": pk,
        "attr": Model.html.attr_name,
        "update_at": utc_now.isoformat(),
    },
)
s3path_image.write_bytes(
    image_data,
    metadata={
        "pk": pk,
        "attr": Model.image.attr_name,
        "update_at": utc_now.isoformat(),
    },
)

try:
    print("Update DynamoDB ...")
    model.update(
        actions=[
            Model.html.set(s3path_html.uri),
            Model.image.set(s3path_image.uri),
        ]
    )
    print("(optional) Remove old S3 object ...")
    s3path_existing_html.delete()
    s3path_existing_image.delete()
except Exception as e:
    print("(optional) Remove newly created s3 object if DynamoDB update failed ...")
    s3path_html.delete()
    s3path_image.delete()

# ------------------------------------------------------------------------------
# Get item
# ------------------------------------------------------------------------------
print("--- Get Item ---")
model = Model.get(pk)
html = S3Path(model.html).read_bytes().decode("utf-8")
image = S3Path(model.image).read_bytes()
print(f"{html = }")
print(f"{image = }")

# ------------------------------------------------------------------------------
# Inspect S3 Bucket
# ------------------------------------------------------------------------------
print("--- Inspect S3 Bucket ---")
for s3path in S3Path(bucket).iter_objects():
    print(s3path.uri)


# ------------------------------------------------------------------------------
# Delete item
#
# Delete DynamoDB object first, then delete S3. In this case, if DynamoDB operation failed,
# it's OK. If DynamoDB operation succeeded but S3 operation failed, you end up with
# an ghost S3 object, which is OK, you can clean them up anytime.
#
# Don't delete S3 first. Because if S3 operation succeeded but DynamoDB operation failed,
# reader can get DynamoDB item but cannot find the S3 object, which is very bad.
#
# ------------------------------------------------------------------------------
print("--- Delete Item ---")
model = Model.get(pk)
s3path_existing_html = S3Path(model.html)
s3path_existing_image = S3Path(model.image)

print("delete DynamoDB ...")
model.delete()

print("delete S3 ...")
s3path_existing_html.delete()
s3path_existing_image.delete()

# ------------------------------------------------------------------------------
# Get item
# ------------------------------------------------------------------------------
print("--- Get Item ---")
model = Model.get_one_or_none(pk)
print(f"{model = }")

# ------------------------------------------------------------------------------
# Inspect S3 Bucket
# ------------------------------------------------------------------------------
print("--- Inspect S3 Bucket ---")
for s3path in S3Path(bucket).iter_objects():
    print(s3path.uri)


# ------------------------------------------------------------------------------
# Clean Up Unused S3 Object
#
# 注意: 由于 S3 update 的时间可能比真实的 DynamoDB update 时间要早一点
# (取决于写入 S3 的耗时), 所以我们可以把时间回溯个 1 小时, 只对比在这之前的数据既可.
# ------------------------------------------------------------------------------
print("--- Clean Up Unused S3 Object ---")
s3uri_set = set()
for model in Model.scan(attributes_to_get=["html", "image"]):
    s3uri_set.add(model.html)
    s3uri_set.add(model.image)

for s3path in S3Path(f"s3://{bucket}/").iter_objects():
    if s3path.uri not in s3uri_set:
        s3path.delete()
