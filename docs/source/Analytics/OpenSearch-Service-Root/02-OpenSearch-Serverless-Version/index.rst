Amazon OpenSearch Serverless Version
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Serverless.


Connect to OpenSearch Serverless Collection using Python
------------------------------------------------------------------------------
**Method 1**, use boto3 SDK to create collection, configure security policy, and connect to it.

``requirements.txt``

.. literalinclude:: ./create_and_configure_collection_requirements.txt
   :language: python
   :linenos:

``create_and_configure_collection.py``

.. literalinclude:: ./create_and_configure_collection.py
   :language: python
   :linenos:

**Method 2**, use AWS CDK to create collection, configure security policy, and connect to it.
