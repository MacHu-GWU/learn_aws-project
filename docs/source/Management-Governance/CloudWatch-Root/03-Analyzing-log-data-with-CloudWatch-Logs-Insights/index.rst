Analyzing log data with CloudWatch Logs Insights
==============================================================================
Keywords: AWS, Amazon, CloudWatch, CW, Log, Logs, Insight, Insights


How do we learn CloudWatch Logs Insights
------------------------------------------------------------------------------
最好的学习方法永远是实践. 所以我们准备了一个脚本可以轻松的创建 Log Group / Stream 并且往里面每秒打一个自定义的 Log.

我们还有个函数可以轻松地清除这些资源. 一旦我们 run 了 ``delete_log_group`` API, 指定的 Log Group 以及下面的所有 Log Stream 的数据就都会被删除. 我们可以立刻开始一个新的实验.


Query Language Quick Start
------------------------------------------------------------------------------
CloudWatch Logs Insights (下面简称 Insights) 的查询语言是一个类 SQL 的语言. 它的语法包含这么几个部分:

1. 选择, 定义你想要选择哪些字段. 这里包括类似于 SQL 中的 ``SELECT`` 的用来选择字段的 `fields <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Fields.html>`_ 关键字, 以及用来创建图表的 `stats <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Stats.html>`_ 关键字.
2. 筛选, 定义你想要筛选哪些数据. 这里包括类似于 SQL 中的 ``WHERE`` 的用来筛选数据的 `filter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Filter.html>`_ 关键字.
3. 提取数据, 由于 Log 数据并不像 SQL 中的都是严格结构化的数据, 所以你有时候需要从 Log 中提取结构化的数据. 这里的关键字是 `parse <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Parse.html>`_.
4. 和 SQL 一样, Insights 也有 `limit <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Limit.html>`_ 关键字可以限制返回的数据条数, 以及 `sort <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-Sort.html>`_ 关键字可以按照指定的字段排序.

当然以上几个只是核心功能, Insights 还有一些针对 Log 的高阶语法. 我们先不急着展开讲, 之后我们会慢慢学到的.

下面这条是一个最基础的例子, 类似于 SQL 中的 ``SELECT * FROM TABLE LIMIT 10``. 其中 ``@timestamp`` 是 log 的时间戳, ``@message`` 是 log 的内容``. ``@logStream`` 和 ``@log`` 分别是 Stream 和 Group. 带 ``@`` 的都是 CloudWatch log 中的特殊字段::

    fields @timestamp, @message, @logStream, @log
    | sort @timestamp desc
    | limit 20

如果你的 Log Message 的结构是 ``{"server_id": "container-1", "processing_time": 500}``. 那么你可以直接用 JSON Dot Notation 来选择字段::

    fields @timestamp, @message, server_id, processing_time
    | sort @timestamp desc
    | limit 20

当然在 Filter 中的条件也可以使用 JSON Dot Notation::

    fields @timestamp, @message, server_id, processing_time
    | filter server_id = "container-1"
    | sort @timestamp desc
    | limit 20

这里有个小知识点, 如果你要对 timestamp 进行 filter 时, 它不支持 human readable format, 你需要自行将其转化为 millisecond 的 timestamp. 而且你转换的时候一定要注意时区, 否则你的结果可能会出现偏差::

    fields @timestamp, @message, server_id, processing_time
    | filter @timestamp <= 1699797262424
    | sort @timestamp desc
    | limit 20

如果你的 filter 的条件有多个, 你可以用 `逻辑运算符 <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-operations-functions.html#CWL_QuerySyntax-operations-Boolean>`_ ``and``, ``or``, ``not`` 来连接它们. 就跟在 SQL 中的 ``WHERE col1 = value1 and col2 = value2`` 一样.

Pattern
------------------------------------------------------------------------------
Pattern 是一个很强大的函数, 它可以对你的 Log 进行采样, 然后分析出来有哪些 Pattern. 例如我们的测试数据中有两种不同模式的 JSON::

    {"server_id": "container-1", "status": "succeeded"}
    {"server_id": "container-1", "processing_time": 2000}

那么 pattern 这个函数就可以自动分析出这两种 pattern 的 regex::

    fields @timestamp, @message
    | pattern @message


Playbook
------------------------------------------------------------------------------
这里我们提供了几个 Python 模块, 用于方便地创建 fake data, 以及测试不同的 query.

``recipe.py`` 一些能使得代码更精炼的模块.

.. literalinclude:: ./recipe.py
   :language: python
   :linenos:

``shared.py`` 该测试所用到的一些常用的变量值.

.. literalinclude:: ./shared.py
   :language: python
   :linenos:

``data_faker.py`` 用于创建测试数据的脚本.

.. literalinclude:: ./data_faker.py
   :language: python
   :linenos:

``run_query.py`` 用于测试 logs insights query 的脚本.

.. literalinclude:: ./run_query.py
   :language: python
   :linenos:
