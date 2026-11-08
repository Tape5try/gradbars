# Explicit native column adapters / 显式原生列适配（v1.2.1）

The former v1.5.0 plan is included in local v1.2.1 at the maintainer's request.
旧 v1.5.0 规划本次按用户指定编号并入 v1.2.1，不代表发布了 v1.5.0。

```tex
\gradbarsdeclarecolumn{review-score}{frontend=bar,select=true,rank=true,
 aggregate=true,options={min=0,max=100,precision=0}}
\begin{gradtable}[style=adapter-report]
\gradcolumn[width=25mm]{name}{Project}
\gradcolumn[type=review-score,mark=both,aggregate=mean]{score}{Score}
\gradrow{Atlas,80}\gradrow{Birch,0}\gradrow{Cedar,NA}
\gradsummary{Mean}
\end{gradtable}
```

Load `table` (already in the default list). `\gradbarsdeclarecolumn{name}{keys}`
is local to the ordinary TeX group; visible duplicate and built-in type names
are errors. Names use lower-case letters, digits and hyphens, starting with a
letter. A standalone `\gradbarsdeclaretype` registration never becomes a native
column automatically. Its existing independent callback contract is unchanged.

加载 `table`（默认已加载）。声明遵循 TeX 分组；可见重名与内置类型重名报错。
名称须以小写字母开头，后续仅小写字母、数字、连字符。
旧独立图形注册不会自动成为表格列，旧独立回调的调用约定保持不变。

| Key / 键 | Default / 默认 | Contract / 约定 |
| --- | --- | --- |
| `frontend` | `bar` | `bar`, `heat`, `bullet`, `number`, `box` only |
| `options` | empty / 空 | Graphic defaults, before column `options` / 列图形选项之前应用 |
| `select`, `rank`, `aggregate` | `false` each | Explicit raw scalar capabilities / 显式原值能力 |
| `graphic` | empty / 空 | Registered scalar type for `box` / 盒适配的独立图形类型 |
| `box width`, `box height`, `box depth` | `0pt` | Box requires positive width/height, nonnegative depth / 宽高正、深度非负 |

Proxy frontends keep native allocation, fixed/column/named ranges, baseline and
label overhead. Selection, ranking and aggregates operate on canonical raw
numbers, never the drawing or formatter output. CSV locale normalization applies
to scalar proxies before these operations; zero is valid and NA is missing.

标准代理沿用原生分配、固定/自动列/命名范围、基线、外置标签开销。计算只使用
规范原值，不读取图形或格式化文本。标量代理接受显式 CSV 地区输入；零与缺失区分。

## Fixed boxes / 固定盒

A box frontend takes exactly one registered scalar callback and a declared
single-line box. In the callback, expandable `\gradbarscolumnwidth`,
`\gradbarscolumnheight`, `\gradbarscolumndepth` expose **declared box dimensions**,
not the whole cell. Outside this context they report an error. The allocated
graphic width must fit that box; measured contents must fit declared width,
height and depth (0.2pt tolerance). The wrapper preserves the declared text
baseline, suppresses graphic labels, and does not add a Figure of its own.
The callback owns any delegated graphic semantics. The table may still reserve
its configured label slot; explicitly set table `label width=0pt` for a box.

固定盒只接收一个规范标量或 NA。三个公开尺寸命令返回声明的盒宽、高、深，不能
在回调外使用。分配图宽必须容纳盒，内容实测三维尺寸不能超过声明（容差 0.2pt）。
包装层采用声明的文本基线、关闭图形标签，不额外生成 Figure；委托图形的语义由
回调负责。表格仍可能保留标签槽；表格可显式设置 `label width=0pt`。

Admitted table callbacks must be deterministic and repeatable, with no external
writes, counters, labels or global changes. Width measurement may run repeatedly
and discard results; tagging suspension prevents duplicated delegated Figures.
Arbitrary multiline, content-dependent or stateful callback layout is outside
this adapter contract. Independent `\gradgraphic` callbacks remain unrestricted
by these additional table-only admission conditions.

表格回调须可重复且无外部写入、计数、标签或全局修改；试排可多次调用并丢弃结果，
期间暂停标记。任意多行、随内容改变尺寸或有状态的自动布局不属于本适配契约。
这些附加准入条件不追溯限制独立 `\gradgraphic` 调用。

Public-only library: [gradbars-contrib-columns.sty](libraries/gradbars-contrib-columns.sty).
Examples: [English](examples/column-adapters.tex), [中文](examples/column-adapters-cn.tex).
New table presets: `adapter-report`, `rug-report`; new graphic style: `sample-rug`.
