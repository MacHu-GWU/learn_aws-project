Deploy Lambda and Configure Event Mapping with AWS CDK
==============================================================================
Keywords: Amazon, AWS, Lambda, CDK, Event


Overview
------------------------------------------------------------------------------
This document provides a comprehensive list of sample AWS CDK code in Python to deploy a Lambda function and configure event mapping for various AWS services.


S3 put
------------------------------------------------------------------------------
.. dropdown:: s3-put.json

    .. literalinclude:: ./sample-events/s3-put.json
       :language: python
       :linenos:


S3 delete
------------------------------------------------------------------------------
.. dropdown:: s3-delete.json

    .. literalinclude:: ./sample-events/s3-delete.json
       :language: python
       :linenos:


SNS Notification
------------------------------------------------------------------------------
.. dropdown:: sns-notification.json

    .. literalinclude:: ./sample-events/sns-notification.json
       :language: python
       :linenos:


.. dropdown:: app.py

    .. literalinclude:: ./sns/app.py
       :language: python
       :linenos:


SQS
------------------------------------------------------------------------------
.. dropdown:: sqs.json

    .. literalinclude:: ./sample-events/sqs.json
       :language: python
       :linenos:



DynamoDB Update
------------------------------------------------------------------------------
.. dropdown:: dynamodb-update.json

    .. literalinclude:: ./sample-events/dynamodb-update.json
       :language: python
       :linenos:


Kinesis Get Records
------------------------------------------------------------------------------
.. dropdown:: kinesis-get-records.json

    .. literalinclude:: ./sample-events/kinesis-get-records.json
       :language: python
       :linenos:
