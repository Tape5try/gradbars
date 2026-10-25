# Distribution statistics and box plots

Load `\usegradbarslibrary{distribution}` in the preamble. This optional library
does not change the five version-1 default libraries. It supports all three engines.

```latex
\gradboxplot[width=45mm,palette=accessible]{0,1,2,3,100}
\gradboxsummary[width=45mm]{n=5,q1=1,median=2,q3=3,low=0,high=3,outliers={100}}
\gradsummarytext{0,1,2,3,100}
\gradcomputesummary{0,1,2,3,100}{n=\gradstat{n}; median=\gradstat{median}}
```

`\gradcomputesummary{samples}{callback}` computes a scoped record. Inside its
callback, the expandable `\gradstat{field}` reads `n`, `missing`, `min`, `max`,
`mean`, `q1`, `median`, `q3`, `iqr`, `low`, `high`, `outliers`, `outlier count`
and `method`. The record does not escape the callback's TeX group. The text helper
shows n, missing count, quartiles, IQR, observed whiskers and outlier count.

The sample input is a comma-separated list; empty fields and literal `NA` are
missing and zeros are observations. An entirely empty list has n=0, missing=0.
All other values use the existing strict decimal/scientific parser. Expressions,
NaN and infinity are rejected. Arithmetic uses the existing approximately
16 significant digits, independently of label precision. No observations are
removed because they are outliers.

For sorted valid observations x[1]...x[n], type-7 quantiles use
h=1+(n-1)p, j=floor(h), g=h-j and Q(p)=(1-g)x[j]+g*x[j+1], with x[n] at h=n.
Q1/median/Q3 use p=.25/.5/.75. This is the
[type-7 definition in the R statistics manual](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html),
not Tukey hinges. IQR=Q3-Q1. Whiskers are the most extreme **observed** values
inside [Q1-1.5 IQR, Q3+1.5 IQR], inclusive. Points outside are drawn as hollow
circles. Coincident observations overlap visually but retain their count and
complete list in the description. This is not a confidence interval.

n=0 draws the missing marker and returns NA for numeric statistics; n=1 has
identical quartiles/whiskers; n=2 uses the same interpolation formula. Constant
samples and IQR=0 do not change the algorithm. No weights, notches, jitter,
random subsampling or alternate quantile conventions are supported.

`\gradboxsummary` requires named n/q1/median/q3/low/high. n must be positive;
low<=q1<=median<=q3<=high. Optional `missing`, `min`, `max`, `mean` and `outliers`
are validated when supplied. Missing count and outlier count remain **unknown**
when not supplied. With no raw data, the algorithm and the most extreme in-fence
observations cannot be verified. Do not invent counts or claim an inferred
population. Without optional extrema, drawing limits use the supplied whiskers
and outliers; they are not described as verified sample extrema.

Standalone plots use `box range=auto` by default, expanding a constant range
only for drawing. The normal +/-0.5 expansion is retained; when both endpoints
round to the same value at very large magnitudes, use a 5% interval bounded by
the supported +/-1e100 limits. `box range=fixed` uses min/max; `scale group` takes priority.
Overflow uses the existing clip/error contract and descriptions keep raw values.
`value format=percent` is rejected. The default label is none; requesting a
label displays the median in a right-hand slot. Width/height/font, literal and
semantic units, explicit alt and artifact/off are supported. Box plots use
height=3ex unless overridden and are standalone pictures; wrap an outer TikZ
picture with its own description when composing pictures.

Native `gradtable` accepts `type=boxplot` after loading the distribution library.
A row uses `\gradrow{Method,{0,1,2,3,100}}`; a quoted CSV field contains the same
sample list. `scale=column` scans all valid observations, including outliers,
using the table's data/visible scope, include-zero, padding and nice policies.
Filtering/limit selects rows and never subsets an individual cell's samples.
Box columns cannot be ranked, filtered numerically or aggregated as scalars.
They do not silently combine samples across rows.

`style=distribution` adds a 45mm graphic width, booktabs rules, row stretch 1.6,
8pt separation and 3pt padding. `style=accessible` uses row rules, 1.4 stretch,
7pt separation, 2pt padding and the accessible table theme. Both are opt-in.
