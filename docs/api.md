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
commas, units inside numbers, and missing values are not accepted.
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
| `label` | `outside` | `outside`, `inside`, `none`, `end` |
| `label width` | `4.5em` | Fixed right-aligned outside label slot |
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
| `text color` | set by theme | Label color |
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
approximately `width + label gap + label width`; long labels may protrude.
Inside labels align near the track's right edge, regardless of the filled
fraction. They are not automatically resized or contrast-adjusted.

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

Use XeLaTeX for documents, examples, the manual, and regression tests.
The current test runner and GitHub Actions target XeLaTeX only.

## Built-in colors

`lightgreen`, `lightyellow`, `lightblue`, `lightred`, `rose`, `skyblue`,
`gold`, `lavender`, and `peach` are public xcolor names defined by this package.
Use `color=rose` for a solid fill, or use them as gradient endpoints.
Keys apply left to right; a later theme resets its fill and colors.
