Workload Management (WLM)
==============================================================================
Keywords: AWS, Amazon, Athena.


Athena WLM Overview
------------------------------------------------------------------------------
Athena 是通过 Workgroup 来实现 WLM 的. 简单来说 Workgroup 是一个可以包含 Query Execution 的容器. 你可以创建不同的 Workgroup 并为不同的 Workgroup 指定:

- Analytic engine: Athena SQL | Apache Spark.
- Query result S3 location: query result 存放在哪里.
- Per query data usage control: 每个 query 最多允许扫描多大的数据, 最小 10MB, 最大 7EB (EB = 1000 PB, PB = 1000 TB, TB = 1000 GB)
- Work group data usage alert: 在一个时间段内, 例如 每分钟, 每小时, 每天 (最小每分钟, 最多每天), 如果扫描的数据量超过了指定大小则会触发警报, 并将警报以 notification 的形式发送到 SNS Topic.

由于 WLM 背后的算力几乎可以视为无限, 所以 WLM 跟资源分配没关系. 因为 Athena 每扫描 1 TB 就收费 $5.00, 所以这个功能主要是为管理开支而服务的.


Using Workgroup for Running Query
------------------------------------------------------------------------------
**指定用哪个 Workgroup 来运行 query**

你进入 Athena Console 的时候就能看到右上角有一个 Drop down menu 可以选择 Workgroup. 而实际上你在 Athena Console 上的每次点击都是调用了 `boto3.client("athena").start_query_execution(..., WorkGroup=...) <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena/client/start_query_execution.html>` 这个 API. 也就是说你在执行 Query 的时候就要指定 WorkGroup, 如果不指定则用的是默认的 ``primary`` Workgroup.

**管理谁能用哪个 Workgroup 来运行 query 的权限**

1. 首先你的 Principal 的 IAM Policy 里必须有: ``athena:StartQueryExecution`` Action 的权限.
2. 其次你的 Policy 里必须有: ``arn:aws:athena:us-east-1:123456789012:workgroup/${workgroup_name}`` Res 的权限.

仅此而已.

**监控 Query Performance 的统计以及监控 Data Usage**

在创建 Workgroup 的时候你可以勾选 "Publish query metrics to AWS CloudWatch" 选项. 然后你就可以在 CloudWatch 中创建 Dashboard, 并监控 Query Performance 和 Data Usage 了. 当然你还可以创建自定义的 Alert.


Reference
------------------------------------------------------------------------------
- `Workload management <https://docs.aws.amazon.com/athena/latest/ug/workload-management.html>`_
