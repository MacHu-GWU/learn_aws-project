# -*- coding: utf-8 -*-

"""
Create at: 2024-09-06
Author: Sanhe Hu

This script is used to clean up old images in ECR.
"""

import typing as T
import dataclasses
from datetime import datetime, timezone

import boto3


@dataclasses.dataclass
class Image:
    digest: str
    tags: T.List[str]
    pushed_at: datetime

    def get_elapse(self, utc_now: datetime) -> int:
        return int((utc_now - self.pushed_at).total_seconds())


def get_images(
    ecr_client,
    repo_name: str,
) -> T.List[Image]:

    paginator = ecr_client.get_paginator("describe_images")
    response_iterator = paginator.paginate(
        repositoryName=repo_name,
        filter={"tagStatus": "ANY"},
    )
    image_list = list()
    for response in response_iterator:
        image_detail_list = response.get("imageDetails", [])
        for image_detail in image_detail_list:
            image_digest = image_detail["imageDigest"]
            image_tags = image_detail.get("imageTags", [])
            image_pushed_at = image_detail["imagePushedAt"]
            if len(image_tags) == 0:
                continue
            image = Image(
                digest=image_digest,
                tags=image_tags,
                pushed_at=image_pushed_at,
            )
            image_list.append(image)
    return image_list


def do_we_delete_it(
    image: Image,
    utc_now: datetime,
    untagged_ttl: int,
    general_ttl: int,
) -> bool:
    """
    - Delete all image created long ago (based on TTL).
    - Delete all untagged images.
    """
    if "latest" in image.tags:
        return False
    elapse = image.get_elapse(utc_now)
    if len(image.tags) == 0:
        return elapse > untagged_ttl
    else:
        return elapse > general_ttl


def delete_old_image(
    ecr_client,
    repo_name: str,
    utc_now: datetime,
    untagged_ttl: int,
    general_ttl: int,
):
    image_list = get_images(ecr_client, repo_name)
    to_delete = list()
    for image in image_list:
        if do_we_delete_it(
            image=image,
            utc_now=utc_now,
            untagged_ttl=untagged_ttl,
            general_ttl=general_ttl,
        ):
            if image.tags:
                uri = "{}:{}".format(repo_name, "|".join(image.tags))
            else:
                uri = f"{repo_name}:{image.digest}"
            print(f"delete: {uri}")
            to_delete.append({"imageDigest": image.digest})
    if len(to_delete):
        ecr_client.batch_delete_image(
            repositoryName=repo_name,
            imageIds=to_delete,
        )


if __name__ == "__main__":
    aws_profile = "bmt_app_devops_us_east_1"
    repo_name = "simple_lbd_container"
    general_ttl = 30 * 24 * 60 * 60
    untagged_ttl = 1 * 24 * 60 * 60
    boto_ses = boto3.Session(profile_name=aws_profile)
    ecr_client = boto_ses.client("ecr")
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)

    delete_old_image(
        ecr_client=ecr_client,
        repo_name=repo_name,
        utc_now=utc_now,
        untagged_ttl=untagged_ttl,
        general_ttl=general_ttl,
    )
