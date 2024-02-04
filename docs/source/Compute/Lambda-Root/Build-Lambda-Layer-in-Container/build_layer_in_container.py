# -*- coding: utf-8 -*-

"""
This shell script can run a `AWS SAM CI/CD docker images <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html>`_
container and build AWS Lambda Python Layer in it.

This script is based on this official document:

- `How do I create a Lambda layer using a simulated Lambda environment with Docker <https://repost.aws/knowledge-center/lambda-layer-simulated-docker>`_
"""

import subprocess
from pathlib import Path

dir_here = Path(__file__).absolute().parent

python_version = "3.9"
is_arm = False
container_name = "lbd_layer_build"
if is_arm:
    image_uri = f"public.ecr.aws/sam/build-python{python_version}:latest-arm64"
    platform = "linux/arm64"
else:
    image_uri = f"public.ecr.aws/sam/build-python{python_version}:latest-x86_64"
    platform = "linux/amd64"

args = [
    "docker",
    "run",
    "--rm",
    "--name",
    container_name,
    "--platform",
    platform,
    "--mount",
    f"type=bind,source={dir_here},target=/var/task",
    image_uri,
    "python",
    "build_layer.py",
]
subprocess.run(args)
