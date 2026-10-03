# gradbars

**直接嵌入 LaTeX 表格的数据条与迷你图形。**

**v0.0.3 · pdfLaTeX / XeLaTeX / LuaLaTeX · MIT**

[English](README.md) · [中文手册 PDF](gradbars-manual-v0.0.3.pdf) · [英文手册 PDF](gradbars-manual-en-v0.0.3.pdf) · [参数说明](docs/api.md) · [版本说明](docs/releases/v0.0.3.md)

![对比、正负贡献、趋势与目标评价](docs/images/overview-v0.0.3.svg)

在普通单元格中加入图形，保持共享尺度并保留原始数值。无需额外包裹 `tikzpicture`，无需开启 shell escape。

## v0.0.3 新增内容

- **哑铃对比图**：空心基准点、实心当前点，可显示当前值减去基准值。
- **正负混合堆叠**：正负从零点分别累计，显示净值或两侧小计。
- **迷你趋势线**：等间隔观测，缺失断点，极值和末点标记，行内自动或共享固定范围。
- **目标与区间评价**：越接近目标越好、处于区间内最好，评价只改变颜色。
- **成组配色与类别纹理**：分类、顺序、发散、黑白四类方案；重排类别后仍可保持颜色与纹理。
- **重整图文手册**：六部分、56 个编号示例、六个应用表格、四类真实排版案例及接口索引。

普通条、正负条、双层条、棒棒糖、浮动区间、误差线、CSV、数值列与命名样式继续可用。

## 快速开始

将 `gradbars.sty` 放在主 `.tex` 文件旁，可使用 **pdfLaTeX、XeLaTeX 或 LuaLaTeX**。
宏包依赖 TikZ、xparse、expl3、collcell。中文字体只用于中文手册，宏包本身不要求中文文档类。

```latex
\documentclass{article}
\usepackage{booktabs,gradbars}
\begin{document}
\gradbarssetup{width=35mm,precision=0}
\begin{tabular}{ll}
\toprule
View & Data \\
\midrule
Value & \gradbar{72} \\
After / Before & \graddumbbell{58}{76} \\
Positive / Negative & \gradstack[min=-50,stack totals=separate]{60,-20,15,-10} \\
Trend / Last & \gradspark[spark range=fixed,min=0,max=100]{25,45,NA,60,80} \\
\bottomrule
\end{tabular}
\end{document}
```

## 如何选图形

| 目的 | 入口 |
| --- | --- |
| 单个数值、相对零点的增减 | `\gradbar[min=-50,max=100]{值}` |
| 更少填充面积 | `\gradbar[shape=lollipop]{值}` |
| 宽基准条与细当前条 | `\gradcompare{基准}{当前}` |
| 比较两个位置或差值 | `\graddumbbell[compare label=delta]{之前}{之后}` |
| 给定上下界 | `\gradrange[range point=50]{35}{75}` |
| 可相加的贡献 | `\gradstack[min=-60]{60,-25,20,-15}` |
| 等间隔变化趋势 | `\gradspark{25,40,NA,60,80}` |
| 点估计与不确定性 | `\gradbar[error minus=5,error plus=8]{60}` |

## 保持正确的数据含义

- 同列共用 `min`、`max`、`width`；负值需要负的 `min`。
- `unit` 只附加单位；`value format=percent` 计算数值相对于 max 的比例，且只用于非负量程。
- 空输入和 `NA` 为缺失；趋势中的缺失保留横向位置并断开，末项缺失不会用前一项替代。
- 正负堆叠的默认总标签是净值，`stack totals=separate` 显示“正小计 / 负小计”。净值为零仍可能有两侧贡献。
- 堆叠分段百分比为 `abs(段值) / sum(abs(所有段值))`，表示绝对活动量份额；不是净值占比，也不自动归一化条形。
- 自动趋势范围用于看形状；跨行比较水平和波动时，应统一 `spark range=fixed`、min、max、width、height。
- 越界默认警告并截断图形，标签保留原值；`overflow=error` 可改为报错。

## 目标与区间评价

```latex
\gradbar[better=target,quality target=50,
  thresholds={5,15},target=50,palette=diverging]{52}

\gradbar[better=interval,quality range={40,60},
  thresholds={0,10},band={40,60},palette=diverging]{68}
```

这两种模式的 thresholds 是非负距离：距离不超过第一个阈值为好，不超过第二个为中，否则为差。
`threshold colors` 顺序仍为差、中、好。quality 参数负责评价，target/band 负责绘制参考，需要分别设置。
已有的 `better=higher|lower` 用于越大或越小越好的指标。

## 复用排版与类别身份

```latex
\gradbarsstyle{paperrow}{preset=paper,width=40mm,max=100,precision=1}
\gradbar[style=paperrow]{82.5}

\gradbarscategory{Compute}{gradbarsBlue}{diagonal}
\gradbarscategory{Storage}{gradbarsOrange}{dots}
\gradstack[stack names={Compute,Storage}]{60,30}
\gradstack[stack names={Storage,Compute}]{30,60}
\gradbarslegend{Compute,Storage}
```

排版预设：`paper`、`report`、`presentation`、`outline`。
成组配色：`categorical`、`sequential`、`diverging`、`mono`。
原有七种主题和九种单色继续保留。

未注册名称时按段序号循环取色；注册后按名称匹配。print/mono 使用灰度配色并保留命名类别纹理。
图例与分段共用同一映射，颜色不足时可结合名称和纹理识别。

## CSV 与现有表格

```latex
\gradbarsloadcsv{results}{results.csv}
\gradbarscsvstyle{shared}{results}{Score}
\gradbarcsv[style=shared]{results}{1}{Score}
\gradbarscolumn{G}{style=shared}
```

支持按列名读取、引号内逗号、缺失值映射和整列共享范围。CSV 字段按字符读取，不作为 TeX 执行。
完整用法与表格源码集中在手册中。

## 一本文档，效果与源码对照

[手册源码](docs/gradbars-manual.tex) 按入门、图形、数据接口、外观、案例与参考六部分组织。
56 个编号示例包含前后对比、收支贡献和趋势汇总，以及双栏论文、跨页长表、黑白打印和幻灯片。
示例数据仅用于演示。

生成仓库根目录中的版本 PDF：

```sh
python scripts/build_manual.py
```

脚本先编译四类真实排版，再用 XeLaTeX 两遍编译中文手册、pdfLaTeX 两遍编译英文手册。中文文档需要 ctex/Fandol。
Python 仅用于文档构建；宏包本身不需要。仓库包含中英文 v0.0.3 PDF 与源码；所有文本文件采用 LF 换行。

## 当前边界

- 宏包已通过 pdfLaTeX、XeLaTeX、LuaLaTeX 检查（包括 CSV）；中文手册使用 XeLaTeX。完整坐标轴或大型绘图仍应使用专门工具。
- CSV 仅接受逗号分隔的单行字段，自动生成的 CSV 表格不自动分页。
- 堆叠不接受缺失段、条件阈值与误差线。
- 趋势线不解析日期，不接受柱形目标线、误差线、背景区间或阈值评价；观测必须等间隔。
- 固定量程要求 min 不大于零、max 为正；自动趋势范围支持正数、负数与恒定序列。
- 标签避让限于单个图形，长标签和图例仍需要表格预留空间。
- 尚未实现图形专用无障碍 PDF 标签或 tabularray 专用列接口。

MIT 许可证。提交问题时请附最小 `.tex` 示例、编译引擎和日志。
