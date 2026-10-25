# Public backend contract, schema 1

The supplied renderer remains TikZ. This contract provides registration,
capability negotiation and a public read-only record for **bar and Heat cells**.
It does not supply a lightweight renderer or remove the PGF/TikZ dependency.
Compound data records remain a separate extension task.

```latex
\gradbarsdeclarebackend{my-backend}
 {bar,heat,missing,signed,gradient,print,labels,units,clip,
  decorations,embedded,tagging,artifact}
 {\gradbarsbackenddefault}
\gradbar[backend=my-backend]{72.125}
```

The callback receives one argument: `bar` or `heat`. Registration is global and
preamble-only. Names start with a lowercase letter and contain lowercase letters,
digits and hyphens. Duplicate names, including `tikz`, are errors. A registration
must name bar or heat and only supported capabilities. `backend=name` is scoped
like other graphic options; the default remains tikz.

`\gradbarsifbackendcapable{name}{capability}{yes}{no}` queries the declaration;
unknown names/capabilities return no. A declaration is a provider's promise, not
a certification that its output is correct. Only declare features actually
implemented or delegated to the supplied renderer.

## Capability negotiation

| Capability | Required when |
|---|---|
| bar / heat | The corresponding scalar frontend is used |
| missing | The observation is missing |
| signed | The range includes negative values |
| gradient | The effective bar fill is a gradient |
| print | Print mode is enabled |
| labels | A label is requested |
| units | Literal or semantic units are present |
| clip | A raw value lies outside the display range and frontend policy allows clipping |
| decorations | Rounded corners or, for bars, patterns, outlines, non-bar shapes, thresholds or reference/error annotations are requested |
| embedded | Rendering occurs inside an existing TikZ picture |
| tagging / artifact | Active document tagging requests a described figure / decorative artifact |

An unsupported request fails before invoking the callback. Explicit
`backend fallback=tikz` delegates that whole graphic to the native renderer;
default `error` prevents silent changes. Stack, spark, comparison, dumbbell,
range, bullet, boxplot and all three legend families currently require tikz or
this explicit fallback. An interval collection consists of range graphics.
No partially rendered compound plot is sent to a scalar callback.

## Read-only record

Inside a callback, expandable `\gradbarsbackendvalue{field}` returns the scoped
snapshot. Outside a callback, and for an unknown/unavailable field, it reports an
error. `\gradbarsbackendversion` is the schema version (currently 1), independent
of the package version. Added fields may extend schema 1; existing field meaning
must remain compatible.

| Fields | Meaning |
|---|---|
| version, kind | Record schema and scalar kind |
| raw-value, value | Original input tokens and canonical unrounded number; value is NA for missing input |
| display-value | Number after percent conversion, before label rounding; NA when missing |
| min, max | Resolved numeric display range |
| position, zero | Value and zero positions clipped to [0,1]; position is NA when missing |
| width, height | Physical TeX dimensions, expressed in pt in the current drawing context |
| missing, print, gradient, embedded, tagging | Literal true/false flags; gradient describes the bar fill |
| alt | Resolved automatic or explicit description; never a fabricated display-rounded value |
| start, stop, end | Validated bar positions, available only for bar records |
| heat-rgb | Effective Heat fill RGB triple, available only for Heat records |

The following keys preserve the effective existing graphic option values and
TeX tokens, using these exact record names. Heat option fields are guaranteed
for Heat records; unavailable feature fields report an error:

- `shape`, `baseline`, `baselineshift`, `label`, `labelalign`, `precision`,
  `numberformat`, `format`, `percentbase`, `better`, `overflow`, `accessibility`.
- `left`, `right`, `negativecolor`, `track`, `textcolor`, `text`, `rounded`, `pattern`, `patterncolor`,
  `overflowmark`, `change`, `changecolor`, `markershape`, `markerfill`, `markersize`.
- `unit`, `unitcode`, `unittext`, `missingtext`, `gap`, `labelwidth`.
- `target`, `targetcolor`, `band`, `bandcolor`, `bandopacity`, `references`,
  `errorminus`, `errorplus`, `errorcolor`, `thresholds`, `thresholdcolors`.
- `heatpalette`, `heatcenter`, `heatcentercolor`, `heatlow`, `heathigh`, `heatmissing`.

Color fields contain xcolor expressions in the current document context. Option
records keep their existing public grammar; referenced values have already been
validated. Scalar geometry uses the normalized positions and resolved numeric range.
Do not parse raw-value to replace the canonical value, recompute statistics,
change ranges or round coordinates. Formatting is separate from numeric geometry.

## Drawing, labels and semantics

The callback emits one inline graphic and preserves width, baseline, clipping,
units and the selected accessibility policy. `\gradbarsbackendlabel` typesets the
existing formatted label with its configured font and units; it adds no placement
or Figure wrapper. The callback decides placement using the record and honors
label=none. Independent backends must supply suitable contrast and correct
Figure/artifact handling before declaring the corresponding capabilities.

`\gradbarsbackenddefault` draws the captured native continuation once. It neither
calls a public graphic frontend again nor revalidates input. The starter delegates
through this function, preserving native TikZ layout and descriptions. Calling
it twice, outside a callback, or recursively entering a selected custom backend
is an error. Reading records after the callback has returned is also an error.

Table measurement can invoke a callback multiple times for discarded boxes.
Callbacks must be free of external writes and other observable side effects.
Only the actual output should contribute graphic descriptions; respect the
current suspended-tagging state. Shared legends freeze scale/color semantics,
not backend selection. Document-wide PDF/UA conformance requires separate checks.

See the [public-only starter](libraries/starter/README.md),
[domain reports](reports.md) and [stability contract](stability.md).
