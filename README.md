# gradbars

**Compact data graphics inside ordinary LaTeX tables.**

**v0.0.3 · XeLaTeX · MIT**

[中文说明](README.zh-CN.md) · [Illustrated manual source](docs/gradbars-manual.tex) · [API reference](docs/api.md) · [Release notes](docs/releases/v0.0.3.md)

![gradbars: comparisons, signed contributions, trends and quality rules](docs/images/overview-v0.0.3.svg)

Use a consistent scale, keep real numbers visible, and add a small graphic directly
to a table cell. No `tikzpicture` wrapper or shell escape is required.

## New in v0.0.3

- **Dumbbell comparisons:** hollow reference points, filled current points, optional current-minus-reference labels.
- **Signed stacks:** accumulate positive and negative contributions independently; show the net or both subtotals.
- **Sparklines:** equally spaced observations, gaps for missing values, extrema and last-point markers, automatic or shared fixed ranges.
- **Target and interval quality:** evaluate distance from a goal or acceptable interval without changing data geometry.
- **Semantic palettes:** categorical, sequential, diverging and monochrome schemes; named categories keep their colors and patterns when reordered.
- **One reorganized manual:** 56 numbered output/source examples, six application tables, four real layout cases and an interface index.

Existing bars, lollipops, layered comparisons, floating intervals, error whiskers,
CSV input, numeric table columns and named styles remain available.

## Quick start

Copy `gradbars.sty` next to your main `.tex` file and select **XeLaTeX**.
The package uses TikZ, xparse, expl3 and collcell, available in standard TeX installations.
Chinese fonts are needed only for the Chinese manual, not for the package.

```latex
\documentclass{article}
\usepackage{booktabs,gradbars}
\begin{document}
\gradbarssetup{width=35mm,precision=0}
\begin{tabular}{ll}
\toprule
View & Data \\
\midrule
Single value & \gradbar{72} \\
Current / reference & \graddumbbell{58}{76} \\
Positive / negative & \gradstack[min=-50,stack totals=separate]{60,-20,15,-10} \\
Trend / last value & \gradspark[spark range=fixed,min=0,max=100]{25,45,NA,60,80} \\
\bottomrule
\end{tabular}
\end{document}
```

## Choose a graphic

| Need | Command or option |
| --- | --- |
| One magnitude or signed change | `\gradbar[min=-50,max=100]{value}` |
| Compact stem and endpoint | `\gradbar[shape=lollipop]{value}` |
| Wide reference behind a narrow current bar | `\gradcompare{reference}{current}` |
| Two positions and their difference | `\graddumbbell[compare label=delta]{before}{after}` |
| Known lower and upper endpoints | `\gradrange[range point=50]{35}{75}` |
| Additive contributions | `\gradstack[min=-60]{60,-25,20,-15}` |
| Equally spaced time-series shape | `\gradspark{25,40,NA,60,80}` |
| A point estimate with uncertainty distances | `\gradbar[error minus=5,error plus=8]{60}` |

## Preserve data meaning

- Bars share explicit `min`, `max` and `width`. Zero stays at zero; negative values require a negative minimum.
- `unit` appends text. `value format=percent` computes value/max only for nonnegative ranges. Formatting never changes geometry.
- Empty input or `NA` denotes missing data. A missing spark observation breaks the line and retains its horizontal position.
- Signed stacks accumulate from zero independently on each side. The default total is the algebraic sum; `stack totals=separate` shows positive / negative subtotals.
- Stack segment percentages use `abs(segment) / sum(abs(segments))`. They are shares of absolute activity, not of the net balance. Stacks do not automatically normalize to full width.
- Auto-scaled sparklines compare shapes. Use `spark range=fixed` with the same `min`, `max`, `width` and `height` to compare levels across rows.
- Overflow warns and clips the drawing while retaining raw labels; use `overflow=error` for strict checking.

## Express quality separately

```latex
% Within 5 of the goal is good; within 15 is intermediate.
\gradbar[better=target,quality target=50,
  thresholds={5,15},target=50,palette=diverging]{52}

% Inside [40,60] is good; no more than 10 away is intermediate.
\gradbar[better=interval,quality range={40,60},
  thresholds={0,10},band={40,60},palette=diverging]{68}
```

`threshold colors` always lists bad, intermediate, good. In target/interval modes,
thresholds are nonnegative distances with inclusive upper boundaries.
`quality target` / `quality range` evaluate data; `target` / `band` draw references.
`better=higher|lower` remains available for monotonic metrics.

## Reuse appearance and category identity

```latex
\gradbarsstyle{paperrow}{preset=paper,width=40mm,max=100,precision=1}
\gradbar[style=paperrow]{82.5}

\gradbarscategory{Compute}{gradbarsBlue}{diagonal}
\gradbarscategory{Storage}{gradbarsOrange}{dots}
\gradstack[stack names={Compute,Storage}]{60,30}
\gradstack[stack names={Storage,Compute}]{30,60}
\gradbarslegend{Compute,Storage}
```

Four layout presets: `paper`, `report`, `presentation`, `outline`.
Four group palettes: `categorical`, `sequential`, `diverging`, `mono`.
Seven themes and nine original solid colors remain available.
Unregistered categories use cyclic position-based palettes; registered names preserve
their assigned color and pattern. In print/mono mode category colors use the grayscale
palette, while registered patterns remain. Legends use the same mapping as segments.

## CSV and existing tables

```latex
\gradbarsloadcsv{results}{results.csv}
\gradbarscsvstyle{shared}{results}{Score}
\gradbarcsv[style=shared]{results}{1}{Score}
\gradbarscolumn{G}{style=shared}
```

CSV fields are read as character data, not executed as TeX. Named columns, quoted commas,
custom missing tokens and shared column ranges are supported. See the manual for complete tables.

## Documentation and building

The [single Chinese manual](docs/gradbars-manual.tex) is organized into quick start,
graphic selection, data interfaces, appearance, complete layouts, and reference.
It contains 56 numbered examples, including before/after evaluation, a monochrome
contribution ledger and a monthly trend summary. All example data are illustrative.

To generate the versioned PDF in the repository root:

```sh
python scripts/build_manual.py
```

The script uses XeLaTeX to rebuild the four layout previews and then the manual twice.
It requires ctex/Fandol and the LaTeX extra packages; Python is only a documentation-build helper.
The editable manual is the current v0.0.3 reference; an older PDF is not a substitute for it.

## Scope and limits

- XeLaTeX is the supported engine. This is a table-oriented interface, not a full plotting system.
- CSV accepts single-line comma-separated fields; automatic CSV tables do not paginate.
- Stacks reject missing segments, conditional thresholds and error whiskers.
- Sparklines use equally spaced observations; they do not parse dates or draw bar targets, error whiskers or reference bands.
- Fixed scales require `min <= 0` and `max > 0`; auto spark ranges can be positive, negative or constant.
- Label avoidance is local to a graphic. Allow room for long external labels and legends.
- Accessible tagged chart descriptions and tabularray-specific column handling are not implemented.

MIT licensed. Bug reports should include a minimal `.tex` example, engine and log.
