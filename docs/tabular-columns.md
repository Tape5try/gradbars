# Numeric columns in ordinary tables

The existing `\gradbarscolumn` collects numeric cells in `tabular` and
`longtable`. Version 1.1.0 adds a compact starred form and `\gradbarshead`.
Default package loading already includes their `csv` library; no CSV file is
needed. With minimal loading, use `\usegradbarslibrary{csv}` in the preamble.
The package loads array/collcell itself.

```latex
\usepackage{gradbars,booktabs}
\gradbarscolumn*{G}{min=0,max=1,width=8mm,precision=3,
  theme=gray,height=3ex,font=\scriptsize}

\begin{tabular}{lGG}
\toprule
Method & \gradbarshead{Precision} & \gradbarshead{Recall}\\
\midrule
Alpha & 1.000 & 0.968\\
Beta  &       & 0.750\\
Zero  & 0     & NA\\
\bottomrule
\end{tabular}
```

The starred form supplies `baseline=text,label=inside,label align=cell`, then
applies your options, so later explicit keys take priority. It centers numeric
labels across the whole graphic rather than the filled portion. Other graphic
settings, such as range, precision, font, height, units, named styles and colors,
retain their usual meanings. Width is the graphic width; ordinary table headers,
column separation and outside labels can make the complete column wider.

A literal empty/whitespace-only cell remains blank and reserves the configured
graphic width. It does not emit a missing-value Figure description. `NA` still
renders an explicit missing observation, and zero remains a real numeric value.
Whitespace is not a numeric zero. Do not put full drawing commands or arbitrary
text in numeric cells; invalid numeric input is still an error.

`\gradbarshead{text}` expands to `\multicolumn{1}{c}{text}`. It bypasses numeric
collection and centers one text heading. For grouped headings, use standard
`\multicolumn{2}{c}{Group}` and booktabs rules. Braces alone do not bypass
conversion in ordinary tabular; that convention belongs to tabularray.

Choose an unused single ASCII letter as the column name. The starred form rejects
reserved/existing array column types rather than replacing them. Definitions
follow TeX grouping, just like array column declarations. Define separate letters
for different column options. No G/H names are installed automatically, and
tabularray's independently registered column types remain available.

The unstarred `\gradbarscolumn{G}{options}` retains its earlier behavior:
ordinary graphic defaults apply, and empty input is rendered as missing. It
continues to follow array's existing redefinition behavior. Existing documents
need no changes. The new form does not infer scales, rank values or aggregate
columns; use native gradtable for those data operations. It does not add full
table structure tagging. Use text-only repeated headers in longtable.

See the [complete Precision/Recall example](examples/precision-recall.tex).
Its table data are adapted from [Sebastiano's example](https://tex.stackexchange.com/a/767118)
under CC BY-SA 4.0, with attribution in the source. The column collector uses the
public [collcell interface](https://ctan.org/pkg/collcell), which does not support
verbatim cell material.
