Amazon FSX for Windows Overview
==============================================================================
Keywords: AWS, Amazon, FSX, Overview.


Overview
------------------------------------------------------------------------------
在 1990 - 2010 之间的很多老牌公司的内部电脑都是用 Windows File Server (WFS) 用来分享文件的. 简单来说 WFS 就像是一个内网的文件服务器大网盘, 然后个人电脑用客户端将盘挂载为虚拟硬盘, 对文件进行读写. 而配置 WFS 需要请人安装电脑, 配置网络, 可不是一件轻松的事情. 虽然已经进入了云时代, 但是由于 WFS 已经是公司内部成熟的工具, 并且很多人天天用, 所以不可能说一下子就切换成 S3 之类的后台存储, 还是要使用 WFS. 但企业又想减少运维和维护成本, 所以 AWS 推出了 FSx for WFS, 用来替代传统的 WFS. 你只需要将文件迁徙到 FSx 上, 然后大家的客户端重新挂载一下即可, 大大方便了 WFS 的维护工作.


Setup Amazon FSx for WFS and CloudFormation Stack
------------------------------------------------------------------------------
`Accessing SMB file shares remotely with Amazon FSx for Windows File Server <https://aws.amazon.com/blogs/storage/accessing-smb-file-shares-remotely-with-amazon-fsx-for-windows-file-server/>`_ 是一篇交你怎么使用 FSx for WFS 的官方博客, 建议精读. 但是整个步骤其实还是挺复杂的, 你需要创建很多 VPC, Active Directory, VPN Endpoint 等很多资源. 下面是我用 cottonformation 创建这些资源的脚本, 虽然其中有一些例如导入 Certificate 证书等步骤还是需要手动做, 但是这样已经自动化了 90% 的工作了.

.. literalinclude:: ./iac.py
   :language: python
   :linenos:


Reference
------------------------------------------------------------------------------
- `Microsoft Training - Manage Windows Server file servers <https://learn.microsoft.com/en-us/training/modules/manage-windows-server-file-servers/>`_: 微软介绍 WFS 的官方文档.
- `Accessing SMB file shares remotely with Amazon FSx for Windows File Server <https://aws.amazon.com/blogs/storage/accessing-smb-file-shares-remotely-with-amazon-fsx-for-windows-file-server/>`_: 一篇叫你怎么使用 FSx for WFS 的官方博客, 建议精读.
- `fsxpathlib <https://github.com/aws-samples/fsxpathlib-project>`_: Python 面向对象的客户端, 是对 SMB 协议的封装.
