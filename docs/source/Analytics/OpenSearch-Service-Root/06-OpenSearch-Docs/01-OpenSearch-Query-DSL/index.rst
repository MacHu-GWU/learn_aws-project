OpenSearch Query DSL
==============================================================================
Keywords: AWS, Amazon, OpenSearch, OS, OSS, Doc, Docs, Query, DSL

query domain-specific language (DSL) 是 OpenSearch 的核心查询语法. 用的是 JSON 格式. 本节对查询语法相关的内容进行了一个总结. 便于以后查阅.

Ref:

- https://opensearch.org/docs/latest/query-dsl/

Query and filter context
------------------------------------------------------------------------------
查询语言里分两个大块, filter 和 query.

Filter:

- filter 指的是对结果进行过滤, 和 SQL 中的 where 类似.
- 从每个 Document 的视角来看, filter 的结果只有 match 和不 match.
- 从查询引擎的视角看, filter 是直接在内存中进行比较实现的.

Query:

- 而 query 指的是一个 document 跟你的查询的相关性.
从每个 Document 的视角看, query 的结果是一个代表着相关性的数值.
- 从查询引擎的视角看, query 是使用 Index 实现的.

Ref:

- https://opensearch.org/docs/latest/query-dsl/query-filter-context/


Term-level and full-text queries compared
------------------------------------------------------------------------------
Query 主要有两类. Term 和 Full-text search (FTS). Term 指的是那种确定性的, 决定性的. 例如 SQL 中的 WHERE A = B, WHERE A < B < C. 这些也走的是 Index. FTS 是基于倒排索引, 文本相关性算法, 分词技术, 同义词技术, 模糊搜索技术等一系列技术实现的一种针对文本的搜索.

Ref:

- https://opensearch.org/docs/latest/query-dsl/term-vs-full-text/


Term-level queries
------------------------------------------------------------------------------
Term level 的 query 有以下几种:

- term: Searches for documents containing an exact term in a specific field.
- terms: Searches for documents containing one or more terms in a specific field.
- terms_set: Searches for documents that match a minimum number of terms in a specific field.
- ids: Searches for documents by document ID.
- range: Searches for documents with field values in a specific range.
- prefix: Searches for documents containing terms that begin with a specific prefix.
- exists: Searches for documents with any indexed value in a specific field.
- fuzzy: Searches for documents containing terms that are similar to the search term within the maximum allowed Levenshtein distance. The Levenshtein distance measures the number of one-character changes needed to change one term to another term.
- wildcard: Searches for documents containing terms that match a wildcard pattern.
- regexp: Searches for documents containing terms that match a regular expression.

Ref:

- https://opensearch.org/docs/latest/query-dsl/term/index/


Full-text queries
------------------------------------------------------------------------------
FTS 的 query 有以下几种:

- intervals: Allows fine-grained control of the matching terms’ proximity and order.
- match: The default full-text query, which can be used for fuzzy matching and phrase or proximity searches.
- match_bool_prefix: Creates a Boolean query that matches all terms in any position, treating the last term as a prefix.
- match_phrase:Similar to the match query but matches a whole phrase up to a configurable slop.
- match_phrase_prefix:Similar to the match_phrase query but matches terms as a whole phrase, treating the last term as a prefix.
- multi_match: Similar to the match query but is used on multiple fields.
- query_string: Uses a strict syntax to specify Boolean conditions and multi-field search within a single query string.
- simple_query_string: A simpler, less strict version of query_string query.

Ref:

- https://opensearch.org/docs/latest/query-dsl/full-text/index/


Compound queries
------------------------------------------------------------------------------
Compound queries 指的是将多个搜索条件用逻辑运算排列组合起来.

- bool (Boolean): Combines multiple query clauses with Boolean logic.
- boosting: Changes the relevance score of documents without removing them from the search results. Returns documents that match a positive query, but downgrades the relevance of documents in the results that match a negative query.
- constant_score: Wraps a query or a filter and assigns a constant score to all matching documents. This score is equal to the boost value.
- dis_max (disjunction max): Returns documents that match one or more query clauses. If a document matches multiple query clauses, it is assigned a higher relevance score. The relevance score is calculated using the highest score from any matching clause and, optionally, the scores from the other matching clauses multiplied by the tiebreaker value.
- function_score: Recalculates the relevance score of documents that are returned by a query using a function that you define.
- hybrid: Combines relevance scores from multiple queries into one score for a given document.

Ref:

- https://opensearch.org/docs/latest/query-dsl/compound/index/


Geographic and xy queries
------------------------------------------------------------------------------
Geographic and xy queries 是 为地理坐标高度优化的查询.

Ref:

- https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/


Span queries
------------------------------------------------------------------------------
Span 就是一个一个的 word 的意思. Span query 是对 span 在文档中的位置顺序 (官方的定义是 "span" refers to a contiguous sequence of words or tokens within a document), 以及相互的位置关系的查询. 例如一个词必须出现在一个词的后面的多少个词以内. 这种 query 常用于 Legal document 和 pattern 文件. 例如在租房 lease 中你搜索 rent 附近的数字, 认为这个数字就是租金.

Ref:

- https://opensearch.org/docs/latest/query-dsl/span-query/


Match all queries
------------------------------------------------------------------------------
Match all 就相当于 SQL 中的 ``SELECT *``.

Ref:

- https://opensearch.org/docs/latest/query-dsl/match-all/


Specialized queries
------------------------------------------------------------------------------
一些特殊的 query.

- distance_feature: Calculates document scores based on the dynamically calculated distance between the origin and a document’s date, date_nanos, or geo_point fields. This query can skip non-competitive hits.
- more_like_this: Finds documents similar to the provided text, document, or collection of documents.
- neural: Used for vector field search in neural search. (一种用神经网络技术优化 query, 把上下文纳入考量, 不局限于 query 的文本本身, 也会搜索相关的概念的一种搜搜技术)
- neural_sparse: Used for vector field search in sparse neural search.
- percolate: Finds queries (stored as documents) that match the provided document. (就是反过来输入一个文档, 返回可以 match 这篇文档的 query. 前提是你把 query body 当成 document 已经按照指定格式存到了 index 中)
- rank_feature: Calculates scores based on the values of numeric features. This query can skip non-competitive hits.
- script: Uses a script as a filter. (你可以编写脚本用来进行过滤. 默认的脚本语言叫做 painless, 还有其他脚本语言可选, 你可以自定义一些 if else 来定义复杂的过滤逻辑)
- script_score: Calculates a custom score for matching documents using a script.
- wrapper: Accepts other queries as JSON or YAML strings. (相当于不用原始的 JSON 语法, 而是将一个 query 序列化为 JSON 然后作为字符串传入. 这种 query 常用于你动态构建 query 的情况).

Ref:

- https://opensearch.org/docs/latest/query-dsl/specialized/index/
