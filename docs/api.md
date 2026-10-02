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

Numbers must be decimal literals (signed values require a negative min), or macros expanding to them.
Examples: `0`, `.5`, `+12`, `125000`, `86.50`. Expressions, scientific notation,
commas and units inside numbers are not accepted. Empty input and uppercase `NA`
are missing values for `\gradbar`; all other nonnumeric input is an error.
Use decimal points and put units in `unit`. Floating point arithmetic has finite
precision. TeX's dimension resolution limits the smallest drawable bar.

## Keys

| Key | Default | Meaning |
| --- | --- | --- |
| `min` | `0` | Nonpositive scale minimum; negative enables signed bars |
| `max` | `100` | Positive scale maximum |
| `width` | `24mm` | Positive track width; excludes outside label |
| `height` | `1.5ex` | Positive track height |
| `theme` | `blue` | `blue`, `teal`, `solid`, `gray`, `lbyellow`, `viblue`, `cyblu` |
| `label` | `outside` | `outside`, `inside`, `none`, `end`, `auto` |
| `label width` | `4.5em` | Minimum right-aligned outside label slot with automatic overflow handling |
| `label gap` | `.6em` | Gap between track and outside label |
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

## Geometry and labels

The scale satisfies `min <= 0 < max`. The zero line is at
`width * (-min)/(max-min)`. The value endpoint is at
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
- This version does not generate accessible tagged chart descriptions.

## XeLaTeX workflow

Use XeLaTeX. GitHub Actions builds the manual; all examples are included in it.

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
formatting never changes geometry. Input remains decimal notation.

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
The tabularray column machinery has not been validated.

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
Only numeric operations apply the mapping. Valid numbers follow `\gradbar`'s decimal
literal rules; arbitrary text, formulas, units and scientific-notation input error.
Zero remains an observation. CSV input does not change `\gradbar`'s own missing tokens.

Auto ranges use `min(0, smallest valid value)` and `max(0, largest valid value)`;
if the computed maximum is zero, it becomes 1. Missing fields are ignored.
Thus all-zero/all-missing/header-only columns use [0,1], and all-negative columns
use [minimum,1]. This keeps the upper limit positive as required by the bar API.
Ranges cover the whole column, even if only some rows are subsequently displayed.
Explicit table options are applied after the computed range and can override it.
Fix ranges explicitly when comparing different files or runs.

The generated table does not paginate or sort. For longtable, custom headers or
multiple metrics, use the cell/bar commands in your own table layout. Imported
columns are not automatically bound to a `\gradbarscolumn` definition.

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

Sparklines default to height=4ex. Auto range is per row; fixed scales require min<=0 and max>0. Constant auto series sit at mid-height; a singleton sits at the horizontal midpoint; all-missing input draws only the track and missing label. The last label reflects the last *position*, not the last nonmissing observation. All markers use `marker size`; line width is `stem width`. In extrema mode low/high markers use their own colors; a non-extreme last point uses the line color. Missing observations break paths. Auto range rejects computed percent labels. Target, band, thresholds and error whiskers are unsupported. Labels are outside; area patterns and rounded fill styles do not apply to the line.

For target mode, distance is abs(value-goal). For interval mode, distance is max(0,lo-value,value-hi). Both require two nonnegative increasing thresholds: d<=t1 is good, t1<d<=t2 intermediate, otherwise bad. `threshold colors` remains ordered bad/intermediate/good. Evaluation changes color, never geometry or labels. `quality target/range` do not implicitly draw `target/band`. These modes do not apply to stacks, floating intervals or series.

Categorical has six colors; sequential has five blue levels; diverging has five orange/neutral/teal levels and sets quality/negative/reference colors. They select colors by segment order, not value. Mono applies print settings and cycles three gray colors and diagonal/dots/crosshatch. Registered categories override cyclic color and texture by `stack names`; unregistered names fall back to position. Print/mono replaces registered colors with gray while preserving their patterns. Declarations follow grouping; the same names work in standalone legends. Color/pattern lists cycle, so distinct names or textures are needed beyond the palette length.

## Visual presets and v0.0.2 shapes

`\gradcompare[options]{reference}{current}` draws a full-height reference layer and a centered current layer. `compare ratio=.45` must lie strictly between 0 and 1; `compare color=black!20` sets the reference color. Missing layers are independent.

`\gradrange[options]{lower}{upper}` draws only the given interval, with optional `range point` inside the original endpoints. Equal endpoints draw a cap, not an inflated bar. Both endpoints must be present or both missing. Ranges reject error whiskers and quality thresholds; default labels show the endpoint pair.

`shape=lollipop` on gradbar draws a stem and point. Zero draws a point; missing data does not. `marker size=2pt`, `stem width=.6pt`, `outline width=.4pt` must be positive; `row padding=0pt` must be nonnegative.

`preset=paper|report|presentation|outline` applies thin academic, rounded report, large presentation or hollow outline settings. Presets do not invent ranges, target values or thresholds. Later keys override earlier settings. `outline=true` also works for stacks and legends; segment labels move outside. `print` clears outline mode. Group palettes set color/texture roles rather than row dimensions.
