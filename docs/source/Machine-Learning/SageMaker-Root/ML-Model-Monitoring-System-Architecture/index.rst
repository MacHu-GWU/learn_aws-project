ML Model Monitoring System Architect
==============================================================================


CloudWatch Log Group and Log Stream Hierarchy
------------------------------------------------------------------------------
在企业中, 通常会有按照职能, 小组, 项目分的层级结构. 有的企业很扁平, 有的企业层级很复杂. 自然地就会有权限管理, 以及按照组织架构来管理资源的需求. 而 AWS 也有 Account, Region, 然后有 Log Group, Log Stream 的层级概念. 官方并没有一个推荐的最佳实践指导我们如何将公司组织架构映射到 AWS 架构中. 本节主要尝试建立一套方法论来指导这种映射关系.

**首先, 我们来理一下已有的信息**

首先, 企业中的职能, 小组, 项目层级结构因人而异, 我们是无法预测的, 我们很难说用两层的结构或是三层的结构就一定能满足某个公司的需求. 这也是这个问题的主要难点.

其次, AWS CloudWatch Log Group 的名字支持以 ``/`` 分隔的层级结构 (最多 512 个字符). 并且 `boto3.client("logs").describe_log_groups(...) <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/client/describe_log_groups.html>`_ API 支持用 prefix 来过滤. 而用字符串来描述各种层级结构是非常灵活的, 基本上无论公司的架构是几层, 都可以用字符串来描述.

根据官方文档 `Working with log groups and log streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ 中的描述. 一个 log stream 对应了一个 source. 而一个 log group 则是共享一套设置的 log stream 的集合. 参考 AWS Lambda 中的官方设置, 一个 Lambda function 在并发状态下会有多个 container 实例, 而每个实例则有一个 log stream, 可以大致得出一个部署的具体的服务器实例可以对应一个 log stream. 而一个 Lambda function 所有的 container 实例都属于一个 CloudWatch group, 可以大致得出同一个 App 下功能类似的的所有节点可以共享一个 log group.

    A log stream is a sequence of log events that share the same source. Each separate source of logs in CloudWatch Logs makes up a separate log stream.

    A log group is a group of log streams that share the same retention, monitoring, and access control settings. You can define log groups and specify which streams to put into each group. There is no limit on the number of log streams that can belong to one log group.

**映射关系**

组织架构和 AWS Account 的映射关系:

1. 每个组织架构中的节点使用不同的 AWS Account
2. 多个组织架构中的节点共享同一个 AWS Account

为了简化系统复杂度, 我建议无论使用哪种映射关系, 我们都严格的讲组织架构中的节点和 CloudWatch log Group name 进行一一映射. 例如在电商行业中, 一个负责管理库存管理的日志 IT 系统在组织架构中的位置可以是 ``IT 部门 / 库存部门 / 库存转运日志``. 于是 log group name 可以是 ``/it/inventory/transportation``. 即使库存转运团队独享一个 AWS Account, 我们一样使用这种命名格式.

.. code-block:: python

    {
        # common
        "model_name": "document_classification",
        "environment": "prod",
        "deployment_id": 1,
        "model_version": 1,
        "server_id": 1,
        # all kinds of inference transaction should have these
        "type": "inference_transaction",
        "request": {"payload_here": "..."},
        "response": {"payload_here": "..."},
        "request_size": 4096,
        "response_size": 1024,
        "start_at": "2020-01-01T00:00:00.000Z",
        "end_at": "2020-01-01T00:00:00.350Z",
        "status": "succeeded | failed | timeout | ...",
        "elapse": 350,
        "requester": {
            "principal": "arn:aws:iam::123456789012:role/document_classification_app",
            "ip": None,
            "...": "...",
        },
        # for document classification only
        "confidence": 98.05,
    }

A sample query to find slow inference transactions.

.. code-block:: python

    # A sample query to find slow inference transactions
    # log group = /abc_corp/claim/doc_classification
    # time range = (24 hours ago, now)
    fields @timestamp, @message, deployment_id, model_version, server_id, elapse
    | filter elapse >= 3000
    | sort @timestamp desc
    | limit 20

.. code-block:: SQL

    -- A sample query to find slow inference transactions
    -- model = /abc_corp/claim/doc_classification
    -- time range = (24 hours ago, now)
    SELECT
        *,
        json_extract(message, '$.elapse') AS elapse,
    FROM model_monitoring_logs t
    WHERE
        t.model_name = 'document_classification'
        AND t.measurement_type = 'inference_transaction'
        AND t.start_at >= '2023-01-01T00:00:00.000Z'
        AND t.start_at <= '2023-01-02T00:00:00.000Z'
        AND t.elapse >= 3000
    ORDER BY t.start_at DESC
    LIMIT 20;
    """

.. code-block:: python

    # asdf
    # asdf
    # index = inference_transaction
    {
        "size": 20,
        "query": {
            "term": {
                "model_name": "document_classification",
            },
            "range": {
                "start_at": {
                    "gte": "2023-01-01T00:00:00.000Z",
                    "lte": "2023-01-02T00:00:00.000Z",
                },
                "elapsed": {
                    "gte": 3000,
                },
            },
        },
        "sort": [
            {"start_at": {"order": "desc"}},
        ],
    }

Model Version Metadata

.. code-block:: python

    {
        "namespace": "/abc_corp/claim",
        "model_name": "doc_classification",
        "model_version": 1,
        "description": "this version improves here and there, so that ...",
        "artifacts": [
            {
                "name": "trained",
                "uri": "s3://abc_corp/claim/doc_classification/trained/1.tar.gz",
            },
            {
                "name": "static_data",
                "uri": "s3://abc_corp/claim/doc_classification/static_data/1.tar.gz",
            }
        ],
        "create_at": "2023-01-01T00:00:00.000Z",
        "created_by": "arn:aws:iam::123456789012:user/alice",
    }

Model Deployment Metadata

.. code-block:: python

    {
        "namespace": "/abc_corp/claim",
        "model_name": "doc_classification",
        "model_version": 3,
        "deployment_id": 1,
        "create_at": "2023-01-15T00:00:00.000Z",
        "endpoint": "https://abc.execute-api.us-east-1.amazonaws.com/doc_classification_prod",
        "environment_variables": [
            {"name": "FOO", "value": "BAR"},
            {"name": "BAZ", "value": "QUX"},
        ],
        "deployment_method": "self hosted ECS | self hosted EKS | AWS Lambda | AWS SageMaker",
        "rolling_strategy": "blue green | canory | rolling",
    }
