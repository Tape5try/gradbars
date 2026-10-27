# Table, continuous and shared legends

## Horizontal table-header legends

`\gradtablelegend[graphic options]{names}` draws one horizontal category row at
its natural width. `\gradtablelegendhead[graphic options]{title}{names}` centers
an ordinary text title above that row, with a 2pt vertical gap. Both commands
belong to core and work with `\usepackage[libraries=none]{gradbars}`; no optional
`legend` library is needed. They render only when explicitly called and do not
insert legends into existing bars or tables.

```latex
\begingroup
\gradbarssetup{stack colors={gray,teal,blue,orange,red}}
\begin{tabular}{lc}
Service & \gradtablelegendhead{Response status}{Pending,Fast,Normal,Slow,Timeout}\\
\hline
Lookup & \gradbar[max=1000,width=42mm,color=teal,precision=0,unit={ ms}]{120}\\
Export & \gradbar[max=1000,width=42mm,color=blue,precision=0,unit={ ms}]{420}\\
\end{tabular}
\endgroup
```

Names use the existing comma-list category syntax. Registered
`\gradbarscategory{name}{color}{pattern}` mappings take precedence; other names
use `stack colors` by position, cycling when needed. Print mode reuses category
textures and monochrome colors. These helpers do not infer thresholds, classify
observations or change any bar's colors. Set the corresponding bar colors or
classification rules explicitly.
The table swatches remain filled even with `outline=true`; use
`legend border color` and `legend border width` for their frames. Setting the
border width to zero removes the frame.

The following `/gradbars` keys can be set in `\gradbarssetup` or either helper's
optional argument. They follow ordinary TeX grouping and left-to-right overrides;
they are not new native `gradtable` declaration keys.

| Key | Default | Meaning |
|---|---|---|
| `table legend` | `true` | `true`/`false`; the bare key means true; false hides the category row |
| `legend font` | `\sffamily\scriptsize` | Category-label font |
| `legend swatch size` | `6pt` | Positive square swatch size |
| `legend text gap` | `2pt` | Nonnegative gap between a swatch and its label |
| `legend item gap` | `4pt` | Nonnegative gap between category items |
| `legend border color` | `black` | Swatch border color |
| `legend border width` | `.4pt` | Nonnegative border width |

With `table legend=false`, `\gradtablelegend` emits no category row, while
`\gradtablelegendhead` retains its title with no reserved legend gap:

```latex
\gradtablelegendhead[table legend=false]{Response status}{Pending,Fast,Normal,Slow,Timeout}
```

Use the header helper directly in an ordinary `tabular` heading or a
`\gradcolumn` title. In a collected numeric column, write
`\gradbarshead{\gradtablelegendhead{Response status}{Pending,Fast,Normal,Slow,Timeout}}`
to bypass numeric collection. The helper itself does not insert `\multicolumn`.
It can replace a handwritten title/minipage/TikZ-swatch macro; keep any desired
column spanning in the surrounding table code. See the
[service-response example](examples/service-response-legend.tex).

The category graphic retains the existing automatic/explicit `alt`,
`accessibility=auto|artifact|off` and `category-legend` backend rules, including
explicit native fallback when required. The title is ordinary text outside the
legend Figure. The older vertical `\gradbarslegend` and automatic stack
`legend=true` behavior are unchanged; `table legend` controls only these new
helpers.

## Continuous and shared legends

For the commands below, load `\usegradbarslibrary{legend}` in the preamble
(depends on core and heat). Existing category registration and
`\gradbarslegend` remain available.

```latex
\gradscale{score}{min=-10,max=30}
\gradlegenddefine{score}{scale group=score,palette=accessible,
  heat palette=purple-teal,heat center=0,unit={ pt},legend title={Score}}
\gradheat[legend group=score]{10}
\gradlegenduse[width=60mm,height=3mm]{score}
```

