# v1.4.0: two-level CSV tables / 两级 CSV 表格

This document retains the former local v1.3.0/v1.4.0 planning labels. Those
features are included in the actual **v1.2.1** snapshot at the maintainer's request;
see [the numbering and migration notes](migration-v1.2.1.md).
本文沿用原本地规划标签；相关功能保留于本次指定编号 v1.2.1，并未分别发布这些规划版本。


The explicit `group levels={parentID,leafID}` table key accepts exactly two
different, declared `text` column IDs in a CSV-backed native `gradtable`. It is
separate from legacy `group by` and manual `\gradgroup`; combining them is an
error. Arbitrary depth and manual nested grouping are outside this version.
/ 仅新增自动 CSV 两级文本分组，不改变旧单层接口，不支持任意层级或手工嵌套。

```latex
\gradbarsloadcsv{teams}{docs/data/hierarchical-teams.csv}
\begin{gradtable}[data=teams,style=hierarchical,
 group levels={region,team},rank scope=parent,
 parent summary=true,leaf summary=true]
\gradcolumn[source=Project,width=22mm]{project}{Project}
\gradcolumn[source=Region,width=18mm]{region}{Region}
\gradcolumn[source=Team,width=18mm]{team}{Team}
\gradcolumn[source=Score,type=number,aggregate=mean,
 mark=both,width=20mm]{score}{Score}
\gradcolumn[source=Trend,type=trendcompare,
 options={min=0,max=100,compare label=delta}]{trend}{Endpoints / trend}
\gradsummary{All visible}
\end{gradtable}
```

## Paths and order / 路径与顺序

Keys are trimmed literal CSV text; an empty key uses `group missing label` for
its heading. Literal `NA` is a distinct **text** key. A structured path combines
parent identity and leaf text: identical leaf names under different parents do
not merge, and commas/slashes in names are ordinary characters. Group order is
first appearance in the original CSV, both for parents and their children.
No heading or level summary is rendered for groups with no visible rows.
/ 裁剪后空键与字面 NA 区分，分隔符不是路径编码；不同父组下同名子组互不合并。

The pipeline remains `filter -> stable global sort -> global limit -> grouping`.
Selected rows retain global sorted order **within** each leaf, then groups render
in source appearance order. The table is therefore not necessarily globally
sorted after grouping. Limit is never per-group. Scales remain table/column
scales; no hidden per-group scale is introduced. / 先全局选择再分组，组内保留排序，
组按原始首次出现顺序；不引入组内 limit 或暗含尺度。

## Ranking and summaries / 排名与摘要

`rank scope=table` remains the default. New `parent` compares visible data rows
within each parent across its leaves; `leaf` compares visible rows within one
structured leaf. Ranking uses original canonical numbers, ties share emphasis,
and second place is the second **distinct** value. Missing values are excluded.
`rank scope=group` remains for legacy single-level groups and is rejected with
`group levels`; use `parent` or `leaf` explicitly. / 父级排名跨该父组全部叶组；
叶级排名只看该路径，仍按规范原值判断并列及第二不同值。

| Key / 参数 | Default / 默认 | Meaning / 含义 |
| --- | --- | --- |
| `parent summary`, `leaf summary` | `false` | Independently enable each level / 分别开启 |
| `parent summary scope`, `leaf summary scope` | `visible` | `visible` selected rows; `data` original bound rows in that node / 可见或该组全部绑定原始行 |
| `parent summary label` | `Parent summary` | Parent summary title / 父级摘要标题 |
| `leaf summary label` | `Leaf summary` | Leaf summary title / 叶级摘要标题 |

Each numeric column retains its explicit `aggregate`; no aggregation is inferred
from grouping. Disabled levels compute/render no summaries. Data-scope summaries
can include filtered/limited rows of a visible group; entirely invisible groups
stay omitted. Overall `\gradsummary` and its independent `summary scope` remain
available. Summary rows never enter ranks or automatic scales. Count remains
unit-free. Legacy `group summary` keys are rejected with the new hierarchy.
/ 各级独立使用列 aggregate；data 可含被筛除的同组原始行，但不显示空组摘要；
总摘要作用域独立，不参与排名和自动尺度。

## Pagination and preset / 分页与预设

`style=hierarchical` adds accessible colors, extra row spacing and indented leaf
headings; set labels/summary options explicitly for the report. With `long=true`,
parent and child heading chains stay with the first row; leaf, parent and overall
summaries stay with their corresponding last data row. Groups can break between
data rows. A complete keep-chain must fit on a page; oversized single rows or a
chain taller than the usable page cannot be made to fit automatically.
Native longtable is verified with `booktabs`, `grid`, `rows` and `none` rules by
actual shipout pages, including exactly-once headings and summaries.
/ 标题与首行、逐级摘要与末行保持同页，允许数据行之间分页；单个连接链需能放入一页。

This is layout grouping, not a new complete Tagged PDF hierarchy contract.
Existing Figure alternatives continue; automatic table-header inference and
PDF/UA certification are not added. / 本版不新增完整的层级 Tagged PDF 表结构保证。

Executable examples: [English](examples/hierarchical-teams.tex),
[中文](examples/hierarchical-teams-cn.tex),
[longtable](examples/hierarchical-longtable.tex).
See [trend compositions](trend-compositions.md), [API](api.md) and
[stability](stability.md).
