.. _aws-cognito-overview:

Amazon Cognito Overview
==============================================================================
Keywords: AWS, Amazon, Cognito, Overview.


Background Knowledge
------------------------------------------------------------------------------
学习 Cognito 的时候, 你首先需要对 身份验证 (Authentication), 授权 (Authorization) 以及相关的 Oauth2 和 OIDC (OpenId Connect) 有一定的了解. 这几篇文章含金量非常高.

- 基于 OAuth2 的认证（译）: https://www.cnblogs.com/linianhui/p/authentication-based-on-oauth2.html
- Json Web Token: https://www.cnblogs.com/linianhui/p/oauth2-extensions-protocol-and-json-web-token.html#auto_id_5
- OIDC（OpenId Connect）身份认证（核心部分）: https://www.cnblogs.com/linianhui/archive/2017/05/30/openid-connect-core.html


Concepts
------------------------------------------------------------------------------
最重要的两个概念是 User Pool 和 Identity Pool.

- User Pool: User pools are user directories that provide sign-up and sign-in options for your app users. 简单来说, 这个是给人类用的, 需要注册, 登录, 有密码, 有用户名, 有邮箱, 有手机号码等等.
- Identity Pool: Identity pools enable you to grant your users access to other AWS services. 而 Identity Pool 主要是用于匿名访问 AWS 上的资源. 例如一个 Public 的 App 上用户临时需要获得一个 AWS 上的文件.
- You can use identity pools and user pools separately or together.

App Authentication Workflow:

1. Authentication and get tokens from User pool
2. Exchange tokens for AWS Credentials
3. Access AWS Service with credentials

Reference:

- `What is Amazon Cognito? <https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html>`_

Reference:

- What is Amazon Cognito: https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html


Cognito 的使用场景
------------------------------------------------------------------------------
1. Authenticate with a user pool: 帮你管理你的 App 的用户登录系统, 登录成功以后, 可以访问一些 AWS 上的资源.
2. Access your server-side resources: 和上面类似
3. Access resources with API Gateway and Lambda: 你可以用 Cognito 管理你的 API Gateway 的访问权限. 例如用户登录以后就可以发送请求到 API Gateway, 而不登录的用户就不能访问.
4. Access AWS services with a user pool and an identity pool: 你可以用 Cognito 来给你 AWS Account 以外的用户访问位于你的 AWS account 上的资源.
5. Authenticate with a third party and access AWS services with an identity pool: 同上面一样, 不过登录方式变成了第三方 IDP provider 的登录, 例如 Google, Facebook.
6. Access AWS AppSync resources with Amazon Cognito: App Sync 是 AWS Graph QL 的一个服务, 和 cognito 结合很紧密.

Reference:

- `Common Amazon Cognito Scenarios <https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-scenarios.html>`_
- 这篇文档也很不错的介绍了 Cognito 的用法: `Authentication with AWS Cognito <https://www.integralist.co.uk/posts/cognito/#client-sdk>`_
