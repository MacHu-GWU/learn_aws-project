.. _dynamodb-pricing:

DynamoDB Pricing
==============================================================================


1. 简介
------------------------------------------------------------------------------
Dynamodb 的收费模型是依据你读了多少数据以及写了多少数据来进行收费的. 而这个读了多少数据和写了多少数据时有最小单位的, 分别叫 Read Request Unit (RRU) 和 Write Request Unit (WRU). 如果实际的读写比特小于这个则向上取整. 详情请参考 :ref:`RRU 和 WRU 的详细文档 <dynamodb_rru_wru>`.

Dynamodb 还有两种收费模式, 分别叫 On-Demand 和 Provisioned. 简单来说 On-Demand 就是你用了多少就 Charge 你多少, 但是单价会比较贵. Provisioned 则是你预设一个值, 超过这个值的请求就会收到报错的回复. 详情请参考 :ref:`On-Demand 和 Provisioned 的详细文档 <dynamodb_on_demand_provisioned>`.

Reference:

- `Read and write operations <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/read-write-operations.html>`_: 详细介绍了 RRU 和 WRU 的定义.
- `DynamoDB throughput capacity <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html>`_: 详细介绍了 on demand 和 provisioned 两种收费模式.


.. _dynamodb_rru_wru:

2. RCU WCU 详解
------------------------------------------------------------------------------
**前置知识**:

- eventually consistence read: 你写入后立刻读, 可能不一定读到最新的数据, 因为对于分布式系统新写入的数据需要一定时间用 gossip 算法传播到所有的节点. 你读的节点可能不是写的节点, 所以可能不是最新的数据. 这个延迟其实在 100 毫秒级别, 所以问题一般并不大, 但是对于银行等系统可能就不行了. **这是 Dynamodb 默认的读数据的方式, 除非你手动指定 Strong consistence read**.
- strong consistence read: 你写入后立刻读, 只要你读的时间是在成功写入之后, 那么一定读到的是最新的数据, 但是延迟会比 eventually consistence read 高. 而且收费也贵一些.
- transaction read: 在一个 transaction 里面有 write 有 read, 那么里面的 read 就是 transaction read.

**Read Request Unit (RRU)**

- 一个 RRU 等于对一个 4KB 的 item 进行 1 个 strong consistence read, 或 2 个 eventually consistence read. 如果 item 不超过 4KB, 按照 4KB 计算. 大于 4KB 的 item 会除以 4KB 然后向上取整. 举例来说对 1 个 4KB 的 item 进行一个 strong consistence read 就是 1 RRU, 对 2 个 4KB 的 item 进行 eventually consistence read 就是 1 个 RRU.
- 一个 transaction read request 需要 2 个 RRU.
- 对于 get 单个 item, 如果小于 4KB 则向上取整到 4KB 收费. 如果大于则除以 4KB 并将结果向上取整.
- 对于 batch get items, 每个 item 和 get 单个 item 一样, 分别算钱. 注意, 它不会讲所有的 items 汇总后算钱.
- 对于 query, 所有的 item 合在一起后算钱.
- 对于 scan, 是按照 evaluate 过的 item 算钱, 也就是在使用 filter 之前扫过的所有 item 算钱.
- 对于以上操作, 如果你只返回 item 的部分 attribute, 它依然按照整个 item 算钱.

**Write Request Unit (WRU)**

- 一个 WRU 等于对于 1KB 的 item 进行 write request (超过的话计算和 read 同理).
- 一个 transaction write request 需要 2 个 WRU.
- 对于 put 单个 item, 按照 1KB 算钱.
- 对于 update 单个 item, 按照 update 前后较大的那个算钱.
- 对于 delete, 按照原 item 大小算钱.
- 对于 batch put, 每个 item 和 put 单个 item 一样, 分别算钱. 注意, 它不会讲所有的 items 汇总后算钱.

注意: Global Secondary Index 也占用额外的 R/W RU.


.. _dynamodb_on_demand_provisioned:

3. On Demand 和 Provisioned 详解
------------------------------------------------------------------------------
**On Demand 模式**

Dynamodb 会自动 Scale 来适应你的 traffic, 简单来说就是当 traffic 达到你之前的 peak 设定值的一定百分比 (自己可以设置), 就自动 double. 如果你的 traffic 很快超过了 double, Dynamodb 也会自动给更多的 Capacity 的, 不过如果你的 traffic 用了少于 30 分钟就超过了之前的 peak 的 double, 那么就会发生 "节流" 导致部分请求失败. 所以 Dynamodb 建议你提前 30 分钟以上进行 Scale. 注意 peak setting 是决定了 table 最大的吞吐量, 只会影响你的 app 是否会请求失败, 并不影响计费.

**On Demand 模式初始吞吐量**

如果你刚把一个 table 切换到 on-demand 的模式, 或是用 on-demand 模式创建了一个新的 table, 新的 peak settings 是这样的.

- 新表: 2000 WRU, 6000 RRU
- 已有的表: 是你当时创建 Provisioned Table 是的 WRU, RRU 的一半, 或是新 On demand 的表的默认值 (即 2000 WRU, 6000 RRU) 取高的那个. 换言之, 你的表至少是 新 On demand 的表 的吞吐量的水平.

**当切换模式时 Table 的行为**

通常切换需要几分钟来进行. 这期间 WRU, RRU 和 PEAK 都保持不变.

**Provision 模式**

在 Provision 模式下, 你的 Peak 就是你设置的 WRU, RRU.

**Provision 模式的 Auto Scaling**

Auto Scaling 的意思是你可以定义一个 WRU, RRU 的 range, 有一个上限和下限. 你还要定义一个百分比, 例如 70%. 这样你就可以用 Provision 的模式来处理变化有规律的流量, 从而节约成本.

**Reserved Capacity**

和 EC2 类似, 你提前付款确保一定时间内的 Capacity, 当然价格会比 On-demand 和 provisioned 要低得多.


Burst and adaptive capacity
------------------------------------------------------------------------------
**Burst capacity**

当你使用了 Provision 模式, AWS 会把 5 分钟内你没有用掉的 capacity 保留下来. 并在你用的 capacity 超过你的限制的时候, 使用这些 capacity. 例如你的限制是 100 RRU 每秒. 如果你 5 分钟内没有用, 那么你会积攒 30000 个 RRU. 如果你下一秒有一个 query 需要用 1000 个 RRU, 虽然超过了 100 RRU 的限制, 但是你可以用积攒的 RRU, 所以你的 query 还是会成功.

**Adaptive capacity**

由于 DynamoDB 是一个分布式系统, 所以这些 Capacity unit 其实是分配到每一个 partition 上的. 但是不是所有的 partition 的 traffic 都是平均的. 例如你的限制是 100 RRU, 那么如果你有 5 个 partition 就是每个 partition 20 RRU. 如果你有一个 query 落在了一个 partition 上并消耗了 50 RRU, DynamoDB 会自动适应.

Reference:

- `Burst and adaptive capacity <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/burst-adaptive-capacity.html>`_


.. _dynamodb-pricing-example:

4. Pricing Example
------------------------------------------------------------------------------
- Provisioned:
    - WRU: 0.00065 / Hour
    - RRU: 0.00013 / Hour
- On-demand:
    - WRU: 1.25 / Million
    - RRU: 0.25 / Million

在 Dynamodb 中我们通常假设 写/读 比例为 1:3.

例子 1: 假设我们每秒平均 100 个 WRU 请求 (100KB 每秒), 300 RRU 个读请求 (1.2MB 每秒).

- Provisioned 模式: 由于 traffic 有一定波动, 我们最好把实际请求控制在我们的 Limit 的 70% 以下. 也就是 140 个 WRU, 420 个 RRU. 最终费用为 (30 * 24) * (140 * 0.00065 + 420 * 0.00013) = 104.8
- On-demand 模式: (30 * 24 * 3600) * (100 * 1.25 + 300 * 0.25) = 518.4
