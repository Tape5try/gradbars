# Changelog

## 0.0.3 — 2026-10-03

- English manual with executable examples, and versioned bilingual PDF documentation.
- Cross-engine validation: pdfLaTeX, XeLaTeX and LuaLaTeX; fix UTF-8 BOM handling in pdfTeX CSV input.
- LF text policy via .gitattributes.

- Dumbbell comparisons and optional current-minus-reference labels.
- Signed stacks with independent positive/negative accumulation and subtotals.
- Segment shares use absolute contributions, including zero-net compositions.
- Sparklines with missing gaps, extrema/last markers and fixed or automatic ranges.
- Target-distance and acceptable-interval quality rules, with inclusive distance boundaries.
- Categorical, sequential, diverging and monochrome palettes; scoped named category colors and patterns.
- Six-part manual with 56 numbered examples, three additional complete application tables and an interface index.
- Updated bilingual READMEs, feature overview and release notes.


## 0.0.2 — 2026-10-02

- Stack names, automatic/shared legends, segment values and percentages.
- Small segment labels move outside with leader lines and collision avoidance.
- Automatic total label placement, black/white text, and long-label handling.
- Numeric table columns via `\gradbarscolumn`, with common options and missing values.
- Selection guide and FAQ covering label width, row height, shared scales and missing data.
- Four real layout cases: two-column article, multi-page longtable, grayscale and Beamer.
- CSV loading, named-column access, missing-token mapping and shared column range styles.
- Black-and-white patterns for bars and legends, with white backgrounds behind print labels.
- `better=higher|lower` reverses threshold quality colors without changing geometry.
- Unified manual with 42 numbered examples; build script and CI rebuild the real layouts first.
- New dependency: collcell (and its array/etoolbox dependencies).

## 0.0.1 — 2026-10-02

Initial public version.

- Unified scoped configuration with `\gradbarssetup` and `\gradbar`.
- Seven themes and nine built-in colors for inline and table data bars.
- Raw values, computed percentages, custom labels, and input validation.
- Rounded corners, target lines, conditional colors, and endpoint labels.
- Signed bars and symmetric/asymmetric error whiskers.
- Illustrated Chinese manual, bilingual READMEs, and three complete examples.
- GitHub Actions builds the XeLaTeX manual.

- Named styles, explicit missing values, and scientific/grouped number labels.
- Reference bands and nonnegative stacked bars with shared scales.
- Six additional illustrated examples in the single manual.