`\gradheatlegend[graphic options]` displays a continuous *quantity* with a
256-strip vector ramp whose base colors use the same Heat color function.
Fine semitransparent white separators are drawn over the strip boundaries in
both orientations, including print mode. They change the visible texture, not
the numeric encoding, and do not represent categories or bins. `width` is the
ramp length and `height` its thickness;
`legend orientation=vertical` rotates the layout (low at bottom). Endpoints and
an interior diverging center are default ticks. `legend ticks={...}` supplies
strictly increasing numeric ticks within range. `legend title` adds a heading.
Horizontal tick labels use two measured rows; overly dense labels produce an error.
Tick locations use raw values; labels use the normal formatter/precision/units.
A separate missing-color swatch and marker appear below the ramp by default.
Set `legend missing=false` to hide both this item and its automatic description;
`legend missing=true` (or bare `legend missing`) restores it. The switch works
in `\gradheatlegend[...]`, `\gradlegenduse[...]` and shared definitions,
with local overrides and normal TeX grouping. It does not change data handling. Increase precision
or reduce tick density if labels round to the same text or overlap.

The ramp respects better=lower, print, the exact asymmetric center, and centers
at either endpoint. The direction changes colors, not numeric tick positions.
Use physical dimensions for standalone legends; automatic column scales are not
inferred from a previously encountered table.

`\gradlegenddefine{name}{graphic options}` freezes the resolved explicit scale,
color roles, print state, direction and units in the current group. Names use
lowercase letters, digits and hyphens, starting with a letter. Unknown names and
duplicate definitions in the same scope are errors. Redefinition inside a new
scope is intentionally rejected while a name is visible; define a distinct name.
The same declaration supplies independent figures, native columns through
`options={legend group=...}`, and tabularray cells. Its explicit named scale is
resolved at definition time, so later scale changes do not silently change it. Automatic box and spark ranges
cannot replace the frozen explicit range. Win-loss series require [-1,1].
Percent display and its denominator are captured together and described explicitly.

`legend group=name` applies the frozen configuration. Changes to its range,
unit or color roles before drawing produce a conflict error. Scoped declarations
do not leak into the next table. `\gradlegenduse[layout]{name}` only accepts
width, height, title, ticks, orientation, precision, number format, font, alt, accessibility and `legend missing`;
it cannot replace the scale/colors/unit. `legend group={}` releases the binding
while leaving current graphic settings available for explicit overrides. It leaves following graphics unchanged.

`legend kind=heat` is the default. `categorical` uses `legend names={A,B,...}`
and the existing category renderer. `reference` uses names encoded as
`type/description` records. Keep descriptions literal and avoid `/` inside them.

```latex
\gradreferencelegend{target/Declared target,reference/Reference value,
  band/Reference range,error/Error distances,box/Quartiles and observed whiskers}
```

Supported reference symbols are target (solid vertical), reference (dashed
vertical), band (filled region), error (capped distances) and box (box/median
with observed whiskers). Text declares their actual meaning: error distances
are not automatically confidence intervals, and box whiskers are not errors.
Their graphic options reuse target/band/error colors. Shared reference legends
freeze the same roles; match actual reference line styles in your labels.

Automatic descriptions state the scale, direction, unit, neutral center and
missing meaning, or all reference descriptions. `alt` replaces the description;
`accessibility=artifact` makes a decorative repeat an artifact. Visual category
names remain essential if the finite color/texture sequence cycles.

## Built-in Heat palettes

Use one `heat palette=name` instead of three color assignments. The preset also
selects sequential or diverging interpolation and automatic black/white text.

| Name | Low → center → high | Mode |
|---|---|---|
| `blue` | white → blue | sequential |
| `teal` | white → teal | sequential |
| `purple` | white → purple | sequential |
| `orange` | white → orange | sequential |
| `purple-teal` | purple → white → teal | diverging |
| `blue-red` | blue → white → red | diverging |
| `orange-blue` | orange → white → blue | diverging |
| `brown-teal` | brown → white → teal | diverging |

Set these in `\gradlegenddefine`, `\gradheat`, `\gradheatlegend` or Heat column
options. A shared legend freezes the resolved colors. `heat center` still
defines the numeric center and must lie within the diverging range. Place explicit
color keys after the preset to override individual colors; `better=lower` and
`print` retain their existing behavior. Presets do not change ranges or centers.
Existing `sequential`, `diverging`, `accessible-sequential` and
`accessible-diverging` defaults remain unchanged. The new names are design
shortcuts, not additional claims of color-vision or contrast certification.
