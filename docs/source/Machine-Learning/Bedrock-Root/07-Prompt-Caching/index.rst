Prompt Caching
==============================================================================


Boosting AI Efficiency with Prompt Caching
------------------------------------------------------------------------------
Every time you send a message to an AI model, it must first process your input by tokenizing it, analyzing embeddings, and performing other transformations to make it understandable. This requires computational resources. In multi-round conversations, every new query includes not only the latest input but also the full history of prior interactions, further increasing the processing load. Prompt Cache helps optimize this by allowing you to specify which messages should be stored (cache write). In subsequent API calls, if the same message appears again, the system can recognize it as a duplicate and retrieve the pre-processed result from the cache (cache read), rather than reprocessing it from scratch. This significantly reduces computational costs, improves response times, and enhances the efficiency of AI-powered applications, especially for scenarios involving repeated prompts or structured interactions.


Reference
------------------------------------------------------------------------------
- Anthropic News - Prompt caching with Claude: https://www.anthropic.com/news/prompt-caching
- Anthropic 对 Prompt Cache 的解释 (英文版): https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Anthropic 对 Prompt Cache 的解释 (中文版): https://docs.anthropic.com/zh-CN/docs/build-with-claude/prompt-caching
- AWS Blog - Reduce costs and latency with Amazon Bedrock Intelligent Prompt Routing and prompt caching (preview): https://aws.amazon.com/blogs/aws/reduce-costs-and-latency-with-amazon-bedrock-intelligent-prompt-routing-and-prompt-caching-preview/
- AWS Bedrock Pricing (regular read/write and cache read/write): https://aws.amazon.com/bedrock/pricing/
