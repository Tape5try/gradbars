# v1.2.1 metric preview / 指标效果图重建

Both images render actual TeX output with fictitious review data; only page
margins are cropped. No numerical labels or drawing positions are edited.
图片来自实际编译，只裁去页面边缘；没有改动数值、标签或绘图位置。

Run from the repository root with TeX Live and Poppler:

```sh
mkdir -p build/previews
TEXINPUTS="$PWD/sty:" pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/previews docs/examples/report-metrics.tex
TEXINPUTS="$PWD/sty:" xelatex -interaction=nonstopmode -halt-on-error -output-directory=build/previews docs/examples/report-metrics-cn.tex
pdftoppm -scale-to 1300 -x 60 -y 55 -W 880 -H 730 -singlefile -png build/previews/report-metrics.pdf docs/images/report-metrics-v1.2.1
pdftoppm -scale-to 1300 -x 60 -y 55 -W 880 -H 730 -singlefile -png build/previews/report-metrics-cn.pdf docs/images/report-metrics-v1.2.1-cn
```

Sources: [English](../examples/report-metrics.tex), [中文](../examples/report-metrics-cn.tex),
[data](../data/report-metrics.csv). First table: raw Review top two, visible mean
60.0 pt. Second: first two Followup rows displayed, all valid Followup data mean
50.0 pt. Histories retain NA positions; the last position is current.
