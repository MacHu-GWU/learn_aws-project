Hosting a static website on Amazon S3
==============================================================================
Keywords: AWS, Amazon, S3, Host, Hosting


Summary
------------------------------------------------------------------------------
使用 S3 作为 Host 静态网站的后台是一种非常方便省钱的方式. 传统静态网站都是需要一个长期在线的文件服务器, 这个文件服务器本身就是一部分开支. 如果使用 S3, 则你只需要支付存储和流量的费用即可. 并且 S3 有很多优势, 比如可以使用 CDN, 可以使用 Route53 换域名等等, 都是云原生支持的, 非常方便安全.


使用 S3 host static website 的关键步骤
------------------------------------------------------------------------------
1. 创建一个 S3 Bucket, 并且在 bucket 里的 permissions 菜单里将 Block public access (bucket settings) 设置为 Off. 这并不意味着你的数据就全变成 public 了, 这只是意味着关闭了 block public access 的功能. 这里要注意的是, 除了每个 bucket 可以单独设置这个, 在整个 Account 的 `S3 settings <https://s3.console.aws.amazon.com/s3/settings?region=us-east-1>`_ 也可以设置对全部 bucket 生效的 block public access settings. 通常情况下一个安全的 AWS Accounts 会将这个设置打开, 也就是所有 bucket 默认拒绝 public access. 为了 host website, 你需要将 account 级别的这个设置关掉才能对具体的 bucket 也关掉这个设置. 但这意味着新建的 bucket 就不会默认打开这个设置了. 所以我一般推荐专门用一个 AWS Account 来做 public facing 的事情.
2. 到 bucket 里的 properties 菜单里将 Static website hosting 打开.
3. 到 bucket 里的 permissions 菜单里修改 Bucket policy, 定义谁可以访问这里的数据. 就如前面说的, 关闭 Block public access 并不会让你的数据变成 public, 而 Bucket policy 才是真正定义了将你的网站变成 public.

这里有两个 Statement 最为重要, 一个是 Allow 的部分, 定义了谁可以访问. 一个是 Deny, 定义了谁不可以访问. AWS 的规则是 explicit deny > explicit allow > default deny.

