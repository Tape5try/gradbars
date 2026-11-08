# v1.3.0 / v1.4.0 migration / 升级说明

This document retains the former local v1.3.0/v1.4.0 planning labels. Those
features are included in the actual **v1.2.1** snapshot at the maintainer's request;
see [the numbering and migration notes](migration-v1.2.1.md).
本文沿用原本地规划标签；相关功能保留于本次指定编号 v1.2.1，并未分别发布这些规划版本。


This local v1.4.0 development snapshot includes both roadmap versions. Install
all 22 matching runtime modules together; do not mix versions. No upload, tag,
Release or CTAN submission was performed. / 本地 1.4.0 开发版包含两个版本规划，
22 个运行模块须整套使用；本轮没有上传或发布。

Existing calls and defaults remain. / 旧调用及默认语义保持。

- v1.3.0: opt in through `\gradbarsparsenumber` or CSV scalar-column `input decimal`/`input grouping`. Do not add separators to old strict entries without normalization. See the [input matrix](regional-input.md).
- v1.3.0: `\gradsparkband` adds exactly one fixed-reference composition; it is not a computed confidence interval. / 固定参考带独立启用，不作为观测。
- v1.4.0: use `group levels={parentID,leafID}` for automatic two-level CSV text groups; migrate old `rank scope=group` to explicit parent/leaf only when adopting the new entry. Old group by/manual tables need no changes. See [hierarchy contract](hierarchical-tables.md).
- v1.4.0: `\gradsparkcompare` and native `type=trendcompare` share one series/range/unit. First/last NA remain missing. `scale=column` reads all valid observations. See [panel contract](trend-compositions.md).
- New native presets: regional and hierarchical. They do not select input locale or infer grouping. Custom scalar backends need explicit TikZ fallback for the new compound kinds; backend schema remains 1.

The existing v1.2.0 readability additions remain available. v1.5.0/v1.6.0 work
and the lightweight backend are not implemented by that snapshot; the latter is now planned for v3.0.0 and
continues to await the documented l3draw maturity review.
