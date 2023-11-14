Use Amazon CloudWatch metrics
==============================================================================
Keywords: AWS, Amazon, CloudWatch, CW, Metric, Metrics


What is Metrics
------------------------------------------------------------------------------
Metrics 本质上是对某个特定的指标的 measurement 的时间序列. 你可以理解为对 Logs 时间序列数据计算后的结果. 它本质上也是一个离散的时间序列. 通常一个 Metrics 是一个单一指标. 而 metrics 的 metadata 被称为 **dimension** (非常重要). 例如 EC2 的 CPU usage 是 metrics, 而 EC2 instance id 就是 dimension. 这是时间序列数据建模的关键技术之一.

Reference:

- `Use Amazon CloudWatch metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html>`_
