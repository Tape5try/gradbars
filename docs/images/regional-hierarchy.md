# v1.3.0 / v1.4.0 rendered examples / 效果图

The [regional preview](regional-reference-v1.3.0.png) and
[hierarchical preview](hierarchical-trends-v1.4.0.png) come from actual English
[regional input](../examples/regional-input.tex) and
[project review](../examples/hierarchical-teams.tex) TeX sources. Illustrative data
and matching Chinese sources are documented in the [example index](../examples/README.md).

Rebuild from the repository root with all matching `sty/` modules:

```sh
mkdir -p build/v140/examples
TEXINPUTS="$PWD/sty:" pdflatex -halt-on-error -interaction=nonstopmode \
 -output-directory=build/v140/examples docs/examples/regional-input.tex
TEXINPUTS="$PWD/sty:" pdflatex -halt-on-error -interaction=nonstopmode \
 -output-directory=build/v140/examples docs/examples/hierarchical-teams.tex
pdftoppm -scale-to 1600 -png -singlefile build/v140/examples/regional-input.pdf \
 build/v140/regional-en
pdftoppm -scale-to 1600 -png -singlefile build/v140/examples/hierarchical-teams.pdf \
 build/v140/hierarchical-en
```

The committed previews remove surrounding white margins and add a 16-pixel white
border. Use the full page renders above to inspect the complete layout; no plot
values or annotations are edited in the images. The reference band is fixed,
not a computed confidence interval. Endpoint NA never falls back to interior data.

效果图由真实 TeX 编译生成，仅裁去白边并增加 16 像素白边框；不编辑图形数值或标签。
地区输入先归一化再汇总，参考带不混入观测；同名子组以父级路径区分。
