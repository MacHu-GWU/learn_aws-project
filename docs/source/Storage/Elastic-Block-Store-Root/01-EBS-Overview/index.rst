.. _aws-ebs-overview:

Amazon EBS Overview
==============================================================================
Keywords: AWS, EBS, Elastic Block Storage.


What is EBS
------------------------------------------------------------------------------
Block Storage 是块存储的意思, 顾名思义 EBS 是一个云端的块存储服务. 常见的云存储有 块存储, 对象存储 和 文件存储. 如果你不了解它们的含义和区别, 可以参考以下官方文档.

Reference:

- `数据块、对象和文件存储有什么区别 <https://aws.amazon.com/cn/compare/the-difference-between-block-file-object-storage/#:~:text=%E6%96%87%E4%BB%B6%E5%AD%98%E5%82%A8%E9%9C%80%E6%B1%82%EF%BC%9F-,%E6%95%B0%E6%8D%AE%E5%9D%97%E3%80%81%E5%AF%B9%E8%B1%A1%E5%92%8C%E6%96%87%E4%BB%B6%E5%AD%98%E5%82%A8%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB%EF%BC%9F,%E5%A4%A7%E5%B0%8F%E7%9B%B8%E7%AD%89%E7%9A%84%E6%95%B0%E6%8D%AE%E5%9D%97%E3%80%82>`_
- `What is EBS? <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html>`_


EBS Concepts
------------------------------------------------------------------------------
- `Volume <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html>`_: 一个数据卷, 你可以将其理解为一堆块的集合.
- `Attachment <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-attaching-volume.html>`_: 你需要将数据卷 attach 到 EC2 上 (或是其他的计算资源上) 才能使用.
- `Snapshot <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html>`_: 对数据卷的一个快照, 本质是储存了块的索引. 它只会追踪被改变了的块. 一旦一个块被 snapshot 所追踪, 那么这个块就不会变了, 对这个块上的数据的改动会被记录到新的块上.


EBS Knowledge Graph
------------------------------------------------------------------------------
以下是 EBS 的知识图谱, 对所有的知识点进行了一个梳理.
