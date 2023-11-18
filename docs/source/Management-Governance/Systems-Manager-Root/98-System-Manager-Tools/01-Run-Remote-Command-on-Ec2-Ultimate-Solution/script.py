# -*- coding: utf-8 -*-

"""
一个需要在 EC2 上运行的脚本, 它会打印一些包含特殊符号的字符串的 JSON 到 stdout.
"""

import sys
import json


def run() -> dict:
    print("start")
    print("done")
    return {
        "python": sys.executable,
        "weird_string": "\\a\nb\tc\"d'e@f#g:h/i"
    }


if __name__ == "__main__":
    print(json.dumps(run()))
