AWS Systems Manager Parameter Store
==============================================================================
Keywords: AWS, Amazon, System, Systems, SSM, Parameter Store


Overview
------------------------------------------------------------------------------


Managing parameter tiers
------------------------------------------------------------------------------
你创建 Parameter 的时候, 在 API 中你需要指定 tier. AWS parameter store 有两个 tier, 分别是 Standard 和 Advanced.

- Standard: 免费, 最多创建 10k 个, 最大 4kb
- Advanced: 收费, 最多创建 100k 个, 最大 8kb

还有一个 tier 叫 Intelligent-Tiering, 它会自动创建 Standard tier, 然后在需要的时候 (Standard tier 的 parameter 数量达到了 10k, 或是大小超过了 4KB) 时候自动转换成 Advanced tier.

Reference:

- `Managing parameter tiers <https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-advanced-parameters.html>`_