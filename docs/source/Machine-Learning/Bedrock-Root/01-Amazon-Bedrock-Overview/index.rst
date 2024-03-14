Amazon Bedrock Overview
==============================================================================
Keywords: AWS, Amazon, Bedrock, GenAI


What is Amazon Bedrock
------------------------------------------------------------------------------
在 2022 年 11 月, OpenAI 发布了 ChatGPT, 被誉为第四次工业革命的技术就这么突然的来到了公众面前, 变得人人都触手可得. 作为商业云的龙头 Amazon 自然也不甘示弱, 在 2023 年 9 月, 推出了 Amazon Bedrock 服务, 用于帮助企业快速构建和部署基于 Large Language Model (LLM) / Generative AI (下面我们统称为 GenAI, 提到 GenAI 的同时也附带包含了 LLM) 的应用. 我们目前没有一个很好的词和术语来概括 Amazon Bedrock 到底是什么, 因为这个领域太新了, 变化太快了. 但是简单来说, Bedrock 是一款能把大语言模型变得跟传统的线性回归这种简单机器模型一样易用的云服务. 并且和 AWS 先进的网络基础设施, 权限管理工具, 数据安全架构, 以及监控工具深度整合, 解决了使用第三方 GenAI 服务的时候最让企业担心的数据安全, 以及权限管理的问题. 使得模型完全被企业掌控, 并且能在企业的私有网络环境中运行.

在我看来 OpenAI 可能代表着目前大语言模型和 GenAI 的领先方向, 但 AWS Bedrock 则是将其做成了一个人人可用, 安全有保障的企业级产品.


Amazon Bedrock Core Feature
------------------------------------------------------------------------------
这里我们假设你已经有一定的 GenAI 的知识. 对大语言模型中的 Token, Prompt, Response 有一定的基础了解. 下面我们来看看 Bedrock 的核心功能, 以及这些核心功能在企业级的 GenAI 的应用场景中的重要性.

1. Foundation Model (FM): bedrock 提供了一系列基础模型. 你可以轻松的跟这些模型在 Playground 中进行测试. 这些模型有:
    - Amazon 自己的 Titan. 能够 text / gen image
    - 由 Amazon 和 Google 注资 (amazon 为主) 的 Anthropic 公司的 Claude. 能够 text, vision
    - 加拿大的 AI 公司 Cohere 的 Command / Embedd. 能够 text.
    - 以色列的 AI 公司 AI21 Labs 的 Jurassic. 能够 text.
    - Meta 的 Llama. 能够 text.
    - 在马里兰的小团队 AI 公司 Mistral AI 的 Mistral. 能够 text.
    - Stability AI 的 Stable diffusion. 能够 image.
2. Custom Model: bedrock 允许你在 FM 的基础上, 用私有数据对模型进行进一步的训练. 它有两种方式 continued pre-training 和 fine-tuning. 由于无论是模型还是数据, 训练还是部署, 还是 API 调用, 全部都在 AWS 的环境内, 对于企业来说数据安全有绝对的保障, 这也是企业用户的核心需求.
    - Continued pre-training: 你可以用 **Unlabeled** data 来让 FM 熟悉一些公开渠道没有的知识, 例如企业内部的文档和数据.
    - Fine-tuning: 你可以用 **Labeled** data 来让 FM 熟悉一些特定的任务, 例如客服对话, 金融数据分析, 以及医疗数据分析. 主要是说对于特定的输入, 它应该给出什么样的输出. 这会修改 pre-trained 中的权重.
3. Knowledge Base: 你可以给你的模型制定一个 knowledge base, 使得模型在输出的时候会考虑, 使用, 引用这个 knowledge base 中的信息. 这种技术叫做 `retrieval augmented generation (RAG) <https://aws.amazon.com/what-is/retrieval-augmented-generation>`_. 它的底层是将 knowledge base 的 data 放在 S3 中, 然后将信息以 embedding 的形式 index 到 vector database 中使得 FM 可以使用. 通常是用 Amazon OpenSearch 来做. 并且 Amazon 有全托管式的 ETL 服务, 能够当你的数据更新时自动更新 knowledge base.

    这个功能解决了企业用户担心把自己的私有数据交给 GenAI 的数据安全问题. 这是大部分企业对 GenAI 持观望态度的核心原因. 由于这些模型本身就在 AWS 环境内, 而 AWS 的网络, 数据, 权限管理都很成熟, 而且这个模型也是企业内部私有的, 不用担心数据泄露给 AWS 以及其他用户. 其次, 你无需搭建一套 ETL pipeline 以及 vector database 来存你的私有数据, 这些在 AWS 生态里都非常成熟.

4. Agent: 可以让你用 GenAI 来做一些平时需要用程序和调 API 才能做的工作. 你只要写好 Prompt, 定义一个 OpenAPI spec, 然后配置好后端的 Lambda Function. 它就会根据你的输入判断你的意图, 并且自动生成一个执行方案, 并且智能的判断是不是这一步需要调 API, 以及如何生成 API 的 request 参数, 以及如何解读 API 的 response, 并将其转化成一个人类可读的回答. 并且这个 Lambda Function 还可以调用 Step Function 来执行一些更复杂的业务流程.

    我认为该功能是企业 AI 应用中的杀手功能. 并且 Amazon bedrock agent 它把 Agent 和底层的 Action 解耦和了. 这意味着你能底层的各种细粒度的 Task 都用 API 封装成 Action, 然后让 Agent 来使用一个或多个 Action, 使其能够复用. 最后将多个 Agent 组合起来成为一个完整的 App. 这种架构方式天然适合复用, 是比较成熟的生产可用的架构, 完全符合企业的需求.




Learning Resources
------------------------------------------------------------------------------
- `Amazon Bedrock 主页 <https://aws.amazon.com/bedrock/>`_:
- `Amazon Bedrock Workshop <https://catalog.us-east-1.prod.workshops.aws/workshops/a4bdb007-5600-4368-81c5-ff5b4154f518/en-US>`_: 一个 AWS 官方的 Workshop 系列.
- `Training - Building Generative AI Applications Using Amazon Bedrock <https://explore.skillbuilder.aws/learn/course/external/view/elearning/17904/building-generative-ai-applications-using-amazon-bedrock>`_: 一个 AWS 官方的培训.


Reference:

- `bedrock <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock.html>`_: 主要是对 bedrock 中的 model 进行管理. 创建, 删除, 更新, 查询等.
- `bedrock-runtime <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html>`_: 主要是跟 model 进行输入输出的交互.
- `bedrock-agent <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html>`_: 主要是对 bedrock 中的 agent 进行管理. 创建, 删除, 更新, 查询等.
- `bedrock-agent-runtime <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html>`_: 主要是跟 agent 进行输入输出的交互.
