AWS CloudFormation Custom Resources
==============================================================================
Keywords: AWS, Amazon, CloudFormation



What is AWS CloudFormation Customer Resources
------------------------------------------------------------------------------
首先我们回顾一下 CloudFormation 解决了什么问题. CloudFormation 用了一种声明式的语言, 定义了每个 AWS Resources 应该处于一种什么状态. 这里的状态通常是这个 Resource 的一些属性, 例如 EC2 的 Security Group, S3 Bucket 的 Bucket Policy. 如果不用 CloudFormation, 我们往往连续调用 ``create``, ``describe``, ``update``, ``delete`` API 来确保最终 Resource 的状态是我们想要的. 这里的 API 可以是 create_ec2, create_vpc, create_s3_bucket 任何资源. 有的 API 调用还不是瞬间完成的, 往往需要进行等待, 例如创建一个 EC2. 如果开发者自己实现这一逻辑, 将会是地狱级的难度. 而 CloudFormation 服务把复杂的逻辑交给 AWS 处理, 我们只需要定义我们想要的最终状态即可.

虽然 CloudFormation 有很多函数可以在一个个创建资源的过程中进行一些简单计算, 但是如果是复杂的计算, 或者涉及到对 AWS 之外的资源, CloudFormation 就无能为力了. 例如你是一个 IT 软件公司, 你给你的客户提供了一个 CloudFormation 用来在客户的 AWS Account 中部署你所提供的软件. 例如第一步是创建网络等基础设施, 而第二步就是用客户部署时候填写的他付费获得的 API Key, 根据这个 API Key 你才能给客户的 AWS Account 授予一些权限, 或者在你的 S3 中创建一些软件服务器的镜像提供给客户. 而这些授权, 和创建资源等行为是 CloudFormation 做不到的.

**Custom Resources** 是 CloudFormation 的一个功能. 它允许用户定义一个 Custom Resource, 这个 Resource 并不由这个 Custom Resource 的声明代码而创建 , 而是一个已经存在的 Resource. 目前这个 Resource 只能是 Lambda Function 和 SNS Topic. 当 CloudFormation 引擎执行到 Custom Resource 的时候, 就会给这个 Resource 后端发送一个 HTTP Request, 其中这个 Request 有一个重要字段是 ``ResponseURL``. 这个 Resource 要除了负责实现你所需的业务逻辑之外, 还要对这个 ``ResponseURL`` 发送一个 HTTP Post 的 Request, 这个 Request 要告诉 CloudFormation 你的逻辑 SUCCESS 还是 FAILED, 以及可以发送任意的 JSON Key Value Pair 对象作为这个 Resource 的 Attribute, 以供 CloudFormation 后面的 Resource 所使用. 由于 AWS Lambda Function 几乎可以用来做任何事, 所以这个机制就实现了在 CloudFormation 执行到一半的时候可以用复杂的代码做任何事.

这么说你可能只有一个模糊的感觉, 相信你看完下面这个例子后, 就会有一个很清晰的理解了. 还是上面的例子, 你是一个 IT 软件公司, 这个 CloudFormation 是用来在你的客户的 AWS Account 中部署软件. 你的 CloudFormation 逻辑是:

1. 创建基础设施, 例如网络.
2. 根据用户填写的 API Key 获取服务器镜像的网络连接.
3. 将服务器镜像部署到 AWS.

显然这里的难点是 2, 而这部分的逻辑需要写代码处理, CloudFormation Template 本身是无法实现这些业务逻辑的.

**而使用了 Custom Resource 之后的流程则是**:

1. 创建基础设施, 例如网络.
2. 把用户填写的 API Key 发送给 Custom Resource 所对应的 Lambda Function.
3. Lambda Function 鉴权之后将镜像的地址通过 HTTP Post 发送到 ``ResponseURL``, 告知 CloudFormation 这一步 SUCCESS.
4. 后续的步骤就可以通过这个 Custom Resource 的 Attribute 获取到镜像地址了.
5. 将服务器镜像部署到 AWS.


Request Object
------------------------------------------------------------------------------
下面是 CloudFormation 发送给 Custom Resource 的 Request JSON body. 如果是 Lambda Backed Resource, 以 Python 为例, 那么 ``def lambda_handler(event, context):`` 中的 event 的内容就是这个. 关于里面的每个字段的解释可以看 `这篇官方文档 <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html>`_. 其中 ``ResponseURL`` 是你需要将结果发送到的 URL. 而 ``ResourceProperties`` 则是你的 CloudFormation 中定义的 Custom Resource
 Properties 中除了 ServiceToken 的其他 Key Value Pair. 也就是你用来传递自定义参数的机制.

.. code-block:: javascript

    {
        "Type": "Custom::ResourceName",
        "Properties": {
            "ServiceToken": "arn:aws:lambda:us-east-1:111122223333:function:lbd_func_name",
            "Key1": "Value1",
            "Key2": "Value2"
        }
    },

下面是一个 Request Object 的例子.

.. code-block:: javascript

    {
       "RequestType" : "Create",
       "ResponseURL" : "http://pre-signed-S3-url-for-response",
       "StackId" : "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
       "RequestId" : "unique id for this create request",
       "ResourceType" : "Custom::TestResource",
       "LogicalResourceId" : "MyTestResource",
       "ResourceProperties" : {
            "Key1": "Value1",
            "Key2": "Value2"
       }
    }


Response Object
------------------------------------------------------------------------------
下面是你的 Custom Resource 需要给 ``ResponseURL`` 发送的 POST request 的 JSON body. 如果是 Lambda Backed Resource, 以 Python 为例, 那么用 Request 库发送 ``requests.post(response_url, body=json.dumps(payload)`` 中的 payload 的内容就是这个. 关于里面的每个字段的解释可以看 `这篇官方文档 <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html>`_

下面是一个 Response Object 的例子.

.. code-block:: javascript

    {
       "Status" : "SUCCESS",
       "PhysicalResourceId" : "TestResource1",
       "StackId" : "arn:aws:cloudformation:us-west-2:123456789012:stack/stack-name/guid",
       "RequestId" : "unique id for this create request",
       "LogicalResourceId" : "MyTestResource",
       "Data" : {
          "OutputName1" : "Value1",
          "OutputName2" : "Value2",
       }
    }

其中 ``Status`` 如果不是 SUCCESS 则 CloudFormation 则认为这一步创建 Custom Resource 失败, 并停止后续的步骤. 而 ``Data`` 则是任何自定义的数据结构, 这些数据结构会被作为 Custom Resource 的 Attribute 返回给 CloudFormation, 并且可以用 ``GetAtt`` Intrinsic Function 读取到里面的值. 例如你的 CloudFormation template 要创建一个 EC2, 而你要用 Custom Resource 来获取这个 AMI ID. 你的 CloudFormation Template 长这样:

.. code-block:: javascript

    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "GetEC2AmiId": {
                "Type": "Custom::IamGroupInfo",
                "Properties": {
                    "ServiceToken": "arn:aws:lambda:us-east-1:111122223333:function:lbd_func_name",
                    "Key1": "Value1",
                    "Key2": "Value2"
                }
            },
            "MyEC2Instance": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "ImageId": {"Fn::GetAtt": ["GetEC2AmiId", "ami_id"]}
                },
                "DependsOn": "IamGroupInfo"
            }
        }
    }

而你发送的 Response Object 长这样:

.. code-block:: javascript

    {
       "Status" : "SUCCESS",
       "PhysicalResourceId" : "...",
       "StackId" : "...",
       "RequestId" : "...",
       "LogicalResourceId" : "...",
       "Data" : {
          "ami_id" : "a1b2c3"
       }
    }

可以看出 Response Object 中的 ``Data`` 字段包含了 ami_id 的信息. 然后里面的 key 都变成了 ``GetEC2AmiId`` 这个 Custom Resource 的 Attribute, 所以你在后续创建 EC2 的 ``MyEC2Instance`` 中就可以用 ``{"Fn::GetAtt": ["GetEC2AmiId", "ami_id"]}`` 来获取 AMI ID 了


Customer Resource Call Lambda Function in Another Account
------------------------------------------------------------------------------
上面的软件交付案例是 Custom Resource 的常见使用场景. 但客户的 CloudFormation 所在的 AWS Account 一般和你作为软件提供方的 Lambda Function 所在的 AWS Account 不同, 它们可以互相通信么? 答案是可以, 你需要做如下设置:

1. 你的 Lambda Function 和 CloudFormation 所在的 Region 必须相同.
2. 你的 Lambda Function 需要定义 Resource Based Policy 定义了允许客户的 AWS Account 跟它通信.

详情请参考 `How can I use a Lambda function created in one AWS account with an AWS CloudFormation custom resource in another AWS account? <https://repost.aws/knowledge-center/cloudformation-lambda-custom-resource>`_ 这篇 Repost
一般你会将 Lambda Function
R


Custom Resources 软件交付场景中的应用
------------------------------------------------------------------------------
上面的软件交付案例是 Custom Resource 的常见使用场景. 下面介绍了我在使用 Custom Resource 进行软件交付时的一些经验:

1. 你给客户的 CloudFormation 中的前面部分就要负责创建这个 Lambda handler.
2. 这个 Customer resource Lambda handler 里面的逻辑尽可能的简单.
    - 凡是鉴权的逻辑应该让这个 Lambda handler 发送请求给你的公司 API, 而不要写在 Lambda handler 的逻辑里.
    - 如果你需要为客户在你的公司的 Account 而不是客户的 Account 上创建资源, 这些工作交给 Lambda handler 调用你公司的 API 进行.
3. 如果 Lambda handler 的逻辑是 15 分钟都搞不定的, 那么你可以用 CloudFormation 从 S3 Zip 文件 (这个文件的 Key 由 Lambda handler 获得) 创建 CodeCommit repo, 然后创建 CodeBuild project, 把长的业务逻辑交给 CodeBuild 来运行, 从而获得大约 8 小时的 build 时间. 用 Lambda handler 获得 S3 Zip 的原因是我们希望保护我们的自动化部署的代码. 而如果觉得只需要保护你的软件代码就行, 自动化部署的代码不那么重要, 那么你可以创建 Public CodeCommit repo 或是 GitHub repo, 把一切都参数化, 然后只创建 CodeBuild Project 进行构建即可.


Sample Code
------------------------------------------------------------------------------
Sample CloudFormation Template

.. literalinclude:: ./template.json
   :language: json
   :linenos:

Sample Lambda Function

.. literalinclude:: ./lambda_function.py
   :language: python
   :linenos:

Automation Script to Deploy CloudFormation

.. literalinclude:: ./deploy_cf.py
   :language: python
   :linenos:
