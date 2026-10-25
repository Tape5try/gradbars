# Changelog

## 1.1.0 — 2026-10-25

- Add the opt-in reports library with correlation, ablation and metrics presets and column recipes. Preserve raw numeric meanings and explicit metric directions.
- Add a schema-1 public scalar backend contract with registration, capability negotiation, scoped read-only records, a native continuation and explicit error/TikZ fallback for unsupported kinds. The supplied drawing implementation remains TikZ.
- Add semantic version queries/requirements and an independently testable public-only third-party starter. Keep the default five-library load list unchanged.

- Extend the existing collected-column interface with `\gradbarscolumn*` for compact centered labels, explicit blank-cell spacing and unused column-name checks; retain the unstarred behavior. Add `\gradbarshead` and a complete Precision/Recall example so ordinary table data contain only numbers.

- Add eight named Heat palettes: blue, teal, purple, orange, purple-teal, blue-red, orange-blue and brown-teal. Reuse the same resolved colors in standalone Heat cells, columns and shared legends; preserve old defaults and explicit color overrides.

- Add `legend missing=true|false` to continuous and shared legends; keep true by default. Hiding the item also removes its automatic missing-value description.

- Fix constant automatic scales when the numeric engine rounds both +/-0.5 endpoints to the same value (for example 1e100). Preserve normal +/-0.5 bounds; only collapsed intervals use a bounded 5% span, preventing an invalid zero-width scale.
- Add opt-in distribution statistics, type-7 quartiles, observed 1.5 IQR whiskers, raw/precomputed box plots, complete descriptions, native boxplot columns and distribution/accessible table styles. Keep sample counts and unknown precomputed counts distinct.
- Add opt-in continuous, shared categorical and reference legends. Freeze explicit scales through core named-scale resolution (including auto box/spark modes), color roles, units, percentage bases and direction; reject conflicts and semantic overrides at legend rendering.
- Add accessible color roles and sequential/diverging Heat palettes. Retain old defaults, print behavior and the five default libraries.
- Extend tabularray with J/R/V/K/U/B columns and matching helpers for dumbbell/range/spark/stack/bullet/boxplot. Load their libraries in the adapter preamble and reserve spark/dumbbell marker stroke width, including points exactly at scale endpoints.
- Add explicit table structure with captions, logical row order, scoped headers and spans. Repeated tagged longtblr headers require LuaLaTeX and become artifacts after the first page. Opt-in per-page descriptions rebuild fresh content under the original logical cells; explicit multilevel Headers-ID links validate real header cells and reject cycles. Cross-page spans, nested tables and viewer-level certification remain outside this delivery.
- Add three-engine numerical/error/PDF-structure regressions and bilingual chapters. CTAN submission is separate from this GitHub release.

## 0.0.4 — 2026-10-04

### Follow-up fixes — 2026-10-06

- Generate automatic alternative text for standalone graphics and legends when LaTeX PDF tagging is active. Descriptions retain raw values, units, scales, comparison differences, stack segments and subtotals, interval endpoints, and missing spark observations.
- Add `alt={...}` for context-specific descriptions, retaining compatibility with `/tikz/alt`.
- Add `accessibility=auto|artifact|off`; tagging remains opt-in through the document's `\DocumentMetadata` configuration.
- Suspend tagging during discarded table-measurement passes, preventing duplicate graphic descriptions in the PDF structure tree.
- Document tagging usage and limitations in both manuals and READMEs. Graphics inside an existing TikZ picture rely on the outer picture's description; document-wide PDF/UA conformance still requires separate validation.
- Verify the reported example and extended PDF structures with pdfLaTeX and XeLaTeX, plus 30 table regression cases.

### Features and documentation

- Introduce `gradtable` with declarative `\gradcolumn` and `\gradrow` interfaces and nine column types: text, number, bar, bullet, interval, compare, dumbbell, stack and spark.
- Add cell and header alignment, vertical text alignment, four rule styles, header/rule colors, and configurable row and column spacing.
- Allocate a specified total table width across fixed and weighted flexible columns, measuring numeric labels consistently within each column.
- Add multilevel headers and horizontal spans with `\gradheader` and `\gradspan`, plus grouped rows with `\gradgroup`.
- Mark best and second-best values using raw data, supporting ties, missing values and higher/lower metric directions across the entire table.
- Reuse table options and column declarations through named table styles and schemas.
- Support multipage tables with `long=true`, repeated complete headers, captions and references, consistent widths/ranking, and group headings kept with their first data row.
- Add multiple named reference lines, bullet charts and grouped interval comparisons.
- Add overflow indicators, configurable marker shapes/fills, difference arrows/brackets and relative-change labels.
- Reorganize the Chinese manual into six parts, 42 chapters and 77 numbered examples; update the English manual to six parts and 28 sections.
- Refresh the cover with rendered output beside its source and compact the contents layout.
- Make the default GitHub README Chinese, with a separate `README.en.md` and updated v0.0.4 manual links.

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
