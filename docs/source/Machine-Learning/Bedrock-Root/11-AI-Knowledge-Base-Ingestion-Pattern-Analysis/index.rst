AI Knowledge Base Ingestion Pattern Analysis
==============================================================================


Introduction: The Knowledge Base Ingestion Challenge
------------------------------------------------------------------------------
We would like to discuss the AI knowledge-based ingestion pattern in this document. First, let's understand the ingestion process. Our **Source** knowledge typically resides in document systems such as SharePoint, Google Drive, Confluence, GitHub, or GitLab repositories. These constitute our source systems. The final target is an AI knowledge base implemented as a **Vector Store**, which could be OpenSearch, PingKong, PGVector, MongoDB Vector, or similar solutions. This document introduces the key patterns we've identified, analyzes which approach works best in different scenarios, and presents our recommendations.


Core Patterns: Push vs. Pull Architectures
------------------------------------------------------------------------------
When moving data from source to target, two fundamental patterns exist: push and pull. The push pattern triggers a data processor to synchronize data whenever a change occurs in the source system. The pull pattern deploys a scheduled processor that periodically scans the source data, calculates the delta, and performs incremental updates. While full snapshot updates are sometimes used at project initiation, we focus on incremental approaches due to the cost implications for AI processing.


Source System Limitations: The Need for Intermediate Storage
------------------------------------------------------------------------------
Not all source systems support push mechanisms. Most systems support pull operations, but lack change event notifications. For example, SFTP servers only allow manual data retrieval, and platforms like Confluence have complex webhook integration requirements. To address these limitations, we recommend implementing intermediate storage—typically AWS S3—to clone the source documents while maintaining their hierarchy. This approach provides flexibility as S3 supports both notification events (push) and unrestricted API access (pull), overcoming the quotas and limitations often imposed by source systems.


AI-Specific Considerations: Why Pull Outperforms Push
------------------------------------------------------------------------------
While push architectures are generally preferred in big data domains, AI knowledge base ingestion presents different challenges. Consider the typical document editing pattern:

    users frequently save incremental changes, creating multiple versions of a document.

With a push architecture, each save triggers the complete processing pipeline—chunking, context addition, and embedding generation—even for minor edits. This approach is inefficient and costly, especially for large documents split into multiple chunks.


Cost Optimization: Batch Processing and Caching
------------------------------------------------------------------------------
The pull method offers superior control by allowing periodic scans with manifest file comparison to process only meaningful changes. This batch-oriented approach enables several optimizations:

1. Batch inference processing can reduce AI costs by approximately 50%
2. Prompt caching for repetitive content processing can decrease costs by an additional 75%
3. Elimination of unnecessary processing for intermediate document versions


Implementation Challenges: Source Integration vs. Vector Store Integration
------------------------------------------------------------------------------
Contrary to common belief, the more challenging aspect of the pipeline is integrating with source systems rather than vector stores. Vector store integration primarily involves standardized API calls—OpenSearch Update/Insert, PGVector SQL commands, or MongoDB document operations. Major cloud providers like AWS have long offered data pipeline products for vector store integration but still struggle with source system integration. Even AWS Bedrock's knowledge base connectors for platforms like Google Drive and Confluence remain in preview after years of development.


Conclusion: Recommended Approach
------------------------------------------------------------------------------
For most use case, I recommend implementing a pull mechanism from source systems to S3 intermediate storage. This approach provides better control and eliminates the need for frequent synchronization. Similarly, a pull mechanism from intermediate storage to vector store, with manifest file management for source metadata, offers the best balance of control and efficiency. This architecture allows us to leverage batch inferencing and prompt caching technologies to increase processing speed while reducing costs.
