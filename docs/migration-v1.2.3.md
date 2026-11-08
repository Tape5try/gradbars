# Upgrade to v1.2.3 / 升级到 v1.2.3

Update all 23 runtime modules together. Existing documents require no changes:
default libraries, numeric meanings, scalar interfaces and backend schema 1 remain
unchanged. No additional runtime dependencies or implicit unit conversion are added.

本版新增命令声明、显式标签定位与独立数值对扩展。中英文 README 按使用流程重构；
中文版手册按学习顺序组织，并提供单独的完整案例部分。

- `\gradbarsnewcommand` uses scoped m/O signatures, explicit data/option mappings
  and blank-input policies. Existing command names and invalid argument references
  are rejected. Required optional libraries must be loaded explicitly.
- Native bar/Heat labels support sides, anchors and dimensional offsets. Legacy
  modes remain available. Heat requires track reference; unsupported graphic types
  and area-contrast combinations diagnose explicit placement. Custom scalar
  backends require `backend fallback=tikz` for these new placement options.
- `\gradbarsdeclarepairtype` and `\gradpairgraphic` use a separate registry and
  read-only pair record version 1. Callbacks receive two canonical values, retaining
  unrounded inputs and side-specific missing flags. `\gradbarspairdefault` delegates
  once without a second validation or Figure wrapper. Range endpoints still require
  both present or both missing, in order.
- `\gradbarsdeclarepaircolumn` explicitly admits standard compare/dumbbell/range
  proxies into native tables; old scalar columns do not accept compound input.
  Cells use `left/right` or whole-cell `NA`. Pair columns support native shared
  scales and allocated widths, but no scalar ranking, selection or aggregation.
- Custom pair callbacks may be used directly in ordinary tabular and tabularray
  with explicit widths. They do not automatically become native columns or a
  pgfplotstable pair adapter. Callbacks must tolerate repeated table measurements.

See [declaration and placement options](api.md#command-declarations),
[pair fields and restrictions](pair-extensions.md) and the
[Chinese report example](examples/paired-report-cn.tex).
