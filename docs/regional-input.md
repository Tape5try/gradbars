# v1.3.0: regional numeric input / 显式地区数值输入

This document retains the former local v1.3.0/v1.4.0 planning labels. Those
features are included in the actual **v1.2.1** snapshot at the maintainer's request;
see [the change history](../CHANGELOG.md).
本文沿用原本地规划标签；相关功能保留于本次指定编号 v1.2.1，并未分别发布这些规划版本。


This opt-in input layer converts declared regional literals into canonical numbers.
Existing commands retain strict point-decimal/scientific input. It does not guess
locale, evaluate expressions or convert units. / 仅显式启用；旧入口语法和默认值保持，
不猜地区、不计算表达式、不换算单位。

```latex
\gradbarsparsenumber[decimal=comma,grouping=point]{1.234,5}{\amount}
\gradbar[max=2000]{\amount}
```

The helper is available with `libraries=none`. Its last argument must be one
control sequence; assignment follows ordinary TeX grouping. Each call resets
`decimal=point,grouping=none` before applying its options. Macros expanding to
numeric text are accepted, as in existing scalar input. / 此命令属于核心数值模块，
输出局部赋值；每次调用重置入口规则，宏展开规则与已有标量入口一致。

| Input / 输入 | Explicit options / 规则 | Result / 结果 |
| --- | --- | --- |
| `1234.5` | default / 默认 | `1234.5` |
| `1,234.5` | `decimal=point,grouping=comma` | `1234.5` |
| `1.234,5` | `decimal=comma,grouping=point` | `1234.5` |
| `1 234,5` | `decimal=comma,grouping=space` | `1234.5` |
| `1,234` | `decimal=comma,grouping=none` | `1.234` |
| `1,234` | `decimal=point,grouping=comma` | `1234` |
| `1,234` | default / 默认 | error / 错误 |
| `12,34.5` | `decimal=point,grouping=comma` | error / 错误 |
| empty or `NA` / 空 | any valid configuration / 合法配置 | `NA` |
| `0` | any valid configuration / 合法配置 | zero / 零 |

`decimal` accepts `point|comma`; `grouping` accepts `none|point|comma|space`.
The two separators must differ. Grouping is optional, but when present the first
integer group has 1–3 digits and every following group has exactly 3. Fractions
and exponents cannot be grouped. `space` means the ordinary ASCII space, not
thin spaces, nonbreaking spaces or arbitrary TeX spacing commands. Leading and
trailing ordinary spaces are trimmed. / 分组只用于整数部分，首组一至三位，
后组恰三位；space 仅指普通 ASCII 空格。首尾空格会裁剪。

Signs, fractions such as `.5`/`,5`, trailing decimal markers and `e/E` scientific
notation follow the declared decimal rule; the exponent is an ungrouped signed
integer of at most three digits. Canonical output passes the existing validator
(at most 101 digits per integer/fraction part; nonzero magnitude `1e-100` through `1e100`) and
uses finite-precision expl3 arithmetic. Expressions, input units, lowercase
`na`, NaN and infinity are errors. / 归一化后复用同一验证器及数值边界；科学计数法
指数最多三位，不接受表达式、输入单位或非有限数。

## CSV numeric columns / CSV 数字列

```latex
\gradbarsloadcsv{regional}{docs/data/regional-input.csv}
\begin{gradtable}[data=regional,style=regional]
\gradcolumn[source=Item]{item}{Item}
\gradcolumn[source=Amount,type=number,input decimal=comma,
 input grouping=point,aggregate=sum]{amount}{Amount}
\gradsummary{Total}
\end{gradtable}
```

CSV retains its existing missing-token mapping before normalization. / CSV 先沿用已有缺失标记映射，再执行归一化。

Only explicitly configured CSV `number`, `bar`, `bullet` and `heat` columns use
`input decimal` and `input grouping` (defaults `point` and `none`). Manual rows,
text and compound columns reject these keys. Normalization precedes filtering,
stable global sorting, limit, ranking, scales and summaries. Each bound column
can have its own rule; the loaded dataset and text columns retain literal text.
An output formatter never changes these values. / 仅适配明确声明的 CSV 标量列，
在筛选等数据处理前归一化；文本、原始数据集及 CSV 安全边界保持，显示格式不参与计算。

CSV still uses commas as field separators: quote decimal-comma or grouped-comma
fields with double quotes. No delimiter auto-detection or JSON/YAML support is
added. `style=regional` is a native table preset with accessible colors, decimal
number alignment and increased spacing; it does **not** choose input separators.
/ CSV 逗号与引号规则不变，regional 只设排版、不设地区。

See [trend compositions](trend-compositions.md), the [API](api.md), and the
[English](examples/regional-input.tex) / [Chinese](examples/regional-input-cn.tex)
executable examples. / 示例为虚构的图书采购记录。
