# -*- coding: utf-8 -*-

import typing as T
import os
import subprocess
from pathlib import Path

dir_here = Path(__file__).absolute().parent
dir_venv = dir_here / ".venv"


def print_cmd(args: T.List[str]):
    print(" ".join(args))


def create_virtualenv():
    args = ["virtualenv", "-p", "python3.10", f"{dir_venv}"]
    subprocess.run(args)


def install_dependencies():
    args = [f"{dir_venv}/bin/pip", "install", "-r", f"{dir_here}/requirements.txt"]
    subprocess.run(args)


def run_jupyter():
    args = ["cd", f"{dir_here}"]
    print_cmd(args)
    args = [
        f"{dir_venv}/bin/jupyter-lab",
    ]
    print_cmd(args)


if __name__ == "__main__":
    # create_virtualenv()
    # install_dependencies()
    run_jupyter()
