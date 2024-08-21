Runbook
==============================================================================
**Bootstrap**

.. code-block:: bash

    # 在有 cdk.json 的目录下运行该命令, 默认使用当前的 AWS Default Profile 所对应的 Account 和 Region
    cdk bootstrap

    # 显式运行指定的 AWS Account 和 Region
    # 该命令通常用于 bootstrap 同一个 Account 但是不同的 Region,
    # 因为一个 AWS Profile 通常没有几个 Account 的权限, 这需要用 assume role 来做到
    cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1 aws://ACCOUNT-NUMBER-2/REGION-2 ...

    # 显式指定 AWS CLI Profile 所对应的 Account 和 Region
    cdk bootstrap --profile prod

**Deploy**

.. code-block:: bash

    # 定位到正确的目录.
    cd /path/to/here

    # 创建虚拟环境
    virtualenv -p python3.9 .venv

    # 进入虚拟环境
    source .venv/bin/activate

    # 安装依赖
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r requirements-test.txt

    # 单元测试
    python test.py

    # 部署
    python run_cdk_deploy.py

    # 删除
    python run_cdk_destroy.py