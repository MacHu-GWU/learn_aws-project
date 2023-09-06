.. _use-custom-container-in-lambda:

Deploy Lambda with Container Image
==============================================================================
Keywords: Amazon, AWS, Lambda


1. Overview
------------------------------------------------------------------------------
AWS Lambda 作为一款主打 Function As a Service 的服务, 无需管理服务器, 甚至无需管理运行环境是它的主要特点之一. 通常情况下用户会使用 AWS Lambda Layer 来部署依赖, 而用 Deployment 来部署源代码. 但是 AWS Lambda Layer 有解压缩后 250MB 的限制. 在一些应用场景例如需要大量依赖的数据处理, 机器学习的情况下, 250MB 是不够用的.

从 2020 年 12 起, AWS 推出了支持自定义容器镜像的 Lambda, 用户可以使用最大不超过 10GB 的容器镜像, 从而提供了更多的可能性.

新功能发布公告:

- `AWS Lambda now supports container images as a packaging format <https://aws.amazon.com/about-aws/whats-new/2020/12/aws-lambda-now-supports-container-images-as-a-packaging-format/>`_: 新功能发布公告.
- `New for AWS Lambda – Container Image Support <https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/>`_: 一篇讲解这一功能的官方博客.

用容器来部署 Lambda 的话有大约下面几种用法:

1. Using an AWS base image for Lambda: 用 AWS 官方自带各种编程语言 Runtime 的基础容器镜像, 只是在上面安装额外的依赖, 命令行工具等. 这是最常见的应用场景, 也是最简单的.
2. Using an AWS base image for custom runtimes: 用 AWS 的基础容器镜像, 在上面构建其他编程语言的 Runtime. 这个基础镜像自带了 Runtime interface client (是 AWS Lambda 定义的一种接口约定, 任何实现该接口的容器镜像都可以用来部署 Lambda, 这里不展开说, 以后再说), 你只需要安装好你的编程语言的 Runtime, 并将它跟自带的 entrypoint shell script wire 在一起即可.
3. Using a non-AWS base image: 不用 AWS 的基础镜像, 用自己的镜像. 你需要按照文档自己安装 Runtime, 也要自己实现 Runtime interface client 的接口 (它对应的 Entrypoint shell script)

本文不全部展开说, 本文以第一种用法 "Using an AWS base image for Lambda" 以及 Python 变成语言为例, 介绍如何用容器部署 Lambda.


2. Deploy Lambda with Python Container Image
------------------------------------------------------------------------------
本节我们用 AWS 官方自带 Python 的基础镜像, 在上面安装额外的依赖, 并部署 Lambda.

**基础镜像**

首先我们要选择一个基础镜像. 我们可以在 `ECR Public Gallery <https://gallery.ecr.aws/lambda?page=1>`_ 上找到所有 AWS 提供的各种编程语言的基础镜像. 这里简单说一下 ECR Public Gallery 是一个由 AWS 维护的, 类似于 DockerHub 的网站, 可供开发者发布公开镜像. 由于 AWS 财大气粗, 它没有 DockerHub 的每天 200 次的限制. 而 `lambda/python <https://gallery.ecr.aws/lambda/python>`_ 这个仓库有不同 Python 版本的基础镜像. 例如你用的如果是 Python3.9, 那么镜像的 URI 就是 ``public.ecr.aws/lambda/python:3.9``.

**安装依赖**

我们将依赖放在 ``requirements.txt`` 中. 实际情况下安装所有依赖肯定是要超过 250MB, 但是本文主要是为了学习, 所以我们就只安装一个依赖.

.. literalinclude:: ./requirements.txt
   :linenos:

**Lambda Function Source Code**

这里我们用一个简单的 Lambda Function 来测试. 代码如下. 它的目的是简单地返回一些接口的调用信息, 并打印依赖的版本来验证依赖是否安装成功.

.. literalinclude:: ./lambda_function_1.py
   :language: python
   :linenos:

**Docker File**

.. literalinclude:: ./Dockerfile_1
   :language: docker
   :linenos:

**在本地测试 Lambda Function**

AWS 提供的 Base Image 已经实现好了 Runtime interface client, 所以你可以直接在本地用 ``docker run ...`` 命令启动容器, 这个容器会暴漏 9000 端口 (你可以自己改) 给宿主机. 这个运行动作其实就是模拟 AWS 初始化 Lambda 容器的过程, 并 import 所有的依赖, 之后你只要调用这个函数即可.

.. code-block:: bash

    docker run --rm -p 9000:8080 your_container_repository_name:your_image_tag

然后你可以用下面的命令在本地把请求发送到这个接口, 从而测试 Lambda Function 是否正常工作.

不带输入的情况.

.. code-block:: bash

    curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

带输入参数的情况.

.. code-block:: bash

    curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'

**源码是一个 Python 库, 并且有多个 Lambda Function Handler 的情况**

在企业级, 比较复杂的项目中, 通常不会说让给每一个 Lambda Function 单独实现一个 python script, 或是单独开一个项目. 最佳实践是把相关的 Lambda Function 放在一个项目中, 然后开发一个 Python 库, 把核心逻辑都放在这个库中方便进行充分的单元测试, 然后用一个 ``lambda_function.py`` import 核心逻辑并封装成简单的 ``def lambda_handler_1(event, context):``, ``def lambda_handler_2(event, context):``, ``def lambda_handler_3(event, context):`` 这样的函数.

之前介绍 Dockerfile 的内容时我们说了, 我们需要指定一个 ``CMD``, 它的值要是我们的 Lambda handler 的接口. 但是我们一个项目中一套代码有三个接口, 难道我们要构建三个容器吗? 这里我们来详细讲解一下实际生产项目中的最佳实践.

**用一个容器部署多个 Lambda Function**

查阅以下常用的三种部署 AWS Lambda 的官方工具可以得知, 它们都有一个 ``Code`` 参数, 可以指定 ImageUri, 还有一个 ``ImageConfig`` 参数, 可以 Override ``EntryPoint``, ``Command``, ``WorkingDirectory``, 这就给我们提供了很多灵活性. 我们可以用一个容器镜像, 不管 Dockerfile 里面的 CMD 是什么, 这里我们都 override 成我们需要的 handler. 例如 ``lambda_function_1.lambda_handler_1``, ``lambda_function_1.lambda_handler_2``, ``lambda_function_1.lambda_handler_3``. 这样我们就可以只构建一次镜像, 但部署成多个 Lambda Function.

- `boto3 AWS Python SDK lambda.create_function <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/create_function.html>`_
- `CloudFormation AWS::Lambda::Function <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html>`_
- `AWS CDK AWS::Lambda::Function construct <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html>`_

**用一个容器对多个 Lambda Function** 进行测试

前面我们介绍了用 ``docker run --rm -p 9000:8080 your_container_repository_name:your_image_tag`` 命令在本地运行容器并对其进行测试, 但是这个命令是无法 Override CMD, 我们又要如何对多个 Lambda Function 进行测试呢?

其实很简单, 你只需要稍微修改一下你的 ``lambda_function.py`` 脚本, 把所有的 lambda function handlers 封装到一个新的函数中. 这个新的函数就是一个新的 Lambda function handler, 并且能够用参数选择运行底层的哪个 lambda function handlers.

.. literalinclude:: ./lambda_function_1.py
   :language: python
   :linenos:

如果原本的 handler 1 的 event 应该是 ``{"name": "alice"}``, 那么对应的新 event 就是 ``{"handler": "handler_1", "event": {"name": "alice"}}``

.. code-block:: bash

    curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"handler": "handler_1", "event": {"name": "alice"}}'


2. Example
------------------------------------------------------------------------------

.. code-block:: bash

    # build docker image
    docker build -t hello-world .

    # run container at port 9000 to take http request invokation
    docker run -p 9000:8080 hello-world

    # test lambda function locally
    curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

    # login to AWS ECR
    AWS_ACCOUNT_ID="$(aws sts get-caller-identity | jq '.Account' -r)"
    AWS_REGION="us-east-1"
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

    # create "hello-world" docker image repository
    aws ecr create-repository --repository-name hello-world --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

    # tag the newly built image
    docker tag hello-world:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/hello-world:latest

    # push to AWS ECR
    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/hello-world:latest

Then you can create a Lambda function from docker image and run test event.


3. Understand the AWS Lambda Base Image
------------------------------------------------------------------------------

docker run --rm --name dev public.ecr.aws/lambda/python:3.8 ls /var
docker run --rm -dt --name dev lambci/lambda:build-python3.8 pwd ~
docker exec -it dev bash
docker container stop dev


Reference
------------------------------------------------------------------------------
- `Using container images with Lambda <https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html>`_: 使用容器部署 Lambda 的开发者文档.