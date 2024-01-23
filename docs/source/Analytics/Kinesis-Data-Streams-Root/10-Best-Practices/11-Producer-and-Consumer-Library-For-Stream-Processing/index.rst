Producer and Consumer Library For Stream Processing
==============================================================================
.. note::

    我有一个开源项目 `unistream <https://unistream.readthedocs.io/en/latest/index.html>`_, 是一个 Producer and Consumer Library For Stream Processing 的框架. 把所要用到的模块全部抽象化了, 例如 producer 需要的 buffer, consumer 需要的 checkpoint 等. 使得我们可以用任何后端系统实现这些模块, 并于任何 Stream system 集成.


What is Producer Library
------------------------------------------------------------------------------



What is Consumer Library
------------------------------------------------------------------------------
Consumer Library 是一个客户端程序, 它能从 Stream 中读取数据, 并对数据进行处理.


Consumer Behavior and Related Concepts
------------------------------------------------------------------------------
这里我们以 Kafka, AWS Kinesis 举例, 了解一下一个 Consumer 在消费数据时到底做了些什么.

为了方便说明, 我们定义以下概念:

- 我们用 ``Stream`` 来统一指代流数据系统, 无论它是 Kafka 还是 AWS Kinesis 还是别的什么.
- 用 ``Record`` 来指代一条条的数据, 也就是流数据中的数据最小单位. 虽然在 Kafka 中, 一条数据叫做 message, 但我们这里统一用 record 来指代.
- 用 ``Batch`` 来指代一小批按照顺序排列的 record. 凡是来自于同一个 producer 的 record 在一个 batch 中的顺序和它们在 produce 的时候的顺序一致.
- Consumer 会向 stream 拉取 batch 数据. 每次拉取数据是要指定一个起点 + limit 的. 这个起点可以是整个 stream 的最开头, 也可以是当前 stream 的结尾, 也可以是某个时间戳对应的位置, 也可以是手动指定的一个位置. 这个起点位置在 Kafka 中叫 offset, 在 AWS Kinesis 中叫 shard iterator, 在 Pulsar 中叫 MessageID. 我们统一称之为 ``Pointer``. 一个 batch 开始的 pointer 我们称之为 ``StartPointer``. 而如果这个 batch 是 Consumer 启动时的第一次拉取, 这个开始的 pointer 我们称之为 ``InitialPointer``.
- 获得 batch 之后会对里面的 record 进行处理. 有的 record 可能会处理成功, 有的可能会失败. 为了容错以及确保 record 只被处理刚好一次, 通常要 track 一个 batch 内所有的 record 的处理状态. 这样才能在重试的时候仅仅处理那些失败了的 record. 这个状态的信息通常需要被持久化, 这个被持久化的内容我们称之为 ``Checkpoint``, 而这个管理 Checkpoint 的模块我们称之为 ``Tracker``.
- 我们在获取 batch 的时候, 除了有我们用来获得 batch 用到的 ``StartPointer``, 通常也会获得这个 batch 结尾的 Pointer, 用来获取下一个 batch. 这个 batch 结尾的 Pointer 我们称之为 ``NextPointer``. 这个 StartPointer 和 NextPointer 在开始处理任何数据之前就应该将其持久化, 以便于在 Consumer 出错时能够恢复到上一次处理的位置. 它们也是被保存在 Checkpoint 中的, 并且也是由 Tracker 来负责管理.
- 当一个 batch 里的所有的 record 被处理完毕之后, 我们就可以将这 ``NextPointer`` 作为开始的 pointer, 继续获取下一个 batch. 这个过程我们称之为 ``Commit``. 这个 ``CurrentPointer`` 和 ``NextPointer``
- 有的时候我们不希望错误的 record 阻塞整个 processing, 那么我们通常会对错误的 record 进行持久化, 然后继续处理后续的 record 或 batch. 用于保存错误的 record 的持久化的系统我们称之为 ``DLQ`` (Dead Letter Queue). 虽然它名字里有一个 Queue, 但是它不一定是消息队列系统, 它可以是任何存储系统. 我们只是这么称呼它.

我们定义完概念, 也基本上了解一个 Consumer 的行为了:

1. Consumer 是以一个 batch 为周期不断重复进行处理的.
2. 如果 Consumer 是第一次启动, 那么会检查 checkpoint. 如果 checkpoint 存在, 则说明这是从之前的任务中恢复过来的, 我们可以里面的信息判断出 Pointer 以及是否要对 record 进行重试. 而如果 checkpoint 不存在, 则说明这是一个全新的任务, 我们可以选择用何种策略, 从哪里开始.
3. 然后就可以根据当前的信息拉取 batch 了. 如果拉取失败则可能是 stream 系统暂时不可用, 我们可以采用 exponential backoff 策略进行等待重试.
4. 如果拉取 batch 成功, 则需要创建 checkpoint 记录当前的状态.
4. 对每个 batch 内的 record 我们可以按照顺序消费或是并行消费的策略进行. 这取决于你的业务逻辑.
5. 对每个 record 的处理都需要有 tracker 来确保 exactly once 的语义.
