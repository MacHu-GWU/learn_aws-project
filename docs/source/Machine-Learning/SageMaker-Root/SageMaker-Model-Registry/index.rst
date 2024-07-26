Amazon SageMaker Model Registry
==============================================================================
Keywords: AWS, Amazon, SageMaker Model Registry


What is Model Registry
------------------------------------------------------------------------------
为了方便理解 Model Registry 的概念, 我们先来看一下 Python 的包是怎么发布和下载的.

Python 包作者在开发完一个包后会将包的元数据(如名称、版本、依赖关系等) 注册到 PyPI, 并上传包的Artifacts (通常是源码或编译后的文件). 其他开发者可以通过 PyPI 搜索和下载这些包. 这个 PyPI 就是一个 Python Package Registry. 而在容器的世界里, 开发者可以在 Docker Hub 上的 Repository 中下载 Container Image. 而这个 Docker Hub 就是一个 Registry.

同理, Model Registry 跟这些 Registry 一样, 只不过里面的内容是 ML 模型而已.


What is Amazon SageMaker Model Registry
------------------------------------------------------------------------------
而 ML 模型本质上就是由一堆静态的 Code, Metadata (训练数据, Hyper parameter 等), 和 Artifacts (weight file, configuration 等) 再加上一个装有模型的数学实现的软件库以及运行环境构成. 本质上一个 ML 模型就是 Artifacts + Runtime, 这跟传统的 App 本质上就是 Code + Runtime 没什么不同. 而如果你用虚拟机或容器部署的话, 相当于是将 Artifacts 和 Runtime 打包在一起了 (有时候特别大的 Artifacts 可能会在容器启动后下载下来而不是跟容器打包在一起)

`Amazon Sagemaker Model Registry <https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html>`_ 是 Amazon Sagemaker 的子服务, 本质上就是一个比较简化的 Registry, 使得数据科学家在不熟悉传统软件 Registry 的情况下管理 ML 模型的版本.


Key Concepts
------------------------------------------------------------------------------
Model Registry 有两个概念 Model Group 和 Model Package:

- Model Group: 就是一个为了具体业务而实现的 ML Model, 你可以理解为 Python 里的 Package. 一个 Package 有很多不同的版本
- Model Package: 则是一个模型的具体版本, 你可以理解为 Python Package 的谋个具体版本. 版本号是从 1, 2, 3, ... 这样递增的.


Register A Version
------------------------------------------------------------------------------
Reference:

- https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-version.html

.. code-block:: python

    # Specify the model source
    model_url = "s3://your-bucket-name/model.tar.gz"

    modelpackage_inference_specification =  {
        "InferenceSpecification": {
          "Containers": [
             {
                "Image": '257758044811.dkr.ecr.us-east-2.amazonaws.com/sagemaker-xgboost:1.2-1',
            "ModelDataUrl": model_url
             }
          ],
          "SupportedContentTypes": [ "text/csv" ],
          "SupportedResponseMIMETypes": [ "text/csv" ],
       }
     }

    # Alternatively, you can specify the model source like this:
    # modelpackage_inference_specification["InferenceSpecification"]["Containers"][0]["ModelDataUrl"]=model_url

    create_model_package_input_dict = {
        "ModelPackageGroupName" : model_package_group_name,
        "ModelPackageDescription" : "Model to detect 3 different types of irises (Setosa, Versicolour, and Virginica)",
        "ModelApprovalStatus" : "PendingManualApproval"
    }
    create_model_package_input_dict.update(modelpackage_inference_specification)

    create_model_package_response = sm_client.create_model_package(**create_model_package_input_dict)
    model_package_arn = create_model_package_response["ModelPackageArn"]
    print('ModelPackage Version ARN : {}'.format(model_package_arn))


Deploy Model
------------------------------------------------------------------------------
从一个已经注册号的 Model Package 部署一个模型有两种方式:

.. code-block:: python

    # 用 sagemaker SDK (高级封装 API)
    from sagemaker import ModelPackage
    from time import gmtime, strftime

    model_package_arn = 'arn:aws:sagemaker:us-east-1:12345678901:model-package/modeltest/1'
    model = ModelPackage(
        role=role,
        model_package_arn=model_package_arn,
        sagemaker_session=sagemaker_session,
    )
    model.deploy(initial_instance_count=1, instance_type='ml.m5.xlarge')

.. code-block:: python

    # 用 boto3 (底层 API)
    # 1. Create a model object from the model version
    model_name = (
        'DEMO-modelregistry-model-'
        + strftime("%Y-%m-%d-%H-%M-%S", gmtime()
    )
    print("Model name : {}".format(model_name))
    container_list = [{'ModelPackageName': model_version_arn}]

    create_model_response = sm_client.create_model(
        ModelName = model_name,
        ExecutionRoleArn = role,
        Containers = container_list
    )
    print("Model arn : {}".format(create_model_response["ModelArn"]))

    # 2. Create an endpoint configuration
    endpoint_config_name = (
        'DEMO-modelregistry-EndpointConfig-'
        + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    )
    print(endpoint_config_name)
    create_endpoint_config_response = sm_client.create_endpoint_config(
        EndpointConfigName = endpoint_config_name,
        ProductionVariants=[
            {
                'InstanceType':'ml.m4.xlarge',
                'InitialVariantWeight':1,
                'InitialInstanceCount':1,
                'ModelName':model_name,
                'VariantName':'AllTraffic'
            }
        ]
    )

    # 3. Create the endpoint
    endpoint_name = (
        'DEMO-modelregistry-endpoint-'
        + strftime("%Y-%m-%d-%H-%M-%S", gmtime()
        )
    print("EndpointName={}".format(endpoint_name))

    create_endpoint_response = sm_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name,
    )
    print(create_endpoint_response['EndpointArn'])


Model Registry Artifacts
------------------------------------------------------------------------------
这里我们来详细研究一下 SageMaker 到底在底层是如何组织一个模型的 Artifacts 的.


Create Model Package Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
这个没什么好说的, 就是注册一个模型. 模型的版本更为关键.

.. dropdown:: create_model_package_group

    .. code-block:: python

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_package_group.html
        response = client.create_model_package_group(
            ModelPackageGroupName='string',
            ModelPackageGroupDescription='string',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        )


Create Model Package
------------------------------------------------------------------------------

.. dropdown:: create_model_package

    .. code-block:: python

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model_package.html
        response = client.create_model_package(
            ModelPackageName='string',
            ModelPackageGroupName='string',
            ModelPackageDescription='string',
            InferenceSpecification={
                """
                """
                'Containers': [
                    {
                        'ContainerHostname': 'string',
                        'Image': 'string',
                        'ImageDigest': 'string',
                        'ModelDataUrl': 'string',
                        'ModelDataSource': {
                            'S3DataSource': {
                                'S3Uri': 'string',
                                'S3DataType': 'S3Prefix'|'S3Object',
                                'CompressionType': 'None'|'Gzip',
                                'ModelAccessConfig': {
                                    'AcceptEula': True|False
                                }
                            }
                        },
                        'ProductId': 'string',
                        'Environment': {
                            'string': 'string'
                        },
                        'ModelInput': {
                            'DataInputConfig': 'string'
                        },
                        'Framework': 'string',
                        'FrameworkVersion': 'string',
                        'NearestModelName': 'string',
                        'AdditionalS3DataSource': {
                            'S3DataType': 'S3Object'|'S3Prefix',
                            'S3Uri': 'string',
                            'CompressionType': 'None'|'Gzip'
                        }
                    },
                ],
                'SupportedTransformInstanceTypes': [
                    'ml.m4.xlarge'|'ml.m4.2xlarge'|...,
                ],
                'SupportedRealtimeInferenceInstanceTypes': [
                    'ml.t2.medium'|'ml.t2.large'|...,
                ],
                'SupportedContentTypes': [
                    'string',
                ],
                'SupportedResponseMIMETypes': [
                    'string',
                ]
            },
            ValidationSpecification={
                'ValidationRole': 'string',
                'ValidationProfiles': [
                    {
                        'ProfileName': 'string',
                        'TransformJobDefinition': {
                            'MaxConcurrentTransforms': 123,
                            'MaxPayloadInMB': 123,
                            'BatchStrategy': 'MultiRecord'|'SingleRecord',
                            'Environment': {
                                'string': 'string'
                            },
                            'TransformInput': {
                                'DataSource': {
                                    'S3DataSource': {
                                        'S3DataType': 'ManifestFile'|'S3Prefix'|'AugmentedManifestFile',
                                        'S3Uri': 'string'
                                    }
                                },
                                'ContentType': 'string',
                                'CompressionType': 'None'|'Gzip',
                                'SplitType': 'None'|'Line'|'RecordIO'|'TFRecord'
                            },
                            'TransformOutput': {
                                'S3OutputPath': 'string',
                                'Accept': 'string',
                                'AssembleWith': 'None'|'Line',
                                'KmsKeyId': 'string'
                            },
                            'TransformResources': {
                                'InstanceType': 'ml.m4.xlarge'|'ml.m4.2xlarge'|...,
                                'InstanceCount': 123,
                                'VolumeKmsKeyId': 'string'
                            }
                        }
                    },
                ]
            },
            SourceAlgorithmSpecification={
                'SourceAlgorithms': [
                    {
                        'ModelDataUrl': 'string',
                        'ModelDataSource': {
                            'S3DataSource': {
                                'S3Uri': 'string',
                                'S3DataType': 'S3Prefix'|'S3Object',
                                'CompressionType': 'None'|'Gzip',
                                'ModelAccessConfig': {
                                    'AcceptEula': True|False
                                }
                            }
                        },
                        'AlgorithmName': 'string'
                    },
                ]
            },
            CertifyForMarketplace=True|False,
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            ModelApprovalStatus='Approved'|'Rejected'|'PendingManualApproval',
            MetadataProperties={
                'CommitId': 'string',
                'Repository': 'string',
                'GeneratedBy': 'string',
                'ProjectId': 'string'
            },
            ModelMetrics={
                'ModelQuality': {
                    'Statistics': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'Constraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                },
                'ModelDataQuality': {
                    'Statistics': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'Constraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                },
                'Bias': {
                    'Report': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'PreTrainingReport': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'PostTrainingReport': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                },
                'Explainability': {
                    'Report': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                }
            },
            ClientToken='string',
            Domain='string',
            Task='string',
            SamplePayloadUrl='string',
            CustomerMetadataProperties={
                'string': 'string'
            },
            DriftCheckBaselines={
                'Bias': {
                    'ConfigFile': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'PreTrainingConstraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'PostTrainingConstraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                },
                'Explainability': {
                    'Constraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'ConfigFile': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                },
                'ModelQuality': {
                    'Statistics': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'Constraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                },
                'ModelDataQuality': {
                    'Statistics': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    },
                    'Constraints': {
                        'ContentType': 'string',
                        'ContentDigest': 'string',
                        'S3Uri': 'string'
                    }
                }
            },
            AdditionalInferenceSpecifications=[
                {
                    'Name': 'string',
                    'Description': 'string',
                    'Containers': [
                        {
                            'ContainerHostname': 'string',
                            'Image': 'string',
                            'ImageDigest': 'string',
                            'ModelDataUrl': 'string',
                            'ModelDataSource': {
                                'S3DataSource': {
                                    'S3Uri': 'string',
                                    'S3DataType': 'S3Prefix'|'S3Object',
                                    'CompressionType': 'None'|'Gzip',
                                    'ModelAccessConfig': {
                                        'AcceptEula': True|False
                                    }
                                }
                            },
                            'ProductId': 'string',
                            'Environment': {
                                'string': 'string'
                            },
                            'ModelInput': {
                                'DataInputConfig': 'string'
                            },
                            'Framework': 'string',
                            'FrameworkVersion': 'string',
                            'NearestModelName': 'string',
                            'AdditionalS3DataSource': {
                                'S3DataType': 'S3Object'|'S3Prefix',
                                'S3Uri': 'string',
                                'CompressionType': 'None'|'Gzip'
                            }
                        },
                    ],
                    'SupportedTransformInstanceTypes': [
                        'ml.m4.xlarge'|'ml.m4.2xlarge'|...,
                    ],
                    'SupportedContentTypes': [
                        'string',
                    ],
                    'SupportedResponseMIMETypes': [
                        'string',
                    ]
                },
            ],
            SkipModelValidation='All'|'None',
            SourceUri='string',
            SecurityConfig={
                'KmsKeyId': 'string'
            },
            ModelCard={
                'ModelCardContent': 'string',
                'ModelCardStatus': 'Draft'|'PendingReview'|'Approved'|'Archived'
            }
        )



.. dropdown:: create_model

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/create_model.html
    response = client.create_model(
        ModelName='string',
        PrimaryContainer={
            'ContainerHostname': 'string',
            'Image': 'string',
            'ImageConfig': {
                'RepositoryAccessMode': 'Platform'|'Vpc',
                'RepositoryAuthConfig': {
                    'RepositoryCredentialsProviderArn': 'string'
                }
            },
            'Mode': 'SingleModel'|'MultiModel',
            'ModelDataUrl': 'string',
            'ModelDataSource': {
                'S3DataSource': {
                    'S3Uri': 'string',
                    'S3DataType': 'S3Prefix'|'S3Object',
                    'CompressionType': 'None'|'Gzip',
                    'ModelAccessConfig': {
                        'AcceptEula': True|False
                    }
                }
            },
            'Environment': {
                'string': 'string'
            },
            'ModelPackageName': 'string',
            'InferenceSpecificationName': 'string',
            'MultiModelConfig': {
                'ModelCacheSetting': 'Enabled'|'Disabled'
            }
        },
        Containers=[
            {
                'ContainerHostname': 'string',
                'Image': 'string',
                'ImageConfig': {
                    'RepositoryAccessMode': 'Platform'|'Vpc',
                    'RepositoryAuthConfig': {
                        'RepositoryCredentialsProviderArn': 'string'
                    }
                },
                'Mode': 'SingleModel'|'MultiModel',
                'ModelDataUrl': 'string',
                'ModelDataSource': {
                    'S3DataSource': {
                        'S3Uri': 'string',
                        'S3DataType': 'S3Prefix'|'S3Object',
                        'CompressionType': 'None'|'Gzip',
                        'ModelAccessConfig': {
                            'AcceptEula': True|False
                        }
                    }
                },
                'Environment': {
                    'string': 'string'
                },
                'ModelPackageName': 'string',
                'InferenceSpecificationName': 'string',
                'MultiModelConfig': {
                    'ModelCacheSetting': 'Enabled'|'Disabled'
                }
            },
        ],
        InferenceExecutionConfig={
            'Mode': 'Serial'|'Direct'
        },
        ExecutionRoleArn='string',
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        VpcConfig={
            'SecurityGroupIds': [
                'string',
            ],
            'Subnets': [
                'string',
            ]
        },
        EnableNetworkIsolation=True|False
    )





Links
------------------------------------------------------------------------------
- Catalog Models with Model Registry: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html
- Deploy a Model from Registry: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html