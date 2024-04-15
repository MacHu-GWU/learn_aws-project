LLM Observability 101
==============================================================================


Background
------------------------------------------------------------------------------
在企业级机器学习应用领域 ML Model Visibility (或 Observability) 是一个必不可少的模块. 它和传统的软件 App 的 Logging, Tracing 系统类似. 只不过对于 ML 系统, 特别是深度学习模型, 整个输入输出一般不可解读, 像一个黑盒子, 所以对 ML Model Visibility 变得尤为重要, 不然可能会导致整个模型失控. 而对于 LLM, 模型不可解释的问题就变得更为严重, 没人知道模型内部是怎么思考的, 所以 LLM Observability 的很多核心技术跟传统的 Observability 框架区别很大. 本文档是我在研究如何搭建一个企业级的 LLM Observability 的系统时记的笔记.

我在开始研究的时候, 选择从 Arize, 一个 AI Observability Platform 的初创公司, 的一个 white paper 开始学习, 了解这个领域有哪些概念, 哪些技术. 然后我再一步步深入了解, 最后自己消化之后总结形成本文.

- `Arize LLM Observability 101 <https://arize.com/wp-content/uploads/2023/11/LLM-Observability-101-1.pdf>`_
- `Arize LLM Observability 101 Personal Google Drive Backup <https://drive.google.com/file/d/1lSUyTFK129drpSFXuYCMFXLVbGkG-waZ/view?usp=drive_link>`_


LLM Eval
------------------------------------------------------------------------------
1. 让用户直接回答 Prompt 的 input output 的 quality 怎样, 通常是一个 A/B test.
2. 对于一个特定的 Prompt, 你可以让 LLM 自己去 evaluate 这个 prompt 和 response.


Traces and Spans In Agentic Workflows
------------------------------------------------------------------------------
对于 agent workflow 类型的工作, 通常 agent 会在内部进行多步骤的推理. 对于每一个步骤, 会有一个 trace 和 span.它们的目的是追踪就是一个问答的周期内所有的中间步骤和因果关系, 而 这些 trace 和 span 可以用来评估 agent 的工作效率和质量.

Trace and Span:

    In the context of LLM (Large Language Model) observability, traces and spans are concepts borrowed from the field of distributed systems and application performance monitoring. Let me explain them in layman's terms:

    Trace:
    Imagine you have a complex task that involves multiple steps or operations. A trace is like a record or a log that captures the entire journey of that task from start to finish. It helps you understand the flow and the sequence of events that occurred during the execution of the task.

    In the case of LLMs, a trace represents the entire processing of a user's request or input. It includes all the different components, modules, or services that are involved in generating the response. The trace captures the flow of data and the interactions between these components.

    Span:
    Now, within a trace, there are smaller units of work called spans. A span represents a specific operation or a subset of the overall task. It's like breaking down the trace into smaller, more manageable pieces.

    Think of it like a chapter in a book. The entire book is the trace, and each chapter is a span. Each span focuses on a particular aspect of the task and provides more detailed information about that specific operation.

    In LLMs, spans can represent different stages of processing, such as tokenization, encoding, attention mechanism, decoding, or any other specific operation performed by the model. Spans help you dive deeper into the individual components and understand their performance, dependencies, and potential bottlenecks.

    By analyzing traces and spans, developers and system administrators can gain valuable insights into the behavior and performance of LLMs. They can identify slow or inefficient components, detect anomalies, and optimize the overall system.

    Traces and spans provide a structured way to collect and visualize data, making it easier to monitor, debug, and improve the performance of LLMs. They help in understanding the complex interactions within the model and enable effective troubleshooting and optimization.


Prompt Engineering
------------------------------------------------------------------------------


Search and Retrieval
------------------------------------------------------------------------------

Fine-Tuning
------------------------------------------------------------------------------


LLM Span Types and Their Functions
------------------------------------------------------------------------------
LLM: Call to a LLM for completion or chat.
Chain: Link between application steps
Tool: API or Function invoked on behalf of LLM
Agent: Root of a Set of LLM and Tool invocations
Embedding: Encoding of unstructured data
Retriever: Query for context from a data store
Reranker: Relevance-based re-ordering of documents