Use Amazon CloudWatch metrics
==============================================================================
Keywords: AWS, Amazon, CloudWatch, CW, Metric, Metrics


What is Metrics
------------------------------------------------------------------------------
Metrics 本质上是对某个特定的指标的 measurement 的时间序列. 你可以理解为对 Logs 时间序列数据计算后的结果. 它本质上也是一个离散的时间序列. 通常一个 Metrics 是一个单一指标. 而 metrics 的 metadata 被称为 **dimension** (非常重要). 例如 EC2 的 CPU usage 是 metrics, 而 EC2 instance id 就是 dimension. 这是时间序列数据建模的关键技术之一.

Reference:

- `Use Amazon CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html>`_


Dimension
------------------------------------------------------------------------------



Metrics Insights Query
------------------------------------------------------------------------------
Metrics Insights Query 是一个对 Metrics 时间序列用类 SQL 语言来查询的工具. 他跟 CloudWatch Logs Insights 是完全不同的两个东西, 请不要将其混淆.

它的主要功能是, SELECT namespace/metrics, 限定在一定的时间区间内, 用 dimension 对 metrics 进行过滤, 然后用数学函数对其进行计算或者按照 time interval 进行聚合.

下面我们来看一个例子. 我们的日志数据是记录两个服务器 server 1, 2 上的响应时间. 下面这个脚本可以生成日志数据.

``s1_data_faker.py``

.. literalinclude:: ./s1_data_faker.py
   :language: python
   :linenos:

下面这个脚本使用了 metrics filter 来对日志进行过滤, 并生成了一个 metrics. 这个 metrics 是带 dimension 的, dimension 数据是从 server_id 中提取出来的.

``s2_create_metrics.py``

.. literalinclude:: ./s2_create_metrics.py
   :language: python
   :linenos:

下面这个脚本使用了 metrics insights query 来进行分析. 它有两种 API 风格. 一种是用结构化的 JSON 来 build 这个 query. 还有一种是用 SQL 语法来描述这个 query. SQL 语法更简洁好学, 但不适合参数化 (小心 SQL 注入). 下面这个例子两种方法都展示了.

``s3_metrics_insight.py``

.. literalinclude:: ./s3_metrics_insight.py
   :language: python
   :linenos:

Reference:

- `Query your metrics with CloudWatch Metrics Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/query_with_cloudwatch-metrics-insights.html>`_
- `get_metric_data <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_data.html>`_
- `Metrics Insights Limit <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-limits.html>`_
