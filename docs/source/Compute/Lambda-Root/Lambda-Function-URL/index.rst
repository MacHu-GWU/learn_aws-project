Lambda Function URL
==============================================================================
Keywords: Amazon, AWS, Lambda


Overview
------------------------------------------------------------------------------
Lambda Function URL 是 2022-04-06 日发布的一个功能. 允许你为 Lambda Function 直接创建一个 HTTP Request 的 Endpoint, 使得你可以直接用 HTTP request 对 Lambda 发起请求. 它支持无需 Auth 以及需要用 IAM Role Auth 的两种鉴权模式. 在以前, 如果你要用 HTTP Request 来访问 Lambda 则需要用 API Gateway 来做中转, 这意味着你还要维护一个 API Gateway 的部署以及和 Lambda 的 Integration.

诚然 API Gateway 是完整的 API 服务器方案, 包含了鉴权, 缓存, 熔断保护, 统计信息等高级功能. 但有的时候你就仅仅需要一种用 HTTP 来调用 Lambda 的方式, Lambda Function URL 这个功能就很适合.

- `Lambda function URLs <https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html>`_
- `Announcing AWS Lambda Function URLs: Built-in HTTPS Endpoints for Single-Function Microservices <https://aws.amazon.com/blogs/aws/announcing-aws-lambda-function-urls-built-in-https-endpoints-for-single-function-microservices/>`_


IAM Auth
------------------------------------------------------------------------------
如果你发起 HTTP Request 的 Principal 拥有 `Using the AWS_IAM auth type <https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html#urls-auth-iam>`_ 中说明的权限, 那么你就可以可以 Invoke 这个 Lambda URL. 那 HTTP Request 又不是 boto3 SDK, HTTP request 是如何知道你的 Principal 是谁的呢? 官方文档说了, 你如果要用 AWS_IAM auth 那么你的 Request 需要 sign 你的 HTTP request, 这个 sign 的动作本质是跟 AWS 的服务器交换一个非对称密钥, 并对你的 credential 进行签名, 从而在 HTTP request 中不需要发送你的 AWS Credential, 而是发送一个签名后的 credential. 然后将其包含在 HTTP header 中. 这样 AWS 就知道 "你是谁了". 这个签名的动作可以用 `requests_aws4auth <https://pypi.org/project/requests-aws4auth/>`_ 库来做. 配合 ``requests`` 库使用起来非常简单.


CORS
------------------------------------------------------------------------------
CORS 是一种浏览器的机制. 比如你有一个网站页面, 它的一些动态元素需要 invoke Lambda Function URL. 你的 Lambda Function URL 就可以指定允许这个网站访问自己. 这是一种经过浏览器的验证机制, 防君子不防小人. 它无法用 IP 阻止你直接用 HTTP client 对你的 Lambda Function URL 发起请求.


Limit Access from IP Address White-List
------------------------------------------------------------------------------
Lambda Function URL 的 Resource Policy 不支持用 CONDITION 字段限制访问者的 IP 段. 但我看到过这样一个博文 `Restricting Access to Invoke Lambda Functions to an IP Range in a Service Control Policy <https://medium.com/cloud-security/restricting-access-to-invoke-lambda-functions-to-an-ip-range-in-a-service-control-policy-487aad479b06>`_, 它的原理是用 AWS Organization 级别的 SCP (Service Control Policy) 来限定 Lambda. 因为最终的权限是 SCP + IAM + Resource Policy 的交集, 所以它可以绕开 Lambda Resource Policy 的限制. 这个方法我没有试过, 不确定是不是可行.


Lambda Function URL Use Case
------------------------------------------------------------------------------
本节我们来探讨一下 Lambda Function URL 功能的使用场景.

首先, 凡是你能用 AWS CLI 或是 AWS SDK 的场景都不是 Lambda Function URL 的使用场景. 因为你完全可以直接用 AWS API 来 Invoke Lambda.

其次, 你要确保你并不需要一些例如 流量控制, 统计, 熔断 等高阶的 API Gateway 功能. 如果你需要这些功能, Lambda Function URL 不适合你.

我个人不太理解 Lambda Functino URL + IAM Auth 的使用场景. 因为你一旦启用了 IAM Auth, 你就需要用 IAM Credential 来给 HTTP Request 签名. 你都有 IAM Credential 了, 你为什么不用 IAM Policy 来控制这个 Principal 能访问哪些 Lambda Invoke 呢? 我目前还没想到.

我目前能想到的主要使用场景有:

1. 你财大气粗不怕别人对这个 URL 进行攻击, 你愿意将其作为完全 Public 的 Endpoint.
2. 你的 URL Endpoint 是保密的, 仅仅用于你的内部网站拉取资源用. 注意, 你无法用前端技术完全保护你的 URL 不被泄露, 因为最终抓包一定能抓到这个 URL.
3. 你的内部用户不懂 AWS SDK, 只会用 HTTP Client (我个人不太确定真的有没有人这样做, 学一下 AWS SDK 也不难啊), 在里面填写 AWS Credential 签名并发起 HTTP 请求.

另外我重点说一下 Public Lambda Function Url 和 API Gateway 在使用上的区别. 很多人会用 API Gateway + Lambda Function 作为 Rest API 的后端, 鉴权一般由 API Gateway Authorizer 完成, 并且这个鉴权是缓存的. 如果你把 Public Lambda Function Url 当 Rest API 用, 并且你又想要使用一定的 Auth 机制, 那么你就要在你的代码中实现 Auth 机制, 比如到数据库中查表看看 username password 合不合法. 由于 Lambda Function Url 不自带 Cache, 所以你需要自己实现 Cache 机制, 不然黑客对你的 URL 发起大量请求, 你的数据库会分分钟被流量打爆.


Example 1
------------------------------------------------------------------------------
HTTP GET, 无 Auth.

.. dropdown:: lambda_function_1.py

    .. literalinclude:: ./lambda_function_1.py
       :language: python
       :linenos:

.. dropdown:: test_lambda_function_1.py

    .. literalinclude:: ./test_lambda_function_1.py
       :language: python
       :linenos:

Received Event:

.. code-block:: javascript

    {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/",
        "rawQueryString": "",
        "headers": {
            "x-amzn-lambda-proxying-cell": "0",
            "content-length": "0",
            "x-amzn-tls-version": "TLSv1.2",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "x-forwarded-for": "111.111.111.111",
            "x-amzn-lambda-proxy-auth": "HmacSHA256, SignedHeaders=x-amzn-lambda-forwarded-client-ip;x-amzn-lambda-forwarded-host;x-amzn-lambda-proxying-cell, Signature=VA37S5zm4QGGjkLCU1N0tJ4pZ5ac3CX091uNcUzHgoA=",
            "accept": "*/*",
            "x-amzn-lambda-forwarded-client-ip": "111.111.111.111",
            "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
            "x-amzn-trace-id": "Self=1-65c12646-052899e02cd0afe472dd4807;Root=1-65c12646-4483c50e0acfc05666a5fe0b",
            "host": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "content-type": "application/json",
            "x-amzn-lambda-forwarded-host": "a1b2c3d4.lambda-url.us-east-1.on.aws",
            "accept-encoding": "gzip, deflate",
            "user-agent": "python-requests/2.31.0"
        },
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "a1b2c3d4",
            "domainName": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "domainPrefix": "a1b2c3d4",
            "http": {
                "method": "GET",
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "111.111.111.111",
                "userAgent": "python-requests/2.31.0"
            },
            "requestId": "cb4ca2b4-9b33-41fc-91a2-b5d7fd127371",
            "routeKey": "$default",
            "stage": "$default",
            "time": "05/Feb/2024:18:17:42 +0000",
            "timeEpoch": 1707157062219
        },
        "isBase64Encoded": false
    }


``requests.get(...).text``:

.. code-block:: javascript

    {
        "message": "hello world"
    }


