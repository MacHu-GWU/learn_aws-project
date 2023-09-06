Delivery MicroService Solution to Paid Customer via CloudFormation
==============================================================================
Keywords: Amazon, AWS, CloudFormation



Objective
------------------------------------------------------------------------------
假设我们 A 公司开发了一套以 Lambda 为主的 Microservice, 它希望能将这个微服务包装成产品, 卖给客户, 并采用按使用量收费的方式.

1. 如何将软件用自动化的方式交付给客户?
2. 如何鉴权, 判断客户是付费用户?
3. 如何测量客户的使用量.
4. 如何对客户进行收费?
5. 如何防止代码被篡改?


Customer Sign Up an Account
------------------------------------------------------------------------------
- 客户登录 A 公司网站, 用邮箱密码注册一个账号. 用户 ID 就是客户的邮箱.
- 客户在 A 公司网站里的 Developer 页面有一个界面可以创建 API Key. 用户创建时需要指定它的 Expire 的时间. 然后就会获得一个 access_key, 和 secret_key, 其中 access_key 会永久在网页中显示而 secret_key 则只会在创建的时候显示一次, 如果忘记了就只能删掉重新创建一个 API Key. 这两个的组合是用来验证用户的身份的, 也就是 Authentication. 而鉴权方面则是有另外的 Authorization 逻辑, 我们之后再说.
- 客户可以创建多个 API Key, 也就是说每一个 email 可以对应多个 API Key.


How to Delivery MicroService Solution to Customer
------------------------------------------------------------------------------
- 我们可以使用 CloudFormation 作为交付手段, A 公司把 CloudFormation Template 放在 Public Facing 的 Bucket 上, 用户用这个 Template 创建 CloudFormation Stack, 其中需要填写 access_key 和 secret_key 来告知我是谁 (access_key 和 secret_key 就是用来验证身份的). 之后的部署逻辑中会用到这个, 我们之后再说.
- CloudFormation 里面的很多 Resource 例如 Lambda Function Source Code 等都是需要从 S3 上拉取 artifacts 的 (源代码, 容器镜像之类的), 而这些 artifacts 则是由 A 公司提供的.
- CloudFormation 中有一个 Lambda Function backed Custom Resource. 这个 Lambda Function 是由 CloudFormation Template 中最前面的几个 Lambda Function 来创建的, 其中的 Lambda Function 的业务逻辑是将 access_key, secret_key 通过 HTTP Request 发送给 A 公司的 auth server 来鉴权, 鉴权成功后 A 公司的服务端会从 A 公司的代码库中拷贝一份需要的 Artifact 到临时的 S3 Bucket 并共享给客户, 然后这个 Custom Resource 就会返回这些 artifacts 的 S3 Key / URI, 供 CloudFormation Template 之后的逻辑用这些 artifacts 来 Deploy.

CloudFormation Template 看起来像这样:

- 创建 Authenticate Lambda Function
- 创建 Custom Resource, 它的逻辑是用 access_key, secret_key 来获得 artifacts 的地址
- 部署 Solution


How to Authenticate and Authorization
------------------------------------------------------------------------------


How to Measure Usage
------------------------------------------------------------------------------
- 在我们交付的产品中


How to Charge Customer
------------------------------------------------------------------------------


How to Protect Your Source Code
------------------------------------------------------------------------------
售卖的方式是客户可以自己部署软件, 不过 License Key 的方式, 如果


