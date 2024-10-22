Clean up Old Lambda Layer
==============================================================================
A utility script to manage AWS Lambda Layer versions by automatically cleaning up old and unused layer versions.

Purpose:

AWS Lambda Layers can accumulate many versions over time, consuming storage and making layer management difficult. This script helps maintain a clean Lambda Layer environment by:

- Keeping the N most recent versions of each layer
- Removing versions older than a specified retention period
- Supporting dry-run mode for safe verification before actual deletion
- Providing detailed information about deleted versions including size and creation date

Example:

.. dropdown:: clean_up_old_lambda_layer.py

    .. literalinclude:: ./clean_up_old_lambda_layer.py
       :language: python
       :linenos:
