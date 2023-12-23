ML Model Management System Architect
==============================================================================
Model Catalog Data Store

.. code-block:: python

    {
        "namespace": "/abc_corp/claim",
        "model_name": "doc_classification",
        "description": "this model is designed for ...",
        "owner": "alice@example.com",
        "url": "http://abc.corp.com/path/to/the/model/implementation",
        # below are details about the model, they can be maintained at:
        # 1. stored in the metadata store
        # 2. stored in the document file in Git
        # 3. stored in the document file and automatically loaded into the metadata store
        "data_sources": [
            {
                "name": "claim history datawarehouse"
                "type": "snowflake",
                "description": "...",
                "owner": "alice@example.com",
                "connection": {
                    "...": "..."
                }
            },
            {
                "name": "more data source",
            },
        ]
        "inference": {
            "input": {
                "description": "..."
                "schema": {},
            },
            "output": {
                "description": "..."
                "schema": {},
            },
        },
    }

Model Registry Metadata Store

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

Model Deployment Metadata Store

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

Reference:

- Best Machine Learning Model Management Tools That You Need to Know: https://neptune.ai/blog/best-machine-learning-model-management-tools
- MLOps: Model management, deployment, and monitoring with Azure Machine Learning: https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment?view=azureml-api-2