# Complete table examples / 完整表格示例

All new scenarios use illustrative data and existing public interfaces. English
standalone sources compile with pdfLaTeX, XeLaTeX or LuaLaTeX. The manuals also
provide Chinese labels and explain the same values and rules.

以下四组新增案例已放入中英文手册。独立源码使用英文标签，可用三种引擎编译；
手册中的中文版本保持相同数值、量程、单位与统计定义。

| Source / 源码 | Scenario / 场景 | Layout and semantics / 版式与语义 |
| --- | --- | --- |
| [course-progress.tex](course-progress.tex) | Course completion / 课程完成进度 | Assembled status heading, explicit percentages, real zero versus missing / 组装表头图例，区分零进度与待测 |
| [borrowing-channels.tex](borrowing-channels.tex) | Library borrowing channels / 图书馆借阅渠道 | Monochrome textures and stacked count shares / 黑白纹理，按每行总笔数计算分段占比 |
| [energy-retrofit.tex](energy-retrofit.tex) | Energy-use comparison / 改造前后能耗 | Native table, grouped header and common-scale dumbbells / 原生表格，多级表头与统一尺度哑铃 |
| [batch-dimensions.tex](batch-dimensions.tex) | Production batch dimensions / 生产批次尺寸 | Fixed-scale raw-sample box plots, medians and outliers / 固定量程箱线图、中位数与异常点 |

## Compile / 编译

Run from the repository root with the matching `sty/` modules:

```sh
mkdir -p build/table-scenarios
TEXINPUTS=./sty//: pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=build/table-scenarios docs/examples/course-progress.tex
```

Replace the filename for another example; XeLaTeX or LuaLaTeX can replace
pdfLaTeX. `batch-dimensions.tex` explicitly loads `distribution`; the other three
use the default libraries. No extra runtime API or default behavior is added.

Build both manuals with `l3build doc`. Edit the matching Chinese and English
chapter examples together with the standalone source when changing data.

## Other examples / 其他示例

- [Ordinary-table text baseline alignment / 普通表格文字基线对齐](baseline-alignment.tex): the issue #4 table with explicit `baseline=text`, supported in v1.1.0 and later / 为原始表格显式启用文字基线对齐，无需手动升降。

- [Eleven themes on shared signed tracks / 十一主题正负同轨对照](theme-complements.tex): the built-in `\gradsignedbar` places negative and positive values on one track with a shared zero line and scale / 内置命令每行共用一条轨道、零线和量程，保留双侧误差标记。

- [Service response and status legend / 服务响应与状态图例](service-response-legend.tex).
- [Domain reports / 领域报告](domain-reports.tex).
- [Precision/Recall ordinary table / 普通指标表格](precision-recall.tex).

These new sources are MIT licensed. The separately attributed Precision/Recall
adaptation retains the license statement at the top of its own file.
