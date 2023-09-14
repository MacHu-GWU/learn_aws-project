AWS VPC Endpoint for S3
==============================================================================
Keywords: AWS, Amazon, S3, Private Link


What is VPC Endpoint
------------------------------------------------------------------------------
首先 VPC 是亚马逊的最重要的虚拟网络服务, 能让用户把虚拟机部署到私有网络上, 让虚拟机之间的通信不离开 VPC 的网络. 如果当用户从 VPC 内部发起 AWS API 的请求, 默认情况下跟你在家里的机器上发起请求是一样的, 会找到 AWS Service Endpoint 的 DNS 名字 ``com.amazonaws.us-east-1.s3``, 通过 Internet Gateway 或是 Nat Gateway 走公网发送请求. 但有的公司不希望这些请求中的数据通过公网传输, 又或者有的计算资源例如位于 VPC 中的 EC2 压根没有开放公网, VPC Endpoint 就是为这种情况设计的.

VPC Endpoint 能为 VPC 与 AWS Service Endpoint 之间建立一个私有链接, 使得请求不会离开 AWS 数据中心的私网, 从而进一步保证安全.


VPC Endpoint 的分类
------------------------------------------------------------------------------
1. Interface Endpoints: 具体实现技术叫做 Private Link, 他是通过把一个 Elastic Network Interface, 类似 Internet Gateway 或是 Nat Gateway, 是一个具体的硬件, 被放置在 Subnet 中, 并给予一个具体的 DNS Name 作为你想要连接的 Service Endpoint 的 Alias, 例如 vpc-1234.kinesis.us-east-1.vpce.amazonaws.com . 这个 ENI 和 Service Endpoint 之间的连接是不走公网的. 但是, 你的 API 中的请求就需要指定为这个新的 Endpoint. 而如果不指定则请求还是会走公网, 所以会有一些麻烦. 可幸的是, AWS 提供了一个选项叫做 private DNS for endpoint. 如果打开, 只要你在 VPC 内, 即使你指定的是原有默认走公网的 Endpoint, 请求也会走 ENI. 前提是你 VPC 的设置中需要打开 ``true:enableDnsHostnames`` and ``enableDnsSupport`` 这两个选项. Interface Endpoint 主要为 S3 和 Dynamodb 以外的服务提供直连. Interface Endpoint 要计费
2. Gateway Endpoint: 具体实现方式是将一个虚拟的 Gateway 放在 VPC 的边缘. Gateway 和 S3 之间的连接是走 AWS 内网的 (Interface Endpoint 是放在 Subnet 中, 而且是个实际的硬件, 所以要收费). 然后在 Route Table 中定义把请求路由到 Gateway 即可. 麻烦的是, 你需要配置 RouteTable. 好处是 Gateway Endpoint 不收费. Gateway Endpoint 只为 S3 DynamoDB 服务.

简单来说 Gateway endpoint 是一个路由而不是一个设备, 它只是将你发往公网的 S3 / Dynamodb (支持这两个) 路由到 AWS 内部的 endpoint. 而 Interface endpoint 是一个 ENI 设备, 你的请求要指定 Endpoint 到这个 ENI 设备而不是标准的 public endpoint, 它支持的服务更多. 两种 endpoint 都能让你的流量不走公网, 并且都不需要昂贵的 Nat Gateway. 如果你的请求只是跟 AWS 服务通信, 那么你不需要 Nat Gateway, 但如果你要从公网下载东西, 那么还是需要 Nat Gateway 的.

Reference:

- `Types of VPC endpoints for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#types-of-vpc-endpoints-for-s3>`_
- `VPC Interface Endpoint vs Gateway Endpoint in AWS <https://digitalcloud.training/vpc-interface-endpoint-vs-gateway-endpoint-in-aws/>`_


Create VPC Endpoint for S3
------------------------------------------------------------------------------
1. 到 VPC 的 AWS Console.
2. 在左边菜单中找到 Endpoints. 点击 Create endpoint
3. Service category 选择 AWS Services, 然后再搜索框中搜索 S3, 选择 com.amazonaws.us-east-1.s3 + Gateway 即可. 至于 interface endpoint 和 gateway endpoint 的区别请看上面.


Reference
------------------------------------------------------------------------------
- `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_
- `What is VPC endpoints <https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html>`_: VPC 文档中对 VPC Endpoint 的介绍.
- `Amazon VPC Endpoints for Amazon S3 <https://docs.aws.amazon.com/glue/latest/dg/vpc-endpoints-s3.html>`_: Glue 文档中对如何访问配置了 VPC Endpoint 的 S3 bucket 的介绍.
