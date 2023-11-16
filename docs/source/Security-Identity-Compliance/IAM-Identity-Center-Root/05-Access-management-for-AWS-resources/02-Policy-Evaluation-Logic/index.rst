Policy Evaluation Logic
==============================================================================
Keywords: AWS, IAM

Reference:

- `Policy Evaluation Logic <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`_


Allow vs Deny
------------------------------------------------------------------------------
在一个 Policy 中会有很多 Action 以及这 Allow 和 Deny 关键字, 那么如果对同一个资源的同一个 Action 的 Allow 和 Deny 冲突时会发生什么呢?

简单来说就是 **Explicit Deny > Explicit Allow > Default Deny**.

1. 显式 Deny 最大, 你再多的 Allow 也没用.
2. 显式 Allow 了, 才会有这个权限.
3. 如果没有任何 statement 进行定义, 默认是 Deny.
