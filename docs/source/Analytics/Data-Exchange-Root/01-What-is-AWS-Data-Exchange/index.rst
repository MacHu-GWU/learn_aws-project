What is AWS Data Exchange
==============================================================================
Keywords: Amazon, AWS, Data Exchange

AWS Data Exchange 是一个 AWS 的平台, 可供 数据提供商 (Provider) 和 数据使用方 (Subscriber) 在这个平台上浏览, 购买数据类的产品. 对于数据提供商来说, 它免除了 data delivery (如何交付数据), entitlement, or billing technology (收费手段) 等麻烦. 简单来说, 你如果有一个有价值的数据集, 你想要在网上卖, 那么通常你需要搭建一个网站, 然后用户需要创建账号, 付费购买后你就将数据发送给你的客户. 从数据提供商的角度讲, 搭建网站, 管理数据发送的系统都需要额外的工作. 而从数据购买方来说, 它是否能得到长期的数据更新, 以及它的权利如何得到保证, 其实数据购买方心理是很没底的. 而 AWS Data Exchange 提供了一个第三方平台, 方便了数据提供商进行售卖, 也用自己的信用给数据购买兜底, 从而使得数据类的产品的生意更容易成交.


What is an AWS Data Exchange product?
------------------------------------------------------------------------------
一个 AWS Data Exchange product (Product) 是在 AWS Data Exchange 服务中可供用户 Subscribe 的产品的最小单位. 它包含以下几个部分

**Product details**:

定义了产品的详细信息. 主要包括:

- name
- descriptions (both short and long)
- logo image
- support contact information

**Product offers**:

数据提供方提供的购买合同. 它定义了这个数据产品是如何交付到 Subscriber 手中, Provider 和 Subscriber 的权利和义务. 主要包括

- prices and durations.
- data subscription agreement.
- refund policy.
- the option to create custom offers.

**Data sets**:

一个 Dataset 是一个数据集, 你可以理解为多个 Database Table 数据的集合. 而一个 Product 可以有多个 Dataset. Dataset 是有 version 的, 每个 version 一旦 publish 就不可更改 (immutable). Provider 可以选择将哪个 Dataset publish 到 product 中.

Malware prevention
------------------------------------------------------------------------------
这是 AWS 的一个安全措施. 当 Provider 发布数据产品时, AWS 会扫描这些数据, 如果发现了恶意软件 (例如可执行文件), 那么 AWS 就会将其自动删除以保护 Subscriber.


Supported data sets
------------------------------------------------------------------------------


Accessing AWS Data Exchange
------------------------------------------------------------------------------


Pricing
------------------------------------------------------------------------------


Supported Regions
------------------------------------------------------------------------------


Related services
------------------------------------------------------------------------------
