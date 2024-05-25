Optimistic Locking In DynamoDB
==============================================================================
Optimistic Locking (乐观锁) 是一种在分布式系统中对共享资源进行同步访问控制的机制. 它确保在同一时间只有一个进程或线程可以访问共享资源, 防止多个进程同时修改数据而导致的数据不一致问题. 我建议阅读以下资料了解乐观锁以及在它在 DynamoDB 中的实现.

- `Optimistic locking with version number <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.OptimisticLocking.html>`_: AWS 官方对 Optimistic Locking 的说明.
- `Pynamodb Support Optimistic Locking <https://pynamodb.readthedocs.io/en/latest/optimistic_locking.html>`_: pynamodb Python 库对 Optimistic Locking 的支持.
- `Optimistic Locking Pessimistic Locking <https://dev-exp-share.readthedocs.io/en/latest/search.html?q=Optimistic+Locking&check_keywords=yes&area=default>`_ 我写的一篇深度讨论乐观锁和悲观锁的文章. 不仅介绍了原理, 以及介绍了在不同的数据库系统中如何实现, 还评估了主流的数据库对这个特性的支持情况.
