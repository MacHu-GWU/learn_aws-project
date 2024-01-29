Manage Redshift Cluster - Resizing a Cluster
==============================================================================
Keywords: AWS, Amazon, Redshift, Scale, Resize


Elastic Resize
------------------------------------------------------------------------------
Redshift 没有自动伸缩的功能. 不过你可以通过 CloudWatch 监控各项指标, 然后用 Lambda 调 API 来自动伸缩. 2018-11-05 Redshift 发布了 Elastic Resize 功能, 这使得修改 Redshift Cluster 集群的大小的响应时间从以前的 15 分钟降到了 5 分钟以内.

- Scale your Amazon Redshift clusters up and down in minutes to get the performance you need, when you need it: https://aws.amazon.com/blogs/big-data/scale-your-amazon-redshift-clusters-up-and-down-in-minutes-to-get-the-performance-you-need-when-you-need-it/
- Elastic Resize: https://aws.amazon.com/about-aws/whats-new/2018/11/amazon-redshift-elastic-resize/
