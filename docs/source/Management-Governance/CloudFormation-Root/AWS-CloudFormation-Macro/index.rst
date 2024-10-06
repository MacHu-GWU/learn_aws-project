AWS CloudFormation Macro
==============================================================================
Keywords: AWS, Amazon, CloudFormation

Macro 跟 Custom Resource 有点类似, 但是是为了解决不同的问题而设计的. 简单来说 Custom Resource 是为了解决创建 CloudFormation 不支持的资源而设计的. 而 Macro 则像是解决 CloudFormation 的 JSON 语法无法实现的复杂业务逻辑, 而允许你用编程语言替换掉 Macro 的部分而设计的.

举例来说, 假设我们有一个没有参数的 Macro, 叫做 Md5, 它能返回随机的 MD5 字符串. 那么在下面的 CloudFormation Template 中, ``GroupName`` 的值就被替换成了 Macro 的 Lambda Function 的返回值. 注意, 这个返回值不仅仅可以是这个例子中的字符串, 而且可以是任何复杂的 JSON 对象, 甚至重新定义一个 Resource 甚至多个 Resource 都是可以的.

.. code-block:: javascript

    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "IamGroup": {
                "Type": "AWS::IAM::Group",
                "Properties": {
                    "GroupName": {
                        "Fn::Transform": {
                            "Name": "Md5",
                            "Parameters": {},
                        }
                    },
                },
            },
        },
    }

关于这个 Macro 后端的 Lambda Function 的具体实现, 请参考 `Creating a CloudFormation macro definition <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html#template-macros-author>`_ 一文. 其中 Request object 中的 ``params`` 就是上面的 ``"Parameters" : {}`` 部分, 而整个 ``{"Fn: Transform": ...} `` 则是 Response object 中的 ``fragment`` 部分.


More Examples
------------------------------------------------------------------------------
.. autotoctree::
    :maxdepth: 1
