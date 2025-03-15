Contextual Retrieval
==============================================================================


Overview
------------------------------------------------------------------------------
Contextual Retrieval 是一个进阶版的 RAG 技术, 能减少 AI 的幻觉, 增加获取到的 Context 的概率. 本文是一个非常精简的介绍, 详细的介绍请参考 Anthropic 的这篇文章 `Introducing Contextual Retrieval <https://www.anthropic.com/news/contextual-retrieval>`_.


How Does RAG Work
------------------------------------------------------------------------------
要理解为传统的 Rag 是怎么工作的呢:

1. 把文档拆分成 Chunk, 比如几百个 Token 一个 Chunk, 或者一个段落为一个 Chunk. 每个 Chunk 之间有一点 overlap.
2. 对每个 Chunk 进行 Full Text Index, 使用 BM25 或者类似算法给每个 Term 不同的权重. 这个也是搜索引擎的底层算法, 主要基于词.
3. 对每个 Chunk 进行 Text Embedding, 将其转化为向量, 以适配按照文本语义相关性进行搜索, 主要基于语义.
4. 当一个 Query 进来后, 进行 Text Index 匹配和 Text Embedding 匹配, 甚至还可以进行 PageRank 等其他的匹配算法. 然后把每一项匹配的 Top K 结果拿过来一起比较, 选出最好的结果. 这个把多个匹配算法的结果融合比较的过程叫做 Reranking.
5. 然后把最好的结果作为 Context 和原本的 Query 一起交给大模型进行分析并返回结果.

扩展阅读:

- Rank Fusion = 用多个考试（数学、英语、编程）来评估学生，然后融合成绩决定谁更优秀。
- Reranking = 在最初选出的 100 名学生中，进行更细粒度的评估（面试+实战测试），最终选出前 10 名。


Why RAG Sometime Doesn't Work Well
------------------------------------------------------------------------------
这个的解释直接看 `Introducing Contextual Retrieval <https://www.anthropic.com/news/contextual-retrieval>`_ 文章中的 "The context conundrum in traditional RAG" 这一段就可以了. 简单来说就是分 Chunk 的时候这个 Chunk 本身就是一个孤立的信息而没有上下文, 导致最终的搜索结果会不好.


What is Contextual Retrieval
------------------------------------------------------------------------------
这个技术的本质就是, 针对每一个 Chunk, 让 AI 结合全文生成一些 Context 并把这一小段 Chunk 放进去, 这样每个 Chunk 的核心信息都自带 Chunk. 这样做的代价就是每一个 Chunk 都要用 AI 生成一些 Context, 需要更多的计算资源 (Prompt Cache 可以大幅降低这个的成本), 并且每个 Chunk 的大小更大了, 你的 Vector Store 要存的东西也更多了. 但是这样做的好处就是你的 RAG 结果的相关度会好很多.


Reference
------------------------------------------------------------------------------
- Anthropic News - Introducing Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval
- contextual-retrieval Python library: https://pypi.org/project/contextual-retrieval/
- Anthropic 提供的用 Lambda 实现 Contextual Retrieval 的例子: https://github.com/anthropics/anthropic-cookbook/tree/main/skills/contextual-embeddings
