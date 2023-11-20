# -*- coding: utf-8 -*-

import boto3

from config import aws_profile, collection_name
from create_and_configure import (
    create_oss_object_by_collection_name,
    test_oss_connection,
)


if __name__ == "__main__":
    boto_ses = boto3.session.Session(profile_name=aws_profile)
    oss = create_oss_object_by_collection_name(boto_ses, collection_name)
    test_oss_connection(oss, verbose=True)
