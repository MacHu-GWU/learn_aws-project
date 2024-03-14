import json
import random


def lambda_handler(event, context):
    print("Event:", event)

    response_code = 200
    action_group = event["actionGroup"]
    api_path = event["apiPath"]

    print("lambda_handler == > api_path: ", api_path)

    featureRequestID = f"random feature request id {random.randint(1, 1000)}"
    if api_path == "/createFeatureRequest":
        # result = createFeatureRequest(event)
        result = {"featureRequestID": f"Created request {featureRequestID}!"}
    elif api_path == "/updateFeatureRequest":
        # result = updateFeatureRequest(event)
        result = {"featureRequestID": f"Updated request {featureRequestID}!"}
    else:
        response_code = 404
        result = f"Unrecognized api path: {action_group}::{api_path}"

    response_body = {"application/json": {"body": json.dumps(result)}}

    action_response = {
        "actionGroup": event["actionGroup"],
        "apiPath": event["apiPath"],
        "httpMethod": event["httpMethod"],
        "httpStatusCode": response_code,
        "responseBody": response_body,
    }

    api_response = {"messageVersion": "1.0", "response": action_response}

    return api_response
