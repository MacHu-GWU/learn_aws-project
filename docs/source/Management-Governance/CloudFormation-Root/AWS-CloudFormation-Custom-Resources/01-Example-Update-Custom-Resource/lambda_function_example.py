# -*- coding: utf-8 -*-

"""
Sample CloudFormation Custom Resource Handler lambda function code.
"""

import typing as T
import json
import traceback
import dataclasses

import urllib3  # this is not a standard library, but this is available as a boto3 dependency

# if you need to make HTTP request, you can use the standard library ``urllib.request``
# import urllib.request


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
http = urllib3.PoolManager()

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


class RequestTypeEnum:
    Create = "Create"
    Update = "Update"
    Delete = "Delete"


@dataclasses.dataclass
class Request(Base):
    """
    The request object for CFN custom

    Reference:

    - Request: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
    """

    RequestType: str = dataclasses.field()
    ResponseURL: str = dataclasses.field()
    StackId: str = dataclasses.field()
    RequestId: str = dataclasses.field()
    ResourceType: str = dataclasses.field()
    LogicalResourceId: str = dataclasses.field()
    PhysicalResourceId: T.Optional[str] = dataclasses.field(default=None)
    ResourceProperties: T.Optional[T_DATA] = dataclasses.field(default=None)
    OldResourceProperties: T.Optional[T_DATA] = dataclasses.field(default=None)

    def is_create_type(self) -> bool:
        return self.RequestType == RequestTypeEnum.Create

    def is_update_type(self) -> bool:
        return self.RequestType == RequestTypeEnum.Update

    def is_delete_type(self) -> bool:
        return self.RequestType == RequestTypeEnum.Delete


class StatusEnum:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclasses.dataclass
class Response(Base):
    """
    The response object for CFN custom resource.

    Reference:

    - Response https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html
    """

    Status: str = dataclasses.field()
    PhysicalResourceId: str = dataclasses.field()
    StackId: str = dataclasses.field()
    RequestId: str = dataclasses.field()
    LogicalResourceId: str = dataclasses.field()
    NoEcho: bool = dataclasses.field(default=False)
    Data: T_DATA = dataclasses.field(default_factory=dict)
    Reason: str = dataclasses.field(default=None)


def send_to_cloudformation(
    request: Request,
    context,
    response_status: str,
    response_data: T.Dict[str, T.Any],
    physical_resource_id: T.Optional[str] = None,
    no_echo: bool = False,
):
    """
    Send the CFN custom resource response back to CFN.

    Reference:

    - Request: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
    - Response https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html

    :param request: the original lambda event object, which is a :class:`Request` object
    :param context: the original lambda context object
    :param response_status: SUCCESS or FAILED, you decide
    :param response_data: user data you want to return as Custom Resource attribute
    :param physical_resource_id: This value should be an identifier unique to the
        custom resource vendor, and can be up to 1 KB in size. The value must be
        a non-empty string and must be identical for all responses for the same resource.
    :param no_echo: Optional. Indicates whether to mask the output of the
        custom resource when retrieved by using the Fn::GetAtt function.
        If set to true, all returned values are masked with asterisks (*****),
        except for those stored in the Metadata section of the template.
    """
    response = Response(
        Status=response_status,
        PhysicalResourceId=physical_resource_id or context.log_stream_name,
        StackId=request.StackId,
        RequestId=request.RequestId,
        LogicalResourceId=request.LogicalResourceId,
        NoEcho=no_echo,
        Data=response_data,
        Reason="See the details in CloudWatch Log Stream: " + context.log_stream_name,
    )
    # This looks nice in cloudwatch log
    print("---------- Response body ----------")
    json_response_body = json.dumps(response.to_dict())
    print(f"{json_response_body = }")

    headers = {
        "content-type": "application/json",
        "content-length": str(len(json_response_body)),
    }
    try:
        response = http.request(
            "PUT",
            request.ResponseURL,
            body=json_response_body.encode("utf-8"),
            headers=headers,
        )
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(...) failed executing requests.put(...): " + str(e))
        raise e


def lambda_handler(event, context):
    print("========== Start Lambda Function ==========")
    print("---------- Event body ----------")
    event_body = json.dumps(event)
    print(f"{event_body = }")

    request = Request.from_dict(event)
    try:
        result = process(request=request, context=context)
        send_to_cloudformation(
            request=request,
            context=context,
            response_status=result.response_status,
            response_data=result.data,
            physical_resource_id=result.physical_resource_id,
            no_echo=result.no_echo,
        )
        status_code = 200
    # your custom request processing logic my have bug,
    # it is very important to catch all exceptions and send a FAILED signal back to CFN
    # otherwise, CFN will wait for the response for one hour (by default)
    except Exception as e:
        print("---------- failed to process request, see traceback below ----------")
        tb_string = traceback.format_exc(limit=20)
        print(tb_string)
        # send a failed signal back to CFN
        send_to_cloudformation(
            request=request,
            context=context,
            response_status=StatusEnum.FAILED,
            response_data={"error": str(e)},
            physical_resource_id=request.PhysicalResourceId,
            no_echo=False,
        )
        status_code = 400

    print("========== End Lambda Function ==========")
    return {"statusCode": status_code}


# ------------------------------------------------------------------------------
# Implement this
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class Result:
    """
    The result of the :func:`process` function.
    """

    data: T_DATA = dataclasses.field()
    physical_resource_id: str = dataclasses.field()
    response_status: str = dataclasses.field(default=StatusEnum.SUCCESS)
    no_echo: bool = dataclasses.field(default=False)


def process(
    request: Request,
    context,
) -> Result:
    """
    Put your custom resource request processing logic here.

    :param request: the original lambda event object, which is a :class:`Request` object

    :return: a :class:`Result` object, which provide necessary information to
        create the :class:`Response` object.
    :param context: the original lambda context object.

    Here's some hint:

    - if you believe the cloudformation deployment should not proceed, set the
        ``Result.status`` to ``StatusEnum.FAILED``.
    - include logic to handle ``if request.is_create_type():``,
        ``if request.is_update_type():``, ``if request.is_delete_type():``.
    - when request type is Create, you should use a deterministic physical resource id,
            such as ``context.log_stream_name`` or a hard coded value.
    - when request type is update, if you believe your custom resource update logic
        should be a simple update, then just set physical_resource_id to the same value
        you used in Create logic branch
    - when request type is update, if you believe your custom resource update logic
        should be an update then delete old one, then you should set a different
        physical_resource_id value than the one you used in Create logic branch,
        for example, you can use ``uuid.uuid4().hex``.
    """
    raise NotImplementedError
