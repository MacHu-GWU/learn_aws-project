What is ECR
==============================================================================
Keywords: AWS, Amazon, Elastic Container Registry, ECR, Overview.


Overview
------------------------------------------------------------------------------
AWS ECR 是一个容器镜像的管理服务. 相当于私有的 DockerHub, 并且你有更多的控制权. 既支持 private 也支持 public. 对于开源社区而言, 由于 docker 公司并不大, 并不能负担巨大的流量费用, 所以它们对 public image 的 Pull 操作做出了限制, Authenticated User 每 6 小时只能 pull 200 次. 这对于 CI/CD 是非常不友好的. 而 AWS 财大气粗, 它们的 Public ECR Gallery 平台则对 public image 免费, 并且没有 pull 的限制.

Reference:

- `Private ECR <https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html>`_: 私有的 ECR 官方文档.
    - `Pushing an image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push.html>`_: 从 push image 到 Private Repo
    - `Pulling an image <https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-pull-ecr-image.html>`_: 从 Private Repo pull
- `Public ECR <https://docs.aws.amazon.com/AmazonECR/latest/public/what-is-ecr.html>`_: 公有的 ECR 官方文档.
    - `Pushing an image <https://docs.aws.amazon.com/AmazonECR/latest/public/docker-push-ecr-image.html>`_: 从 push image 到 Public Repo
    - `Pulling an image <https://docs.aws.amazon.com/AmazonECR/latest/public/docker-pull-ecr-image.html>`_: 从 Public Repo pull
