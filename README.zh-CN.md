# gradbars

**一行命令，为 LaTeX 表格添加数据条。**

适合论文中的模型对比、数据集统计和报告中的进度展示。支持正文内嵌、
七种主题与九种内置颜色、统一列范围和明确的数值语义。

[English](README.md) · [图文宏包手册 PDF](gradbars-manual-v0.0.1.pdf) · [完整参数说明](docs/api.md)

![模型对比表格](docs/images/model-comparison.png)

## 快速开始

将 `gradbars.sty` 放在主 `.tex` 文件旁边即可。使用 XeLaTeX 编译，需要带 TikZ 的较新 TeX
发行版，无需 Python、shell escape 或中文宏包。
在 Overleaf 中上传宏包和示例，将相应 `.tex` 设为主文档即可使用。
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

中文文档可自行选择 `ctexart` 或加载 `ctex`，宏包本身不再强制加载中文支持。

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
- **超出最大值**：默认警告并截断条长，保留真实标签；`overflow=error` 改为报错。
- **正负双向条**：通过负的 `min` 启用；默认范围不接受负数。最大值必须为正。
- **双向条标签**：不使用计算占比模式；百分数变化可用 `unit` 添加单位。
- **小数位数**：`precision=0` 至 `6`；默认保留一位小数。
- **标签对齐**：默认在轨道外右对齐，固定槽宽；较长单位可增大 `label width`。

## 七种主题与九种内置颜色

![主题与标签位置](docs/images/theme-gallery.png)

| 参数 | 样式 |
| --- | --- |
| `theme=blue` | 蓝色渐变，默认 |
| `theme=teal` | 青绿渐变 |
| `theme=solid` | 蓝色纯色 |
| `theme=gray` | 灰度 |

`label=outside`、`label=inside`、`label=none` 控制标签位置。
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


## 三个完整示例

优先阅读 [13 页图文宏包手册](gradbars-manual-v0.0.1.pdf)：22 个编号示例、
三个完整应用案例、目录、参数速查与使用限制均集中在一个文档中。
短示例采用左右对照，完整表格采用“上侧效果、下侧源码”；效果与高亮源码
由同一段代码生成。[手册源码](docs/gradbars-manual.tex) 可继续编辑。

安装包含 ctex 和 Fandol 字体的中文 TeX 支持后，在仓库根目录用 XeLaTeX 编译两次，以生成完整目录：

~~~sh
xelatex -interaction=nonstopmode -halt-on-error -jobname=gradbars-manual-v0.0.1 docs/gradbars-manual.tex
xelatex -interaction=nonstopmode -halt-on-error -jobname=gradbars-manual-v0.0.1 docs/gradbars-manual.tex
~~~

示例数据均为演示数据，不代表真实实验结论。

完整示例与源码均收录在手册中。编译后的 `gradbars-manual-v0.0.1.pdf` 直接保存在仓库根目录。GitHub Actions 会在推送和拉取请求时编译手册。

本版支持正负数据条、目标线和误差区间，暂不提供自动列范围、CSV 导入、堆叠条或图表语义的无障碍 PDF 标记。

代码采用 [MIT 许可证](LICENSE)。
