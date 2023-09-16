On prem Kafka to AWS MSK Migration
==============================================================================
Keywords:


Overview
------------------------------------------------------------------------------
Kafka 是开源消息中间件的事实标准 (2011 - 2023 本文成文为止都都是). 各种部署方案层次不穷. 作为企业, 经常会有将 Kafka 从小的 cluster 迁徙到大的 cluster, 或是更换服务商, 或是 Kafka 上云等需求. 这就涉及到迁徙, 以及如何在迁徙的过程中尽量减少服务中断的时间.

本文详细的讨论了进行迁徙的关键技术, 以及基于笔者的项目经验给出的几种方案.


What is MirrorMaker
------------------------------------------------------------------------------
MirrorMaker 是 Kafka 自带的一个迁徙工具, 可以用于将一个 Kafka cluster 上的流量复制到另一个 Kafka cluster 上, 从而实现迁徙. 如果我们将待迁徙的 Kafka 叫 Source, 迁徙的目标叫 Target, 那它的本质原理就是在 Target 上运行一个程序, 这个程序即是 Consumer 也是 Producer, 在 Source 看来, 这个程序是 Consumer, 不断地从 Source 上的 Topic 中读数据, 从 Target 看来, 这个程序是 Publisher, 不断地将数据写入到 Target 上的 Topic 中. 这里补充一下,

虽然 MirrorMaker 既可以在 Source 上运行, 也可以在 Target 上运行. 但是一般选择在 Target 上运行, 也就是从 Source 远端读取, 但本地写入到 Target 中, 也就是从 MM 看来只要收到了数据, 由于写入延迟很低, 所以几乎可以视为收到数据的瞬间数据就有保证了. 而且在一个迁徙项目中, 尽量不要对 Source 坐任何修改, 将 MM 放在 Target 上运行比较符合工程实践, 你调试过程中就不会影响到 Source 的正常运行.


MirrorMaker 1 vs 2
------------------------------------------------------------------------------
从 2019-12-16 发布的 2.4.0 起, MirrorMaker 2 正式发布, 和 1 相比的增强功能主要有:

- MM1 所能同步的 Topic 以及 Partition 是在启动 MM1 的瞬间就决定了. 如果 Source 新增了 Topic, 或者 Topic 的 Partition 数量变了, MM1 并不能将这些变化反映到 Target. 但 MM2 可以.
- MM1 只能同步 Topic 的数据, 而不能同步 Configuration. 但 MM2 可以.
- MM2 还支持 active-active 也就是双活, 这对于容灾是非常重要的.
- MM2 除了 MM1 的那种直接在 Kafka cluster 上运行的模式, 还支持以下三种部署方式:
    - MM2 专用集群部署: 无需依赖 Kafka connect, MM2 已经提供了一个 driver 可以单独部署 MM2 集群, 仅需一条命令就可以启动: ``./bin/connect-mirror-maker.sh mm2.properties``
    - 依赖 Kafka connect 集群部署: 需要先启动 Kafka connect 集群模式, 然后手动启动每个 MM2 相关的 connector, 相对比较繁琐. 适合已经有 Kafka connect 集群的场景.
    - 依赖 Kafka connect 单机部署: 需要在配置文件中配置好各个 connector, 然后启动 Kafka connect 单机服务. 不过这种方式便捷性不如MM2 专用集群模式, 稳定性不如 Kafka connect 集群模式, 适合测试环境下部署.

从 2021-09-21 发布的 3.0.0 起, MM1 正式被弃用, 被 MM2 完全取代.

总结起来 MM2 是完爆 MM1 的, 但是如果你生产环境的 Kafka 比较旧, 迁徙后的新的 Kafka 也不准备升级, 那么就只能用 MM1, 否则用 MM2 肯定更好.

- `Kafka MirrorMaker Overview: Key Features and Benefits <https://www.openlogic.com/blog/kafka-mirrormaker-overview>`_
- `Migrating clusters using Apache Kafka's MirrorMaker <https://docs.aws.amazon.com/msk/latest/developerguide/migration.html>`_
- `Kafka mirroring (MirrorMaker) <https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=27846330>`_


Migration Execution
------------------------------------------------------------------------------
下图介绍了 4 种可行的迁徙执行策略. 其中 1, 2, 3 都是只有一个 Kafka cluster 情况下的迁徙. 4 则讨论了如果有多台 Kafka 互相之间复制流量的情况下如何迁徙. 其中 4 的例子只涉及到了 2 个 Kafka 互通, 但是即使你有 N 个 Kafka, 也可以拆分成两两互通的情况, 然后用分而治之的方式解决.

.. raw:: html
    :file: ./On-prem-Kafka-to-AWS-MSK-Migration.drawio.html
