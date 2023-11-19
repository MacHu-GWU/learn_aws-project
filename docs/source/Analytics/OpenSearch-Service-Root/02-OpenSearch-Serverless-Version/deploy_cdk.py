# -*- coding: utf-8 -*-

import os
import subprocess
from pathlib import Path

dir_here = Path(__file__).absolute().parent
os.chdir(str(dir_here))

args = [
    "cdk",
    "deploy",
    "--require-approval",
    "never",
]
subprocess.run(args, check=True)
