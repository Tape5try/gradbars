# Continuous and shared legends

Load `\usegradbarslibrary{legend}` in the preamble (depends on core and heat).
Existing category registration and `\gradbarslegend` remain available.

```latex
\gradscale{score}{min=-10,max=30}
\gradlegenddefine{score}{scale group=score,palette=accessible,
  heat palette=purple-teal,heat center=0,unit={ pt},legend title={Score}}
\gradheat[legend group=score]{10}
\gradlegenduse[width=60mm,height=3mm]{score}
```

`\gradheatlegend[graphic options]` displays a continuous *quantity* with a smooth
256-strip vector ramp using the exact same Heat color function. It is not a set
of categories or bins. `width` is the ramp length and `height` its thickness;
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
