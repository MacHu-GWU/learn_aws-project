# -*- coding: utf-8 -*-

import shutil
import subprocess
from pathlib import Path

dir_here = Path(__file__).absolute().parent
dir_data = dir_here / "data"
if dir_data.exists() is False:
    dir_data.mkdir(parents=True)

CONTAINER_NAME = "opensearch-node"


def remove_data():
    shutil.rmtree(dir_data, ignore_errors=True)


def run(
    auto_remove: bool = True,
    mount_data: bool = False,
    clear_data: bool = False,
):
    args = ["docker", "run"]
    if auto_remove:
        args.append("--rm")
    args.extend(
        [
            "-p",
            "9200:9200",
            "-p",
            "9600:9600",
            "-e",
            "discovery.type=single-node",
            "--name",
            CONTAINER_NAME,
            "-d",
        ]
    )
    if mount_data:
        args.extend(["-v", f"{dir_data}:/usr/share/opensearch/data"])
    if clear_data:
        remove_data()
    args.append("opensearchproject/opensearch:latest")
    subprocess.run(args, check=True)


def stop():
    args = ["docker", "stop", CONTAINER_NAME]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    run(auto_remove=True, mount_data=False, clear_data=False)
    # stop()
