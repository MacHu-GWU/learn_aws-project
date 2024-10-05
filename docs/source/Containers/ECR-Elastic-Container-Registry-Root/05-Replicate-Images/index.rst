AWS ECR - Replicate Images
==============================================================================
Keywords: AWS, Amazon, Elastic Container Registry, ECR

https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html

What is Replicate Image
------------------------------------------------------------------------------
这是 ECR 的一个功能. 它允许当一个 Image 被 push 到 Source Account Region 的 repo 后, 自动用同样的 repo name, tag 将其同步到一个 Target Account Region 的 repo 中.

这个功能适合于维护只有一个 Source of Truth 的 Image (也就是 source account 中的), 然后将其分发到 distribution account 中从而分发给其他人. 这样避免了统一从单个 Source Account Region 中拉取容器. 例如一个容器要被频繁拉取, 但是你的业务分布于多个 Region, 那么你可以在将原始镜像分发到多个 Region 中的 Repo 中 (只用交一次钱), 这样就不用每次拉取镜像都要交 cross region transfer data 的费用了.


Pricing
------------------------------------------------------------------------------
不 cross region 不花钱. 否则花钱.


Consideration
------------------------------------------------------------------------------
下面是一些你使用这个功能所需的考量.

- Only repository content pushed to a repository after replication is configured is replicated. Any preexisting content in a repository isn't replicated. Once replication is configured for a repository, Amazon ECR keeps the destination and source synchronized.
    - 也就是说你开启这个功能后的镜像才会被复制, 开启之前的镜像不会自动被复制.
- The repository name will remain the same across Regions and accounts when replication has occurred. Amazon ECR doesn't support changing the repository name during replication.
    - repo name 不能变.
- The first time you configure your private registry for replication, Amazon ECR creates a service-linked IAM role on your behalf. The service-linked IAM role grants the Amazon ECR replication service the permission it needs to create repositories and replicate images in your registry. For more information, see Using service-linked roles for Amazon ECR.
- For cross-account replication to occur, the private registry destination must grant permission to allow the source registry to replicate its images. This is done by setting a private registry permissions policy. For more information, see Private registry permissions in Amazon ECR.
    - 你得在 target recr repo 中设定 permission policy, 允许别人将镜像 push 到你的 repo 中.
- If the permission policy for a private registry are changed to remove a permission, any in-progress replications previously granted may complete.
    - 你如果在镜像传输过程中突然取消 permission, 那么已经在传输的镜像会继续传输.
- For cross-Region replication to occur, both the source and destination accounts must be opted-in to the Region prior to any replication actions occurring within or to that Region. For more information, see Managing AWS Regions in the Amazon Web Services General Reference.
- Cross-Region replication is not supported between AWS partitions. For example, a repository in us-west-2 can't be replicated to cn-north-1. For more information about AWS partitions, see ARN format in the AWS General Reference.
- The replication configuration for a private registry may contain up to 25 unique destinations across all rules, with a maximum of 10 rules total. Each rule may contain up to 100 filters. This allows for specifying separate rules for repositories containing images used for production and testing, for example.
- The replication configuration supports filtering which repositories in a private registry are replicated by specifying a repository prefix. For an example, see Example: Configuring cross-Region replication using a repository filter.
- A replication action only occurs once per image push. For example, if you configured cross-Region replication from us-west-2 to us-east-1 and from us-east-1 to us-east-2, an image pushed to us-west-2 replicates to only us-east-1, it doesn't replicate again to us-east-2. This behavior applies to both cross-Region and cross-account replication.
- The majority of images replicate in less than 30 minutes, but in rare cases the replication might take longer.
- Registry replication doesn't perform any delete actions. Replicated images and repositories can be manually deleted when they are no longer being used.
- Repository policies, including IAM policies, and lifecycle policies aren't replicated and don't have any effect other than on the repository they are defined for.
- Repository settings aren't replicated. The tag immutability, image scanning, and KMS encryption settings are disabled by default on all repositories created because of a replication action. The tag immutability and image scanning setting can be changed after the repository is created. However, the setting only applies to images pushed after the setting has changed.
- If tag immutability is enabled on a repository and an image is replicated that uses the same tag as an existing image, the image is replicated but won't contain the duplicated tag. This might result in the image being untagged.


API
------------------------------------------------------------------------------
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/put_replication_configuration.html