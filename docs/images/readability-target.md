# v1.2.0 readability preview

The [PNG](readability-target-v1.2.0.png) is rendered from the English
[executable example](../examples/readability-target.tex), using illustrative data.
It demonstrates measured legends, label-area contrast panels, explicit spark
references and the readable native-table preset. No CPU timing example is used.
The [Chinese source](../examples/readability-target-cn.tex) is also executable.

Rebuild from the repository root with the complete local `sty/` modules:

```sh
mkdir -p build/v120/example-en
TEXINPUTS="$PWD/sty:" pdflatex -halt-on-error -interaction=nonstopmode \
  -output-directory=build/v120/example-en docs/examples/readability-target.tex
pdfcrop --margins 8 build/v120/example-en/readability-target.pdf \
  build/v120/readability-target-crop.pdf
pdftoppm -scale-to 1400 -png -singlefile build/v120/readability-target-crop.pdf \
  docs/images/readability-target-v1.2.0
```

此图由实际 TeX 编译生成；虚线是显式目标参考，不混入观测。标签白底表示原覆盖区域的
黑／白文字对比度界不足时采用的回退，不表示原渐变已达标。中文源码用 XeLaTeX 或 LuaLaTeX。
