# API reference

## Commands and scope

```latex
\usepackage{gradbars}
\gradbarssetup{key=value,...}
\gradbar[key=value,...]{number}
```

Settings follow ordinary TeX grouping. A setup in the preamble applies to the
document; a setup inside a group is local. Per-bar overrides never leak.
Keys apply left to right: put `theme` before individual color overrides.

Numbers may be decimal or e/E scientific literals, or macros expanding to them; signed bars need an appropriate range.
Examples: `0`, `.5`, `+12`, `125000`, `86.50`, `1.2e-3`, `-2.5E4`. Expressions,
commas and units inside numbers are not accepted. Empty input and uppercase `NA`
are missing values for `\gradbar`; all other nonnumeric input is an error.
Use decimal points and put units in `unit`. Floating point arithmetic has finite
precision. TeX's dimension resolution limits the smallest drawable bar.

## Keys

| Key | Default | Meaning |
| --- | --- | --- |
| `min` | `0` | Decimal scale minimum, strictly below max |
| `max` | `100` | Decimal scale maximum, strictly above min |
| `width` | `24mm` | Positive track width; excludes outside label |
| `height` | `1.5ex` | Positive track height |
| `theme` | `blue` | `blue`, `teal`, `solid`, `gray`, `lbyellow`, `viblue`, `cyblu`, `violet`, `orange`, `forest` |
| `label` | `outside` | `outside`, `left`, `inside`, `none`, `end`, `auto` |
| `label width` | `4.5em` | Minimum right-aligned outside label slot with automatic overflow handling |
| `label gap` | `.6em` | Gap between track and outside label |
| `baseline` | `auto` | `auto`, `text`, `center` or `bottom` baseline preset |
| `baseline shift` | `0pt` | Additional vertical baseline shift |
| `precision` | `1` | Integer from `0` to `6`; trailing zeros shown |
| `value format` | `value` | `value` or `percent` |
| `unit` | empty | Suffix for raw values, e.g. `{\%}` or `{\,ms}` |
| `text` | empty | Custom label; empty restores automatic formatting |
| `overflow` | `clip` | `clip` with warning, or `error` |
| `color` | unset | Set a solid fill using an xcolor color name |
| `fill` | set by theme | `gradient` or `solid` |
| `left color` | set by theme | Gradient start, or entire solid fill |
| `right color` | set by theme | Gradient end; ignored for solid fill |
| `track color` | set by theme | Empty track color |
| `text color` | set by theme | Label color, or `auto` to select black/white |
| `rounded` | `0pt` | Nonnegative corner radius; clamped to fit each bar |
| `target` | empty | Reference value within the scale; empty disables |
| `target color` | `gradbarsInk` | Target line color |
| `negative color` | `lightred` | Solid fill for negative values |
| `negative fill` | `solid` | `solid` or `gradient` for negative bars |
| `negative left color` | empty | Left endpoint of a negative gradient; setting it enables gradient fill |
| `negative right color` | empty | Right endpoint of a negative gradient; setting it enables gradient fill |
| `thresholds` | empty | Two strictly increasing cutoffs; empty disables |
| `threshold colors` | `lightred,gold,lightgreen` | Three ordered solid colors |
| `error` | empty | Set both error magnitudes; empty clears both |
| `error minus` | empty | Nonnegative lower error magnitude |
| `error plus` | empty | Nonnegative upper error magnitude |
| `error color` | `gradbarsInk` | Error whisker color |
| `font` | inherited | Label declarations, e.g. `{\small\bfseries}` |

Lengths use LaTeX units such as `mm`, `pt`, `em`, and `ex`. Supply nonnegative
label spacing and enough label width for the content. An outside bar occupies
approximately `width + label gap + max(label width, actual text width)` by default.
Inside labels align near the track's right edge, regardless of the filled
fraction. Oversized labels move outside by default; use `text color=auto` for
automatic contrast. Font size is never reduced automatically.

## Themes

Three additional gradient themes are included in v0.0.5:

| Theme | Gradient endpoints | Track | Label color |
| --- | --- | --- | --- |
| `violet` | `#7C3AED` to `#C4B5FD` | violet at 6% over white | gradbarsInk |
| `orange` | `#EA580C` to `#FDBA74` | warm orange at 6% over white | gradbarsInk |
| `forest` | `#166534` to `#86EFAC` | forest green at 6% over white | gradbarsInk |

```latex
\gradbar[theme=violet]{72}
\gradbar[theme=orange]{72}
\gradbar[theme=forest]{72}
```

Themes set fill, gradient endpoints, track and text colors; later explicit keys
override these settings. They use the existing numeric scales and sign rules.
Negative bars retain `negative color`, thresholds retain priority, and `print`
applied after the theme selects monochrome settings. Themes do not select a
heat palette or stack category palette.

## Geometry and labels

The scale satisfies `min < max`. The zero baseline is at
`width * (clamp(0,min,max)-min)/(max-min)`. The value endpoint is at
`width * (clamp(value,min,max)-min)/(max-min)`. Filling extends between these
positions, so equal absolute positive and negative values have equal lengths
under one shared range. A true zero has no colored area.

Rounded corners never extend the bar length; their radius is clamped to half
the height and half the actual fill length. Very short bars are not inflated.

`value format=value` prints the original value and suffix. `percent` computes
`100*value/max` only when `min=0`. Cross-zero scales reject computed percent
labels because their interpretation would be ambiguous. Use `unit` for
percentage-point changes. `text` overrides the complete label.

`label=end` places the label above the value endpoint, nudging it inward at the
track edges. It increases height but does not reserve the outside label slot.
An unusually long label wider than the track can still overhang: increase
`width` or use `label=outside`. The track baseline remains stable.

`label=left` reserves the outside slot before the track and right-aligns the
formatted label against the track. It keeps `precision`, `number format`, `unit`,
`text`, `label width` and `label gap` semantics, so a column can apply the option
directly to each cell. The default `label width` is measured in the surrounding
text font before TikZ draws the picture.

The default `baseline=auto` preserves the historical visual baseline. Use
`baseline=text` to align the graphic with the current text label box,
`baseline=center` to place the baseline at the graphic center, or
`baseline=bottom` to place it at the track's lower edge. `baseline shift` applies
an additional vertical shift and is useful for table rows with custom font sizes.

Negative bars use `negative color` as a solid fill by default. Set both gradient
endpoints directly, or select the mode explicitly:

```latex
\gradbar[min=-100,max=100,
  negative fill=gradient,
  negative left color=magenta!25,
  negative right color=magenta]{-60}
```

For a negative bar the left endpoint is the outer, negative side and the right
endpoint is the side nearest zero. Threshold colors and `print` retain priority
over the negative gradient.

## Targets, thresholds and uncertainty

`target` uses data units and must lie inside the scale; out-of-range targets
raise an error even with `overflow=clip`.

Thresholds `{a,b}` select colors for `value<a`, `a<=value<b`, and `value>=b`.
Selection uses the original value, before clipping or display rounding.
Conditional colors use solid fills and take priority over themes and negative
colors, regardless of key ordering. Set `thresholds={}` to disable them.

`error=e` draws a horizontal whisker from `value-e` to `value+e`.
`error minus` and `error plus` support asymmetric, nonnegative magnitudes.
An unspecified side is zero unless it inherits a value from setup.
Use `error={}` to clear both sides. Keys apply left to right.
The package does not calculate uncertainty or confidence intervals.

Values and error endpoints outside the scale warn and clip by default; the
label is unchanged. A clipped whisker cap is not the true interval endpoint.
Prefer `overflow=error` or enlarge the range for scientific interval displays.
Invalid options produce a package error and no bar if compilation continues.

## Usage notes

- Keep scales and sizes identical within a comparison column.
- State the maximum or range when it is not obvious from the table heading.
- Larger values are not inherently better; latency is a counterexample.
- Keep numbers beside bars when exact comparisons matter.
- A `siunitx` numeric `S` column expects numbers. Put bars in ordinary `l`, `c`,
  `r`, or paragraph columns instead.
- TikZ-backed commands are not expandable; avoid PDF bookmarks.
- In an existing `tikzpicture`, bars draw in a local scope at `(0,0)` under the
  surrounding coordinate transformations.
- With document tagging enabled, graphics provide automatic or explicit Figure
  descriptions; `accessibility=artifact|off` retains its documented meaning.
  See [accessibility.md](accessibility.md) for table structure and tested limits.

## Engine and documentation workflows

Package checks pass with pdfLaTeX, XeLaTeX and LuaLaTeX, including UTF-8 BOM CSV input. The Chinese manual uses XeLaTeX/ctex; the English manual builds with pdfLaTeX. GitHub Actions builds both manuals.

## Built-in colors

`lightgreen`, `lightyellow`, `lightblue`, `lightred`, `rose`, `skyblue`,
`gold`, `lavender`, and `peach` are public xcolor names defined by this package.
Use `color=rose` for a solid fill, or use them as gradient endpoints.
Keys apply left to right; a later theme resets its fill and colors.


## Named styles

`\gradbarsstyle{name}{keys}` defines or replaces a named style in the current
TeX scope. `style=name` applies it to `\gradbar`, `\gradstack`, or setup.
Keys apply in order; later keys override the style. Styles can reference other
styles, resolved when used. Unknown names and nesting beyond 32 levels error.

## Missing values

`\gradbar{NA}` and `\gradbar{}` show an empty track and `missing text` (default `--`).
Leading/trailing whitespace is ignored and macros may expand to these tokens.
Missing data is distinct from numeric zero; arbitrary text still errors.
There is no fill, error whisker, unit, or percent suffix. Target and band references
remain visible. `text` overrides the missing label; `label=none` hides it.
All scale and option validation still applies.

## Number formatting

`number format=fixed` (default) prints fixed decimals and thin-space grouping.
`grouped` uses comma thousands separators. `scientific` prints a mantissa and
power of ten without first rounding a tiny input to zero. `precision=0..6` sets
decimal places, or mantissa decimal places for scientific output.
`value format` still chooses original values or computed percentages;
formatting never changes geometry. Scientific e/E input is also accepted.

## Reference bands

`band={lo,hi}` draws a reference background behind the fill, extending 2pt above
and below the track. It is not a computed uncertainty interval. Endpoints must
be strictly increasing and within the scale, including signed scales.
Out-of-range bands error regardless of overflow policy. `band={}` disables it.
`band color=gold` and `band opacity=0.3` are defaults; opacity must be in [0,1].

## Stacked bars

`\gradstack[keys]{a,b,c}` accumulates positives to the right and negatives to the left of zero. Negative segments require an explicit negative `min`. Positive and negative subtotals independently follow the overflow policy. Missing segments and empty lists are errors. Zero segments consume a palette index without visible width.

The default label is the algebraic sum (net). `stack totals=separate` shows positive / negative subtotals. Stacks do not normalize to full width. Segment percentages use `100*abs(segment)/sum(abs(segments))`; positive-only behavior is unchanged. A zero net does not erase nonzero contributions. Total percent formatting still requires `min=0`.

`stack colors={gradbarsBlue,gradbarsTeal,gold}` is the default cyclic palette. Stacks use solid fills or textures; rounded corners apply to the combined visible extent. Target, band, dimensions, number formatting and names are shared with ordinary bars. Stacks reject thresholds and error whiskers. Registered category names override position-based colors except in print mode.

## Stack names, labels and legends (v0.0.2)

| Key | Default | Meaning |
| --- | --- | --- |
| `stack names` | empty | Names in segment order; if supplied, count must match segments |
| `legend` | `false` | Draw a vertical, wrapping legend below the stack; requires names |
| `segment labels` | `none` | `none`, `value`, `percent`, `name`, `name value`, `name percent` |
| `segment font` | `\scriptsize` | Font declaration for segment labels |
| `segment text color` | `auto` | Automatic black/white text or an explicit color |

```latex
\gradstack[width=70mm,height=16pt,precision=0,
  stack names={Train,Validation,Test},
  segment labels=name percent,legend=true]{80,2,18}
\gradbarslegend[stack colors={skyblue,rose,gold}]{Train,Validation,Test}
```

Segment percentages use the **sum of absolute raw segment values**, including clipped portions.
The total's `value format=percent` still uses **max**. For `{20,30}` and `max=200`,
segments display 40% and 60%, the total displays 25%, and the track is quarter filled.
Segment values use the configured precision and number format, without the total's
unit suffix. Zero or fully clipped segments have no segment labels but keep their
palette indices and legend entries. An all-zero stack produces no segment percentages; a zero net with nonzero contributions still has percentages.

Labels that do not fit their visible segment move above the track with leader lines.
Overlapping external label boxes are placed on successive levels. A target crossing
a segment label also moves that label out. External labels can increase picture size.
Automatic legends require a width greater than 14pt and use the ordinary `font`.
Long legend names wrap inside the track width; a single unbreakable word may need a wider width.
Standalone `\gradbarslegend[options]{names}` uses `stack colors` and `width`;
share a named style with the bars to ensure matching colors. Legend names must not be empty.

## Horizontal table-header legends (v1.1.1)

These core commands also work with `libraries=none`; the optional `legend`
library is not required. Both accept ordinary `/gradbars` options.

| Command | Behavior |
|---|---|
| `\gradtablelegend[options]{names}` | One horizontal category row at natural width |
| `\gradtablelegendhead[options]{title}{names}` | Center an ordinary text title above the row, with a 2pt gap |

| `/gradbars` key | Default | Contract |
|---|---|---|
| `table legend` | `true` | Boolean; bare key means true; false hides the category row |
| `legend font` | `\sffamily\scriptsize` | Category-label font |
| `legend swatch size` | `6pt` | Must be positive |
| `legend text gap` | `2pt` | Swatch-to-label gap; must be nonnegative |
| `legend item gap` | `4pt` | Item-to-item gap; must be nonnegative |
| `legend border color` | `black` | Swatch border color |
| `legend border width` | `.4pt` | Must be nonnegative |

Table swatches are filled; the graphic `outline` switch does not turn them into
empty boxes. Set `legend border width=0pt` to remove their frame.

Set these keys in `\gradbarssetup` or per call, with normal TeX grouping and
left-to-right overrides. They are graphic keys, not native table declaration
keys. A true switch never inserts a legend automatically: only an explicit
helper call produces one. With false, `\gradtablelegend` is hidden and
`\gradtablelegendhead` prints only its title without a reserved legend gap.

```latex
\gradtablelegendhead[
  stack colors={gray,teal,blue,orange,red}
]{Response status}{Pending,Fast,Normal,Slow,Timeout}
```

