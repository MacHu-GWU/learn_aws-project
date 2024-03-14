Knowledge Base For Amazon Bedrock
==============================================================================
Keywords: AWS, Amazon, Bedrock, GenAI


Overview
------------------------------------------------------------------------------
Knowledge Base 的本质不是说用你的知识库来训练一个新模型, 而是让已有的基础模型在生成回答的时候, 利用知识库中的信息, 来生成更加准确的回答. 这种技术做 `Retrieval-Augmented Generation (RAG) <https://aws.amazon.com/what-is/retrieval-augmented-generation/>`_. 和 Custom Model 有着本质区别.

Knowledge Base For Amazon Bedrock 是一项 AWS 的全托管功能. 你只需要将文件上传到 S3, 然后选择一个 Embedding Storage, 一般是用 OpenSearch (Knowledge base 的知识会以 vector embedding 的形式存在), 然后每次更新知识库的时候就调用一次 API 重新 Index 既可. 注意这里的 Reindex 是 Incremental 的, 例如你已经有 1000 个文档了, 然后你增加了 1 个新文档, 你只需要对这一个新文档进行 embedding (我对此表示怀疑, 我觉得新文档可能会改变已有的 token 的权重, 可能还是隔一段时间需要重新 index 一遍).


Reference
------------------------------------------------------------------------------
- `Knowledge Base <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>`_
- `Custom Model <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>`_


