# Domain report presets

Load `\usegradbarslibrary{reports}` in the preamble. This opt-in library depends
on table and legend (and their dependencies); the five default libraries remain
unchanged. It packages supplied scalar data, ranges, styles and table-column
recipes rather than calculating statistical estimates.

| Use | Standalone graphic | Native table style | Native column helper |
|---|---|---|---|
| Correlation matrix | `\gradcorrelation[options]{r}` | `style=correlation` | `\gradcorrelationcolumn[options]{id}{heading}` |
| Ablation comparison | `\gradablation[options]{reference}{current}` | `style=ablation` | `\gradablationcolumn[options]{id}{heading}` |
| Performance metrics | `\gradmetric[options]{value}` | `style=metrics` | `\gradmetriccolumn[options]{id}{heading}` |

## Correlation

The standalone command fixes [-1,1], uses a white center at zero with purple/teal
endpoints, displays two decimals and rejects out-of-range values. NA is missing.
It keeps a fixed range even if a surrounding scale group has different limits.
The native column recipe uses Heat with fixed correlation defaults. It does not
compute correlations, check symmetry/positive semidefiniteness, impute cells or
infer significance. Supplied diagonal values are displayed normally.

```latex
\begin{gradtable}[style=correlation]
\gradcolumn{name}{Variable}
\gradcorrelationcolumn{a}{A}
\gradcorrelationcolumn{b}{B}
\gradrow{A,1,-.38}
\gradrow{B,-.38,1}
\end{gradtable}
```

## Ablation

Dumbbells distinguish reference/current observations; the main label is current
minus reference in the original units. The default range is [0,100], not an
inferred percentage convention. Set suitable min/max in drawing options for
other units. A column cell contains `reference/current`, including NA/NA when
both are missing. No confidence interval, significance test or causal conclusion
is implied by an observed difference.

```latex
\begin{gradtable}[style=ablation]
\gradcolumn{name}{Variant}
\gradablationcolumn{effect}{Score change}
\gradrow{Without feature,80/76}
\gradrow{With extra data,80/84}
\end{gradtable}
```

## Metrics

The standalone graphic defaults to [0,100], two decimals and accessible solid
color roles. Native metric columns instead use the existing column range scan,
include zero and mark best/second values. Each column retains its own units and
range. Higher is better by default; explicitly use better=lower for costs such
as latency. No overall score or cross-metric aggregate is invented.

```latex
\begin{gradtable}[style=metrics,width=\linewidth]
\gradcolumn{name}{Model}
\gradmetriccolumn{acc}{Accuracy}
\gradmetriccolumn[options={style=report-metric,better=lower,
  unit={ ms},precision=1}]{lat}{Latency}
\gradrow{A,92,35}\gradrow{B,95,48}\gradrow{C,90,28}
\end{gradtable}
```

Column helpers apply their defaults before caller-supplied native column keys.
Explicit keys can customize a recipe. The native `options={...}` field replaces,
rather than merges with, the helper's field: retain the corresponding graphic
style when overriding it. Graphic styles are `report-correlation`,
`report-ablation` and `report-metric`; table styles are separate registrations.
Use ordinary gradcolumn when designing a different schema. Caller-supplied
numeric overrides remain the caller's responsibility.

All commands reuse existing formatting, units, missing semantics, print mode,
explicit alt/artifact/off and table measurement. The backend scalar contract
covers correlation Heat and metric bars; ablation dumbbells require the native
backend or explicit fallback. The [complete example](examples/domain-reports.tex)
contains all three report types. The [third-party starter](libraries/starter/README.md)
shows how to package similar recipes using public interfaces.
