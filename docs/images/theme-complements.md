# Signed theme gallery / 正负同轨主题展示

The PNG is rendered from the actual built-in `\gradsignedbar` example using
illustrative values -24 and 24, a common -50 to 50 scale and error distance 8.
All eleven themes share the same geometry. No custom clipping macro is used.

PNG 来自内置命令的实际编译结果：全部 11 个主题共用相同的数据、量程和尺寸，
不使用外部自定义裁剪宏。源码和图像均采用 MIT 许可证。

From the repository root / 在仓库根目录运行：

```sh
mkdir -p build/theme-complements/pdflatex
TEXINPUTS=./sty//: pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=build/theme-complements/pdflatex docs/examples/theme-complements.tex
pdftoppm -r 150 -x 110 -y 175 -W 850 -H 535 -png -singlefile \
  build/theme-complements/pdflatex/theme-complements.pdf \
  docs/images/theme-complements-v1.1.1
```

The crop includes the table and omits surrounding prose. If fonts or page geometry
change, inspect the result and adjust the crop accordingly.
裁剪保留完整表格；修改字体或页面尺寸后需重新核对裁剪范围。
