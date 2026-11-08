# Explicit pair consumers / 显式数值对扩展

Pairs have an independent registry and read-only record. Existing scalar graphics,
scalar columns and backend schema 1 keep their original contracts. These interfaces
do not remove TikZ or interpret observations as uncertainty.

```latex
\gradbarsdeclarepairtype{boxed-review}{dumbbell}{\fbox{\gradbarspairdefault}}
\gradpairgraphic[min=0,max=100,width=30mm]{boxed-review}{66}{82}
```

## Registration and invocation

| Interface | Contract |
| --- | --- |
| `\gradbarsdeclarepairtype{name}{frontend}{callback}` | Global registration; lowercase letter followed by lowercase letters, digits or hyphens; visible duplicates and existing scalar names rejected |
| `\gradpairgraphic[graphic keys]{name}{left}{right}` | Scoped call; native frontend validates both inputs, options and geometry before invoking the consumer |
| `\gradbarspairversion` | Expandable pair-record version, currently 1; independent of `\gradbarsbackendversion` |
| `\gradbarspairvalue{field}` | Expandable, read-only snapshot access during a consumer callback; unknown fields and out-of-context access diagnose errors |
| `\gradbarspairdefault` | Draw the captured native continuation once, including when used inside a nested box; no revalidation or second Figure wrapper |
| `\gradbarspairlabel` | Typeset the frontend's existing full pair label with its font and units, without placement or a Figure wrapper |
| `\gradbarsifpairtypecapable{name}{feature}{yes}{no}` | Query the pair registry; unknown type or feature takes the no branch |

The builtin names are `compare`, `dumbbell` and `range`, each delegating to its
matching native frontend. Registered callbacks receive **two canonical, unrounded
numbers or NA**, as arguments 1 and 2. A blank argument follows the corresponding
native missing rule. No expression, locale, unit or statistical role is guessed.

compare/dumbbell roles are **reference, current**. Range roles are **lower, upper**;
range order and optional point constraints retain native validation. Comparisons
allow either or both observations to be missing; ranges require both endpoints
present or both missing. Zero remains an observation. Native labels for comparisons
show current/reference, independently of the reference/current input order.

声明格式为名称、原生前端、回调；回调接收两个规范原值或 NA。比较类按参考值、当前值输入，
区间按下界、上界输入。比较允许单侧缺失，区间仍要求两端同时有效或同时缺失。
公开入口不会把数值对送入旧标量回调，也不自动把独立类型注册为表格列。

## Record fields

| Field | Value and semantics |
| --- | --- |
| `version`, `type`, `kind` | Pair schema version, registered name, native compare/dumbbell/range kind |
| `left-role`, `right-role` | reference/current or lower/upper |
| `raw-left`, `raw-right` | Original trusted TeX argument tokens; never a source for reparsing CSV or recomputing canonical values |
| `left`, `right` | Canonical unrounded values, or literal NA |
| `left-missing`, `right-missing` | true/false |
| `missing`, `complete` | none/left/right/both; complete is true only when neither is missing |
| `min`, `max`, `zero` | Resolved shared numeric range and zero normalized/clipped to [0,1] |
| `left-position`, `right-position` | Clipped normalized positions; NA for the missing side |
| `left-clipped`, `right-clipped` | true if the original side lies outside the display range; false for missing sides |
| `delta` | Unrounded right minus left, or NA for an incomplete pair; range delta is an endpoint span, not inferred uncertainty |
| `width`, `height` | Physical native track dimensions in TeX pt; excludes external label and marker overhead |
| `label`, `precision`, `comparelabel` | Effective native label options, preserved without replacing raw values |
| `unit`, `unitcode`, `unittext`, `accessibility` | Effective option tokens; no automatic conversion |
| `alt` | Native full description, including explicit alt override and raw values; reading it creates no tagging |

Precision only changes visual formatting. Clipping keeps raw values and delta
unchanged, and retains the frontend's warning/error policy. Shared scales resolve
before record construction. Record access closes when the callback returns and
cannot read another invocation's values. There is no public record setter.

## Capability query

All registered pair consumers have `pair`, `read-only`, `missing`, `shared-scale`,
`clip`, `native-default`, and their native kind (`compare`, `dumbbell`, or `range`).
`partial-missing` is true only for compare/dumbbell. `native-column` is true only
for the three builtin names. These features describe the provided record and
delegation path; they do not certify arbitrary user-written rendering or contrast.

```latex
\gradbarsifpairtypecapable{range}{partial-missing}
  {Supported}{Both endpoints must be present or missing}
```

## Callback lifecycle and semantics

Use `\gradbarspairdefault` to retain native dimensions, baseline, clipping,
formatting and Figure alternatives. It calls the captured continuation, not a
second public frontend. Recursive `\gradpairgraphic` calls and repeated delegation
are diagnosed. The once-only guard is restored on callback exit, including after
discarded measurement boxes. Independent callbacks may surround the delegated
output or add text, and own the resulting layout and accessibility of added content.

Tables can measure a cell multiple times. Consumers used in ordinary tables or
tabularray must be repeatable and avoid external writes, counters, labels and
global side effects. Reading a record and delegating creates no extra Figure;
embedded graphics retain the enclosing picture's description. A scalar backend
selected for a native pair still needs explicit `backend fallback=tikz`; pair
registration does not grant capabilities to an old backend.

## Native table proxies

```latex
\gradbarsdeclarepaircolumn{review-pair}{frontend=dumbbell,
  options={min=0,max=100,precision=1}}
\begin{center}
\begin{gradtable}[style=paired-report,width=\linewidth]
  \gradcolumn{name}{Service}
  \gradcolumn[type=review-pair]{pair}{Current / reference}
  \gradrow{Booking,66/82}
  \gradrow{Pending,NA/0}
\end{gradtable}
\end{center}
```

Load `table` (default). `\gradbarsdeclarepaircolumn{name}{keys}` is locally scoped
and shares the column namespace, so scalar/native/visible duplicate names are
rejected. Keys are `frontend=compare|dumbbell|range` (default dumbbell) and
`options={graphic keys}`. Only builtin native pair proxies are admitted, not
arbitrary standalone consumers. The native internal pair allocation path handles
the allocated track, label measurement, widths and pagination.

Cells use `left/right`; whole NA represents two missing endpoints. CSV source
binding and fixed, automatic-column or named scales reuse existing native pair
semantics, including both observations when computing a column range. Options
apply before per-column options; resolved scales and final allocated widths still
win. Pair columns do not admit scalar sorting/filtering, ranking or aggregation.
The old scalar column registry still rejects compound frontends and data.

原生表格须显式声明标准双值代理，只接受 compare、dumbbell、range。
单元格使用左值/右值，整格 NA 表示两端缺失；普通 tabular 和 tabularray 则可直接调用
`\gradpairgraphic`。新接口不自动扩大标量列的筛选、排名、汇总或地区数字输入权限。

## Other hosts and examples

Ordinary tabular cells can call `\gradpairgraphic` directly. tabularray Q cells
also accept explicit calls; use sufficient explicit widths, with separate opt-in
structure tagging if required. A cmd that passes one cell argument needs an
explicit two-value splitter; do not treat two observations as one scalar input.
No general custom-pair column callback, automatic pgfplotstable pair binding, or
natural-width tagged tabularray support is implied.

- Public-only consumer: [gradbars-contrib-pairs.sty](libraries/gradbars-contrib-pairs.sty).
- Same-data report presets: [English](examples/paired-report.tex), [中文](examples/paired-report-cn.tex); accessible and monochrome themes, zero, partial NA, and supplied intervals.
- [Scalar backend contract](backends.md), [scalar column adapters](column-adapters.md), [API](api.md), [accessibility](accessibility.md).
