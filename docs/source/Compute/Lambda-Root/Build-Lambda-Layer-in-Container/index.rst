Build Lambda Layer in Container
==============================================================================
Keywords: Amazon, AWS, Lambda, Build, Layer, Docker, Container


Summary
------------------------------------------------------------------------------
Lambda Layer 保存了你的程序所需的依赖. 而有些编程语言的依赖是要编译成二进制代码的. 你在不同的架构的机器上编译出来的依赖可能会不兼容. 例如你的 Lambda Function 是 Linux/AMD64, 而你的电脑是 Mac. 并且还有可能不仅仅操作系统不一样, CPU 架构也不一样. 例如你的 Lambda Function 是 Linux/AMD64, 而你的电脑是 ARM 的 Mac.

当然. 在企业项目中, build layer 一般是在跟 Lambda runtime 一致的服务器上进行. 而开发者总归是有在本地构建 Lambda Layer 的需求的. 为了解决这一问题, 最通用的方法是使用和 Lambda runtime 一致的 Container 中构建. 并且在构建的时候, 用 ``--platform linux/amd64`` 或 ``--platform linux/arm64`` 确保你构建出的镜像和 Lambda 的 CPU 架构一致 (详情请参考 `Docker Multi-platform images <https://docs.docker.com/build/building/multi-platform/>`_).


Pick a Base Image
------------------------------------------------------------------------------
**不要这么做**

    根据 `Working with Lambda container images <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html>`_ 官方文档, AWS 在 Public ECR Gallery 维护着 `多个编程语言的基础镜像 <https://gallery.ecr.aws/lambda/>`_. 这些基础镜像是用来部署 Lambda 的, 你无法把它当成一个普通的镜像, 然后在里面运行一些 bash script 来构建你的 Layer.

**应该这么做**

    AWS SAM (Serverless application Model) 框架的官方文档中提到了, `它们提供了一系列的 Container Image <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html>`_, 提供了和 Lambda 一致的 Runtime, 可以用来 CI CD. 这些镜像 host 在了 `Public ECR Gallery sam <https://gallery.ecr.aws/sam/build-python3.9>`_. 这个镜像是用来在里面 run CI/CD 自动化脚本的, 你也可以进入到 interactive bash 中.


Play with the SAM image
------------------------------------------------------------------------------
本节我们来探索一下 SAM image 里面有些什么, 目录结构是怎样的. 我是 Python 开发者, 所以我用 Python3.9 为例. 该镜像解压前 550MB, 解压后 1.6GB.

.. code-block:: bash

    # 定义一些变量
    # container name
    export CONTAINER_NAME="lbd_layer_build_test"

    # X86 架构用这个
    export IMAGE="public.ecr.aws/sam/build-python3.9:latest-x86_64"

    # ARM 架构用这个
    export IMAGE="public.ecr.aws/sam/build-python3.9:latest-arm64"

    # 拉取这个容器
    docker pull ${IMAGE}

    # 以 Interactive Terminal 的形式运行这个容器
    # 注意, 如果你要为 X86 架构 build layer 就加上 --platform linux/amd64
    docker run --rm -dt --name ${CONTAINER_NAME} --platform linux/amd64 ${IMAGE}

    # 注意, 如果你要为 ARM 架构 build layer 就加上 --platform linux/arm64
    docker run --rm -dt --name ${CONTAINER_NAME} --platform linux/arm64 ${IMAGE}

    # 进入这个容器的 Bash, 按 Ctrl + D 退出
    docker exec -it ${CONTAINER_NAME} bash

    # 停止这个容器, 由于我们前面加了 --rm, 这个容器会被自动销毁
    docker container stop ${CONTAINER_NAME}

你进入到这个容器后当前目录是 ``/var/task``, 也是一个空目录. 在 Build layer 的时候我们会将这个目录 mount 到我们的当前目录. 这样构建好了之后我们就可以获得 Layer 的 zip 文件了.

- 默认工作目录: ``/var/task``
- Python 解释器: ``/var/lang/bin/python``
- Pip 的 Site packages: ``/var/lang/lib/python3.9/site-packages``


Pick a Machine
------------------------------------------------------------------------------
由于 Docker 是可以在一个架构的机器上构建出另一个架构的镜像的 (例如你是 Arm Mac, 但构建出 AMD64 的镜像). 由于 Image 的大小并不小, 会比较占用磁盘空间. 我不想浪费我 Mac 宝贵的磁盘, 所以我选用 AWS Cloud 9 来做宿主机来 build layer. Cloud 9 磁盘空间如果不够的化请参考这篇文档 `Resize an Amazon EBS volume used by an environment <https://docs.aws.amazon.com/cloud9/latest/user-guide/move-environment.html#move-environment-resize>`_ 来给 EBS 扩容. 请参考这篇文档 `Docker sample for AWS Cloud9 <https://docs.aws.amazon.com/cloud9/latest/user-guide/sample-docker.html>`_ 来在 Cloud 9 上安装 Docker.


Build Layer In Container Automation Script
------------------------------------------------------------------------------
在这个例子中我们有两个脚本. ``build_layer.py`` 是要在 Container 中运行的脚本, 它能在 Container 里面安装依赖并打包 Layer zip 文件. ``build_layer_in_container.py`` 是在宿主机上运行的脚本, 它能运行 ``docker run ...`` 命令, 指挥 docker 在 container 里面运行前面介绍的 ``build_layer.py`` 脚本.

.. dropdown:: build_layer.py

    .. literalinclude:: ./build_layer.py
       :language: python
       :linenos:

.. dropdown:: build_layer_in_container.py

    .. literalinclude:: ./build_layer_in_container.py
       :language: python
       :linenos:

构建完之后你就可以 upload 到 s3, 然后用 ``publish_layer_version`` API 来发布一个新的 Layer 了.


Reference
------------------------------------------------------------------------------
- 本文的知识主要来自于这篇官方文档, How do I create a Lambda layer using a simulated Lambda environment with Docker?: https://repost.aws/knowledge-center/lambda-layer-simulated-docker
- AWS SAM's underlying ``amazon/aws-sam-cli-build-image`` Docker images, 这是 SAM 框架用来构建 Layer 的 Docker Image: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-image-repositories.html
- `Deploy Python Lambda functions with container images <https://docs.aws.amazon.com/lambda/latest/dg/python-image.html>`_
- `AWS ECR Gallery Lambda Python <https://gallery.ecr.aws/lambda/python>`_: 这是你 build 你自己的 Lambda Function docker container 时用的基础镜像, 当然也可以用来 build layer, 只不过复杂的多
- `Avoiding Permission Issues With Docker-Created Files <https://vsupalov.com/docker-shared-permissions/>`_: 这篇博文介绍了如何在 Docker 中修改 User Owner 权限.
- `Can't Delete file created via Docker <https://stackoverflow.com/questions/42423999/cant-delete-file-created-via-docker>`_: 这篇讨论介绍了一个无法在 docker 中 delete 文件的问题.
