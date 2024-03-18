Prompt Engineering In Enterprise
==============================================================================


Overview
------------------------------------------------------------------------------
我在充分学习了 Prompt Engineering 的核心技术后, 结合企业中的实际需求, 对 Prompt Engineering 在企业中的应用进行了一些思考. 这篇文档记录了我认为 Prompt Engineer 在企业中如何落地的解决方案.


Diagram
------------------------------------------------------------------------------
.. raw:: html
    :file: ./Prompt-Engineering-in-Enterprise.drawio.html


1. Prompt Elements
-------------------------------.-----------------------------------------------
这一节我们对 Prompt Engineering 的本质进行了一个拆解. 我们可以看到一个 Prompt 由很多 Elements 组成. 为了不同目的的 Prompt 所需要的 Elements 是不同的. 而对于同一个 Elements, 例如 Role 的部分, 我们可以有很多 Choice. 而有了 Element + Choice 之后, 只需要对其进行排列组合就可以创建一个 Prompt.


2. Prompt DataStore
------------------------------------------------------------------------------
我们假设我们有一个企业内部的 Element + Choice 的清单了, 那么我们应该如何储存他们呢? 我认为用传统的 Relational Database 就足够了. 这一节我给出了一个 Data Model 的建模, 以及说明了如何对 Prompt Elements 进行搜索.


3. Prompt Evaluation
------------------------------------------------------------------------------
在企业应用中对 Prompt 进行版本呢管理, 评估都是很重要的. 我们可以通过改变一个 Prompt Element 的 Choice, 然后对大量的 Data 进行 A/B Test 以获得最优的 Prompt.


4. Enterprise Prompt Engineering Platform
------------------------------------------------------------------------------
最终, 我认为一个企业需要的 Prompt Engineering Platform 包含这么几个部分.

1. 一个 IDE, 能够方便的撰写 Prompt, Element, Choice; 能够方便的对其进行 A/B Test; 能够对 Prompt 进行搜索; 能够选择 Element 从而创建一个 Prompt; 能够将 Prompt 保存到数据库中.
2. 对于人类使用者, 需要一个 GUI 或者 SDK 能允许搜索和选择 Prompt, 然后把 Prompt 发给对应的 Foundation Model.
3. 对于机器使用者, 主要是 AI Agent, 我们需要能将 AI Agent 和所需的 Prompt 进行绑定, 使其能正常工作. 而最终人类或者 IT 系统就只需要跟这个 Agent 交流就可以了.
