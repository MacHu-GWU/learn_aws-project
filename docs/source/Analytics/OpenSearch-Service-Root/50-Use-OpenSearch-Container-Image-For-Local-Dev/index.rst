Use OpenSearch Container Image For Local Development Version
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Docker, Unittest, Unit Test.


OpenSearch Container Image for Local Development
------------------------------------------------------------------------------
If you just want to try out OpenSearch, learn app development, Query language syntax, or test your app, you can use container image to run a test server locally.

- `Docker Hub <https://hub.docker.com/r/opensearchproject/opensearch>`: preferred for local dev, but docker hub has rate limit, you should use ECR for your CI/CD job.
- AWS ECR Gallery: https://gallery.ecr.aws/opensearchproject/opensearch

First, ensure that you have docker daemon running on your machine. On Windows or MacOS, you use `Docker desktop <https://www.docker.com/products/docker-desktop/>`_.

**Pull image**

.. code-block:: bash

    docker pull opensearchproject/opensearch:latest

**Run it locally**. The default username password is admin/admin. It has a built-in SSL server. I added ``--rm``, so the container will be removed after you stop it. Note that all index and data will be gone after you stop the container.

.. code-block:: bash

    docker run --rm -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" --name opensearch-node -d opensearchproject/opensearch:latest

If you want to retain the data after you stop the container, you can mount a local folder to the container. The following command will mount the local folder:

.. code-block:: bash

    docker run --rm -v /path/to/your/data/folder:/usr/share/opensearch/data -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" --name opensearch-node -d opensearchproject/opensearch:latest

This command will **stop container** and remove it:

.. code-block:: bash

    docker stop opensearch-node

``connect_to_local_oss.py`` tests the connection to a local OpenSearch container.

.. literalinclude:: ./connect_to_local_oss.py
   :language: python
   :linenos:


