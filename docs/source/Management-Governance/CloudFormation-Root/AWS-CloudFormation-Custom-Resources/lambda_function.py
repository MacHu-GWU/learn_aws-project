# -*- coding: utf-8 -*-

"""
Sample CloudFormation Custom Resource Handler lambda function code.
"""

import typing as T
import json
import urllib3

http = urllib3.PoolManager()

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send(
    event: T.Dict[str, T.Any],
    context,
    response_status: str,
    response_data: T.Dict[str, T.Any],
    physical_resource_id: T.Optional[str] = None,
    no_echo: bool = False,
):
    """
    Send the CFN custom resource response back to CFN. You can reuse this function
    in other projects.

    Reference:

    - Request: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
    - Response https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html

    :param event: the original lambda event object
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
    response_url = event["ResponseURL"]
    response_body = {}
    response_body["Status"] = response_status
    response_body["Reason"] = (
        "See the details in CloudWatch Log Stream: " + context.log_stream_name
    )
    response_body["PhysicalResourceId"] = (
        physical_resource_id or context.log_stream_name
    )
    response_body["StackId"] = event["StackId"]
    response_body["RequestId"] = event["RequestId"]
    response_body["LogicalResourceId"] = event["LogicalResourceId"]
    response_body["NoEcho"] = no_echo
    response_body["Data"] = response_data

    json_response_body = json.dumps(response_body)

    print("Response body:\n" + json_response_body)

    headers = {
        "content-type": "application/json",
        "content-length": str(len(json_response_body)),
    }

    try:
        response = http.request(
            "PUT",
            response_url,
            body=json_response_body.encode("utf-8"),
            headers=headers,
        )
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))


def lambda_handler(event, context):
    print(json.dumps(event, indent=4))
    send(
        event,
        context,
        SUCCESS,
        {"group_name": "CftCustomResourcePocGroup2"},
        physical_resource_id=None,
        no_echo=False,
    )
    return {"statusCode": 200}
