# gradbars

**用一套接口，在 LaTeX 表格中呈现数值、比较与趋势。**

**v0.0.4 · pdfLaTeX / XeLaTeX / LuaLaTeX · MIT**

**已收录至 CTAN**：访问 [gradbars 宏包页面](https://ctan.org/pkg/gradbars)，查看收录版本、文档与下载入口。

[仓库首页](README.md) · [English](README.en.md) · [中文手册 PDF](gradbars-manual-v0.0.4.pdf) · [英文手册 PDF](gradbars-manual-en-v0.0.4.pdf)

![对比、正负贡献、趋势与目标评价](docs/images/overview-v0.0.3.svg)

既可把单个图形嵌入现有 `tabular`，也可通过 `gradtable` 声明列、填写数据，统一生成可视化表格。图形保留共享尺度与真实数值，无需额外包裹 `tikzpicture`，无需开启 shell escape。

## v0.0.4：专属可视化表格

- **声明列，直接填数据**：`gradcolumn` 与 `gradrow` 组织表格，不必手写单元格分隔与换行命令。
- **九种列类型**：文本、数字、普通条、子弹图、区间、双层对比条、哑铃、堆叠条和迷你趋势线。
- **可控的布局**：左／中／右对齐、独立表头对齐、文本垂直对齐、四种线条样式，以及列间距和行高设置。
- **自动分配列宽**：根据总宽度、固定列和权重分配空间；同列标签预先测量，图形共用尺度。
- **多级表头与分组**：跨列标题、分组行、最佳值加粗和次佳值下划线，支持并列值及优劣方向。
- **复用与跨页**：保存表格样式和列定义；`long=true` 重复完整表头，跨页保持列宽与排名一致。
- **更完整的图形标注**：多条参考线、子弹图、多组区间、越界提示、点形状、差值箭头与百分比变化。

中文手册包含 **六部分、42 章、77 个编号示例**；英文手册包含 **六部分、28 节**。两份手册均提供实际效果与源码。

## 快速开始

将 `gradbars.sty` 放在主 `.tex` 文件旁，可使用 **pdfLaTeX、XeLaTeX 或 LuaLaTeX**。
宏包依赖 TikZ/PGF、xparse、expl3、collcell、array、booktabs、colortbl 和 longtable。中文字体只用于中文手册，宏包本身不要求中文文档类。

```latex
\documentclass{article}
\usepackage{gradbars}
\setlength{\parindent}{0pt}
\begin{document}
\begin{gradtable}[width=\linewidth,header align=c,
  label width=12mm,column sep=6pt]
  \gradcolumn{method}{Method}
  \gradcolumn[type=bar,weight=2,mark=both,
    options={max=100,precision=1}]{score}{Score}
  \gradcolumn[type=number,width=22mm,mark=best,
    options={better=lower,precision=1}]{time}{Time / ms}
  \gradheader{\gradspan{1}{Setup}\gradspan{2}{Evaluation}}
  \gradgroup{Baselines}
  \gradrow{Method A,82.4,14.8}
  \gradrow{Method B,91.6,18.2}
  \gradgroup{Improved}
  \gradrow{Method C,87.3,11.5}
  \gradrow{Pending,NA,NA}
\end{gradtable}
\end{document}
```

得分越高越好，耗时越低越好；最佳值加粗，得分次佳值加下划线。`NA` 表示缺失，不等于零。上例使用英文表头，可直接用三种引擎编译；中文内容可使用 XeLaTeX 和 `ctexart` 文档类。

默认表格不跨页。需要跨页时，添加 `long=true`，将表格直接放在单栏正文中；不要置于浮动体或 `minipage` 内。

## 如何选图形

| 目的 | 入口 |
| --- | --- |
| 单个数值、相对零点的增减 | `\gradbar[min=-50,max=100]{值}` |
| 更少填充面积 | `\gradbar[shape=lollipop]{值}` |
| 宽基准条与细当前条 | `\gradcompare{基准}{当前}` |
| 比较两个位置或差值 | `\graddumbbell[compare label=delta]{之前}{之后}` |
| 给定上下界 | `\gradrange[range point=50]{35}{75}` |
| 分级背景上的完成度 | `\gradbullet[bullet bands={{60/black!8},{100/black!20}},target=85]{78}` |
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

[中文手册源码](docs/gradbars-manual.tex) 按入门、图形、外观、专属表格、案例与参考六部分组织。
77 个编号示例包含前后对比、收支贡献、趋势汇总和专属表格，以及双栏论文、跨页长表、黑白打印和幻灯片。
[英文手册源码](docs/gradbars-manual-en.tex) 同步介绍 v0.0.4 接口，章节与示例编号独立。
示例数据仅用于演示。

生成仓库根目录中的版本 PDF：

```sh
python scripts/build_manual.py
```

脚本先编译四类真实排版，再用 XeLaTeX 两遍编译中文手册、pdfLaTeX 两遍编译英文手册。中文文档需要 ctex/Fandol。
Python 仅用于文档构建；宏包本身不需要。仓库包含中英文 v0.0.4 PDF 与源码；所有文本文件采用 LF 换行。

## 当前边界

- 宏包已通过 pdfLaTeX、XeLaTeX、LuaLaTeX 检查（包括 CSV）；中文手册使用 XeLaTeX。完整坐标轴或大型绘图仍应使用专门工具。
- CSV 仅接受逗号分隔的单行字段，自动生成的 CSV 表格不自动分页。
- 堆叠不接受缺失段、条件阈值与误差线。
- 趋势线不解析日期，不接受柱形目标线、误差线、背景区间或阈值评价；观测必须等间隔。
- 固定量程要求 min 不大于零、max 为正；自动趋势范围支持正数、负数与恒定序列。
- 标签避让限于单个图形，长标签和图例仍需要表格预留空间。
- 尚未实现图形专用无障碍 PDF 标签或 tabularray 专用列接口。

MIT 许可证。提交问题时请附最小 `.tex` 示例、编译引擎和日志。
