Mlflow Root
==============================================================================
Keywords: mlflow, MLOps, ML, Machine Learning


Overview
------------------------------------------------------------------------------
`mlflow <https://mlflow.org/>`_ 是 databricks 公司开发并开源的用于管理机器学习生命周期的开源平台. 它提供了一组工具, 可以帮助数据科学家和工程师跟踪实验, 重现结果, 部署模型并共享代码. Mlflow 的目目标在于将机器学习过程中涉及到的步骤与操作都标准化, 管理整个机器学习工程的生命周期.

这里简单介绍一下这个框架背后的团队. 我们先将时间拉倒 2009 年. UC Berkeley AMPLab 研究出了当时最新的分布式计算引擎 Spark, 对老一代分布式计算框架 Hadoop 进行了革命, 并将其捐献给了 Apache 基金会开源. 之后 Spark 的创始人 Matei Zaharia 博士和他的团队成立了 Databricks 公司, 专注于 Spark 的商业化应用. Mlflow 则是 Databricks 公司的 AI 实验室在 2018 年的研究成果并在同年开源. 到目前 2023 年发展了 5 年, 已经逐渐成熟.

Reference:

- `mlflow 官网 <https://mlflow.org/>`_
- `Mlflow 初探 <https://juejin.cn/post/7292302859964579890>`_: 稀土掘金社区的一片博文


Mlflow OpenSource Tools
------------------------------------------------------------------------------
Mlflow 平台包含如下组件:

- `mlflow Python SDK <https://github.com/mlflow/mlflow>`_: 这是编程用的 SDK. 里面集成了众多模块. 例如打 Log 的函数, Deploy 的函数, 运行 Experiment Job 的函数, 和第三方平台集成的模块等.
- `mlflow tracking server <https://mlflow.org/docs/latest/tracking/server.html>`_: 用来监控 run job 的状态的服务器.


Mlflow Model Registry
------------------------------------------------------------------------------
在我的理解里 Model Registry 本质上跟传统软件的 Repository 没有区别. Repository 里一个个发布的对象叫做 Package, 而 Package 本质上是一堆 Artifacts 的集合. 而 Model 和 Package 是等价的概念, 同样也有一堆 Artifacts. 而 Package 和 Model 都是有 Versioning 的, 并且每个 Versioning 都是 Immutable 的.

Reference:

- `MLflow Model Registry <https://mlflow.org/docs/latest/tracking/backend-stores.html>`_:
- `Registering an Unsupported Machine Learning Model
 <https://mlflow.org/docs/latest/model-registry.html#registering-an-unsupported-machine-learning-model>`_:


Mlflow Projects
------------------------------------------------------------------------------
Mlflow Project 是对一个 ML 项目的抽象. 一个 Project 包含三个部分:

1. name:
2. entry points: 用于 inference 的接口, 一般是一个 ``.py`` 或是 ``.sh`` 脚本. 类似于 Dockerfile 中的 entry points 的概念.
3. environment: 定义了运行环境, 依赖等.

.. note::

    这跟我对 Mlflow 的抽象一致, 不过我认为 entry points 本质上是 API 的一种, 例如执行 inference 是一种 API, 获得模型 metadata 也是一种 API. 只不过 inference 是最重要的那个 API.

Mlflow 定义了一套 Project folder structure 的标准, 叫做 `Project Directories <https://mlflow.org/docs/latest/projects.html#project-directories>`_. 其中的核心是里面要有一个 ``MLproject`` YAML 文件. 里面定义了上面说的 name, entry points, environment 的各种信息.

.. note::

    跟我自己的设计一样, 也是参考 pyproject.toml 设计了一套文件结构规范.

有了这个规范, 然后把我们的模型具体实现的部分的 Python 代码和 Mlflow 框架 wire 好, 只要有了代码, 你就可以在任何 runner 上来真正执行例如 training, evaluation, register, deploy, testing 之类的工作. 官方支持在 Databricks 平台或是 K8S 上运行.

- `MLflow Projects <https://mlflow.org/docs/latest/projects.html>`_


Mlflow Model
------------------------------------------------------------------------------
Mlflow Model 是对一个 ML 模型的抽象.

一个 Mlflow Model 本质上是一个里面有很多 artifacts 的文件夹. Mlflow 规定了目录结构 Storage Format. 大概看起来长这样:

.. code-block::

    # Directory written by mlflow.sklearn.save_model(model, "my_model")
    my_model/
    ├── MLmodel
    ├── model.pkl
    ├── conda.yaml
    ├── python_env.yaml
    └── requirements.txt

其中 ``MLmodel`` 又是一个 YAML 文件, 定义了一些 metadata. 这些 metadata 会保存到后续的 Model Management Metadata Store 数据库中.


.. note::

    这又跟我自己设计的一样. 由于 ML 工作流的复杂性, 对各个步骤的抽象相当关键, 一定要留有扩展的余地.



- `Storage Format <https://mlflow.org/docs/latest/models.html#storage-format>`_

Mlflow Model Deployment
------------------------------------------------------------------------------
- Built-In Deployment Tools: https://mlflow.org/docs/latest/models.html#built-in-deployment-tools