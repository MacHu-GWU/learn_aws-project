# -*- coding: utf-8 -*-

"""
This module provides utilities to load config data.
"""

import typing as T
import json
import dataclasses
from pathlib import Path


@dataclasses.dataclass
class Config:
    aws_profile: T.Optional[str] = dataclasses.field(default=None)
    host: T.Optional[str] = dataclasses.field(default=None)
    port: T.Optional[int] = dataclasses.field(default=None)
    database: T.Optional[str] = dataclasses.field(default=None)
    username: T.Optional[str] = dataclasses.field(default=None)
    password: T.Optional[str] = dataclasses.field(default=None)
    workgroup: T.Optional[str] = dataclasses.field(default=None)
    cluster_id: T.Optional[str] = dataclasses.field(default=None)

    @classmethod
    def load(cls, path: Path):
        return cls(**json.loads(path.read_text()))
