# -*- coding: utf-8 -*-

"""
This tool can print the aws console url of a S3 object / folder URI or ARN.
"""

from s3pathlib import S3Path

uri_or_arn = """
s3://my-bucket/my-key
""".strip()
print(S3Path(uri_or_arn).console_url)
