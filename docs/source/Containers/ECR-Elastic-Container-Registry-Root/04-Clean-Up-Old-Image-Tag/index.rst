Clean Up Old Image Tag
==============================================================================
AWS ECR 自带一个 Life Cycle Policy 的 功能能让没有被 Tag 的 image 自动在一定时间后删除. 但用户对 Life Cycle Policy 的需求是多种多样的, 我们希望能够更加精确的控制什么时候执行删除, 删除哪些 Image.

这里我提供了一个脚本用于自定义删除 ECR 的任务:

.. dropdown:: clean_up_old_image.py

    .. literalinclude:: ./clean_up_old_image.py
       :language: python
       :linenos:
