.. _aws-cloudwatch-overview:

Amazon CloudWatch Overview
==============================================================================
Keywords: AWS, Amazon, CloudWatch, CW, Overview.


Visibility 和 Monitoring 系统简介和行业现状
------------------------------------------------------------------------------
AWS CloudWatch 是 AWS 旗下的一款围绕着日志来构建的存储, 分析, 可视化的监控系统. 监控系统在互联网的发展的历史非常悠久. 期间涌现了非常多优秀的开源框架, 开源软件, 商业产品. 为了能更好的理解和学习 CloudWatch, 我希望先对监控系统行业的现状 (本文写于 2023 年) 做一个简单的介绍.


为什么需要 Visibility 和 Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
一个成熟的商业公司, 是不希望它的商业产品以及后台的系统发生故障导致商业损失的. 但是故障是不可能完全避免的, 我们能做的是通过监控来尽早的发现问题的苗头, 以及在故障发生的时候能够快速的溯源定位问题. 这就需要我们对系统的运行状态有一个全面的了解, 也就是 Visibility. 而一个监控系统能帮助我们在问题还没有扩大到非常严重的地步的时候就能发现问题, 也就是 Monitoring.


监控系统的三剑客 Logging, Metrics, Tracing.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
监控系统领域有三个重要的概念, Logging, Metrics, Tracing.

- Logging: 也叫日志, 相信开发者对它都很熟悉. 例如运行程序的时候 Print 出来的非结构化的或者结构化的信息就叫做 Logging. 日志的本质是一些离散的事件的集合. 也是监控系统最基础的组成部分.
- Metrics: 也叫指标, 相信 Business 的工作者对它很熟悉, 往往会为了衡量我们对目标的完成度, 我们要衡量这些这些指标. 对于某个我们感兴趣的特定信息就叫做 Metrics. 例如 CPU 的使用率, 错误发生的次数, 系统响应的延时, 这都叫做 Metrics. Metrics 通常是一个数值量, 并且是可以根据时间进行聚合的. 我们一般只关心在一定周期内的 Metrics 数值, 例如 1 分钟内的 CPU 使用率, 1 分钟内的错误发生次数, 1 分钟内的系统响应延时. Metrics 可以看错是对 Logging 进行聚合分析后的结果. 跟 Metrics 相关的还有一个 Alarm 的概念. Alarm 本质是 Metrics 达到某个阈值或是满足某种条件的特殊时间. 例如 CPU 使用率持续 1 小时高于 90% 就可以算是一个 Alarm. 我们最终关心的也是 Alarm, 不过我们必须先要有 Metrics, 才可能有 Alarm.
- Tracing: 也叫埋点, 相信运维对它都很熟悉. 任何用来追踪溯源的信息都可以被称作 Trace. 在实际应用中, Trace 本质上是一个特殊用途的 Logging, 而 Trace 往往是记录在一个事务生命周期内发生的事情. 之所以我们叫它埋点, 是因为我们创建 Trace 的时候问题往往还没有发生, 我们只是将这些 Logging 埋在这里, 一旦出现问题, 它们就起作用了.


监控系统的架构以及组件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
如果要搭建一个完整的监控系统, 这个系统中会有哪些组件呢?

1. Log Client: 也就是嵌入到应用程序中用于生成日志, 发送日志的客户端程序. 每个编程语言几乎都有很多这类的库和框架.
    - requirements: 作为一个 Log Client, 能生成非结构化或结构化的日志, 并且能将日志发送到各种 log sink (日志的接收端), 并带一些 buffer 以提高吞吐量, 以及失败重试等高级功能.
2. Log pipeline: 日志管道. Log Client 一般会将日志发送到专门的管道. 管道是一个将日志和日志存储解耦合的组件. 因为一个日志可能会被发送到多个存储系统中, 并且到达不同的存储系统前可能需要做不同的处理. 所以不直接将日志发送到存储, 而是先发送到管道是很有必要的.
    - requirements: 作为一个 Log pipeline, 能保证日志不会因为系统崩溃而丢失, 能横向扩展以应付超大流量, 能够支持 publisher 和 subscriber 模型, 是基本需求.
3. Log Storage: 日志存储. 你总得有个地方长期储存日志. 有些日志存储数据库还自带分析查询功能.
4. Log Analytics: 日志分析. 通常是一个 MMP 分布式查询引擎. 能支持多种对数据的查询需求, 聚合分析, 时序分析等. Log Storage 和 Log Analytics 有时候会合并成一个组件, 但有的系统设计中会将其解耦合, 使得整个系统更灵活. 而对 Metrics 的计算, 以及对 Trace 的分析一般是由这个系统完成.
5. Visualization and Dashboard: 当我们的监控需求非常明确的时候, 就需要一个可视化面板能供维护人员实时监控系统的指标. 毕竟作为人类, 我们更喜欢看图表, 而不是看一堆数字.
6. Alarm and Notification: 当 Metrics 达到一定阈值, 也就触发了一个 Alarm 事件. 这时我们就要发邮件或者短信通知需要知道这个事情的人 (或者机器), 让维护人员介入, 定位原因, 评估影响. Alarm 事件还可以被程序自动化处理, 例如自动扩容, 自动重启等.
7. Alarm Reaction: 对 Alarm 的反应就成为 Alarm Reaction. 我们通常需要一个 publisher 和 subscriber 系统来将 Alarm 和反应解耦合.


