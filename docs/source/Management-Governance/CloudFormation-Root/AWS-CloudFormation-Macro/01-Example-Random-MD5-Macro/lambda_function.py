# -*- coding: utf-8 -*-

"""
这个 Lambda Function 实现了一个 AWS CloudFormation Macro, 用来生成一个随机的 MD5 字符串.
"""

import typing as T
import uuid
import traceback
import dataclasses

T_DATA = T.Dict[str, T.Any]


@dataclasses.dataclass
class Base:
    @classmethod
    def from_dict(cls, dct: T_DATA):
        kwargs = {}
        for field in dataclasses.fields(cls):
            if field.name in dct:
                kwargs[field.name] = dct[field.name]
        return cls(**kwargs)

    def to_dict(self) -> T_DATA:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Request(Base):
    region: str = dataclasses.field(default=None)
    accountId: str = dataclasses.field(default=None)
    fragment: dict = dataclasses.field(default=None)
    transformId: str = dataclasses.field(default=None)
    params: str = dataclasses.field(default=None)
    requestId: str = dataclasses.field(default=None)
    templateParameterValues: dict = dataclasses.field(default=None)


SUCCESS = "success"


@dataclasses.dataclass
class Response(Base):
    requestId: str = dataclasses.field(default=None)
    status: str = dataclasses.field(default=None)
    fragment: dict = dataclasses.field(default=None)
    errorMessage: str = dataclasses.field(default=None)


def lambda_handler(event, context):
    print("========== Start CloudFormation Macro Lambda Function ==========")
    print("event: " + str(event))

    request = Request.from_dict(event)
    try:
        response = process(request)
    except Exception as e:
        traceback.print_exc()
        response = Response(
            requestId=request.requestId,
            status="failure",
            errorMessage=str(e),
        )

    return response.to_dict()


def process(request: Request) -> Response:
    return Response(
        requestId=request.requestId,
        status=SUCCESS,
        # --- 方法 1. 返回一个简单的字符串本身
        # fragment=uuid.uuid4().hex,
        # --- 方法 2. 返回一个 CloudFormation JSON 中的一个 object 对象, 这个例子中是一个简单的
        # intrinsic function Fn::Sub, 只是用来演示. 实际上你可以返回任何复杂的 JSON 对象.
        # 甚至定义一个 Resource, 或是 nested stack 都可以
        fragment={
            "Fn::Sub": [
                "${value}",
                {"value": uuid.uuid4().hex},
            ],
        },
    )