Example 2
------------------------------------------------------------------------------
HTTP POST, 无 Auth.

.. dropdown:: lambda_function_2.py

    .. literalinclude:: ./lambda_function_2.py
       :language: python
       :linenos:

.. dropdown:: test_lambda_function_2.py

    .. literalinclude:: ./test_lambda_function_2.py
       :language: python
       :linenos:

Received Event:

.. code-block:: javascript

    {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/",
        "rawQueryString": "",
        "headers": {
            "x-amzn-lambda-proxying-cell": "0",
            "content-length": "17",
            "x-amzn-tls-version": "TLSv1.2",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "x-forwarded-for": "111.111.111.111",
            "x-amzn-lambda-proxy-auth": "HmacSHA256, SignedHeaders=x-amzn-lambda-forwarded-client-ip;x-amzn-lambda-forwarded-host;x-amzn-lambda-proxying-cell, Signature=VA37S5zm4QGGjkLCU1N0tJ4pZ5ac3CX091uNcUzHgoA=",
            "accept": "*/*",
            "x-amzn-lambda-forwarded-client-ip": "111.111.111.111",
            "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
            "x-amzn-trace-id": "Self=1-65c127b0-3e4ac5437eb5d00761057e90;Root=1-65c127b0-111394f70cbd54261cefb70f",
            "host": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "content-type": "application/json",
            "x-amzn-lambda-forwarded-host": "a1b2c3d4.lambda-url.us-east-1.on.aws",
            "accept-encoding": "gzip, deflate",
            "user-agent": "python-requests/2.31.0"
        },
        "requestContext": {
            "accountId": "anonymous",
            "apiId": "a1b2c3d4",
            "domainName": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "domainPrefix": "a1b2c3d4",
            "http": {
                "method": "POST",
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "111.111.111.111",
                "userAgent": "python-requests/2.31.0"
            },
            "requestId": "89a59336-2777-48ac-b6b9-0971c0ac9069",
            "routeKey": "$default",
            "stage": "$default",
            "time": "05/Feb/2024:18:23:44 +0000",
            "timeEpoch": 1707157424532
        },
        "body": "{\"name\": \"Alice\"}",
        "isBase64Encoded": false
    }

``requests.get(...).text``:

.. code-block:: javascript

    {
        "message": "hello Alice"
    }


Example 3
------------------------------------------------------------------------------
HTTP GET, 有 Auth.

.. dropdown:: lambda_function_3.py

    .. literalinclude:: ./lambda_function_3.py
       :language: python
       :linenos:

.. dropdown:: test_lambda_function_3.py

    .. literalinclude:: ./test_lambda_function_3.py
       :language: python
       :linenos:

Received Event:

.. code-block:: javascript

    {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/",
        "rawQueryString": "",
        "headers": {
            "x-amz-content-sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "x-amzn-lambda-proxying-cell": "0",
            "content-length": "0",
            "x-amzn-tls-version": "TLSv1.2",
            "x-amz-date": "20240205T183347Z",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "x-forwarded-for": "111.111.111.111",
            "x-amzn-lambda-proxy-auth": "HmacSHA256, SignedHeaders=Authorization;x-amzn-lambda-forwarded-client-ip;x-amzn-lambda-forwarded-host;x-amzn-lambda-proxying-cell, Signature=9jMcIoiOqvMqOFq0URZ6hs4UE5Dhlg7eEVs7SP4O8x8=",
            "accept": "*/*",
            "x-amzn-lambda-forwarded-client-ip": "111.111.111.111",
            "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
            "x-amzn-trace-id": "Self=1-65c12a0b-42ee20cb30e6c40462ddd34e;Root=1-65c12a0b-1ad48554022572e132d241c2",
            "host": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "content-type": "application/json",
            "x-amzn-lambda-forwarded-host": "a1b2c3d4.lambda-url.us-east-1.on.aws",
            "accept-encoding": "gzip, deflate",
            "user-agent": "python-requests/2.31.0"
        },
        "requestContext": {
            "accountId": "111122223333",
            "apiId": "a1b2c3d4",
            "authorizer": {
                "iam": {
                    "accessKey": "ABCD",
                    "accountId": "111122223333",
                    "callerId": "ABCD",
                    "cognitoIdentity": null,
                    "principalOrgId": "o-igflpr8b78",
                    "userArn": "arn:aws:iam::111122223333:user/alice",
                    "userId": "ABCD"
                }
            },
            "domainName": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "domainPrefix": "a1b2c3d4",
            "http": {
                "method": "GET",
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "111.111.111.111",
                "userAgent": "python-requests/2.31.0"
            },
            "requestId": "175967d9-69b6-4eb5-93bb-ed54335b3890",
            "routeKey": "$default",
            "stage": "$default",
            "time": "05/Feb/2024:18:33:47 +0000",
            "timeEpoch": 1707158027520
        },
        "isBase64Encoded": false
    }


