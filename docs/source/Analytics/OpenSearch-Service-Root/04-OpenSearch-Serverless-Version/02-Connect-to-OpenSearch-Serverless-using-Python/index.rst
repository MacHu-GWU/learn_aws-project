Connect to OpenSearch Serverless using Python
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Serverless.

We introduced two methods that can quickly setup an public accessible (need IAM permission) collection and connect to it using Python.

**Method 1**

use `boto3 SDK <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html>`_ to create collection, configure security policy, and connect to it.

``use-boto3/requirements.txt``

.. literalinclude:: ./use-boto3/requirements.txt
   :language: python
   :linenos:

``use-boto3/create_and_configure.py``

.. literalinclude:: ./use-boto3/create_and_configure.py
   :language: python
   :linenos:

``use-boto3/connect_and_test.py``

.. literalinclude:: ./use-boto3/connect_and_test.py
   :language: python
   :linenos:

**Method 2**

use `AWS CDK <https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_opensearchserverless.html>`_ to create collection, configure security policy, and connect to it.

``use-cdk/requirements.txt``

.. literalinclude:: ./use-cdk/requirements.txt
   :language: python
   :linenos:

``use-cdk/app.py``

.. literalinclude:: ./use-cdk/app.py
   :language: python
   :linenos:

``use-cdk/deploy.py``

.. literalinclude:: ./use-cdk/deploy.py
   :language: python
   :linenos:

``use-cdk/connect_and_test.py``

.. literalinclude:: ./use-cdk/connect_and_test.py
   :language: python
   :linenos:
