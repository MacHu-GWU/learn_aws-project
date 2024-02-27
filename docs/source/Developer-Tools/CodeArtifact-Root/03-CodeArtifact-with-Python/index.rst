.. _aws-code-artifact-with-python:

AWS CodeArtifact with Python
==============================================================================
Keywords: AWS, Amazon, CodeArtifact, Code Artifact, Python.


将你的包发布到 AWS CodeArtifact
------------------------------------------------------------------------------
首先你要在本地先 build 好 distribution artifacts:

.. code-block:: bash

    # 在 Setup.py 中用 distutils, 2021 年已经不推荐使用了.
    python setup.py sdist bdist_wheel --universal

    # 用 build https://build.pypa.io/en/latest/, 这个 Python 官放的工具打包, 非常推荐
    python -m build

    # 用 Poetry https://python-poetry.org/docs/cli/#build, 也能用, 跟 build 的差别不大, 但不够轻量
    poetry build

然后用 aws cli 对 CodeArtifact 进行身份验证, 并自动对 Python 的包发布工具 `twine <https://twine.readthedocs.io/en/stable/>`_ 进行配置, 这个本质就是获得一个 token 然后把这个 token 放在 twine 的配置文件 ``~/.pypirc`` 中.

.. code-block:: bash

    aws codeartifact login --tool twine --domain my_domain --domain-owner 111122223333 --repository my_repo

然后你就可以用 twine 将你的 artifacts 发布到你的私有 repo 里了:

.. code-block:: bash

    # 注意, 这个 codeartifact 是 aws cli 自动创建的 config profile, 请不要乱改
    twine upload --repository codeartifact dist/*

Reference:

- `Python configure twine <https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-twine.html>`_


从 AWS CodeArtifact 上安装你已发布的包
------------------------------------------------------------------------------
然后用 aws cli 对 CodeArtifact 进行身份验证, 并自动对 Python 的包管理 `pip <https://pip.pypa.io/en/stable/>`_ 进行配置, 这个本质就是获得一个 token 然后把这个 token 放在 pip 的配置文件 ``~/.config/pip/pip.conf`` 中.

.. code-block:: bash

    aws codeartifact login --tool pip --domain my_domain --domain-owner 111122223333 --repository my_repo

然后你就可以使用 ``pip install ...`` 命令了, pip 会优先到你的 repo 上去搜索, 搜不到才会去 public PyPI 上搜索.

Reference:

- `Configure and use pip with CodeArtifact <https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-pip.html>`_
- `Configure repositories for Poetry <https://python-poetry.org/docs/repositories#repositories>`_


Reference
------------------------------------------------------------------------------
- `aws_codeartifact_python-project README <https://github.com/MacHu-GWU/aws_codeartifact_python-project>`_: 一个详细讲解怎么将 Poetry 和 AWS CodeArtifacts 一起使用的示例项目.
- `cookiecutter-aws-codeartifact-python-project <https://github.com/MacHu-GWU/cookiecutter-aws-codeartifact-python-project>`_: 这是一个 cookiecutter 的模板项目. 如果你需要发布并维护一个私有的 Python 包并发布在 CodeArtifact 上, 那么你可以用这个模板项目快速生成项目的文件目录. 如果你的项目仅仅是使用在 CodeArtifact 上的私有包, 那么这个模板并不适合.
