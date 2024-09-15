DynamoDB - Incremental Export
==============================================================================
这个 POC 是用来验证 DynamoDB 在 2023-09 推出的 Incremental Export 功能的.

下面这个 ``gen_data.py`` 脚本能够每一秒生成一条数据, 并且写入到 DynamoDB 中.

.. dropdown:: gen_data.py

    .. literalinclude:: ./gen_data.py
       :language: python
       :linenos:

这个 ``export_data.py`` 脚本则分别导出了 initial load 和 incremental load, 并且读取了里面的数据.

.. dropdown:: export_data.py

    .. literalinclude:: ./export_data.py
       :language: python
       :linenos:

**重要结论**

- full export 的时候, export time 是结尾时间, 是 exclusive 的 (不包含 export time 本身)
- incremental export 的时候, start time 是包括本身的, 而 end time 不包括.
- full export 的数据是在 Item field 下的.
- incremental export 的数据是在 NewImage field 下的.
- incremental export 的 window 必须在 15 分钟以上.
- incremental export 会在 S3 prefix 下直接创建一个 data 的目录来保存数据 (而 full export 会根据时间戳自动创建一个子文件夹). 所以建议 incremental export 的 prefix 的 folder name 包含 export period 的时间戳, 这样能比较确保不同的 incremental export 不会互相影响.
- 哪怕是很小的数据量, 一般 export 的时间也在 5 分钟左右.

由以上结论可以得出, 现在要想将 DynamoDB 同步到数据仓库中, 不用 fancy 的流数据处理, 就能实现不超过 20 - 30 分钟数据延迟的同步. 对于大多数应用来说这已经够了. 这个 20 分钟是建立在假设你有一个 8:00 的数据, 你只有在 8:15 的时候才能开始运行一个 15 分钟窗口的 incremental export, 而 export 本身需要 5 分钟, 数据处理需要大约 1 分钟, 所以总共的延迟是 20 分钟. 当然你也可以在 8:05 的时候就做一个 7:50 - 8:05 的 export, 然后数据处理时 filter 掉不要的数据, 这样的延迟可以做到 10 分钟左右. 但无论怎么样, 数据延迟都不会低于 export 本身需要的时间 (大约 5 分钟).

**DynamoDB to Data Lake Solution**

我的这套方案不需要任何 Orchestration, 只需要 Lambda Function 既可.

1. **Initial Export Lambda**:
    - Description: 这个 Lambda 的任务是负责打开 PITR, 然后适时启动 Full Export Job.
    - Detail: 它会不断检测目标 Table 是否打开了 PITR, 如果打开了, 就会在 15 分钟整点后启动一个 Export Job, 并且在 S3 中写一个 Tracker 文件, 表示时间已经推进到了这个 Initial Load Export Time. 这样后续的 Incremental Export Lambda 看到这个 S3 文件就知道可以开始进行 Incremental Export 了.
    - Schedule: 15 分钟运行一次.
2. **Initial Export Data Processing Lambda**:
    - Description: 这个 Lambda 的任务是负责处理 Full Export 的数据, 并且写入到 Data Lake 中.
    - Detail: 这个 Lambda 会 5 分钟运行一次, 检查 Full Export 完成没有, 如果完成了就会读取 Full Export 的数据, 然后写入到 Data Lake 中. 这个 Lambda 会根据 Full Export 的时间戳来决定写入到 Data Lake 的目录结构.
    - Schedule: 15 分钟运行一次.
3. **Incremental Export Lambda**: 这个
    - Schedule: 5 分钟运行一次.
4. Incremental Export Data Processing Lambda.

1. 你先开启 PITR. 然后等个 15 分钟, 然后找之前最近的一个 15 分钟的节点, 进行一次 Full Export. 例如你 7:55 打开的 PITR, 然后你 8:00 的时候进行一次把 8:00 之前的全部数据导出的 Full Export, 然后用本地运行的程序运行个一次

你需要两个定时运行的 Lambda