Names reuse `\gradbarscategory` mappings, positional `stack colors` fallback
and print textures. No thresholds or bar colors are inferred. The title helper
works in an ordinary `tabular` heading, a `\gradcolumn` title, or inside
`\gradbarshead{...}` to bypass collected numeric cells. It does not insert
`\multicolumn`. Existing `\gradbarslegend` remains vertical and stack
`legend=true` is independent of `table legend`.

Automatic/explicit `alt`, `accessibility` and the `category-legend` backend path
follow the existing category-legend rules, including explicit native fallback
when required. The ordinary text title remains outside the legend Figure.
See [table legend examples](legends.md#horizontal-table-header-legends) and the
[service-response table](examples/service-response-legend.tex).

## Automatic label layout (v0.0.2)

`label=auto` centers the total in the filled portion when it fits, otherwise puts it
outside. `text color=auto` selects black or white using sRGB luminance at the label
center; for gradients this is an estimate. Put it **after** `theme`, which sets text color.
Outside automatic text is black, assuming a light page. Set explicit colors for dark pages.

`label overflow=auto` (default) moves oversized inside/end labels out, moves overly
tall inside labels out, and expands the outside slot to fit its text. `label overflow=allow`
retains manual overflow for inside/end labels and the configured outside slot width.
An auto label still requires enough width to fit inside even in allow mode.
Targets crossing the label, error whiskers, or enabled stack segment labels force
inside total labels outside. End totals sit above external segment labels.

Collision handling applies within one bar, not across table cells or separate bars.
Outside labels may still exceed a column/page; shorten them or allocate more width.
For consistent numeric alignment set a common `label width` large enough for the
longest label. Contrast at a single point cannot cover a long label spanning several colors.

## Numeric table columns (v0.0.2)

The v1.1.0 starred form `\gradbarscolumn*{G}{options}` selects compact centered
labels and preserves literal empty cells as blank; `NA` is still missing and zero
is numeric. `\gradbarshead{text}` provides a text heading. See
[ordinary-table examples and compatibility](tabular-columns.md).


```latex
\gradbarscolumn{G}{max=100,width=35mm,precision=0}
\begin{tabular}{lG}
Model & \multicolumn{1}{c}{Score}\\
Alpha & 82\\
Pending & NA\\
Empty & \\
Zero & 0\\
\end{tabular}
```

Choose an unused single ASCII letter as the column name. The interface uses array
and collcell; the cells are left aligned and accept the same values as `\gradbar`.
Column options override surrounding setup on each cell and may reference a named style.
Use `\multicolumn{1}{c}{...}` for headers or exceptional nonnumeric cells. Put units
in column options, not the raw input. A literal 0 remains distinct from empty/NA.
Column definitions follow array's scoping; define reusable columns in the preamble.
This does not scan the column, infer maxima, or implement an siunitx S column.
The manual exercises tabular and multi-page longtable, including Beamer tables.
For tabularray, use the separate adapter below; array/collcell columns are not its interface.

## CSV input (included in v0.0.2)

```latex
\gradbarsloadcsv[missing={NA,N/A,null,--}]{results}{results.csv}
\gradbarscsvtable[width=40mm,precision=1]{results}{Model}{Score}
\gradbarscsvstyle{latency}{results}{Latency}
\gradbarcsv[style=latency,unit={\,ms}]{results}{1}{Latency}
\gradbarscsvcell{results}{1}{Model}
```

| Command | Behavior |
| --- | --- |
| `\gradbarsloadcsv[missing={...}]{dataset}{file}` | Read a UTF-8 CSV into the current TeX scope; reloading replaces the dataset locally |
| `\gradbarscsvcell{dataset}{row}{column}` | Print the raw text field, without interpreting TeX commands or mapping missing tokens |
| `\gradbarcsv[bar options]{dataset}{row}{column}` | Read, validate and draw a numeric field; regular bar range defaults apply |
| `\gradbarscsvstyle{style}{dataset}{column}` | Define/replace a named style containing the column's computed `min` and `max` |
| `\gradbarscsvtable[bar options]{dataset}{text column}{numeric column}` | Draw a two-column tabular in file order, using the numeric column's shared range |

Dataset names must start with an ASCII letter and contain only ASCII letters,
digits, `_` or `-`. Column names are exact and case sensitive; row numbers are
positive integer literals, starting at 1 after the header. Unknown datasets,
columns and row numbers are errors. Data and computed styles obey TeX grouping.
Reload data and recompute styles after editing the file, normally on recompilation.

The reader accepts comma-separated fields, quoted commas, doubled quotes inside
quoted fields, optional initial UTF-8 BOM, and blank lines. Leading/trailing field
whitespace is trimmed, including within quoted fields. The first nonblank line is
the header; names must be nonempty and unique, and all data rows must match its width.
Unclosed quotes, quotes inside unquoted fields, and text following a closing quote
are errors. Multiline fields and alternate separators are not supported. This is
a deliberately bounded CSV reader, not a full spreadsheet/database interpreter.
The file is read as character data; its backslashes, percent signs and other TeX
syntax do not execute. Do not use CSV cells to inject formatting commands.

Empty numeric fields always mean missing. Default missing tokens are `NA`, `N/A`,
and `null`, case sensitive; the `missing` option **replaces** that list.
Only numeric operations apply the mapping. Valid numbers follow `\gradbar`'s decimal/scientific
literal rules; arbitrary text, formulas and units inside numeric fields error.
Zero remains an observation. CSV input does not change `\gradbar`'s own missing tokens.

Auto ranges use `min(0, smallest valid value)` and `max(0, largest valid value)`;
if the computed maximum is zero, it becomes 1. Missing fields are ignored.
Thus all-zero/all-missing/header-only columns use [0,1], and all-negative columns
use [minimum,1]. This keeps the upper limit positive as required by the bar API.
Ranges cover the whole column, even if only some rows are subsequently displayed.
Explicit table options are applied after the computed range and can override it.
Fix ranges explicitly when comparing different files or runs.

The legacy `\gradbarscsvtable` does not paginate or sort. For multicolumn visual
tables and pagination, use the v0.0.5 native data interface below.

## v0.0.5: native data, column scales and heat cells

```latex
\gradbarsloadcsv{results}{docs/data/results.csv}
\begin{gradtable}[data=results,width=\linewidth,scale=column]
  \gradcolumn[source=Model]{method}{Method}
  \gradcolumn[type=bar,source=Score,mark=both]{score}{Score}
  \gradcolumn[type=heat,source=Latency,include zero=false,
    options={better=lower,precision=0}]{time}{Latency}
\end{gradtable}
```

| Key / command | Default | Behavior |
| --- | --- | --- |
| Table `data=dataset` | empty | Generate rows from an already loaded CSV, in file order |
| Column `source=header` | column id | Exact, case-sensitive CSV header; columns may be reordered or reused |
| Table / column `scale=fixed\|column` | fixed; columns inherit | Keep configured ranges, or compute one range for all rows of each numeric column |
| Table / column `include zero=true\|false` | true; columns inherit | Include zero when computing a column range |
| Column `type=heat` | — | A filled rectangle with the formatted value inside; uses the column's content width |
| `\gradheat[options]{value}` | range [0,100], height 3ex | Standalone heat cell, also usable in ordinary tables and TikZ pictures |
| `heat low color` | `gradbarsBlueLight!15` | Low endpoint color |
| `heat high color` | `gradbarsBlue` | High endpoint color |
| `heat text color` | auto | Select black/white by contrast, or use an explicit color |
| `heat missing color` | `gradbarsTrack` | Neutral fill for missing values |

With `data`, declare columns and optional spanning headers; omit `\gradrow` and
`\gradgroup`. Manual data rows cannot be mixed with an imported dataset. Use
`long=true` for pagination, with the same rules, headers, widths, ranks and scales
as a manually populated `gradtable`. Unknown datasets or sources are errors even
when the CSV contains only a header. Text fields remain literal character data;
empty text cells are retained. Numeric missing tokens use the dataset's mapping.
Compound cells use the same pair/interval/list syntax as manual cells; quote CSV
lists containing commas. Missing-token mapping applies to the whole field;
within a compound field use `NA` for a missing observation or endpoint.

`scale=column` applies to manual and imported tables. Missing observations are
ignored; zero is retained. Scalars use their extrema; compare/dumbbell/interval
columns use all supplied endpoints and point estimates; spark columns use every
observation and automatically select `spark range=fixed`; stack columns use each
row's positive and negative cumulative totals, including their zero baselines.
Text columns ignore the scale setting. Computed ranges override `options={min=...,
max=...}`. Select `scale=fixed` on an individual column to preserve explicit ranges.
Targets, reference lines and error magnitudes are not observations used to compute
the range; use fixed ranges when those annotations need additional space.

All-missing and header-only columns use [0,1]. All-zero columns with zero included
also use [0,1]. Without zero, a constant column uses [value-0.5,value+0.5]. Other
ranges are exact, without rounding or padding. For example, {70,90} produces
[0,90] by default and [70,90] without zero; {-30,-10} produces [-30,0] by default
and [-30,-10] without zero. These rules apply to the entire table before measuring
labels or pagination. Fix ranges when comparing tables from different datasets.

v0.0.5 drawing ranges accept any decimal `min < max`, including positive-only and
negative-only ranges. For bars the zero baseline is clipped to the nearest border
when zero lies outside the range, so bar lengths then describe distance from that
border. Use `include zero=true` when lengths must express magnitudes relative to
zero. Percent labels still require min=0 and max>0. Legacy CSV range helpers retain
their existing zero-inclusive rules described above.

Heat interpolates the endpoint colors continuously over min/max; `better=lower`
reverses the interpolation. Missing is a separate neutral fill, not the zero color.
`mark=best|both`, precision, unit, number format, custom text, rounded corners,
overflow policy, `label=none`, named styles and explicit alternative text work.
Heat is a scalar color encoding: bar targets, error whiskers, patterns and threshold
bins are not drawn. `print`/`palette=mono` use a grayscale heat scale. The colored
rectangle covers content width, leaving normal intercolumn spacing intact.

In the GitHub checkout, run `texlua scripts/check.lua` for the three-engine regression suite, including
range assertions, special CSV characters, missing/constant data, shared spark
ranges, signed stacks, schema reuse, paginated CSV tables and expected errors.
The CTAN source archive omits `tests/`; these development checks require the checkout.

## v0.0.6 summaries, shared scales and table presentation

```latex
\gradscale{accuracy}{min=0,max=100}
\begin{gradtable}[style=academic,theme=violet,width=\linewidth]
  \gradcolumn{name}{Method}
  \gradcolumn[type=bar,scale group=accuracy,aggregate=mean]{score}{Score}
  \gradcolumn[type=number,aggregate=sum]{time}{Time}
  \gradrow{A,72,20}
  \gradrow{B,90,30}
  \gradrow{Missing,NA,0}
  \gradsummary{Summary}
\end{gradtable}
```

### Summary rows

Declare `aggregate=none|count|sum|mean|min|max` on scalar numeric columns
(`number`, `bar`, `bullet`, `heat`), then use `\gradsummary[scope=visible|data]{label}`
inside the table. One summary row is supported. The label goes in the first text
column; use an empty label for an all-numeric table. Columns with aggregate=none
have empty summary cells. Text and compound graphic columns cannot be aggregated.

Visible is the default: aggregate after CSV filtering, sorting and limit. Data uses
all imported rows; for manual tables both scopes use all data rows. Missing values
are skipped and zero is retained. Count counts valid numeric observations. For
empty/all-missing input count and sum are zero; mean, min and max are missing.

The summary is rendered as formatted numbers, including in graphic columns, so
sums outside the graph range are not clipped. It does not participate in ranges,
ranking or source-row counts. Number columns retain their alignment, bar/bullet
summaries align right and heat summaries center. Precision and units are inherited;
count is an integer with no unit or computed-percent formatting. Summary labels
wrap in allocated text columns. Labels and values are measured before allocation.
Long tables display the summary once, keeping it with the last data row.

Table keys `summary color=auto|<color>` and `summary font={...}` control its
appearance. An empty summary color disables fill; auto follows the table theme,
or uses no fill without a theme. Default summary font is bold text and math.

### Shared named scales

`\gradscale{name}{min=<decimal>,max=<decimal>}` declares both limits and requires
min<max. Definitions obey TeX grouping; redefining a name replaces it locally.
`scale group=name` is available for standalone graphics and table/column options.
The table setting is inherited by columns; `scale group={}` on a column clears it.
Unknown names are errors. Groups are explicit and do not depend on table order.

A group overrides min/max in drawing options regardless of key order. Referencing
a group in an ordinary spark selects its fixed range; win-loss retains its sign
categories. Named groups require scale=fixed in table columns; scale=column is a
conflict rather than silently recomputing the group. Cross-table automatic range
collection is not implemented. Global graphic scale-group settings do not
implicitly bind table columns; use the table key or column drawing options.

### Automatic range padding and nice bounds

Table/column keys `scale padding=<nonnegative decimal>` and `scale nice=true|false`
apply to scale=column only. Padding is a percentage of the already zero-adjusted
span, at each nonzero endpoint; endpoints at zero remain anchored. Defaults are
0 and false. Column settings override table defaults. Fixed/group scales are not
expanded. Operation order is data extrema, zero inclusion/constant fallback,
padding, then outward rounding to a 1/2/5 power-of-ten step targeting five intervals.

For example, {63,87} with zero included gives [0,87]; 10% padding gives [0,95.7];
nice=true then gives [0,100]. With {70,90} and zero excluded, 10% padding gives
[68,92]. Missing/empty input retains the existing [0,1] starting range.

Raw values, rankings and aggregates do not change. When adjustment is enabled,
computed-percent labels retain the unexpanded upper bound as their denominator.
Drawing key `percent base=<positive decimal>` explicitly overrides the denominator;
without an override or adjustment it remains max, preserving existing behavior.
Graphic percent formatting still requires min=0. Thus padding does not turn the
old maximum's 100% label into a smaller percentage. Alternative text states the
denominator when percent formatting is active. Heat centers must still lie within
the resolved display range; padding does not invent target or error bounds.

### Built-in table styles and themes

| Table style | Settings and intended use |
| --- | --- |
| `style=academic` | Paper preset, booktabs rules, centered headings, 1.2 row stretch and 6pt spacing |
| `style=compact` | Paper preset, small text, 1.05 row stretch, 4pt spacing and smaller natural column widths |
| `style=dashboard` | Report preset, row rules, 1.5 row stretch, 8pt spacing, 2pt row padding and blue theme |

Table `theme=none|blue|teal|violet|orange|forest|mono` is independent of layout
style; none is the default. It sets graph fills and sequential heat endpoints.
Auto header/summary fills follow the selected hue; explicit colors or empty fills
override them. Column drawing options override the table's drawing colors, so a
column may use a different theme or a diverging heat palette. Mono applies print.
`font={...}` controls table text; graphic fonts can be set through column options.
Styles use the existing named style registry and may be redefined with
`\gradtablestyle`. Put a style before explicit overrides, for example
`style=dashboard,theme=forest,rules=booktabs`. Existing preset=paper|report|mono
remains supported. No statistical or scale defaults are changed by these styles.

## CSV sorting and filtering (v0.0.5)

```latex
\gradbarsloadcsv{results}{docs/data/results.csv}
\begin{gradtable}[data=results,width=\linewidth,scale=column,
  sort=score,order=descending,filter={score>=75},limit=2]
  \gradcolumn[source=Model]{method}{Method}
  \gradcolumn[type=bar,source=Score]{score}{Score}
  \gradcolumn[type=number,source=Latency]{time}{Latency}
\end{gradtable}
```

| Table key | Default | Meaning |
| --- | --- | --- |
| `sort` | empty | Declared column id to sort by; its `source` selects the CSV field |
| `order` | ascending | `ascending` or `descending` |
| `filter` | empty | Comma-separated conditions, combined with AND |
| `limit` | 0 | Nonnegative integer; zero displays all selected rows |
| `scale scope` | data | `data` uses all imported rows for automatic ranges; `visible` uses the displayed rows |

Selection runs in order: filter, stable sort, then limit. Ranking uses the displayed
rows; automatic ranges use the chosen scope before measurement and pagination.
`sort`, `filter` and a positive `limit` require `data`. Their column ids must be
declared; supported types are text, number, bar, bullet and heat. Pair, interval,
stack and spark fields do not have an implicit scalar sorting/filtering rule.

Numeric sorting uses raw decimal values, not formatted labels; equal values retain
file order and missing values come last in both directions. Text sorting uses
case-sensitive character order, not locale-specific collation; empty text comes
last, while literal text such as NA stays text. Limit counts missing rows too.

Numeric conditions support `=`, `!=`, `<`, `<=`, `>` and `>=`, for example
`filter={score>=75,time<100}`. Decimal equality is numerical, so 30 and 30.0 match.
Missing numeric fields fail ordinary numerical comparisons, including `!=30`.
Use `score=NA` or `score!=NA` to test missingness after the dataset's mapping.
Text conditions support only literal, case-sensitive `=` and `!=`; `method=`
matches empty text. Protect a whole condition containing a comma, for example
`filter={{method=Compact, tuned}}`. There is no expression execution, OR,
regular-expression matching or implicit unit conversion.

With `scale scope=data` (default), filtering and limiting do not change the original
column range. With `visible`, range calculation uses the retained rows, after
limiting. An empty visible selection uses the existing [0,1] fallback. The loaded
dataset remains unchanged and may be reused in another table.

## Diverging heat and center values (v0.0.5)

```latex
\gradheat[heat palette=diverging,min=-50,max=100,heat center=0]{-25}
\gradheat[heat palette=diverging,min=20,max=80,heat center=50]{65}
```

`heat palette=sequential|diverging` defaults to sequential. Selecting sequential
sets the existing light-blue/blue endpoints; selecting diverging sets orange/white/
teal. Named shortcuts `blue|teal|purple|orange` select white-to-color sequential ramps;
`purple-teal|blue-red|orange-blue|brown-teal` select white-centered diverging ramps.
They work in Heat cells and shared/continuous legends; see [palette examples](legends.md#built-in-heat-palettes).
Place custom endpoint colors after the palette. `heat center` defaults to 0;
`heat center color` defaults to white. The center must be a decimal within the
closed [min,max] range, including its boundaries.

Diverging interpolation runs independently from min to center and center to max,
so the center maps exactly to the neutral color even with asymmetric ranges.
At a boundary center only the other half is used; no zero-width division occurs.
`better=lower` swaps endpoint colors, retaining the center. Overflow clips color
but retains the raw label; missing keeps its separate neutral fill. Print uses
gray endpoints with a white center; sign remains visible in labels. Sequential
colors and labels retain v0.0.5 behavior. Automatic ranges do not automatically
expand to include a center outside the data range: use a suitable fixed range or
include zero when the center is zero. Alternative text includes the center.

## Bar and win-loss sparks (v0.0.5)

```latex
\gradspark[spark type=bar]{20,-10,NA,40,0,-30}
\gradspark[spark type=winloss]{20,-10,NA,40,0,-30}
\gradcolumn[type=spark,options={spark type=bar}]{trend}{Trend}
```

| Drawing key | Default | Meaning |
| --- | --- | --- |
| `spark type` | line | `line`, `bar` or `winloss` |
| `spark bar width` | .7 | Fraction of each equally sized observation slot; must be in (0,1] |
| `spark win color` | gradbarsTeal | Positive win-loss observations |
| `spark loss color` | gradbarsOrange | Negative win-loss observations |
| `spark zero color` | black!45 | Baseline and short zero strokes |

Bar height encodes the original magnitude from a zero baseline. Automatic bar
ranges include zero; all-zero and all-missing auto bars use [0,1]. Fixed bar ranges
use min/max and existing overflow rules, clipping the baseline to the nearest
border if zero is outside the range. Positive bars use the ordinary fill color;
negative bars use `negative color`. All observations occupy equal-width slots.

Win-loss maps positive values to +1, negatives to -1 and zero to a short baseline
stroke. Heights express categories, not magnitudes; min/max and spark range do
not affect these categories. Missing leaves its slot empty. Labels and alternative
text retain raw observations and the original last position, including a missing
last observation. Computed-percent labels are unsupported for win-loss.

Both modes support CSV/gradtable spark columns, named styles and grayscale print.
`spark points` and extrema marker colors apply to line mode only. Existing line
geometry, per-row auto ranges and marker behavior remain unchanged. All spark
types still require equally spaced observations and do not parse dates.

## Print patterns (included in v0.0.2)

| Key | Default | Meaning |
| --- | --- | --- |
| `pattern` | `none` | `none`, `diagonal`, `reverse`, `dots`, `crosshatch`, `horizontal`, `vertical` |
| `pattern color` | `black` | Color of overlaid pattern strokes/dots |
| `stack patterns` | `{none}` | Per-segment pattern names; cycle like stack colors |
| `print` | not applied | Apply the monochrome preset described below |
| `print labels` | `false` | Add a small white background behind inside labels; enabled by `print` |

```latex
\gradbar[print,pattern=dots,height=16pt,label=auto]{72}
\gradstack[print,stack names={Train,Validation,Test},
  height=17pt,segment labels=percent,legend=true]{60,25,15}
\gradbarslegend[print]{Train,Validation,Test}
```

Patterns overlay existing fills and follow clipping/rounded boundaries. Single
bars use `pattern`; stacked bars and legends use `stack patterns`. Zero segments
consume a pattern index. Lists must be nonempty and contain known pattern names.
The preset `print` sets a gray theme, white fill, light-gray track, black text and
pattern color, white negative fill, diagonal single bars, and a cyclic diagonal/
dots/crosshatch stack palette over white segments. It also sets threshold colors
to light/medium/darker gray and enables white inside-label backgrounds.
Explicit options after the preset can override its settings; it does not erase
targets, thresholds or number formatting. Use the same style on bars and shared
legends. Names and values should remain present; patterns alone do not express
statistical or ordinal meaning. Pattern spacing follows TikZ's built-in patterns.

## Metric direction (included in v0.0.2)

`better=higher` is the default and preserves earlier threshold behavior.
`better=lower` reverses threshold **color indices**, without changing bar lengths,
raw values, labels, scale, targets or errors. It has no effect without `thresholds`.

For ascending thresholds `{a,b}`, bins remain `v<a`, `a<=v<b`, and `v>=b`.
`threshold colors={bad,neutral,good}` always lists quality from bad to good:
higher uses indices 1/2/3; lower uses 3/2/1. Equality still enters the right bin.
For latency, `{70,100}` with lower means below 70 is good, [70,100) is neutral,
and 100 or more is bad. Thresholds still override sign-based fill colors.
Stacks do not support thresholds, so this does not rate individual segments.


## v0.0.3 comparison, trend and semantic styling

| Entry | Meaning |
| --- | --- |
| `\graddumbbell[options]{reference}{current}` | Hollow reference point, filled current point; line only if both exist |
| `compare label=values|delta` | Default values show current / reference; delta shows current minus reference; also applies to gradcompare |
| `stack totals=net|separate` | Default net; separate shows positive / negative subtotals |
| `\gradspark[options]{list}` | Equally spaced decimal observations; empty fields and NA preserve missing positions |
| `spark range=auto|fixed` | Default auto uses each series' extrema; fixed uses min/max |
| `spark points=extrema|all|last|none` | Default extrema includes tied extrema and the last position if present |
| `spark high color`, `spark low color` | Defaults gradbarsTeal, gradbarsOrange; a constant series uses the high color |
| `better=target|interval` | Evaluate distance to a goal or acceptable closed interval |
| `quality target` | Required decimal goal for target mode; default empty |
| `quality range={lo,hi}` | Required ordered endpoints for interval mode; default empty |
| `palette=categorical|sequential|diverging|mono` | Group colors and textures; no palette applied by default |
| `\gradbarscategory{name}{color}{pattern}` | Scoped literal-name mapping used by segments and legends |

Dumbbells share bar scales, target/error markers, number formatting, missing values and overflow policies. Error whiskers refer to the current value. Equal endpoints overlap. Missing either endpoint suppresses the connector and makes a delta label missing. Internal labels move outside. `compare color`, `marker size` and `stem width` control reference point, point radius and connector width.

Sparklines default to height=4ex. Auto range is per row; fixed scales require min<max. Constant auto series sit at mid-height; a singleton sits at the horizontal midpoint; all-missing input draws only the track and missing label. The last label reflects the last *position*, not the last nonmissing observation. All markers use `marker size`; line width is `stem width`. In extrema mode low/high markers use their own colors; a non-extreme last point uses the line color. Missing observations break paths. Auto range rejects computed percent labels. Target, band, thresholds and error whiskers are unsupported. Labels are outside; area patterns and rounded fill styles do not apply to the line.

For target mode, distance is abs(value-goal). For interval mode, distance is max(0,lo-value,value-hi). Both require two nonnegative increasing thresholds: d<=t1 is good, t1<d<=t2 intermediate, otherwise bad. `threshold colors` remains ordered bad/intermediate/good. Evaluation changes color, never geometry or labels. `quality target/range` do not implicitly draw `target/band`. These modes do not apply to stacks, floating intervals or series.

Categorical has six colors; sequential has five blue levels; diverging has five orange/neutral/teal levels and sets quality/negative/reference colors. They select colors by segment order, not value. Mono applies print settings and cycles three gray colors and diagonal/dots/crosshatch. Registered categories override cyclic color and texture by `stack names`; unregistered names fall back to position. Print/mono replaces registered colors with gray while preserving their patterns. Declarations follow grouping; the same names work in standalone legends. Color/pattern lists cycle, so distinct names or textures are needed beyond the palette length.

## Visual presets and v0.0.2 shapes

`\gradcompare[options]{reference}{current}` draws a full-height reference layer and a centered current layer. `compare ratio=.45` must lie strictly between 0 and 1; `compare color=black!20` sets the reference color. Missing layers are independent.

`\gradrange[options]{lower}{upper}` draws only the given interval, with optional `range point` inside the original endpoints. Equal endpoints draw a cap, not an inflated bar. Both endpoints must be present or both missing. Ranges reject error whiskers and quality thresholds; default labels show the endpoint pair.

`shape=lollipop` on gradbar draws a stem and point. Zero draws a point; missing data does not. `marker size=2pt`, `stem width=.6pt`, `outline width=.4pt` must be positive; `row padding=0pt` must be nonnegative.

`preset=paper|report|presentation|outline` applies thin academic, rounded report, large presentation or hollow outline settings. Presets do not invent ranges, target values or thresholds. Later keys override earlier settings. `outline=true` also works for stacks and legends; segment labels move outside. `print` clears outline mode. Group palettes set color/texture roles rather than row dimensions.

## v0.0.7 sorting, grouping and within-group statistics

```latex
\gradbarsloadcsv{families}{docs/data/families.csv}
\begin{gradtable}[data=families,width=\linewidth,theme=teal,
  group by=family,rank scope=group,group summary=true,
  sort keys={score/descending,time/ascending}]
  \gradcolumn[source=Method]{method}{Method}
  \gradcolumn[source=Family]{family}{Family}
  \gradcolumn[type=bar,source=Score,mark=both,aggregate=mean]{score}{Score}
  \gradcolumn[type=number,source=Time,aggregate=min,
    options={better=lower}]{time}{Time}
  \gradsummary{All visible}
\end{gradtable}
```

### Multiple sort keys

`sort keys={id/ascending,id/descending,...}` compares declared column IDs,
not CSV source names. Each entry requires its own direction; table `order`
is used only with the existing single-column `sort` option. Using both nonempty
`sort` and `sort keys` is an error. Text/scalar column restrictions and literal
text collation remain unchanged. Empty text and missing numeric values sort
last in either direction at each key; equal/missing keys proceed to the next
key. All keys tied retain the original CSV row order, including numeric 2/2.0.

### Automatic CSV groups

`group by=id` uses one declared text column, whose `source` can reference a
different CSV header. A hidden/undeclared CSV field cannot be used directly.
CSV selection runs filter -> global stable sort -> global limit -> grouping.
`limit=0` is unlimited; no per-group limit is added. Groups follow first
occurrence in the original CSV, omitting groups with no displayed rows.
Within a group, selected rows retain their global-sort order.

Leading/trailing group-label spaces are trimmed. Empty text forms a real group
headed by `group missing label={(ungrouped)}` (customizable); literal `NA` and
configured text missing tokens remain distinct group names. No rows are dropped
because of empty names. Automatic grouping requires CSV and cannot be combined
with manual `\gradgroup`. Only one group level is supported.

### Group ranks and summaries

`rank scope=table|group` defaults to table. Group ranks use displayed rows in
each automatic or manual group, skip missing numbers and retain real zero.
Ties and second distinct values follow existing marking semantics. Repeated
manual group titles still identify separate groups. Rows before the first
manual heading form an implicit group when group statistics are requested.
Group statistics without automatic or manual groups are errors.

`group summary=true` adds one numeric row at each displayed group's end using
the existing `aggregate=none|count|sum|mean|min|max` column settings. It does not
require an overall `\gradsummary`. `group summary scope=visible|data` defaults
to visible; data uses all imported rows of that group, including filtered or
limited-out rows, but does not introduce undisplayed groups. Manual groups have
the same rows in both scopes. `group summary label={Summary}` appears in the
first text column; color/font reuse `summary color`/`summary font`.

The overall `\gradsummary[scope=...]` is independent. Empty/all-missing count
and sum are 0; mean/min/max are missing. Count has no unit or computed percent.
Both kinds of summary are excluded from sorting, ranks and automatic scales.
Column/explicit shared scales span all groups; per-group auto-scaling is not
implemented. Across pages, a group heading stays with its first row, each group
summary appears once with its last row, and the overall summary follows the
final group summary on that page. Group headings are not repeated on continued
pages. See `tests/v007-smoke.tex` and `tests/cases/v007-regression.tex`.

## Research numeric presentation (v0.0.8)

### Shared scientific input

The grammar is `[+-]?(digits[.digits]?|.digits)([eE][+-]?digits)?`.
The implementation accepts at most 101 digits on each side of the decimal point
and at most three exponent digits. Nonzero input magnitudes must lie in
`[1e-100,1e100]`; zero is valid. These bounds also apply to explicit ranges and
displayed computed statistics. Numbers use expl3 floating point arithmetic with
approximately 16 significant digits: distinct input beyond that precision may
compare equal. Arithmetic expressions, locale separators, input units, NaN and
infinity are errors. Formatting precision remains 0--6 decimal places and does
not alter calculations. Tiny differences may be below TeX's drawing resolution.
Native/legacy CSV, sorting, group/table ranking, aggregate calculations and
auto/shared ranges accept the same literals. Numeric `2e1` and `20` tie.

### Formatter and semantic units

```latex
\usepackage{siunitx} % v3; optional, explicitly loaded by the user
\usepackage{gradbars}
\gradbar[formatter=siunitx,precision=3,
  unit code={\milli\second},unit text={milliseconds}]{1.23456e1}
```

Drawing `formatter=builtin|siunitx` defaults to builtin. Tables and columns have
the same key (a table default, then a column override); drawing keys inside
column `options` may override it. Table defaults are independent of standalone
drawing setup. Selecting siunitx without explicitly loading v3 is an error.
Only public `\num` and `\unit` interfaces are used: the entire graphic is never
passed to an S column. Precision and fixed/grouped/scientific display modes are
mapped explicitly; this is not an adapter for every siunitx option or uncertainty
input. Dot output is enforced, grouped output uses comma thousands separators,
and fixed output uses thin spacing. Outside decimal-aligned columns, builtin
retains the existing PGF formatter. The SI formatter preserves the current math
version so bold ranking/summary labels remain bold.

`unit={...}` remains an arbitrary literal suffix. Semantic `unit code={...}`
requires `formatter=siunitx` and nonempty `unit text={...}`; the latter is a plain,
human-readable description for automatic alternative text. Do not combine unit
and unit code or combine semantic units with computed-percent labels. Put the
unit code and text in column drawing `options`. Missing numbers have no suffix;
count summaries suppress both unit forms. Automatic graphic descriptions retain
unrounded values and use unit text rather than copying unit macros. Explicit
`alt` still replaces the complete automatic description.

### Decimal anchors and the research style

Table/column `number align=none|decimal` defaults to none. Only number columns
can explicitly select decimal alignment; a table default applies to number
columns while leaving text and graphic columns unchanged. `align=l|c|r` locates
the complete aligned number block within the cell; it is independent of decimal
alignment. Fixed/grouped decimals align at the point; scientific displays align
at the mantissa's point and reserve room for exponent signs/digits and units.
`precision=0` aligns the integer endpoint. Missing labels are centered in the
number block. Explicit rounding ties go away from zero for aligned displays.

Both sides are measured using actual fonts and marks over displayed data, each
group summary and the overall summary, before width allocation. A `scope=data`
summary may need more width than visible values. Per-column explicit widths
that cannot accommodate the aligned block are errors. Number formatting never
becomes input to sorting/ranking/aggregation. Long tables use the same anchors
on every page. All-missing/empty columns remain safe.

`style=research` is a compatible preset: paper/booktabs, centered headers,
row stretch 1.3, column separation 5pt, row padding 1pt, group separation 5pt,
decimal number alignment and bold summaries. It has no mandatory color theme
or SI dependency. Combine any existing table theme and put explicit overrides
after the style. Academic, compact and dashboard retain their existing defaults.
This is the new preset after the v0.0.7 and v0.0.8 functional-theme updates.

See `tests/v008-smoke.tex`, `tests/cases/v008-builtin.tex`, `tests/v008-alignment.tex`
and `tests/v008-tagged.tex`. SI typesetting follows the
[official siunitx manual](https://mirrors.ctan.org/macros/latex/contrib/siunitx/siunitx.pdf).

## Modular loading and public callbacks (v1.0.0)

Default `\usepackage{gradbars}` retains complete loading. Use
`\usepackage[libraries=none]{gradbars}` and preamble-only
`\usegradbarslibrary{stack,spark,heat,csv,table}` for optional engines. The table
library automatically loads the other four; each depends on core. Package
`libraries={heat,spark}` is also supported. Repeated loading is safe; unknown
names, missing files, cycles and native module version mismatches are errors.
Install all twenty-two matching runtime .sty files, including optional libraries and adapters, together. SI formatting remains optional.

`\gradbarsset` delegates to `\gradbarssetup`, sharing TeX grouping and precedence.
`\gradbarsiflibraryloaded{name}{yes}{no}` queries availability. Registrations are
global and duplicates are errors; names start with a lower-case letter and use
letters, digits and hyphens.

| Command | Contract |
| --- | --- |
| `\gradbarsdeclarelibrary{name}{dependencies}{file.sty}` | Preamble registration; comma-separated dependencies and a TeX-searchable file |
| `\gradbarsdeclaretype{name}{callback}` | Stable scalar callback with validated value/NA as #1 |
| `\gradgraphic[options]{name}{value}` | Scoped dispatch to a registered scalar renderer; builtin bar and heat names are reserved |
| `\gradbarsdeclareformatter{name}{callback}` | Stable number-only callback: display value #1, precision #2, format mode #3 |
| `\gradbarsformatnumber[options]{value}` | Public builtin/SI number helper with precision/format options; no unit suffix |

Custom renderers are standalone, not additions to the native gradcolumn types.
Custom formatters work with graphic labels and ordinary number columns and reject
decimal alignment. The engine adds literal unit/percent suffixes; semantic units
still require siunitx. Callbacks do not become statistical input. Private commands
and variables remain outside the contract. See [developer.md](developer.md),
[migration-v1.1.0.md](migration-v1.1.0.md) and
[the contributed library](libraries/gradbars-contrib-demo.sty).

## Stable version 1 contract

The documented commands, keys, defaults, data semantics and library dependencies
are covered by [stability.md](stability.md). Private implementation names and
module layout are excluded. The supported baseline is LaTeX 2025-11-01+, expl3
2025-12-29+ and PGF/TikZ 3.1.11a+. No public interface is deprecated in 1.0.0.

`style=reference` is an optional native-table preset using paper/booktabs,
centered headers, decimal number alignment, row stretch 1.25 and column separation
6pt. It does not force a color theme or replace existing presets. Put explicit
overrides after the style.

The generated `gradbars.dtx`/`gradbars.ins` extract all runtime modules using
docstrip. `texlua scripts/source.lua --check` verifies source consistency.
The private model module separates validated raw data and normalized positions
from TikZ drawing. Only the TikZ backend is supplied. Schema-1 scalar backend
registration and read-only callback records are public; private model storage
is excluded. See [backends.md](backends.md) for the bar/Heat contract and explicit
fallback requirements for compound graphics and legends.

## tabularray library and cell interfaces

```latex
\usepackage{tabularray} % 2025C (2025-11-27) or newer
\usepackage{gradbars}
\UseTblrLibrary{gradbars}
\gradtblrsetup{min=-10,max=10,precision=1}
\begin{gradtblr}{colspec={l G{30mm} H{30mm} N{25mm} D{35mm}}}
Method & {Change} & {Heat} & {Number} & {Before/after}\\
A & -5 & 5 & 12.345 & -3/7\\
B & 0 & NA & NA & NA\\
\end{gradtblr}
```

The standard external library file `tblrlibgradbars.sty` lives in `sty/` and
must be installed alongside the base modules. The adapter is optional, requires
tabularray 2025C+, loads the native heat, stack, spark and distribution libraries
and tabularray hook/varwidth, and supports repeated preamble loading.
If gradbars is absent it loads the
minimal core. It is not an extra name in the native `libraries={...}` option.

| Interface | Meaning |
| --- | --- |
| `\gradtblrsetup{options}` | Accumulate adapter defaults within the current TeX group |
| `\gradtblrcell[options]{type}{data}` | Render bar, heat, number, compare, dumbbell or range |
| `\gradbarTblr`, `\gradheatTblr`, `\gradnumberTblr`, `\gradcompareTblr` | Optional keys plus one cell argument; suitable for `cmd=` |
| `G[options]{width}`, `H[options]{width}`, `N[options]{width}`, `D[options]{width}` | Centered fixed-width bar, Heat, number and comparison columns |
| `gradtblr` environment | Optional thin-row-rule, centered-cell, tinted-bold-header preset |
| Native `style=matrix` | Paper preset, row rules, centered cells/headers, row stretch 1.35, column separation 6pt, row padding 1pt |

Pair data uses `reference/current` for compare/dumbbell and `lower/upper` for
range. Empty/NA means both endpoints are missing; individual endpoints can be
NA where the corresponding graphic permits it. Scalar inputs keep scientific
notation, missing/zero, formatter, literal/semantic unit and shared-scale rules.
Number cells format without clipping to graphic limits and do not emit Figures.

The adapter defaults to `baseline=text,label=inside,label align=cell`. Global
graphic settings precede these adapter defaults, then accumulated setup and
per-call options apply. Final allocated graphic dimensions apply last.
`label align=cell` centers inside/auto labels on the full graphic width even
for signed/tiny/missing bars, without automatic relocation. `graphic` is the
unchanged ordinary-graphic default. None/left/outside/end keep their original
placement semantics; Heat retains its centered-label behavior.

`cell width=auto` uses local content width for fixed/Q/X/spanning cells. Natural
trials start from the configured graphic width; actual output uses the allocated
width. Explicit dimensions exclude column separation/rules and must fit the
actual table cell. Left/outside labels reserve their slot and gap; dumbbells
reserve marker extents. An insufficient label/cell width produces an error;
`label overflow=allow` permits intentional overlap without changing alignment.
Standalone helpers should receive an explicit cell width.

Protect headers with `{...}`, or clear `cmd` for those cells after specifying
columns. A single braced cell bypasses tabularray's cmd transformation; direct
graphic calls can be placed in such cells. The library reserves G/H/N/D; rename
existing conflicting custom types before loading it. Ordinary tblr styling is
unchanged. `longtblr` supports the same columns and repeated protected text
headers via `rowhead=1`. CSV selection, automatic ranges, ranks and aggregates
remain native gradtable features.

Public trial hooks suspend tagging during measurement. Three-engine checks cover
fixed/X cells, explicit/automatic descriptions, missing values and artifact/off.
With the basic adapter alone, use text for repeated headers. Explicit table
structure and graphic-header repeat modes require `\gradtblrtagging`, described
in [accessibility.md](accessibility.md). Short tagged tables are tested on all
three engines. Tagged longtblr with repeated headers or footers requires
LuaLaTeX; both artifact copies and explicitly described repeated headers are
supported. Nested tagged tables and cross-page spanning cells remain outside
the verified scope. Structural checks do not certify screen-reader behavior or
whole-document PDF/UA conformance.

## v1.1.0 distributions, legends and accessible tables

`legend missing=true|false` controls the missing-value item in continuous legends,
including `\gradlegenduse` layout overrides; default true.

Optional native libraries `distribution` and `legend` extend the default five
libraries without changing their load list. Full contracts and examples:

- [Distribution statistics and box plots](distributions.md): `\gradboxplot`, `\gradboxsummary`, `\gradcomputesummary`, `\gradstat`, `\gradsummarytext`, native boxplot columns and new styles.
- [Continuous and shared legends](legends.md): `\gradheatlegend`, `\gradreferencelegend`, `\gradlegenddefine`, `\gradlegenduse` and shared configuration.
- [Color and table accessibility](accessibility.md): accessible palettes, print, raw descriptions and opt-in `\gradtblrtagging`.

The optional tabularray adapter adds J (dumbbell), R (range), V (spark), K (stack),
U (bullet) and B (boxplot), all `[options]{width}`, plus matching
`\graddumbbellTblr`, `\gradrangeTblr`, `\gradsparkTblr`, `\gradstackTblr`,
`\gradbulletTblr`, `\gradboxplotTblr`. The generic cell accepts the same types.
The adapter now loads heat, stack, spark and distribution in the preamble.
Spark and dumbbell cells reserve marker radii plus a 1pt stroke allowance, fixing
false width overflow when markers lie exactly at scale endpoints.
G/H/N/D signatures are retained. Spark/stack default to no main label to avoid
external-label overflow; explicitly requested left/outside slots are reserved.
Bullet columns require explicit `bullet bands`; pair formats remain unchanged.
Protect comma-containing sample/series/stack cells with braces and call the
matching helper inside, so tabularray does not bypass the conversion silently.

## Domain reports and backend providers (v1.1.0)

- [Reports](reports.md): opt-in correlation, ablation and metric presets and native column helpers.
- [Backend contract](backends.md): `\gradbarsdeclarebackend`, `\gradbarsifbackendcapable`,
  `\gradbarsbackendvalue`, `\gradbarsbackendlabel`, `\gradbarsbackenddefault`,
  `\gradbarsbackendversion`, `backend` and `backend fallback`.
- [Third-party starter](libraries/starter/README.md): public-only source and three-engine checker.
- `\gradbarsversion` and `\gradbarsrequireversion{minimum}` query/check semantic versions.