Allow 的部分一般是这样, 允许所有人访问这里的数据::

    {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::bucket-name/*"
    }

Deny 的部分有很多种选择, 但是通常的目的是为了默认 deny 所有人, 除非是来自于某些受信的网络. 例如下面这个例子是只允许某些 IP 地址段访问, 而 deny 掉所有其他人::

    {
        "Sid": "VpcSourceIp",
        "Effect": "Deny",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": [
            "arn:aws:s3:::bucket-name",
            "arn:aws:s3:::bucket-name/*"
        ],
        "Condition": {
            "NotIpAddress": {
                "aws:SourceIp": [
                    "111.111.111.111/32"
                ]
            }
        }
    }

这里的关键是 ``Condition`` 的部分. 这里还有几个例子可以参考.

只允许来自于某些 VPC Endpoint 的访问, 使用的是 VPC id::

    "Condition": {
        "StringNotEquals": {
            "aws:SourceVpce": [
                "vpce-1111111",
                "vpce-2222222"
            ]
        }
    },

只允许来自于某些 VPC 的访问, 使用的是 VPC CIDR block::

    "Condition": {
        "NotIpAddress": {
            "aws:VpcSourceIp": [
                "10.1.1.1/32",
                "172.1.1.1/32"
            ]
        }
    },

只允许来自于某些 IP 的访问, 使用的是 Public IPV4 地址::

    "Condition": {
        "NotIpAddress": {
            "aws:SourceIp": [
                "11.11.11.11/32",
                "22.22.22.22/32"
            ]
        }
    },

只允许来自于某些 AWS Account, IAM User, IAM Role 的访问::

    # AROAEXAMPLEID is the role ID of an IAM role that you want to allow
    # AIDAEXAMPLEID is the user ID of an IAM user that you want to allow
    # 111122223333 is the AWS account ID of the bucket, which represents the credentials of the AWS account root user

    "Condition": {
        "StringNotLike": {
            "aws:userId": [
                "AROAEXAMPLEID:*",
                "AIDAEXAMPLEID",
                "111122223333"
            ]
        }
    },

我最常用的 Bucket Policy 设置是只允许来自于受信的 IP 地址访问. 如果是我个人则是我家的 IP 地址, 如果是公司则是公司的 VPN IP 地址. 并且 CORS 没有打开, 因为我一般不自定义 Domain. 我的 Policy 如下::

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::${bucket_name}/*"
            },
            {
                "Sid": "VpcSourceIp",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    "arn:aws:s3:::${bucket_name}",
                    "arn:aws:s3:::${bucket_name}/*"
                ],
                "Condition": {
                    "NotIpAddress": {
                        "aws:SourceIp": "${trusted_ip_address}/32"
                    }
                }
            }
        ]
    }

至此, 你就可以访问你的 static website 了. 其中 S3 object 到网站 URL 的映射关系是: ``s3://${bucket}/${key}`` -> ``https://${bucket}.s3.amazonaws.com/${key}``

Reference:

- Tutorial: Configuring a static website on Amazon S3: https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html
- How can I restrict access to my Amazon S3 bucket using specific VPC endpoints or IP addresses?: https://repost.aws/knowledge-center/block-s3-traffic-vpc-ip


Automation Script
------------------------------------------------------------------------------
下面我们提供了一个脚本, 能够方便地将一个 S3 Bucket 设置为可以 host static website 的状态.

.. literalinclude:: ./setup_s3_bucket_for_static_website_hosting.py
   :language: python
   :linenos:


S3 Policy 把 Admin 都 Deny 了怎么办
------------------------------------------------------------------------------
有的时候因为操作失误, 你给 S3 Bucket Policy 设置了一个 Deny All 的规则. 这就会导致连你的 Admin 都会被 Deny 掉, 无法将这个 Bucket Policy 该回去了. 这个时候唯一的办法就是用 Root Account, 也就是 email password 登录. 然后进到 S3 Bucket 中删除这个 Bucket Policy.

如果你的 Account 是你用邮箱创建的还好. 但是如果你使用 AWS Organization 创建的, 你就需要用创建这个 Account 的时候的 email alias, 也就是带 + 号的那种. 例如你的 Org root email 是 alice@gmail.com, 那么你的 dev account 的 email 就会是 alice+dev@gmail.com. 你应该选择用 alice+dev@gmail.com 进行 root user 登录, 然后走一遍恢复密码的流程, AWS 会发一封 email 到你的 alice@gmail.com, 然后你就可以设一个密码, 然后用 root 登录, 把 bucket policy 删除即可.

Reference:

- `I accidentally denied everyone access to my Amazon S3 bucket. How do I regain access? <https://repost.aws/knowledge-center/s3-accidentally-denied-access>`_
- `Accessing a member account as the root user <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html#orgs_manage_accounts_access-as-root>`_


使用自己的 Domain 的关键步骤
------------------------------------------------------------------------------
如果你想要用自己的 Domain (http://www.my-website.com) 作为 S3 上的 Static Website 的域名 (原本是 http://example-bucket.s3-website-us-west-1.amazonaws.com), **开启 CORS 是一个很关键的步骤**, `CORS <https://developer.mozilla.org/en-US/docs/Glossary/CORS>`_ (Cross-Origin Resource Sharing, 也叫跨域) 是 HTTP 协议中的一部分用于允许一个域读取另一个域上的资源的协议. 如果你没有更改域名, 你的请求是从 AWS 的域读取 S3 上的资源, 这个 AWS 域名和 S3 是同一个域, 所以你不需要 CORS. 而你更改了域名, 等于说是你的请求先到达你的域名服务提供商, 然后你的域名向 AWS 请求数据, 这时候 S3 就需要设置 CORS, 允许来自你的域名的请求.

举例来说, 就是设置一个如果来源是 http://my-website.com 的流量 S3 Bucket 就允许 Read 操作. 然后你在 Domain Registry 服务商那设置了 http://my-website.com, 到你 http://example-bucket.s3-website-us-west-1.amazonaws.com 的映射. 然后从 你的 my-website.com 到 S3 的 Http 请求的 header 里就会带上 Origin = my-website.com, 然后你的 S3 就会允许并返回 html 了.

Reference:

- Tutorial: Configuring a static website using a custom domain registered with Route 53: https://docs.aws.amazon.com/AmazonS3/latest/userguide/website-hosting-custom-domain-walkthrough.html
- Using cross-origin resource sharing (CORS): https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html
- Enabling CORS for a REST API resource: https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
- Amazon S3 – Cross Origin Resource Sharing Support: https://aws.amazon.com/blogs/aws/amazon-s3-cross-origin-resource-sharing/
