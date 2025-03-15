Mulit-Tenant AI Knowledge Base Architecture
==============================================================================


Overview
------------------------------------------------------------------------------
AI knowledge bases present unique architectural challenges compared to traditional databases, particularly when it comes to multitenancy. As organizations increasingly adopt Retrieval Augmented Generation (RAG) systems to enhance their AI capabilities with domain-specific knowledge, the need for proper isolation between different tenants becomes critical. This isolation is not merely a technical preference but often a business, security, and regulatory requirement.

**For internal enterprise deployments**, different departments, teams, or projects may need to maintain separate knowledge domains while leveraging shared infrastructure. **In public-facing applications**, SaaS providers must ensure that each customer's proprietary data remains isolated while optimizing infrastructure costs. In both scenarios, a well-designed multitenant architecture is essential.

Several isolation techniques exist across different architectural layers. Using AWS AI ecosystem as an example, isolation can be implemented at various levels:

- AWS Account Level: Complete resource and security isolation
- OpenSearch Serverless Collection Level: Database-level isolation
- OpenSearch Serverless Index Level: Table-level isolation
- Document Level: Row-level isolation using field-based filtering
- Bedrock Knowledge Base Level: Application-level isolation through knowledge base abstraction

While this document uses AWS services to illustrate concepts, the architectural patterns and isolation strategies apply broadly across providers and technologies. The fundamental challenges of balancing isolation, performance, cost-efficiency, and operational complexity remain consistent regardless of the specific implementation technologies.

This document explores three primary multitenant patterns—Silo, Pool, and Bridge—analyzing their strengths, weaknesses, and optimal use cases to help architects select the most appropriate strategy for their specific requirements.


Multitenancy Patterns
------------------------------------------------------------------------------
When implementing a multitenant architecture for AI knowledge bases, three fundamental patterns have emerged that provide different balances between isolation, resource efficiency, and operational complexity.

Looking at these patterns through the lens of AWS services demonstrates the practical implementation options available:

- **Silo (Isolated Tenancy)**:
    - General Definition: Each tenant has a fully separate instance of the application and database, ensuring maximum isolation and security.
    - AWS Setup: Complete isolation where tenants have separate databases (OpenSearch collections), separate tables (indexes), and dedicated knowledge bases. Nothing is shared between tenants, providing maximum security and customization at higher cost.
- **Pool (Shared Tenancy)**:
    - General Definition: Tenants share some infrastructure (e.g., database schema) while maintaining isolated data access, balancing efficiency and customization.
    - AWS Setup: Maximum resource sharing where tenants use the same database, same tables, and same knowledge base, with isolation enforced through document-level (row-level) filtering. This approach optimizes infrastructure costs but limits tenant-specific customization.
- **Bridge (Hybrid Tenancy)**:
    - General Definition: All tenants share the same application and database, with logical separation ensuring data privacy, maximizing resource efficiency and scalability.
    - AWS Setup: A middle-ground approach where tenants share the same database (OpenSearch collection) but have their own tables (indexes) and dedicated knowledge bases, balancing isolation needs with resource efficiency.

We will evaluate these patterns in detail in the following sections, examining their implications for security, performance, cost, and operational complexity.


AWS Limitation
------------------------------------------------------------------------------
When designing multitenant architectures on AWS, it's important to consider the service limits that may impact your implementation choice:

- Max number of OpenSearch Serverless Collection per account per region is unknown (would be around 100)
- Max number of index you can create per OpenSearch Serverless Collection is 1000
- Max number of Bedrock Knowledge Base you can create is 50


Optimal Use Cases
------------------------------------------------------------------------------
While the `AWS blog post <https://aws.amazon.com/blogs/machine-learning/multi-tenant-rag-with-amazon-bedrock-knowledge-bases/>`_ provides a thorough discussion of implementation details for each pattern, it's valuable to consider additional practical criteria for pattern selection. The table below offers guidance based on **tenant scale** and **use case scenarios** that complements the technical analysis in the AWS documentation:

+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|                                        |                         Silo                         |            Bridge            |       Pool       |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|        Support Number of Tenant        |                         <=20                         |            <=1000            | >=1000,<=1000000 |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|                Good For                | Help big customer to manage their AI Knowledge Infra |  Big enterprise internal use |   SAAS Provider  |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|   Support Tenant Transition and Merge  |                          No                          | Possible, but need more work |       Easy       |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|            Tenant Isolation            |                         High                         |            Medium            |        Low       |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|     Backend maintenance complexity     |                         High                         |            Medium            |       Easy       |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
| Query client implementation (Frontend) |                        Medium                        |             Hard             |       Easy       |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+
|                  Cost                  |                         High                         |            Medium            |        Low       |
+----------------------------------------+------------------------------------------------------+------------------------------+------------------+


Reference
------------------------------------------------------------------------------
- `AWS Blog - Multi-tenant RAG with Amazon Bedrock Knowledge Bases <https://aws.amazon.com/blogs/machine-learning/multi-tenant-rag-with-amazon-bedrock-knowledge-bases/>`_
- `Google Sheet for this document <https://docs.google.com/spreadsheets/d/1OW5IsgMKZDda9O5YaRYiZ2p5r5enowtaH1EoXtH1jz4/edit?gid=0#gid=0>`_
