Disaster Recovery in Kafka
==============================================================================


What is Disaster Recovery (DR)
------------------------------------------------------------------------------
DR 主要指的是因为物理不可抗力原因, 例如地震, 火灾, 停电导致数据中心不可用的情况.


Zero Loss Guarantee
------------------------------------------------------------------------------
所谓 Zero Loss Guarantee 是指你要实现, 当发生灾难时, 切换到备用 Kafka 后开始消费 Message, 凡是 Producer 成功提交的 Message 都不能丢. 举例来说, 当用户在电商网站付款下订单后, 后台会生成一条消息发给 Kafka, 当 Producer 成功将消息写入 Kafka 后就通知用户下单成功.

作为容灾或任何分布式系统, 一般都只会有一个写入主节点收到写入请求, 然后将请求发送给多个节点, 也就是所谓的复制. 这里的关键是从主节点收到写入请求到多个节点的复制成功并告诉主节点之间是有时间差的. 如果是收到写入请求时就通知 Producer 写入成功, 那么是无论如何都无法保证不丢数据的, 因为完全可能在收到 "写入成功" 后系统挂掉, 导致复制也失败了, 从而丢数据. 那逻辑上我们就必须保证复制成功后再告诉 Producer 写入成功.

由上可知, 一切基于从 主 Kafka 的 Topic 中读消息, 并复制到备用 Kafka 的方案都无法实现 Zero Loss Guarantee. 唯一能确保 Zero Loss 的方法是改变 Producer 写入数据时确认成功的机制, 也就是说改为当 Kafka 成功将消息复制到备用节点, 才返回写入成功. 这需要对 Kafka 进行魔改, 目前字节跳动就采用的这一方案.

- `Disaster Recovery for Multi-Datacenter Apache Kafka Deployments <https://www.confluent.io/blog/disaster-recovery-multi-datacenter-apache-kafka-deployments/>`_
- `Kafka多种跨IDC灾备方案调研对比 <https://www.51cto.com/article/707393.html>`_
