Amazon Kinesis Data Streams - Handle Slow Consumer
==============================================================================
Keywords: AWS, Amazon, Kinesis, Data Stream, Best Practice

假设对于每个 Shard, 每秒会产生 100 条 Record. 虽然一个每秒 Consumer 可以拉取 100 条 Record, 但每秒只能消费 10 条 Record. 这样 Shard 中未被处理的数据则会越来越多, 该怎么办呢? 简单来说就是: "单个 Consumer 实体的消费能力跟不上了一个 Shard 上数据产生的速度".

这种情况很自然的会想到增加 Shard 的数量, 使得每个 Shard 上的数据量能被 Consumer 所处理: 这样做很不经济, 因为流数据系统往往是 Consumer 吞吐量要大于 Producer 吞吐量, 你从 Reader 的 2MB 以及 Writer 的 1Mb Quota 上也能看出来这一点. 这会导致创建的 Shard 远远大于写入数据的所需的 Shard 数量, 造成很大的浪费.

其实这个问题的隐藏关键因素是, 同一个 Shard 上的数据消费是否可以打乱并行? 还是说必须要严格按照顺序消费.

如果可以打乱并行, 解决起来会比较简单. 我们可以让 Consumer 本身并不负责执行消费逻辑, 而是分发给多个 worker 并行去执行. 例如你可以用一个 Lambda 来 subscribe kinesis, 然后并发运行多个 Lambda 来消费数据.

如果不能打乱并行, 这个事情从逻辑上就不可行. 因为相当于你的 Producer 每秒产生 100 个必须严格按照顺序执行的任务, 但你每秒只能完成 10 个. 无论你怎么设计, 后面的任务都必须要等前面的任务, 所以你只能考虑看看能否优化你的 Consumer 让你的消费速度提高. 或者看看 Producer 产生的 100 个任务是否可以分成更小的组, 然后只要满足一个小组内的数据被严格按照顺序执行即可.
