# -*- coding: utf-8 -*-

import os
import subprocess
from app import bsm, dir_workspace

os.chdir(str(dir_workspace))
with bsm.awscli():
    subprocess.run(["cdk", "delete", "--force"])
