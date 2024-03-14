AWS Clean Rooms
==============================================================================
Keywords: AWS, Amazon, Clean Rooms, Overview.


What is AWS Clean Rooms?
------------------------------------------------------------------------------
AWS 在数据写作领域已经有多个产品所组成的生态. 有 S3 作为数据存储, 有 Glue Catalog 作为数据的 Metadata Store, 有 Athena 作为 Query 引擎, 有 Lake Formation 作为 Grained Data Access Control Management Control. 看起来已经非常完备了, 那为什么还要有 Clean Rooms 这个产品呢?

企业将自己的数据共享给合作伙伴进行分析一直以来是一个刚需. 但数据的拥有方是不希望将核心资产 "数据" 毫无保留地分享给合作伙伴. 传统的数据仓库里的数据权限管理功能一般是限制访问的列, 对行进行 filter, 对值进行 mask. 但是很多场景下这些功能是不够的, 比如你可能允许用户做 aggregation 聚合查询, 也就是显式 AVG, SUM 之后的值, 但并不允许用户看到原有的值. 还有些企业场景下, 数据查询本质上还是消耗着数据拥有方的资源, 也就是说数据拥有方需要为合作伙伴的查询付费. 这个时候, 数据拥有方就需要有一种机制来控制合作伙伴的查询, 以及查询的资源消耗. 总之很多企业需求是传统的数据权限管理无法满足的, 虽然说你可以在传统数据仓库上做二次开发, 但是这又要消耗额外的工程师资源, 并且当你的合作伙伴很多的时候, 工作量也会线性上升. 而这, 就是 AWS Clean Rooms 所解决的痛点.


How AWS Clean Rooms Works?
------------------------------------------------------------------------------
这一节我们来看看 AWS Clean Rooms 是如何工作的, 期间会涉及到很多 Clean Rooms 中的概念.

- `Collaboration <https://docs.aws.amazon.com/clean-rooms/latest/userguide/glossary.html#glossary-collaboration>`_: 你可以创建一个 Collaboration. 它本质上就是一个工作组, 里面可以有多个 Member. 一个 Member 就是一个 AWS Account. 所以你要使用 Clean Rooms 就要求数据拥有者和数据使用者都是 AWS 用户. 默认情况下数据拥有者的 AWS Account 就是一个 Admin Member, 也是 Collaboration creator. 当你创建 Collaboration 之后, 其他的 Member 就会在他们的 AWS Clean Rooms Console 中收到一个 Invite.
- `Configured Table <https://docs.aws.amazon.com/clean-rooms/latest/userguide/glossary.html#glossary-configured-table>`_: 你可以创建一个 Configurable Table, 它本质上是一个 Glue Catalog Table 和一些额外的 Metadata 的集合. 你可以将 Configurable Table 添加到 Collaboration 中, 这样所有的 Member 就可以对其进行操作了.
- `Analysis Rule <https://docs.aws.amazon.com/clean-rooms/latest/userguide/glossary.html#glossary-analysis-rule>`_: 这是 Clean Room 的重中之重. Analysis Rule 是一个类似 IAM Policy 的 Json, 附着在 Configured Table 之上, 定义了这个 Table 可以被怎样进行查询. 例如前面提到的, 只需对某个 Column 进行 Aggregation 计算, 但看不到原始的值; 或者某个 Column 必须要进行 Masking; 或者某个表中的数据是 dimension data, 你不能直接 query 而是要 JOIN 之后才能看到; 以及你选择数据的时候结果必须包含多少个 ROW 以上, 防止你用通过 Match 结果非常少的 Aggregation Column 来间接的获得原始的值等规则.

AWS Clean Room 这个产品的本质就是通过对 Collaboration, Configured Table, Analysis Rule 进行排列组合以实现既能让 Partner 查询数据, 但又无需拷贝数据, 以及只给 Partner 我想给他看的数据.

Reference:

- `Glossary <https://docs.aws.amazon.com/clean-rooms/latest/userguide/glossary.html>`_


Reference
------------------------------------------------------------------------------
- `AWS Clean Rooms Document <https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html>`_
