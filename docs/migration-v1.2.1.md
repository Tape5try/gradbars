# v1.2.1 local feature snapshot / 本地功能快照

The maintainer explicitly requested that the former v1.5.0 and v1.6.0 roadmap
features use **v1.2.1**. Earlier local v1.3.0/v1.4.0 implementations are retained.
These planning labels were not separate public releases. `\gradbarsversion` now
returns `1.2.1`; version requirements compare the actual number, not feature-plan
labels. Extensions using these new interfaces should require `1.2.1`.

用户明确指定本轮编号为 v1.2.1。保留此前本地规划 v1.3.0/v1.4.0 的已实现功能，
并加入原规划 v1.5.0/v1.6.0。版本比较只认真实编号，不按旧规划标签推断；新扩展
应使用 `\gradbarsrequireversion{1.2.1}`。本轮不上传、不打 tag、不制作 Release 或 CTAN 包。

- [Explicit scalar adapters / 显式标量列适配](column-adapters.md): new registrations are local; old standalone registrations do not automatically become columns. Table callback admission adds repeatability and dimensions, without changing independent callbacks.
- [Optional pgfplotstable / 外部单元格](pgfplotstable.md): adds one module, loaded only by explicit library request. Bar/number work with core; heat additionally needs heat. Host headers and reader trust boundaries remain explicit.
- [Report metrics and two compositions / 指标与两种组合](report-metrics.md): raw box+rug and current-value/history card implement the two former plan recipes. Metric declarations are separate from the old report appearance commands.

Install **all 23 matching runtime files** together. The default five feature
libraries, public backend schema 1, previous numeric defaults, native CSV literal
safety, selection order and old unsupported-option diagnostics are preserved.
New backend kinds `box-rug` and `metric-card` require an explicit TikZ fallback
for scalar custom backends; no new renderer or l3draw prototype is included.

须一起安装 23 个同版本运行文件。默认五库、backend schema 1、原始数字默认、原生
CSV 字符安全及选择顺序保持。新组合在自定义标量后端上须显式 TikZ 回退。轻量后端已调整至 v3.0.0，
继续等待 l3draw 成熟评审，本轮没有启动新后端或性能原型。

All new examples use fictitious project/review/batch data. Zero and NA differ;
metric histories are positional, final NA does not fall back. Unit text and
siunitx macros format values without conversion; metric roles imply no statistics.
