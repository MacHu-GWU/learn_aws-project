# -*- coding: utf-8 -*-

"""
该脚本用于测试用 aio 并发读取 S3 对象的性能跟普通 boto3 的对比.

结论, 大量小文件场景下 aio 优势显著.

- 100 个 1MB 的文件:
    - 普通: 17.03
    - aio: 2.92
- 10 个 10MB 的文件:
    - 普通: 5.82
    - aio: 3.38
"""

from fixa.timer import DateTimeTimer
import asyncio
import aioboto3
from boto_session_manager import BotoSesManager
from s3pathlib import S3Path

aws_profile = "bmt_app_dev_us_east_1"

# content = "a" * 1024 * 1024  # 1MB
# n_file = 100

content = "a" * 1024 * 1024 * 10  # 10MB
n_file = 10

bsm = BotoSesManager(profile_name=aws_profile)
bucket = f"{bsm.aws_account_alias}-{bsm.aws_region}-data"
s3dir_root = S3Path(f"s3://{bucket}/tmp/async-boto3-poc/").to_dir()


def prepare_data():
    s3dir_root.delete(bsm=bsm)
    for i in range(1, 1 + n_file):
        s3path = s3dir_root / f"{str(i).zfill(3)}.txt"
        s3path.write_text(content, bsm=bsm)


def method_1():
    """
    This method uses the aioboto3 library to read multiple S3 objects concurrently.
    It creates a session and client, then reads the objects in parallel using asyncio.
    """
    content_list = []
    for i in range(1, 1 + n_file):
        s3path = s3dir_root / f"{str(i).zfill(3)}.txt"
        content = s3path.read_text(bsm=bsm)
        content_list.append(content)


async def read_s3_object(s3_client, key: str) -> str:
    response = await s3_client.get_object(Bucket=bucket, Key=key)
    async with response["Body"] as stream:
        content = await stream.read()
        return content.decode("utf-8")  # 假设内容是 UTF-8 编码的文本


async def method_2():
    session = aioboto3.Session(profile_name=aws_profile)
    async with session.client("s3") as s3_client:
        object_keys = [
            s3dir_root.joinpath(f"{str(i).zfill(3)}.txt").key
            for i in range(1, 1 + n_file)
        ]
        tasks = [read_s3_object(s3_client, key) for key in object_keys]
        content_list = await asyncio.gather(*tasks)


if __name__ == "__main__":
    prepare_data()
    with DateTimeTimer():
        method_1()
    with DateTimeTimer():
        asyncio.run(method_2())
