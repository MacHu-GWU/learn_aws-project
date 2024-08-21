AWS CDK - CDK vs CloudFormation
==============================================================================
Keywords: Amazon, AWS, Cloud Development, Kit, CDK


Overview
------------------------------------------------------------------------------
在没有 CDK 的年代, 为了解决手写 CloudFormation JSON 不便的问题, 人们一般用 `troposphere <https://github.com/cloudtools/troposphere>`_ 工具用 Python 对象来写 CFT. 我甚至还推出了自己的 `cottonformation <https://github.com/MacHu-GWU/cottonformation-project>`_ 工具.

后来随着 CDK 的诞生, 对于生产项目, 我们一般直接用 CDK 来部署. 虽然 CDK 会生成中间态的 CloudFormation, 但这个 CloudFormation 跟你用前面提到的工具生成的区别还是很大. 因为 CDK 做了很多额外的工作例如管理 metadata, 自动生成 resource id 等等. 这些还是一些底层的区别, 而肉眼可见的就是 CDK 的 string template 系统跟 CloudFormation 完全不同. 一般 CloudFormation 里你会定义一个 Parameter, 然后用这个 Parameter 配合 JOIN 或者 SUB 等 intrinsic 函数来拼接字符串. 而 CDK 中就直接是用 Python 的 fstring + token 引用而无需定义 Parameter 和使用 intrinsic 函数了, 更加符合原生 Python 的写法. 这个做法对于开发者来说好处是显而易见的.

但是, CloudFormation 也不是一无是处. 比如 CDK 你需要有 NodeJS 环境 + Python 环境来运行, 而 CloudFormation 可以直接用 GUI drag and drop. 这对于企业给它的客户 delivery software 的时候非常重要. 因为客户可不一定有软件作者那么强的技术背景, 他们只想要一个简单的工具来部署他们的软件. 所以, 有时候我们还是需要用 CloudFormation 来做一些事情.

那么问题来了, 我们在有 CDK 的年代, 应该用什么来写 CloudFormation 呢? 我的结论是依然用 CDK. 作为开发者, 你用 CDK 的开发效率以及代码可维护性都要远远高于其他所有工具. 而你要 CloudFormation 的时候你只需要修改里面的少数几行代码就可以将你的 CDK Python code 导出为 CloudFormation. 当然, 这里面的几个少数几行代码还是有很多小细节需要注意的, 并不是你可以不看文档就能想象出来的.

**这个文档将详细介绍如何用 CDK 维护代码, 但将其导出为其他人可直接用的 CloudFormation**


How to export CDK to CloudFormation
------------------------------------------------------------------------------
**CDK Stack**

既然你最终要生成 CloudFormation, 那么你就不能用 Token 系统, 而是要回到 CloudFormation Parameter 系统. 而所有的字符串拼接你就要使用 JOIN 和 SUB 了. 这样没有用 token 系统优雅, 但是总体工作量不大.

.. dropdown:: stacks.py

    .. literalinclude:: ./learn_cdk/stacks.py
       :language: python
       :linenos:

**App**

在 ``app.py`` 里有两点要注意:

1. 在创建 stack 的实例时, 如果你要导出 CloudFormation 则要定义 ``synthesizer=...``. 这是因为默认情况下 CDK 会生成一大堆 CDK 专有的 parameter 和 metadata, 而你的 CloudFormation 里是不需要这些东西的.
2. 创建完 stack 的实例后, 将其导出为 CloudFormation template 并写入本地文件.

.. dropdown:: app.py

    .. literalinclude:: ./app.py
       :language: python
       :linenos:

**Deploy Script**

因为我们没有用 token 系统, 所以我们 Deploy 的时候必须指定所有的参数. 你需要给 ``cdk deploy`` CLI 命令指定所有的 parameter. (你还可以用 `cdk.context.json <https://docs.aws.amazon.com/cdk/v2/guide/context.html>`_ 文件来存储这些参数, 我的实验失败了, 以后我再研究这个方法把.)

.. dropdown:: run_cloudformation_deploy_and_destroy.py

    .. literalinclude:: ./run_cloudformation_deploy_and_destroy.py
       :language: python
       :linenos:


Reference
------------------------------------------------------------------------------
- https://docs.aws.amazon.com/cdk/v2/guide/get_cfn_param.html
- https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/DefaultStackSynthesizer.html
