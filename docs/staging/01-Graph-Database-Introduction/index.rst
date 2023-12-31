What is Graph Database
==============================================================================


What is Graph
------------------------------------------------------------------------------
在 2000 后, 社交网络开始兴起. 网上的一人和人之间互为好友, 互相关注. 于是就出现了一种专门针对人和人之间的关系的查询需求. 例如: 从 A 到 B 之间, 如何建立一条关系链? 有多少人间接滴关注了 C. 这种数据模型的本质其实是网络, 每个人都是一个网络上的一个节点, 节点之间如果存在关系则连一条线, 这个线本身包含了一些 metadata, 例如这个关系是什么时候建立的. 而对这种数据模型进行数据库中的数据建模就不能再用 RDBMS 的表格模型了. 你可以想象一下, 传统关系数据模型是用 association table 描述关系的, 如果要建立关联查询就要做一次 JOIN, 如果要查询经历了 2 - 3 次的关系就要做 2 - 3 次 JOIN, 每次 JOIN 的复杂度都是 N 的次方, N 等于数据库中的数据行数, 例如 3 次 JOIN 就是 N 三次方. 这显然在一些分析的需求中是不可接受的.


Data Model for Graph Database
------------------------------------------------------------------------------
那么在底层, 图数据库是如何建模的呢? 根据人类直觉, 我们很容易的就能想象出来这里面要有 "节点", 也叫做 Vertex (复数形式 vertices), 缩写为 V. 节点之间的关系是 "边", 也叫做 Edge, 缩写为 E. 而 V 肯定是要有一个唯一标识符 ID, E 则可能有向, 也可以无向, E 的唯一标志符 ID 是由它所连接的两个节点的 ID 组合而成. 为了让信息更丰富, V 和 E 显然都应该支持 Key / Value 的属性. 于是, 你就得到了业内早期最流行的建模方式 "属性图"

业界主要有两种建模方式:

1. 属性图 (Property Graphs):
    - 节点 (Nodes): 是图中的实体, 用表示其类型的0到多个文本标签进行标记, 相当于实体. 
    - 边 (Edges): 是节点之间的定向链接, 也称为关系. 其中对应的 "from node" 称为源节点, "to node" 称为目标节点. 边是定向的且每条边都有一个类型, 它们可以在任何方向上导航和查询. 相当于实体之间的关系.
    - 属性 (Properties): 是一个键值对, 顶点和边都具有属性. 
2. 资源描述框架图 (RDF Graphs, Resource Description Framework):
    - 节点 (Nodes): 对应图中的顶点, 可以是具有唯一标识符的资源, 也可以是字符串、整数等有值的内容. 
    - 边 (Edges): 是节点之间的定向链接, 也称为谓词或属性. 边的入节点称为主语, 出节点称为宾语, 由一条边连接的两个节点形成一个主语-谓词-宾语的陈述, 也称为三元组. 边是定向的, 它们可以在任何方向上导航和查询. 

这里我们不详细展开比较, 有兴趣的话可以看 Reference 中的文章. 这里我们只说结论:

.. important::

    RDF 比较新, 功能上更强大, 可扩展性更强, 属性图能做到的 RDF 都能做到. 但是对于人类它比属性图更难理解, 不那么直观. 但因为属性图的弊端, 很多功能做不到, 所以大企业基本上都迁徙到了 RDF 上了. 我建议直接从 RDF 开始学习.

Reference:

- 属性图和RDF图简要介绍与比较: https://zhuanlan.zhihu.com/p/260430189
- 人人都在谈的图数据库到底是个啥: https://bbs.huaweicloud.com/blogs/265577


Gremlin Query Language, openCypher 和 graph traversal language
------------------------------------------------------------------------------
这三种都是图查询领域的标准, 各个数据库厂商可以选择支持这些标准, 就可以用通用的这些标准在不同编程语言中的库来操作图数据库. 这样就避免了所有的图数据库厂商彼此割裂的发明一套自己的语言的情况.
