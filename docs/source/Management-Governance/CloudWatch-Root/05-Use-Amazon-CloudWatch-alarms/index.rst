Use Amazon CloudWatch Alarms
==============================================================================
Keywords: AWS, Amazon, CloudWatch, CW, Alarm, Alarms


What is Alarm
------------------------------------------------------------------------------
Alarm 本质是对 Metrics 进行一些数学计算后的结果满足了某种条件的特殊事件. 例如对于每分钟的 CPU 的使用率这个 Metrics, 如果 10 分钟内的平均使用率超过了 90%, 那么这就是一个 Alarm 事件.


How to Create an Alarm
------------------------------------------------------------------------------
创建 Alarm 的方式有很多种. 从你所使用的工具的角度, 你可以用 Console, 也可以用 API, 也可以用 IAC (Infrastructure as Code). 但我们重点不讨论这个. 我们重点讨论从业务逻辑的角度, 有哪些创建 Alarm 的方法.

**AWS recommended Alarm** 是一种很特别的方式. 因为很多 AWS service 例如 EC2, RDS, Lambda 有一些原生的 Metrics. 对这些原生 Metrics 进行监控是非常常见的需求. 所以 AWS 为这些 Metrics 创建了很多 recommended Alarm, 使得用户可以很轻松的创建针对这些 Metrics 的 Alarm. 这篇文档里有详细的使用说明以及所支持的 recommended Alarm 列表 `Best practice alarm recommendations for AWS services <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best-Practice-Alarms.html>`_.

主流的创建 Alarm 的逻辑是根据 Metrics 创建. 继续细分的话, 有下面几种方式:

1. `根据 static threshold <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ConsoleAlarms.html>`_: 也就是这个 metrics 的值只要达到某个值, 就触发 Alarm.
2. `根据 math express <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create-alarm-on-metric-math-expression.html>`_: 也就是对这个 metrics 进行数学计算, 例如求和, 平均, 最大最小值.
3. `根据 metrics insights query <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Metrics_Insights_Alarm.html>`_: 也就是相当于你每几秒就 run 一个 metrics query 来计算一个值, 如果这个值达到某种条件就报警. 请注意, metrics query 和 logs insight query 是两个不同的东西.
4. `根据 anomaly detection <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Anomaly_Detection_Alarm.html>`_: 也就是统计中的 outlier, 你可以自己指定 N 倍的标准差, 如果 metrics 超过了这个范围就报警.


Combining Alarms
------------------------------------------------------------------------------
这是一个非常有用的功能. 你可以将多个 Alarms 整合成一个 Composite Alarm. 当任意一个 Alarm 变成 InAlarm 的时候这个 Composite Alarm 就视为 InAlarm. 当所有的 Alarm 都变成了 OK 时它才会变为 OK.

Reference:

- `Combining alarms <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html>`_


Alarm Actions
------------------------------------------------------------------------------
在以下三种情况下 Alarm 会触发一个 Action.

1. 当 Alarm 超过了指定的 Threshold 的时候. 这也是最常见的, 也就是普通意义上的报警.
2. 当 Alarm 回到了指定的 Threshold 以下时, 也就是警报解除.
3. 当出现了 Insufficient Data 的时候, 也就是数据不足. 这时候 Alarm 变得不可靠, 可能需要人工介入.

Alarm 的 Actions 有很多种. 最常用的, 也是扩展性最好的是发送一个 Notification 给 SNS. 这样你可以用 Lambda 来 Subscribe SNS 从而实现任何复杂的 Action 逻辑. 除此之外, 它还原生支持以下 Actions:

1. Auto Scaling action: 自动 scale in / out
2. EC2 Action: 关机或开机
3. System Manager action:

注意, 这里的触发是一次性的, 也就是仅仅在 Transition 发生的时候会触发. 但如果它一直停留在 InAlarm 的状态下, 它是不会一直执行 Action 的. 如果你想要实现重复不断地执行 Action, 你可以用 Event Bridge 捕获 Alarm State Transition 的 event, 然后触发一个 StepFunction 来每隔一段时间检查一次 Alarm 的状态, 如果还是 InAlarm 的状态, 就执行 Action. 当然你也可以实现 exponential backoff 的机制. 这里有一篇博文详细介绍了这一方法 `How to enable Amazon CloudWatch Alarms to send repeated notifications <https://aws.amazon.com/blogs/mt/how-to-enable-amazon-cloudwatch-alarms-to-send-repeated-notifications/>`_.


Example
------------------------------------------------------------------------------
本节我们会在 AWS 上创建一个真实的 Alarm, 并且在警报响起的时候给自己发邮件.

第一步, 配置我们要用的 AWS Account 以及 log group,

.. literalinclude:: ./shared.py
   :language: python
   :linenos:

然后我们运行一个 data faker 不断地把 log 打到 log group.

.. literalinclude:: ./s1_data_faker.py
   :language: python
   :linenos:

然后我们用 metrics filter 创建一个 Metrics

.. literalinclude:: ./s2_create_metrics.py
   :language: python
   :linenos:

接下来我们手动进入 AWS Console, 找到我们的 metrics, 选中这个 metrics, 然后点击 Create Alarm. 接下来填入以下信息:

- Specify metric and conditions:
    - Statistic = Average
    - Period = 1 minute
    - Threshold type = Static
    - Whenever AverageProcessingTime is... = Greater
    - than... = 1000
    - Next
- Configure actions:
    - Notification
        - Alarm state trigger = In alarm
        - Create new topic, 并填写 topic 名字 (默认的就好) 以及你的 email. 之后你会收到一封确认 subscription 的邮件.

由于我们的设定是 AverageProcessingTime 大约是 5500 左右, 所以一分钟后你就会收到警报邮件.

当然, 我们可以用 Lambda Function 来实现任何复杂的逻辑.
