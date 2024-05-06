.. _dynamodb-backups:

DynamoDB Backups
==============================================================================
Keywords: AWS, Amazon, DynamoDB, Backup


Overview
------------------------------------------------------------------------------
对于任何数据库系统, 备份功能都是保障数据安全的最后一道防线. Dynamodb 提供了两种备份方式:

- On-demand Backup: 该方案本质上是在一瞬间把数据库的机器节点的磁盘上锁一小段时间 (一般小于 1 秒), 然后创建一个磁盘的 Snapshot 备份. 由于基于 Snapshot 的全盘备份备份的实际上是索引, 所以创建 Snapshot 的时间非常快 (一般不超过 1 秒). 然后你可以用 Snapshot 重新创建一个跟原来的 DynamoDB table 一摸一样的 table.
- Point-in-time Recovery: 该方案本质上是备份了所有对 Table 的改动的日志. 你只要从头根据日志重现所有的写操作既可恢复整个数据库.


On-Demand Backup And Restore
------------------------------------------------------------------------------
Dynamodb 使用 Snapshot 技术, 使得备份和恢复对性能几乎没有影响. Dynamodb 支持两种备份方式:

1. AWS Backup Service: AWS Backup 是一个单独的 AWS 服务, 支持对多种 AWS Resource 的备份. 其中就包括 Dynamodb.
2. Dynamodb Backup: 是一个 Dynamodb 内置的功能, 你可以在 Console 上点击, 或是用一个 API Call 就对 Table 的全部数据做一个备份.


Point in Time Recovery for Dynamodb
------------------------------------------------------------------------------
简单来说 Point-in-time (PIT) 就是一种持续备份的机制. 你无需像 Dynamodb Backup 机制一样定期调用 API 进行备份. 不过 PIT 备份最多能恢复到 35 天前的状态.

要特别注意几点:

1. 如果你禁止了 PIT 又启用了 PIT, 那么你的恢复时间将被重置, 你最多恢复到你最新一次启用 PIT 时刻的状态.
2. 你选择恢复到之前时刻, 该操作只恢复数据, 不恢复 Settings. 你的 Settings 还是跟你进行恢复操作前一样.

这里提一嘴, PIT 是一个 Feature, 开启这个 Feature 没有额外的费用. 但是如果你用它来 Export 或者 Import 所产生的存储是要收费的. 并且只有开启这个功能才能使用 Export to S3 功能. 这个功能可以将某个时间点的 DynamoDB Table 中的所有数据导出到 S3 做离线分析. 这里不对 Export to S3 功能做详细介绍. 总之开启这个功能的好处多多, 非常建议你在创建所有的 DynamoDB Table 时开启这一功能.


Reference
------------------------------------------------------------------------------
- `Using On-Demand backup and restore for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BackupRestore.html>`_
- `Point-in-time recovery for DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.html>`_
