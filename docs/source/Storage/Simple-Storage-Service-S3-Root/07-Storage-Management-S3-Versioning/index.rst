Amazon S3 Storage Management - S3 Versioning
==============================================================================
Keywords: AWS, Amazon, S3, Version, Versioning


Overview
------------------------------------------------------------------------------
Versioning 是 AWS S3 中的一个功能, 可以让保留 Object 的所有修改历史, 并且在删除的时候也是用的软删除, 只是将其标记为已删除, 而所有的数据都还在. 这个功能在一些例如网盘, 文件历史等场景中非常有用. 配合上 Life Cycle 功能, 可以实现自动将旧数据或是已被标记为删除的数据在多少天后转移到低成本的存储中, 或是直接删除, 就可以实现最多保存 X 份历史记录的功能.

Reference:

- `Using versioning in S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html>`_


Working with objects in a versioning-enabled bucket
------------------------------------------------------------------------------
如果你的 Bucket 之前没有打开 Versioning, 在存了一些数据之后你打开了这个功能, 那么之前的数据会怎么样呢? 我们来详细介绍一下:

- 首先, 你打开 Versioning 之后, Bucket 会为所有已经存在的 Object 自动添加一个 Version, 这样就不会出现有的 object 没有 version 而有的 object 有 version 的问题了.
- 然后你任何对于 Version 的写操作都是在最新的 version 之上叠加一层. 如果是 Put 操作则会新增一个 version, 如果是 Delete 操作则会新增一个 delete marker.
- 而任何对于 Version 的 Delete 操作如果不指定 version 的话, 则是在最新的一个 version 之上叠加一个 delete marker. 而如果指定了 version 或是 delete marker, 则是删除这个 version 或是 delete marker.


Working with objects in a versioning-suspended bucket
------------------------------------------------------------------------------
如果你曾经打开了 Versioning, 然后又 Suspend 了这个功能. 之后你对这个 Bucket 进行读写会发生什么情况呢? 我们来详细介绍一下:

- 简单来说, 首先你需要打开 Versioning 才能将其关闭. 你关闭这个功能的瞬间 Bucket 什么事都不会做. 而之后你做任何 PUT, POST, COPY 的写操作, S3 都会在 Object 上创建一个 version = null 的 version. 而你之后对同一个 object 的覆写操作会覆盖这个 version = null 的版本. 换言之, 关闭 Versioning 并不会删除任何历史数据.
- 如果你 Put 的 object 还不存在, 那么就会创建一个 null 的 version.
- 如果你 Put 的 object 已经存在 (已经有 version) 了, 那么有两种情况:
    - 这个 object 是在 suspend 之前创建的, 那么它已经有 version 了, 那么就会在上面叠加加一个 null 的 version.
    - 这个 object 是在 suspend 之后创建的, 那么它还没有 version, 那么就会创建一个 null 的 version.
- 如果你要 Get 一个 object, 并且没有指定 version, 那么就会获得最新的 version. 如果指定了 version, 那么你仍然可以获得历史版本.
- 如果你要 Delete 一个 object, 那么只能在最新的 version 是 null 的 object 之上放一个 delete marker. 如果最新的 version 不是 null, 那么这个 request 会失败.
- 简而言之, Suspend 之后对 object 进行任何写操作 (put, delete) 都不会意外删除 Suspend 之前的所有 version, 确保了数据历史版本都不会丢失.


Sample Notebook
------------------------------------------------------------------------------
下面是一些我自己写的博文和代码示例:

.. autotoctree::
    :maxdepth: 1
