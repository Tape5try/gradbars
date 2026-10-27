# Service-response legend preview / 服务响应图例预览

`service-response-legend-v1.1.1.png` is rendered from the actual
[service-response example](../examples/service-response-legend.tex), using the
matching runtime modules in `sty/`. No figure data or labels are redrawn.
The same image appears in both repository READMEs.

该图片由独立示例实际编译生成，使用演示数据；仅裁去页面空白。
中英文 README 共用同一张图。修改示例后，从仓库根目录重建：

```sh
mkdir -p build/readme-service-legend
TEXINPUTS=./sty//: xelatex -interaction=nonstopmode -halt-on-error \
  -output-directory=build/readme-service-legend \
  docs/examples/service-response-legend.tex
pdfcrop --margins 6 \
  build/readme-service-legend/service-response-legend.pdf \
  build/readme-service-legend/service-response-cropped.pdf
pdftoppm -r 160 -singlefile -png \
  build/readme-service-legend/service-response-cropped.pdf \
  docs/images/service-response-legend-v1.1.1
```

Requires XeLaTeX, ctex, pdfcrop/Ghostscript and Poppler. The resulting PDF and
intermediate files remain under ignored `build/`; the PNG is tracked for GitHub
rendering. Publishing the source and preview does not create a GitHub Release.
