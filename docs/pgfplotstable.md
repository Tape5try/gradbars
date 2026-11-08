# Optional pgfplotstable cells / 可选 pgfplotstable 单元格（v1.2.1）

```tex
\usepackage[libraries=none]{gradbars}
\usegradbarslibrary{pgfplotstable} % explicitly loads pgfplotstable
\pgfplotsset{compat=1.18}
\gradpgfplotstablecolumn[min=0,max=100]{Score}{bar}{35mm}
\gradpgfplotstablecolumn[precision=1,unit={\,ms}]{Time}{number}{24mm}
% pgfplotstabletypeset still owns data reading, headings and the table.
```

`\gradpgfplotstablecell[graphic options]{bar|heat|number}{total width}{value}`
formats one cell. `\gradpgfplotstablecolumn[graphic options]{column}{kind}{width}`
appends a `string type` and body `postproc cell content` hook to one named column.
Headings and unbound columns remain under pgfplotstable control. The hook uses
its public preprocessed-cell key, as defined in the
[official data-processing documentation](https://tikz.dev/pgfplots/pgfplotstable-data-processing).

第一个命令格式化一个单元格；第二个命令只给指定列追加字符串类型与正文后处理。
表头、未绑定列仍由 pgfplotstable 管理；不修改全局表格样式。可在之后追加
`column name`。适配读取公开的预处理单元格键，不将表头当数据绘制。

Defaults are `baseline=text,label=none`, plus explicitly supplied graphic keys.
Empty cells and `NA,N/A,null` map to missing; `pgf missing={...}` replaces the
nonempty missing-token list for that call. Zero remains zero. Other values use
the strict numeric input contract, including scientific notation; no locale
inference, formula evaluation or unit conversion. Number cells use the selected
formatter, precision and units without emitting a Figure. Load `heat` explicitly
before using heat cells; bar/number work with core and this optional library only.

默认文本基线、无标签；空白及 `NA,N/A,null` 映射缺失。`pgf missing` 替换非空缺失
标记列表，零保留。其余值须满足严格数字规则，不猜地区输入、不求值、不换算。
数字单元格遵守 formatter、精度、单位，不生成 Figure；Heat 须另外加载 `heat`。

Width is the full emitted cell box, excluding the host table's padding/rules.
For left/outside labels, `label width + label gap` is deducted from the drawing
width. Positive remaining width is required; measured output wider than the
budget reports an error (0.2pt tolerance). Long custom labels must fit explicitly.
Ranges are graphic fixed/named ranges, with no automatic scan across PGF rows.
Missing cells preserve the selected frontend's missing rendering and alternatives.

宽度是单元格内容总盒宽，不含宿主表的间距/规则；外置或左标签先扣标签宽与间隙。
剩余图宽须正，实测输出超预算报错（容差 0.2pt）。范围由图形固定/命名尺度决定，
不会扫描 PGF 数据自动求列范围；缺失外观与替代文本沿用所选图形前端。

This adapter does not inherit `gradtable` CSV filtering, sorting, grouping,
ranking, summaries, automatic scales, repeated-header logic or complete table
structure tagging. Its upstream reader accepts TeX as pgfplotstable normally
does; this is **not** the literal-safe native CSV reader. Use trusted TeX input
or the native CSV path when literal input is required. Neither interface executes
CSV cell text on behalf of the other.

本适配不继承原生 CSV 的选择、分组、排名、摘要、自动尺度、跨页表头或整表结构标记。
上游读取器沿用 pgfplotstable 的 TeX 输入语义，不承诺原生 CSV 的字符安全边界；
需使用可信 TeX 输入，或选择原生 CSV 路径。

Examples: [English](examples/pgfplotstable-cells.tex), [中文](examples/pgfplotstable-cells-cn.tex).
The optional library adds one runtime module; the original five default libraries are unchanged.
