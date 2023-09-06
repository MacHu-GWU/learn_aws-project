Amazon S3 Storage Management - S3 Object Lock
==============================================================================
Keywords: AWS, Amazon, S3


Summary
------------------------------------------------------------------------------
有些监管行业需要保证你存储层满组 write-once-read-many (WORM) model. 即数据一旦被写入, 一定时间内 (或永久) 就不能被修改和删除.

.. important::

    这个功能只能在创建 Bucket 的时候打开. 不能在已有的 Bucket 上打开. 你创建 Bucket 的时候设置的 Retention
 Period 会成为所有 Object 的默认设置. 而你在 Put object 的时候还可指定一个特定的 Retention Period 来覆盖 default 的设置.

Reference:

- `Using S3 Object Lock <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html>`_


Retention Periods
------------------------------------------------------------------------------
- `Retention period <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object_retention.html>`_: 指定一个时间段, 在这个时间段内, 不能修改或删除这个 Object. 但是这个 Object 可以被读取.
- `Legal hold <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_object_legal_hold.html>`_: 和 Retention period 类似, 区别是没有过期时间, 直到你手动关闭这个 Legal hold, 这个 Object 才能被修改或删除.


Retention Modes
------------------------------------------------------------------------------
Retention modes 是一个非常重要的概念. 目前 Object Lock 支持两种 retention modes:

- governance mode: users can't overwrite or delete an object version or alter its lock settings unless they have special permissions. With governance mode, you protect objects against being deleted by most users, but you can still grant some users permission to alter the retention settings or delete the object if necessary. You can also use governance mode to test retention-period settings before creating a compliance-mode retention period.
- compliance mode: a protected object version can't be overwritten or deleted by any user, including the root user in your AWS account. When an object is locked in compliance mode, its retention mode can't be changed, and its retention period can't be shortened. Compliance mode helps ensure that an object version can't be overwritten or deleted for the duration of the retention period.

简单来说 governance (监管) 模式就是说大部分人都改不了, 除非有特殊的 IAM 权限并且在 Request 的时候选择 bypass governance. 而 compliance (合规) 模式就是所有人都改不了, 包括开启这个模式的本人, 也包括 AWS Account Root User, 只有在这个数据到达 Retention period 之后才会解除.
