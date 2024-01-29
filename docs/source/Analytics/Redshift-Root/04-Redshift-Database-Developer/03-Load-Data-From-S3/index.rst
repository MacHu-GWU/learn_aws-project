Load Data From S3 to Redshift
==============================================================================
Keywords: AWS, Amazon, Redshift, Copy

将大量数据 Load 到 Redshift 中的最佳办法是用 S3 作为媒介. 因为 Redshift 能以超高性能并行从 S3 中读数据. 而且 S3 到 Redshift 的网络是内网, 速度非常快. 用 SQL Client 执行 Insert 的本质是 TCP/IP 协议, 并且有一层数据要编译成 SQL, 然后 SQL 又要被解析成数据的过程. 而 S3 到 Redshift 没有数据编译反编译这一过程.


Understand Copy Command
------------------------------------------------------------------------------
A copy command tells Redshift:

- load to which table, which columns? you can custom column mapping.
- from where? s3 / database / others ..., a single file? a folder?
- authorization to perform this command, use either IAM or API Key
- data format? csv / json / parquet ...
- data format specified options, such as ``gzip``, ``IGNOREHEADER 1`` ...


Work with CSV File
------------------------------------------------------------------------------
Data for ``table.users``::

    id,name
    1,Alice
    2,Bob
    3,Cathy


Command::

    COPY users (id, name)
    FROM 's3://<bucket-name>/<data-file-key>'
    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
    csv
    IGNOREHEADER 1;

You can replace::

    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'

with::

    access_key_id 'AAAAAAAAAAAAAAAAAAAA'
    secret_access_key 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

If it is gzip compressed::

    COPY users (id, name)
    FROM 's3://<bucket-name>/<data-file-key>'
    iam_role 'arn:aws:iam::0123456789012:role/MyRedshiftRole'
    csv
    IGNOREHEADER 1
    gzip;


Load Data Best Practice
------------------------------------------------------------------------------
- **S3 COPY is the fastest loading mechanism of data from S3 to Redshift**.
- **Compress the data inside S3 before loading to Redshift**. S3 到 Redshift 的网络传输的速度要远远慢于在 Node 上对数据进行解压的速度, 所以压缩数据是有必要的.
- `Split big file into small files <https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-use-multiple-files.html>`_. Redshift Cluster 由多个 EC2 Instance 组成, 每个 Node 就是一个 EC2 Instance, 每个 Node 内部有根据 CPU 的数量, 分为多个 Slices, 每个 Slices 分配有一定得内存和磁盘. 一个 Node 的多个 Slices 可以并行读取数据. 假设你有 X 个 Node, 每个 Node 有 Y 个 Slices, 当你读取大文件时, 将大文件分为至少 X * Y 个小文件才能获得最高的效率.
- **Store the data already sorted in the sortkey order**. 对于每个读取到的文件中的数据, Redshift 需要使用 Sortkey Column 对其进行排序. 所以如果你能保证整个文件名的顺序和数据的顺序一致, 则会大大提高效率.
- 当文件无法用 glob 前缀表示, 例如分散在多个 bucket 中时候, 用 manifest 文件会比较稳当. 详情请参考 `Using a manifest to specify data files <https://docs.aws.amazon.com/redshift/latest/dg/loading-data-files-using-manifest.html>`_


Reference
------------------------------------------------------------------------------
- `Copy Command <https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html>`_
- `Copy Command Examples <https://docs.aws.amazon.com/redshift/latest/dg/r_COPY_command_examples.html>`_
- `Amazon Redshift best practices for loading data <https://docs.aws.amazon.com/redshift/latest/dg/c_loading-data-best-practices.html>`_
