# v1.3.0–v1.4.0: trend compositions / 微型趋势组合

This document retains the former local v1.3.0/v1.4.0 planning labels. Those
features are included in the actual **v1.2.1** snapshot at the maintainer's request;
see [the change history](../CHANGELOG.md).
本文沿用原本地规划标签；相关功能保留于本次指定编号 v1.2.1，并未分别发布这些规划版本。


Both commands belong to `spark`, loaded by default. They retain the complete
ordered series, require `spark type=line` and an explicit shared value range
(`spark range=fixed,min=...,max=...` or a named scale). They are separate entries;
existing `\gradspark` and `\gradsparktarget` semantics and errors are preserved.
/ 两个新入口属于 spark 库；不重解释旧命令，每个版本各新增一个组合。

```latex
\gradscale{quality}{min=0,max=100}
\gradsparkband[scale group=quality]{20,40,NA,70}{45}{65}
\gradsparkcompare[scale group=quality,compare label=delta]{20,40,NA,70}
```

## v1.3.0 fixed reference band / 固定参考带

`\gradsparkband[options]{series}{lower}{upper}` draws a constant horizontal
reference band across the trend area. It requires `min <= lower < upper <= max`.
`band color=gold` and `band opacity=.3` control its fill; opacity must be in `[0,1]`.
These are strict canonical numeric bounds, independent of regional input.
The band is a supplied reference interval, never an observation or automatically
a confidence interval. It does not fill missing positions or affect statistics,
range or ranking. All-missing input keeps the reference band and a missing label.
Print mode uses a light gray band, dashed boundaries and black trend strokes.
/ 参考上下界严格递增且在量程内，不随位置变化、不补缺失、不改变统计。
打印模式保留灰色参考区间和虚线边界。

## v1.4.0 endpoint dumbbell plus complete trend / 首末哑铃与全过程趋势

`\gradsparkcompare[options]{series}` uses the first and last **positions** for the
left dumbbell panel and all positions for the right trend panel. Empty input is
an error; a single observation is both endpoints. `NA` retains its position and
breaks the trend line. If one endpoint is missing, its marker and the connector
are omitted; the valid endpoint remains. A delta is missing unless both endpoints
exist. Interior valid observations never replace missing endpoints. Zero remains
an observation. / 首末取位置而非首末有效值；中间缺失保留间断，端点缺失不回退。

| Key / 参数 | Default / 默认 | Contract / 约定 |
| --- | --- | --- |
| `compare panel ratio` | `.4` | Left share of usable panel width, strictly between 0 and 1 / 左面板比例 |
| `compare panel gap` | `3mm` | Nonnegative panel gap / 非负面板间距 |
| `compare label` | `values` | `values` (first/last) or `delta` (last minus first) / 首末或末减首 |
| `width` | existing graphic default / 继承 | Total two-panel width including gap and outer marker allowance / 双面板总宽 |
| `height` | existing graphic default / 继承 | Trend height; dumbbell centered vertically / 趋势高度 |

Both panels use one range and one unit, with no inferred secondary axis. Each
outer edge reserves `marker size + 1pt`. After subtracting these two allowances
and the gap, the ratio divides the remaining width. Each panel must exceed twice
that allowance; otherwise increase width or adjust ratio/gap. The outside label
slot and label gap are additional, using existing layout rules. Explicit `text`
overrides the label. `compare label=percent` is rejected; `delta` is in the source
unit. / 总宽包含外侧标记余量与面板间距；外置标签另占空间。

Native `gradtable` adds `type=trendcompare`: use a manual braced series or a quoted
CSV field containing a canonical point-decimal comma-separated sequence. Its
default height is `4ex`. Column scales resolve once for both panels; `scale=column`
uses every valid series observation and existing `scale scope` semantics, never
summary rows. Use explicit `min/max` or a named scale for cross-table comparison.
This compound column is not a scalar: scalar filtering/sorting, ranking,
aggregation and regional input keys are rejected. No third-party scalar column
adapter or new tabularray helper is introduced. / 原生复合列默认高 4ex，自动尺度
读取全部有效观测；不把序列伪装为标量进行排序、聚合或地区转换。

## Accessibility and backend / 无障碍与后端

Each standalone composition creates **one Figure**. Its automatic alternative
retains the full series and range, then describes the fixed reference band or
first/last positions and delta, including missing endpoints. Explicit `alt`,
`accessibility=artifact|off`, and embedded TikZ behavior follow existing rules;
measurement creates no duplicate semantic figures. This adds no PDF/UA
certification or automatic hierarchy Table tagging.
/ 一次组合只生成一个 Figure；保留完整序列和缺失描述，遵循已有显式替代文本及嵌入规则。

Native backend kinds are `spark-band` and `spark-compare`. Scalar custom backends
must select `backend fallback=tikz`; otherwise capability checks fail. Backend
schema remains 1; no new compound callback record is exposed.
/ 原生后端种类显式区分；标量自定义后端须启用 TikZ 回退，记录模式仍为 1。

See [regional input](regional-input.md), [hierarchical tables](hierarchical-tables.md)
and [standalone examples](examples/README.md).
