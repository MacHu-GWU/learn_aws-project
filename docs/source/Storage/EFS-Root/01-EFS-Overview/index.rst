.. _aws-efs-overview:

Amazon EFS Overview
==============================================================================
Keywords: AWS, EFS, Elastic File System.


What is EFS
------------------------------------------------------------------------------
EFS 是一个通过网络挂载的共享文件系统. 可以理解为一个巨大的本地磁盘文件系统. 它主要是给计算资源提供文件系统的访问. 更重要的是, **它能给多个 EC2 / Container 提供 共享文件系统**. 与之相比, 一个 EBS 卷只能挂载到一个 EC2 上.

在使用上, EFS 可以说是一个无限大小的单个硬盘. 熟悉 Linux 的同学知道, Linux 下的磁盘硬件是需要挂载到特定目录才能使用. Linux 启动的时候会用到一个临时文件系统. 在这个文件系统下你可以创建一些空目录, 并将硬件挂载到这个目录. 之后你对这个目录的读写就会使用你挂载的硬件了. 而如果你把 磁盘 1 挂载到 root ``/``, 而把磁盘 2 挂载到 ``/disk2``, 那么写入到 ``/disk2`` 的数据将会被写入到磁盘 2. 所以 EFS 本质上也是要挂载的. 在实践中从 EFS 的视角看, 把 EFS 作为 Root, 那么文件结构可能会是这样::

    /ec2/ec2-uuid/user-id/...

比如你的一台 ec2 你想升级 CPU 内存, 但是想留着数据, 那么可以把 ec2 销毁, 重新创建一个, 然后把 efs 的 /ec2/ec2-uuid 挂载到新的 ec2 的目录下即可.

而这个 user-id 的部分则是用来 Linux 上的各个用户, 不同的用户有不同的文件夹, 就跟 $HOME 的效果类似. 而且 EFS 还能用 IAM Role 来定义访问权限, 这就更方便管理了.

- EFS 的作用是给 VPC 内的 EC2 提供文件系统.
- 必须为 EFS 指定 VPC 配合使用.
- 必须为 EFS 指定 Mount Target.
- 每一个 AZ 可以创建一个 Mount Target.
- 如果一个 AZ 上有多个 Subnet, 可以在其中一个 Subnet 上创建一个 Mount Target. 所有在当前 AZ 上的 EC2 都共享使用同一个 Mount Target.
- AWS 建议为每一个 AZ 都创建一个 Mount Target. 因为 在一个 AZ 上的 EC2 访问另一个 AZ 上的 Mount Target 价格很贵.
- 位于同一个 Region 下的两个 VPC 可以通过使用 VPC Peering 来共享访问一个 EFS. 不同一个 Region 的不行.
- EFS 有专用的 Network File System Port, 而 EC2 本身受到 Security Group 的限制, 所以 Security Group 设置不当可能会导致 EC2 无法访问 EFS.
- EFS 的加密分两种, 存储加密和传输加密. 存储加密只能在创建 EFS 的时候启用. 传输加密则不是 EFS 本身的功能, 需要在启动 EC2 时使用 EFS Mount Helper, 断开再重新挂载同一个 EFS 即可使得传输加密生效, 详情请参考这篇文档 `Data encryption in Amazon EFS <https://docs.aws.amazon.com/efs/latest/ug/encryption.html#encryption-in-transit>`_.
- Performance Mode 有两种: General 和 Max IO. Max IO 是给 几十个上百个 EC2 分享同一个 EFS 时用的, 延迟高一些. General 比较快, 但是 IO 的容量不是特别大.
- Throughput Mode 有两种: Burst 和 Provisioned, Burst 是大多数时间很普通, 5MB/s, 一天能有 18 分钟提供 100MB/S 的速度. Provisioned 适用于 100MB ~ 1TB /S 级别的速度.


EFS Knowledge Graph
------------------------------------------------------------------------------
以下是 EFS 的知识图谱, 对所有的知识点进行了一个梳理.
