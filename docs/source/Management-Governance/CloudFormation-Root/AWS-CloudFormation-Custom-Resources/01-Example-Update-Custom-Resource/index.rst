01 Example Update Custom Resource
==============================================================================
Keywords: AWS, Amazon, CloudFormation

本文是 :ref:`aws-cloudformation-custom-resources` 的后续进阶博文. 给出了详细的最佳实践.

下面 ``lambda_function_example.py`` 的例子是用来 handle custom resource 的 Lambda Function 的最佳实现. 里面的 :func:`process` 特意留空, 以便用户自行实现具体的业务逻辑, 并给出了一些建议. 其他地方都是一些通用的标准最佳实践.

.. dropdown:: lambda_function_example.py

    .. literalinclude:: ./lambda_function_example.py
       :language: python
       :linenos:

``lambda_function.py`` 则是一个具体的实现, 用于演示分别在 Create, Update, Delete Request 的情况下, 如何分别对其进行处理, 以及演示返回不同的 PhysicalResourceId 会造成什么影响. 这里的重要结论就是, 如果你 Update 的时候返回的 PhysicalResourceId 不一样, 那么会先 Update 然后 Delete 旧的, 那么会多发送一个 Delete Request.

.. dropdown:: lambda_function.py

    .. literalinclude:: ./lambda_function.py
       :language: python
       :linenos:

而 ``deploy_cf.py`` 则是一个真实的 CloudFormation Template, 里面的关键点有两个:

1. 用 ServiceTimeout 来设置超时时间, 以防止 CloudFormation 卡死.
2. 用 client_token 来保证 Update Stack 的时候同时也 Update Custom Resource.

.. dropdown:: deploy_cf.py

    .. literalinclude:: ./deploy_cf.py
       :language: python
       :linenos:
