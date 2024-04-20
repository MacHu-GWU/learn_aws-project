Should I Segment Big PDF Before Document Analysis
==============================================================================
Keywords: AWS, Amazon, Textract


Overview
------------------------------------------------------------------------------
在使用 Textract 的 Document Analysis 功能时, 如果输入的 PDF 的页数很多, 这时候我们会面临两种选择:

1. 将整个 PDF 作为一个整体发给 Textract.
2. 将 PDF 分拆成单页 PDF, 然后依次发给 Textract.

这是因为根据 `Set Quotas <https://docs.aws.amazon.com/textract/latest/dg/limits-document.html>`_, Textract 有单个 PDF 不能超过 500 MB / 3000 页 的限制. 根据 `Default Quotas <https://docs.aws.amazon.com/textract/latest/dg/limits-quotas-explained.html>`_, 默认情况下最多支持 5 个并发的 Async Document Analysis Job. 而根据 `Pricing <https://aws.amazon.com/textract/pricing/>`_ Textract 是按照 Page 收费 (跟运行时长无关). 所以我们需要合理利用 Quota 和 API, 使得总处理速度最快.

下面我们通过一个实验来测试到底应该用哪个方法.


Experiment
------------------------------------------------------------------------------
请阅读下列测试代码. 我们用的是一个 6 页的 W2 税表文件做测试. 分别是一次性提交, 和分拆成 6 页依次提交. 请阅读代码中的结论部分.

.. dropdown:: test_should_i_segment_big_pdf_before_document_analysis.py

    .. literalinclude:: ./test_should_i_segment_big_pdf_before_document_analysis.py
       :language: python
       :linenos:
