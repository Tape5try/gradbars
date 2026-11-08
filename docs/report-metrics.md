# Report metrics and compositions / 报告指标与组合图（v1.2.1）

The former v1.6.0 scope is included in v1.2.1 at the maintainer's explicit request.
原 v1.6.0 规划此次并入指定版本 v1.2.1；旧 `\gradmetric` 和 `\gradmetriccolumn`
仍是未绑定的外观配方，默认值不变。New declarations are opt-in; old report recipes remain.

## Declaration and binding / 声明与绑定

Load `\usegradbarslibrary{reports}`. The existing reports dependencies are retained.

```tex
\gradscale{review-range}{min=0,max=100}
\graddeclaremetric{review}{title={Review score},role=score,
 unit={\,pt},better=higher,precision=1,
 scale group=review-range,aggregate=mean}
\gradmetricuse[width=40mm]{review}{80}
\gradmetricnumber{review}{0}
\gradmetriccard{review}{0,40,NA,80}
% In a native table; source binding belongs to this use, not the declaration:
\gradmetricbind[source=Review,mark=both]{review}{score}
\gradmetriccardcolumn[source=History,options={height=5mm}]{review}{history}
```

| Declaration field / 声明字段 | Default / 默认 | Meaning / 含义 |
| --- | --- | --- |
| `title` | required / 必填 | Nonempty display heading and metric alternative / 标题及指标描述 |
| `role` | `scalar` | `scalar,score,count,duration,ratio`; descriptive, no inferred math / 仅描述角色 |
| `unit`, `unit code`, `unit text` | empty / 空 | Existing unit/siunitx semantics; no conversion / 原单位语义、不换算 |
| `better` | `higher` | `higher` or `lower`; raw scalar direction / 原始标量方向 |
| `formatter` | `builtin` | Registered display formatter / 注册显示格式器 |
| `precision` | `1` | Integer 0–6 / 整数 |
| `number format` | `fixed` | `fixed,scientific,grouped` |
| `value format` | `value` | `value,percent`; percent needs min=0 and valid base / 百分比要求零下界与有效基数 |
| `percent base` | empty / 空 | Existing percent denominator, otherwise max; frozen / 百分比基数，未指定取 max，冻结 |
| `min`, `max` | `0`, `100` without groups / 无组时 | Strict increasing fixed range; group supplies omitted bounds / 固定递增范围 |
| `scale group`, `legend group` | empty / 空 | Existing named range/shared legend / 已有命名尺度、共享图例 |
| `aggregate` | `none` | `none,count,sum,mean,min,max`; explicit scalar aggregation / 显式标量聚合 |

Declarations use ordinary TeX scope, lower-case IDs and visible duplicate errors.
There is no silent override or automatic shadowing of a visible ID. Unknown IDs,
fields or enum values are errors. `\gradmetricinfo{id}{field}` expands to declared
metadata; unavailable fields report an error. Source fields are not declaration
keys: bind them at each table use or through the existing `\gradtableschema`.

声明按 TeX 分组生效，不静默覆盖可见重名。未知 ID/字段/枚举有诊断。
`\gradmetricinfo` 可展开查询元数据；源字段只在使用处或已有 schema 中绑定。

Ranges, named scale/legend identity, unit fields, better direction and numeric
format are frozen. Per-use width, height, label placement and ordinary colors may
change; conflicting semantic options report errors. A shared legend additionally
freezes its existing palette/signature contract. Named scale redefinitions cannot
silently change a metric's resolved range. Units and `unit code` are formatting
metadata, not executable conversion instructions. Roles do not imply an aggregate,
a target, quality thresholds, normalization or a combined score. This first metric
declaration interface supports `higher/lower`; existing unbound quality APIs keep
their target/interval support separately.

范围、命名尺度/图例身份、单位、方向及数字格式冻结，调用可改变尺寸、标签位置和
普通颜色。共享图例还遵守已有调色板签名约束。尺度重定义改变范围时也报错。
角色不推断聚合、目标、阈值、归一化或综合评分；首版声明方向只接收 higher/lower。
旧未绑定质量接口的 target/interval 支持保持不变。

`\gradmetricbind[typed column keys]{metric ID}{column ID}` defaults to bar,
fixed scale, declaration title/formatter/aggregate. It supports scalar bar,
number, heat and bullet frontends and explicitly admitted scalar adapters.
`\gradmetriccardcolumn` instead selects `type=metriccard,aggregate=none`.
Scalar summary aggregation must match the declaration; history cannot be ranked,
selected as a scalar, aggregated or accepted as regional scalar input. Native
CSV safety and `filter → global stable sort → global limit → groups` are unchanged.
Visible/data summary scope remains a table choice. Raw values drive geometry,
ranking and summaries; formatter output is never parsed. A count summary suppresses
units as before. Zero is observed; NA is missing.

标量绑定默认条形、固定尺度、声明标题/格式器/聚合；支持 number/heat/bullet 及显式标量
适配。指标卡列关闭聚合，不将历史暗中并入标量统计。可见/data 摘要作用域仍由表格选择，
原始数值参与运算，count 不带单位，零不作为缺失。原生 CSV 安全和选择顺序保持。

## Current-value bar plus full trend / 当前值条＋完整趋势

`\gradmetriccard[graphic options]{metric ID}{history}` takes a nonempty positional
numeric/NA list. The **last position** supplies the current bar; final NA means
missing, even if an earlier position is valid. NA breaks the trend and is never
filled or removed. One point, constant values and all-missing histories work.
The current bar and complete history share one frozen range and unit, without
independent rescaling or a second axis. Signed ranges use the existing zero/bar
geometry. The history column never contributes a hidden current scalar to summaries.

序列非空，末位置就是当前值；末位 NA 不回退。完整历史保留缺失断点，不插值、删点或
另立坐标轴。单点、常量、全缺失均可；两部分共享冻结范围与单位，带符号范围沿用零线几何。

Default standalone style `metric-card` uses 70mm drawing width and 5ex height.
`card panel ratio` defaults to 0.4 of the drawing width **after** `card panel gap`
(default 3mm) is deducted; both panels reserve the existing marker/stroke padding
and require positive interior width. Ratio is strictly between 0 and 1, gap is
nonnegative. Outside/left numeric labels add the existing `label width + label gap`
to standalone width; native table allocation already deducts these costs.
The native column inherits allocated height; choose `options={height=5mm}` as needed.
`label=none` or `inside` avoids external label width. Card rendering always uses
fixed range and a line trend; arbitrary layer composition and dual units are excluded.

独立样式图宽 70mm、高 5ex；先扣 3mm 面板间距，再按 0.4 分配当前条，左右各预留
标记/描边边缘，内部宽须正。ratio 严格在 0 和 1 之间，gap 非负。外置/左标签另外
占标签宽与间隙；原生表格已扣这些开销。表格可显式设置图高；固定范围与线型趋势为本配方约束。

One card emits one combined Figure with current position, full positional history,
range, unit, title, role and direction. Explicit `alt`, artifact/off, embedded
picture behavior and measurement suspension retain the existing contract. No
complete PDF/UA certification is claimed. New native backend kind `metric-card`
requires explicit TikZ fallback for scalar custom backends; backend schema stays 1.

一个指标卡只有一个 Figure，合并当前值、完整历史、范围、单位和指标元数据；显式 alt、
artifact/off、嵌入 picture 与试排去重沿用已有规则。自定义标量后端对新 kind 须显式 TikZ 回退。

## Raw box plus rug / 原始箱线图＋rug

`\gradboxrug[graphic options]{raw samples}` and native `type=boxrug` draw the
existing box plot and ticks for **all valid raw samples**, including duplicates
and non-outliers. Default height is 5ex. Rug ticks overlap at duplicate values;
counts retain multiplicity. Type-7 quartiles, 1.5-IQR observed whiskers and outliers
are unchanged. Nothing is jittered, sampled or binned. At most **2048 raw positions**
(including NA) are accepted; larger input reports an error before drawing.
Precomputed `n=...,median=...` summaries are rejected because positions cannot be
recovered. Zero, missing, one-point and constant samples retain existing statistics.
`box range=auto|fixed`, named ranges, overflow policy and print mode are inherited;
clipping changes drawing positions, never statistics. The combined Figure retains
sample count, quartiles, whiskers and the full valid sample list with repeats.
Native backend kind is `box-rug`; scalar backends need explicit TikZ fallback.

箱线图和 rug 使用同源样本，全部有效值逐一绘制，重复位置可重叠但计数不合并。
type-7 四分位数、1.5-IQR 实际观测须及离群点不变，不抖动、抽样或分箱。
最多 2048 个原始位置（含 NA），超限先报错；摘要不能恢复位置，因此不接受预计算摘要。
自动/固定/命名范围、溢出策略、打印模式沿用箱线图；裁剪不改变统计。组合 Figure 包含
统计和保留重数的有效样本列表。原生后端 kind 为 box-rug，schema 仍为 1。

New presets: `metric-report`, `rug-report`; styles: `metric-card`, `sample-rug`.
Examples: [two tables and standalone, English](examples/report-metrics.tex),
[中文](examples/report-metrics-cn.tex); [raw rugs, English](examples/column-adapters.tex),
[中文](examples/column-adapters-cn.tex). All sample data are fictitious.
