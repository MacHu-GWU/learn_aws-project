.. _run-remote-command-on-ec2-ultimate-solution:

Run Remote Command on Ec2 Ultimate Solution
==============================================================================
Keywords: AWS, EC2, System, Systems, Manager, SSM, Python, Remote, Command


我们想要做什么
------------------------------------------------------------------------------
出于多种原因, 往往是网络相关的原因, 很多时候代码必须要在 EC2 环境内执行. 而作为开发者, 如何像在本地电脑上执行 Python 自动化脚本一样在 EC2 环境内执行命令呢? 如果能做到这一点, 想象空间可以是无限的. 下面我们详细的拆解一下需求:

从具体执行的命令复杂度来看, 可以分为两类:

1. 单条在 Terminal 内的命令. 例如 ``aws s3 ls``.
2. 以 Python 脚本形式存在的命令, 具体的命令的逻辑在 Python 脚本中被定义的. 这个脚本并不是事先准备好的, 换言之, 在执行脚本前我们要现将脚本上传到 EC2 环境内.

从对反馈的要求来看, 可以分为三类:

1. 我只需要执行, 不需要反馈.
2. 我需要知道执行的返回码是成功 (0) 还是失败 (非 0).
3. 我不仅需要知道执行状态, 这个命令可能还会返回一些数据, 我还需要知道这个数据.

从命令的发起者来看,

1. 只需要我的开发电脑能发起命令即可.
2. 这个命令需要能被任何有权限的地方发起, 例如另一台 EC2, 一个 Lambda.

可以看出, 以上需求可以排列组合, 从而出现 2 * 3 * 2 = 12 种情况. 有没有一种解决方案能够同时满足这 12 种情况呢? 答案是肯定的, 我们将在下面的章节中详细的介绍.


探索可能的解决方案
------------------------------------------------------------------------------
我们对上面的需求来一条一条的分析, 看看这些需求后面的本质.

- 单条在 Terminal 内的命令. 例如 ``aws s3 ls``.

    这个没什么说的, 就是一条远程命令.

- 以 Python 脚本形式存在的命令, 具体的命令的逻辑在 Python 脚本中被定义的. 这个脚本并不是事先准备好的, 换言之, 在执行脚本前我们要现将脚本上传到 EC2 环境内.

    这就意味着我们总得有一个简单, 可重复, 安全的方法将任意脚本上传到 EC2 环境内.

- 我只需要执行, 不需要反馈

    这个没什么说的, 简单执行即可.

- 我需要知道执行的返回码是成功 (0) 还是失败 (非 0)

    这就需要我们能捕获错误码 (return code)

- 我不仅需要知道执行状态, 这个命令可能还会返回一些数据, 我还需要知道这个数据

    要么这个命令本身的设计就是会把返回数据写到 stdout, 那么我们只要能捕获 stdout 即可. 要么在运行时将数据上传到一个中间媒介, 例如 S3, 然后我们再从 S3 读取数据.

- 只需要我的开发电脑能发起命令即可

    要么我的电脑能 SSH 到 EC2 上去. 要么我的电脑有一些相关的 AWS 权限. 这里的权限主要指的是 AWS System Manager Run Command 的权限. 这是一个 AWS 托管的服务器, 可以利用 SSM Agent 在 EC2 上执行任何命令.

- 这个命令需要能被任何有权限的地方发起, 例如另一台 EC2, 一个 Lambda.

    这个发起方只要有上面说的 AWS System Manager Run Command 权限即可. 当然开发电脑也可以有这个权限.

好了, 我们现在对解决每一条需求都有个大概的概念了, 下一步我们来将这些方案组合成一个完整的解决方案. 但在这之前, 我们先来了解一下这里的核心技术 AWS SSM Run Command.


AWS SSM Run Command
------------------------------------------------------------------------------
AWS System Manager 是一个历史悠久的 AWS 服务, 主要用于批量管理 EC2 instance 虚拟机. 你可以将其理解为 AWS 版本的 Ansible. 而它的核心组件就是 System Manager Agent (SSM Agent), 本质上是一个服务端软件, 安装在 EC2 机器上, 属于系统服务的一部分. 而 AWS 内部对 EC2 的管理工作很多都是通过 SSM Agent 来进行的. 而"Run Command" 则是 SSM 的一项功能, 可以通过 SSM Agent 执行远程命令.

简单来说我们选择 SSM Run Command 作为我们解决方案的核心技术是出于以下几点考量:

- SSM Run Command 是受 IAM Role 权限保护的, 非常安全且灵活, 兼容于各种 AWS 服务, 使得我们可以在任何 AWS 服务内发起 SSM Run Command.
- SSM Run Command 功能 `免费 <https://aws.amazon.com/systems-manager/pricing/>`_, 且支持非常高的并发量.
- SSM Run Command 可以捕获 Return Code, Stdout, Stderr, 使得我们可以满足上面的所有需求.

SSM Run Command 本身有一些限制.

- 通过 API 发送的 Run Command 也是有限制的, 不能超过 100KB. 如果你需要发送大量数据, 那么你需要修改你的远程命令程序, 让它接受 S3 uri 为参数, 然后到 S3 uri 去读输入数据.
- Stdout 是有大小限制的, API 最多显示 24000 个字符. 如果需要捕获大量数据, 那么你需要修改你的远程命令程序, 将结果保存在 S3 上.

这里我不详细展开说 SSM Run Command 这个功能, 建议先看看一下 :ref:`run-remote-command-on-ec2-via-ssm` 这边博文, 对其有个简单的了解


最终解决方案
------------------------------------------------------------------------------
1. 对于运行单条 Terminal Command, 就直接用 SSM Run Command 即可.
2. 对于运行复杂的 Python 脚本呢, 我们可以将在本地的 Python 脚本先上传到 S3, 然后用 Run Command 运行第一条命令 ``aws s3 cp s3://... /tmp/...script.py`` 将其下载到 EC2 上, 然后再指定 Python 解释器来执行该脚本. 如果该脚本是个命令行工具, 我们还能带上参数. 注意, 我们要确保这个 EC2 上预装了 aws cli.
3. 如果我们需要捕获命令返回的结果, 那么我们要么自己能保证这条命令能在 Stdout 中返回一个结构化的数据 (注意, logging 可能会干扰到返回值), 例如 JSON, 要么能运行过程中的数据上传到 S3. 然后我们再从 S3 读取数据.


实际案例
------------------------------------------------------------------------------
``script.py`` 这是我们想要在 EC2 上执行的命令. 我们会在后面的脚本中将其上传到 S3, 然后在 EC2 上下载并执行.

.. literalinclude:: ./script.py
   :language: python
   :linenos:

``ssm_remote_command_helpers.py`` 这是一个库, 能让我们方便的调用 run command 命令

.. literalinclude:: ./ssm_remote_command_helpers.py
   :language: python
   :linenos:

``example.py`` 这是我们的最终代码, 实现了我们的解决方案.

.. literalinclude:: ./example.py
   :language: python
   :linenos:
