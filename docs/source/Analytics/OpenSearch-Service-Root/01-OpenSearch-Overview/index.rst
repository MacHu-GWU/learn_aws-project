.. _aws-opensearch-overview:

Amazon OpenSearch Overview
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Overview.


Background
------------------------------------------------------------------------------
自 2010-02-08 年发布以来 ElasticSearch (ES) 是行业内支持商用的免费开源的搜索数据库的事实标准. AWS 作为云服务商, 拿了 ES 的源码构建了自己的全托管免运维的 ES 集群服务. 而 ES (同名公司) 作为开源软件后面的商业公司, 自然也是靠提供部署运维服务盈利的, 这就产生了严重的商业冲突.

于是 ES 在 2021 年修改了开源协议, 使用了一版它们自己的 Server Side Public License (SSPL) 协议. 简而言之就是自己用可以, 但是拿去卖服务器部署托管运维服务不行. 这个协议不是被开源组织认同的标准协议.

因为开源协议改变的原因, AWS 在 2021 年以 7.10 版本为基准, Fork 了一个由 AWS 维护的版本并且声明永远开源. 并推出了 AWS 托管的 OpenSearch Service 服务以及无服务器, 自动扩容的 OpenSearch Serverless 版本.


How to Learn Amazon OpenSearch
------------------------------------------------------------------------------
OpenSearch 主要包括由社区提供的官方文档, 以及 AWS OpenSearch 服务相关的文档两部分.

- `OpenSearch Org Document <https://opensearch.org/docs/latest/>`_: 由社区维护的 OpenSearch 项目官方文档.
- `Amazon OpenSearch FAQ <https://aws.amazon.com/opensearch-service/faqs/>`_: 常见问题.
- `Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html>`_: AWS OpenSearch 服务的官方文档.
- `Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html>`_: AWS 的 Serverless 部署模式的官方文档.

我建议直接在你的 AWS Account 里创建一个 OpenSearch serverless, 然用 Python 中的


OpenSearch Knowledge Graph
------------------------------------------------------------------------------
以下是 OpenSearch 的知识图谱, 对所有的知识点进行了一个梳理.

- OpenSearch Cluster:
    - Concepts:
    - Management:
        - Create, Connect
        - Choose the right sizing
        - Security
- OpenSearch Serverless
    - Concepts:
    - Management:
        - Create, Connect
        - Security
- Development:
    - Query DSL


What's Next
------------------------------------------------------------------------------
todo
