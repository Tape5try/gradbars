# gradbars

**面向 LaTeX 表格与正文的紧凑数据条。**

直接在单元格或正文中添加数据条，统一配置尺度、标签与参考标记。
gradbars 基于 TikZ，适合论文中的模型对比、数据集统计和报告中的进度展示。

**v0.0.1 · XeLaTeX · MIT**

[English](README.md) · [图文宏包手册 PDF](gradbars-manual-v0.0.1.pdf) · [完整参数说明](docs/api.md)

![模型对比表格](docs/images/model-comparison.png)

## 为什么使用 gradbars？

- **直接放进普通单元格。** 用 `\gradbar{72}` 绘制，无需自行搭建坐标轴或逐个套上 `tikzpicture`。
- **分开处理数据与显示。** 原始数值决定条长，标签可以显示原值、计算占比、自定义文字或科学计数法。
- **保持同列比较一致。** 复用命名样式，明确设置范围、条宽与外部标签槽宽。
- **在单元格中补充参照。** 组合目标线、区间背景、条件配色、正负条和误差线；用 `\gradstack` 展示非负数据组成。
- **从完整示例开始。** 一本手册收录 28 个效果／源码示例，并展示 16 种内置配色：七种主题和九种单色。

gradbars 将已有的可视化方法整理为面向表格的统一接口，不宣称首创这些图形，也不以替代通用绘图系统为目标。

## 快速开始

将 `gradbars.sty` 放在主 `.tex` 文件旁边即可。使用 XeLaTeX 编译，需要带 TikZ 的较新 TeX
发行版，无需 Python、shell escape 或中文宏包。
在 Overleaf 中上传宏包，将下面的示例保存为主 `.tex` 文档，并选择 XeLaTeX 编译器。
目前尚未发布到 CTAN。

```latex
\documentclass{article}
\usepackage{booktabs}
\usepackage{gradbars}
\begin{document}
\gradbarssetup{width=24mm,max=100,precision=1,theme=blue}
\begin{tabular}{lc}
\toprule
Model & Accuracy (\%) \\
\midrule
Baseline & \gradbar{72.4} \\
Proposed & \gradbar{92.7} \\
\bottomrule
\end{tabular}
\end{document}
```

中文文档可自行选择 `ctexart` 或加载 `ctex`，宏包本身无需中文支持。

## 统一接口

```latex
\gradbarssetup{theme=teal,width=25mm,height=1.5ex}
\gradbar{86.5}
\gradbar[theme=gray,max=5000,unit={\,ms},label width=6em]{1250}
```

`\gradbarssetup` 在当前 TeX 作用域内设置默认参数；
`\gradbar` 的可选参数只影响本次绘制。无需手动套 `tikzpicture`。
正文、普通表格和 `booktabs` 表格中都能直接使用。

## 数值与显示含义

默认范围从零开始，长度比例为 `value / max`；设置负的 `min` 后，数据条从零线向两侧延伸。同一比较列应该使用相同的
`max`、`width` 和 `label width`。条越长只表示数值越大，不代表性能越好。

| 输入 | 条长比例 | 标签 |
| --- | --- | --- |
| `\gradbar[max=200]{50}` | 25% | `50.0` |
| `\gradbar[max=200,unit={\,ms}]{50}` | 25% | `50.0 ms` |
| `\gradbar[max=200,value format=percent]{50}` | 25% | `25.0%` |
| `\gradbar[max=100,unit={\%}]{86.5}` | 86.5% | `86.5%` |
| `\gradbar[max=10,text={8 / 10}]{8}` | 80% | `8 / 10` |

`unit` 只添加单位；`value format=percent` 才会计算占比，并自动添加百分号，
此时忽略 `unit`。自定义 `text` 覆盖整个标签，但不改变条长。

- **零值**：保留空轨道，不画出虚假的非零长度。
- **缺失值**：空参数或大写 `NA` 与零值分别显示；其他非数字输入仍会报错。
- **超出最大值**：默认警告并截断条长，保留真实标签；`overflow=error` 改为报错。
- **正负双向条**：通过负的 `min` 启用；默认范围不接受负数。最大值必须为正。
- **双向条标签**：不使用计算占比模式；百分数变化可用 `unit` 添加单位。
- **小数位数**：`precision=0` 至 `6`；默认保留一位小数。
- **标签对齐**：默认在轨道外右对齐，固定槽宽；较长单位可增大 `label width`。

## 16 种内置配色

七种主题及渐变预设使用 `theme` 调用，九种单色使用 `color` 调用。

![主题与标签位置](docs/images/theme-gallery.png)

| 参数 | 样式 |
| --- | --- |
| `theme=blue` | 蓝色渐变，默认 |
| `theme=teal` | 青绿渐变 |
| `theme=solid` | 蓝色纯色 |
| `theme=gray` | 灰度 |

`label=outside`、`label=inside`、`label=end`、`label=none` 分别表示外部、内部、条尾上方和隐藏标签。
颜色与字体也可以覆盖。内部标签需要搭配有足够对比度的文字和背景颜色。

