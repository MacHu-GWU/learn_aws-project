Amazon Neptune Overview
==============================================================================
Keywords: AWS, Amazon, Neptune, Graph Database


What is Amazon Neptune
------------------------------------------------------------------------------
Neptune 是 AWS 推出的闭源云原生图数据库. 它的主要卖点是完全托管, 几乎无运维, 并支持 Serverless 自动弹性伸缩. 以及它能紧密地和各种 AWS 强大的黑科技无缝衔接, 例如跟 OpenSearch 一起提供全文搜索, 跟 SageMaker 一起提供 ML. 他支持主流的 Property Graph 和 RDF 数据模型, 以及 Gremlin, OpenCypher 和 SPARQL 查询语言. 除此之外, 它还提供基于 Notebook 基于 Neptune Workbench



AWS Neptune Workbench and Notebook
------------------------------------------------------------------------------
市场上有很多的传统的关系数据库开发工具, 例如微软的 SQL Workbench, 开源的 Dbeaver 等. 对于非关系数据库例如 MongoDB 或者 DynamoDB 也一般会有一个 GUI 以让用户能更方便地进行交互式的, 探索性的工作. 但是这些 GUI 软件一般只支持简单的 SQL, 并不具备通用性编程能力.

Neptune Workbench 是一个基于 JupyterLab 的 IDE, 里面内置了各种工具能让你使用 Jupyter Notebook 进行 Neptune 开发. 这里工具可不仅仅是一个 Python 环境, 而是集成了 germlin, openCypher, sparql + Jupyter Notebook 的功能, 你可以直接在 JupyterNotebook 中用 % magic 语法运行这些图数据库的查询语言, 并在 Notebook 中以用户友好的 HTML 格式展示结果, 并提供一些简单的 Widget. 我个人觉得这个功能简直是太牛了, 用 % magic 提供了轻量的 GUI 界面, 而用 JupyterNotebook 提供了通用编程能力. 不仅如此, 而且这个 Notebook 用 IAM Role 直连 Neptune, 无需用户手动用编程语言创建数据库连接.

这个工具的底层其实是 SageMaker Notebook, 只不过是为 Graph 工作预装了所需的软件而已, 但是对于用户的价值却是很大的.


AWS Neptune Serverless
------------------------------------------------------------------------------
由于 Neptune 存算分离的架构, Neptune 还提供了 Serverless 选项. 由于存储非常便宜而且可以视为无限, 你只需要弹性伸缩计算的部分即可. 只需要指定最小的 Neptune Capacity Units (NCUs) 和最大的 NCUs, (最小值为 1, 最大值为 128), AWS 就会根据负载自动弹性伸缩. 一个 NCU 大约相当于 2GB 内存, 换言之一个 NCU 数据库的最大体量是 256GB 内存.


Neptune Full Text Search
------------------------------------------------------------------------------
