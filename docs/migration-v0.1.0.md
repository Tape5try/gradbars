# Migrating to gradbars v0.1.0

Existing documents can keep `\usepackage{gradbars}` and all previous public
commands. Full loading remains the default. Raw-number, missing-value, scale,
sorting, tie, aggregation and percentage rules are retained from v0.0.8.

## Install the complete runtime

The package is now a set of fourteen runtime `.sty` files. Install the release
together through the distribution, or place all `gradbars*.sty` files from `sty/` beside the
main document/in the same local TEXMF package directory. Replacing only
`gradbars.sty` is insufficient. Do not mix release versions; the loader reports
mismatched native modules. TeX Live repositories may lag behind this local release.

## Optional loading

```latex
\usepackage[libraries=none]{gradbars}
\usegradbarslibrary{stack,spark}
```

Core includes ordinary bars, comparisons/ranges, reference/quality controls and
legends. Optional libraries are `stack`, `spark`, `heat`, `csv`, `table`.
Package option `libraries={heat,spark}` is equivalent to selecting those libraries
explicitly. Table brings all its dependencies automatically. Put loading in the
preamble. Attempting an unloaded frontend gives an actionable library message.

## Settings and extensions

`\gradbarsset` and `\gradbarssetup` share grouping and option precedence.
New callback registration interfaces are experimental; use the
[developer reference](developer.md) rather than private variables. Custom scalar
renderers use `\gradgraphic`; custom number formatters do not support decimal
alignment. Existing native table types and SI formatting remain unchanged.

## Documentation and release workflow

Chinese/English manuals retain separate Chapter files. Code examples and inline
commands share a `\ttfamily` typography definition. Use `l3build doc` (or the
documented l3build/latexmk workflow) for full builds. Restore full includes before packaging.
The historical builder used `gradbars_CTAN/gradbars-0.1.0.zip`; the current native `l3build ctan` target writes `gradbars-ctan.zip`.

This release does not yet provide `\UseTblrLibrary{gradbars}`. The tabularray
library remains the main v0.1.1 milestone; the next new preset style is scheduled
with that second functional-theme update. v0.0.9 was cancelled and folded into
this release. Long-term API freezing remains a separate v1.0.0 milestone.