新增渐变：`theme=lbyellow`、`theme=viblue`、`theme=cyblu`。
内置单色用法：`\gradbar[color=lightblue]{80}`。
`lightgreen`, `lightyellow`, `lightblue`, `lightred`, `rose`, `skyblue`, `gold`, `lavender`, `peach`.


## 六种效果（v0.0.1）

```latex
\gradbar[rounded=2pt]{72}
\gradbar[target=80]{72}
\gradbar[thresholds={60,80},threshold colors={lightred,gold,lightgreen}]{72}
\gradbar[label=end]{72}
\gradbar[min=-50,max=50]{-25}
\gradbar[error minus=4,error plus=9]{72}
```


## 样式、缺失值、数字格式、区间与堆叠

```latex
\gradbarsstyle{score}{max=100,theme=teal,rounded=2pt}
\gradbar[style=score]{72}
\gradbar[missing text={N/A}]{NA}
\gradbar[max=200000,number format=grouped,precision=0]{125000}
\gradbar[max=1,number format=scientific,precision=2]{0.00001234}
\gradbar[band={60,80},target=70]{75}
\gradstack[stack colors={skyblue,rose,gold}]{30,25,15}
```

命名样式遵循 TeX 分组，并允许单条覆盖。`missing text` 设置缺失标签；数字格式只影响标签，不改变条长。
区间背景使用原始数据单位，端点必须位于量程内。

堆叠条使用非负的原始分段数据，上限默认 100。例如 `{30,25,15}` 占默认轨道的 70%，总量标签为 `70.0`。
它不会自动归一化为满条，也不接受缺失段或负数段。完整校验规则与参数组合见[接口说明](docs/api.md)。

## 与相关宏包的区别

这些工具的能力存在重合。下面比较的是主要使用方式，不表示其他宏包无法实现相同效果。

| 宏包 | 主要用途 | gradbars 的侧重点 |
| --- | --- | --- |
| [progressbar](https://ctan.org/pkg/progressbar) | 将 0–1 的比例显示为可定制条形 | 接收原始数值，提供明确范围、格式化标签和参考标记 |
| [bchart](https://ctan.org/pkg/bchart) | 在图表环境中绘制简洁的水平条形图 | 将独立数据条直接放入现有表格或正文 |
| [sparklines](https://ctan.org/pkg/sparklines) | 紧凑、可融入文字的微型图形 | 专注单元格内的数值条、组成及参考标记 |
| [databar / datatool](https://dickimaw-books.com/latex/admin/html/databar.shtml) | 从数据库数据生成条形图 | 接收现有表格中的数值，不提供数据库或 CSV 读取层 |
| [pgfplots](https://ctan.org/pkg/pgfplots) | 包含坐标轴、条形、堆叠和误差线的通用绘图系统 | 为单元格中的紧凑数据条提供集中配置的接口；完整图表可使用 pgfplots |

如果只需要简单进度条，`progressbar` 可能已经足够；如果需要完整坐标轴和多种统计图，可考虑 `pgfplots`。
当表格是主要呈现形式、各单元格需要使用相同配置的数据条时，gradbars 是一种可选方案。

## 一本手册，效果与源码对照

优先阅读 [16 页图文宏包手册](gradbars-manual-v0.0.1.pdf)：28 个编号示例、
三个完整应用案例、目录、参数速查与使用限制均集中在一个文档中。
短示例采用左右对照，完整表格采用“上侧效果、下侧源码”；效果与高亮源码
由同一段代码生成。[手册源码](docs/gradbars-manual.tex) 可继续编辑。

安装包含 ctex 和 Fandol 字体的中文 TeX 支持后，在仓库根目录用 XeLaTeX 编译两次，以生成完整目录：

~~~sh
xelatex -interaction=nonstopmode -halt-on-error "-jobname=gradbars-manual-v0.0.1" docs/gradbars-manual.tex
xelatex -interaction=nonstopmode -halt-on-error "-jobname=gradbars-manual-v0.0.1" docs/gradbars-manual.tex
~~~

示例数据均为演示数据，不代表真实实验结论。

完整示例与源码均收录在手册中。编译后的 `gradbars-manual-v0.0.1.pdf` 直接保存在仓库根目录。GitHub Actions 会在推送和拉取请求时编译手册。

## 当前范围与限制

- 当前支持的使用流程是 XeLaTeX；宏包依赖 TikZ、`xparse` 和 `expl3`。
- 比较列的范围需要明确设置，暂不提供 CSV 导入或自动列最大值。
- 堆叠条要求 `min=0` 且各段非负，不支持误差线和条件配色；正负数据可使用 `\gradbar`。
- 图例和堆叠段标签需要自行编排。
- 长标签可能需要增大槽宽；内部标签不会自动调整文字与背景的对比度。
- 尚未生成图表专用的无障碍 PDF 语义标签。

## 许可证与反馈

代码采用 [MIT 许可证](LICENSE)。欢迎提交问题和改进建议；报告问题时请附上最小可复现示例、TeX 发行版和编译日志。