``requests.get(...).text``:

.. code-block:: javascript

    {
        "message": "hello world"
    }


Example 4
------------------------------------------------------------------------------
HTTP POST, 有 Auth.

.. dropdown:: lambda_function_4.py

    .. literalinclude:: ./lambda_function_4.py
       :language: python
       :linenos:

.. dropdown:: test_lambda_function_4.py

    .. literalinclude:: ./test_lambda_function_4.py
       :language: python
       :linenos:

Received Event:

.. code-block:: javascript

    {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/",
        "rawQueryString": "",
        "headers": {
            "x-amz-content-sha256": "6d4a333838d0ef96756cccc680af2531075c512502fb68c5503c63d93de859b3",
            "x-amzn-lambda-proxying-cell": "0",
            "content-length": "17",
            "x-amzn-tls-version": "TLSv1.2",
            "x-amz-date": "20240205T183710Z",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "x-forwarded-for": "111.111.111.111",
            "x-amzn-lambda-proxy-auth": "HmacSHA256, SignedHeaders=Authorization;x-amzn-lambda-forwarded-client-ip;x-amzn-lambda-forwarded-host;x-amzn-lambda-proxying-cell, Signature=ZjYfrbJsBXcn1j2GooPNRUQxn0wswtLzZcjYS0ZV8Do=",
            "accept": "*/*",
            "x-amzn-lambda-forwarded-client-ip": "111.111.111.111",
            "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
            "x-amzn-trace-id": "Self=1-65c12ad6-6b2ad2571a826419695ca486;Root=1-65c12ad6-3d9d77d23efd735a0a589ae5",
            "host": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "content-type": "application/json",
            "x-amzn-lambda-forwarded-host": "a1b2c3d4.lambda-url.us-east-1.on.aws",
            "accept-encoding": "gzip, deflate",
            "user-agent": "python-requests/2.31.0"
        },
        "requestContext": {
            "accountId": "111122223333",
            "apiId": "a1b2c3d4",
            "authorizer": {
                "iam": {
                    "accessKey": "ABCD",
                    "accountId": "111122223333",
                    "callerId": "ABCD",
                    "cognitoIdentity": null,
                    "principalOrgId": "o-igflpr8b78",
                    "userArn": "arn:aws:iam::111122223333:user/alice",
                    "userId": "ABCD"
                }
            },
            "domainName": "a1b2c3d4.cell-1-lambda-url.us-east-1.on.aws",
            "domainPrefix": "a1b2c3d4",
            "http": {
                "method": "POST",
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "111.111.111.111",
                "userAgent": "python-requests/2.31.0"
            },
            "requestId": "52475474-4236-4a09-a8f4-9bd504de08ca",
            "routeKey": "$default",
            "stage": "$default",
            "time": "05/Feb/2024:18:37:10 +0000",
            "timeEpoch": 1707158230434
        },
        "body": "{\"name\": \"Alice\"}",
        "isBase64Encoded": false
    }

``requests.get(...).text``:

.. code-block:: javascript

    {
        "message": "hello Alice"
    }