流行的监控系统软件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
我们按照上面的组件划分, 来看看现在业内流行的监控系统软件. 我个人是 AWS 云架构师, 主力语言是 Python, 所以难免有倾向性, 并且会有遗漏, 请见谅.

1. Log Client: 这里我只列出了 Python 社区的工具. 我们主要考虑维护良好, 社区活跃的开源项目.
    - `loguru <https://github.com/Delgan/loguru>`_: 流行度最高的库. 自定义的能力最高. 例如最关键的自定义 log sink. 唯一的遗憾是它是 2018 年的项目, 目前还没有到达 1.0 稳定版.
    - `logbook <https://logbook.readthedocs.io/en/stable/index.html>`_: 历史悠久的库. 它是 2010 年的项目. 使用者也很多.
    - `structlog <https://www.structlog.org/en/stable/>`_: 有商业支持的库. 它是 2013 年的项目, 目前已经达到稳定多年.
    - 我个人选择 structlog 或 loguru
2. Log Pipeline: 任何的流处理, 消息队列系统均可达到这一目的.
    - `logstash <https://www.elastic.co/guide/en/logstash/current/introduction.html>`_: 大名鼎鼎的 ElasticSearch 公司退出的 ELK stack 中的 L. 如果你后续的 Log storage 和 analytics 用的 ElasticSearch, 那么 LogStash 很好, 反之就很一般了.
    - `kafka <https://kafka.apache.org/>`_: 业内流数据中间件的标杆. 和各种其他系统的兼容性极佳.
    - `AWS Kinesis Data Stream <https://aws.amazon.com/kinesis/data-streams/>`_: AWS 的流数据中间件, 无运维, 自扩容. 相当于无服务版本的 Kafka.
3. Log Storage: 日志系统是一个典型的只增加, 不修改的系统. 一般以行为单位存储的关系数据库就不合适了, 而数据仓库类型的存储会更合适一些.
    - `AWS S3 <https://aws.amazon.com/s3/>`_ 以及其他对象存储服务: 日志归档存储的首选. 后续可以对这些数据进行二次处理和分析.
    - `ElasticSearch <https://www.elastic.co/elasticsearch>`_ / `AWS OpenSearch <https://aws.amazon.com/opensearch-service/>`_ 搜索数据库: 全文搜索, 聚合分析的首选. 业内最强搜索数据库.
    - `AWS Redshift <https://aws.amazon.com/redshift/>`_ 以及 Snowflake 等各种数据仓库: 适合处理结构化的日志. 主打的是超高的大数据分析性能.
    - `InfluxDB <https://www.influxdata.com/>`_, `Prometheus <https://prometheus.io/>`_, `AWS TimeStream DB <https://aws.amazon.com/timestream/>`_: 专业的时序数据库. 适合处理时序数据, 例如根据时间聚合计算 Metrics.
    - `AWS CloudWatch Log <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html>`_: 这个比较特殊, 是 AWS 云原生的一套日志服务. 既可以做存储, 也可以做分析, 还能做 Metrics, Alarm, 还能做 Dashboard. 你可以直接把数据打到 AWS CW.
4. Log Analytics:
    - 前面提到的 ElasticSearch, AWS OpenSearch, AWS Redshift, InfluxDB, Prometheus, TimeStream DB 都自带查询和分析能力, 都很不错. 而如果只是全文搜索, 那么只有 ElasticSearch 和 AWS OpenSearch 比较合适. 虽然数据仓库也能做, 但是性能不够好.
    - `AWS CloudWatch Log Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html>`_: 是 AWS 的一款无服务的日志分析工具. 按照扫描的数据量收费.
5. Visualization and Dashboard: 这个领域的工具就太多了. 理论上任何 BI 面板例如 PowerBI, Tableau, AWS QuickSight 都可以. 但是由于日志和监控领域的数据通常是时序数据, 所以有专业的工具.
    - ElasticSearch 旗下 `Kibana <https://www.elastic.co/kibana>`_: 如果你的面板是以 ElasticSearch 为后台, 那么直接上 Kibana 就完了.
    - `Grafana <https://grafana.com/>`_: 开源的监控平台, 支持很多种数据存储系统. 如果你用的是 Prometheus, 那么无脑上 Grafana 就完了.
6. Alarm and Notification: 在 Alarm 这一点上你可以选择自己实现计算部分, 然后发送通知. 有一些产品支持托管式的 Metrics 计算. 而 Notification 任何事件驱动的系统都可以.
    - `AWS CloudWatch Metrics Filter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringPolicyExamples.html>`_ 可以实现托管式的 Metrics 计算.
    - `AWS SNS <https://aws.amazon.com/sns/>`_ 一个专为 notification 设置的系统, 自带支持邮件短信, 以及任何 subscriber. 你要用 Kafka 也可以. 不过还是 SNS 为首选.
7. Alarm Reaction: 任何可以用来运行业务逻辑的计算单元, 都可以,
    - `AWS Lambda Function <https://aws.amazon.com/lambda/>`_: 无服务计算. 可以提供一个环境让你跑任何代码. 并且 subscribe SNS.
    - `AWS Step Functions <https://aws.amazon.com/step-functions/>`_ 或 `Airflow <https://airflow.apache.org/>`_ 等编排工具, 可以用来编排复杂的业务逻辑.

这里领域还有很多公司提供全套的解决方案, 例如下面这些, 这里就不一一展开了.

- DataDog
- NewRelic
- Dynatrace
- Splunk


How does AWS CloudWatch Work
------------------------------------------------------------------------------
AWS CloudWatch (CW) 是 AWS 云原生的监控系统. 它的特点是无运维, 无需配置, 无需维护. 你只需要把数据打到 AWS CloudWatch, 然后就可以在 AWS CloudWatch 上看到数据, 对数据进行查询, 并且可以针对特定的事件 Alarm, 以及做 Dashboard.

CW 由于以下几个组件组成:

1. 基础设施:
    - `Log Group 和 Log Stream <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_. Log Stream 是来自于同一个数据源 (可以是物理意义上的也可以是逻辑意义上的) 的时间序列日志. 而 Log Group 则是一组 retention, monitoring, access control settings 都一样的 Log Stream. 你只需要将 Log 用 API 打到 Log Stream 即可. 它们的本质就是支持查询的一个 Log 存储系统. 你要是需要, 也可以将其中的数据导出到其他系统, 例如 Redshift, ElasticSearch 中. 这就相当于你自己维护了一个 ElasticSearch 集群, 并且自己为 Log 日志创建了 Index 等一系列分库分表等策略. 又或者是你创建了一个 InfluxDB 时间序列数据库用来存储日志数据. 而在 CloudWatch 中你什么都不用做.
2. 核心组件:
    - `CloudWatch log insight <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html>`_ 是一个允许用户用查询语法对 Log 进行分析的工具, 类似于 ElasticSearch 的查询语言, 不过你无需维护任何基础设施.
    - `Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Metric>`_ 则是一组跟业务相关的指标的时间序列. 例如每分钟的 App 平均响应时间. Metrics 通常是通过对 Log 进行筛选, 聚合分析之后得到的结果. 而用户可以轻松地自定义分析的逻辑. 这就相当于是你自己部署了一个应用, 每隔几秒钟就 Run 一次分析, 并刷新结果. 只不过你完全无需维护任何基础设施, 也不需要部署任何东西.
    - `Alarm <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#CloudWatchAlarms>`_ 则是 Metrics 数值满足某一条件的特殊事件. 例如你的 App 每分钟的平均响应时间在 1 小时内连续超过了 1 秒, 这就可以是一个 Alarm. 它就相当于是你自己部署了一个应用, 每隔几秒就检查一次 Metrics, 看看是否满足某种条件. 如果满足, 则发送 Notification. 只不过你完全无需维护任何基础设施, 也不需要部署任何东西. Alarm 可以通过 SNS Topic 或是 Event Bridge 跟其他系统进行集成.
3. 应用层:
    - `Dashboard <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html>`_ 则是一个可自定义的面板. 它支持 10 多种常用的图表, 例如折线图, 柱状图, 饼图等等. 这些图表本质上是将 Metrics 中的数据显示出来. 而且它还允许你用 Lambda Function + 自定义的 JavaScript 来构建任何你想要的图表, 显示你想要的数据. 它就相当于你购买了 Tableau 等类似的面板软件, 而你什么也不用部署, 直接用即可.

这一套下来, 你就拥有了一个完整的云原生监控系统. 相比传统的 ElasticSearch + LogStash + Kibana 或者自己构建一套 Kafka + 容器的流数据处理系统, 自己架设一套数据库, 维护 ElasticSearch 集群以支持日志分析, 购买可视化图表软件例如 Tableau, 最后还要维护这套系统的扩容和健康, 你几乎什么都不用维护, 只要专注于你的业务就可以了. 虽然市场上的这些专业工具都很强大, 但是 AWS 这套系统能解决市场上 90% 的需求, 并且从想法到落地的速度要比分别购买这些组件并将他们集成起来要快一个数量级. 这套方案既可以助力小团队, 也可以支撑起一个大型企业的需求.


CloudWatch Knowledge Graph
------------------------------------------------------------------------------
以下是 CloudWatch 的知识图谱, 对所有的知识点进行了一个梳理.

- Manage Log Group and Stream:
    - Log Group: 创建, 并配置 Retention, KMS Encryption
    - Log Stream: 创建 Stream
    - 如何将你的团队, 你的项目, 你的应用, 你部署的计算单元与 Group 和 Stream 一一对应起来.
- Log Insight:
    - 如何用 Log Insight 对 Log 进行查询, 分析.
    - 