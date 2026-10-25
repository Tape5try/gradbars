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

## 1.0.0 — 2026-10-30

### Compatibility, Libraries, and API Architecture

- Establish the version 1 compatibility and deprecation contract for documented commands, graphic keys, data semantics, native table interfaces, library dependencies and scalar/formatter registrations. Preserve existing signatures and defaults; private variables and internal modules remain outside the contract.
- Add a private model module for validation and normalized geometry preparation, separating that responsibility from the default TikZ backend. Retain raw values independently from display labels and keep font-relative coordinate projection in the drawing context. Install all fifteen matching runtime modules together.
- Replace the previously unverified 2020 LaTeX minimum with the supported, tested baseline: LaTeX 2025-11-01, expl3 2025-12-29 and PGF/TikZ 3.1.11a or newer. Update older distributions before upgrading; siunitx v3 remains explicitly optional.
- Split the runtime into core/key/numeric/TikZ/tagging/API layers, optional stack/spark/heat/CSV/table libraries and private table-data/layout helpers. Preserve default complete loading and the v0.0.8 public commands/data semantics; require installing the complete matching module set.
- Add `libraries=none` or explicit package library lists, `\usegradbarslibrary`, global library registration, dependency resolution, repeated-load protection and clear unknown/missing/cycle/version diagnostics. The table library loads its graphic/data dependencies; optional SI formatting remains explicit.
- Add scoped `\gradbarsset` and experimental public scalar-renderer/number-formatter callbacks with a public-only contributed library and migration/developer documentation. Opaque formatters do not support decimal alignment, and registered scalar types do not alter native table type enums.
- Separate table selection/ranking/aggregation from table layout and consolidate numeric validation into the shared predicate. Add semantic l3build tests alongside the existing detailed three-engine suite, isolated release checks and a fixed-dataset benchmark against v0.0.8.

### Table Features and Styles

- Add the optional `reference` table style with booktabs rules, centered headers, decimal number alignment, row stretch 1.25 and column separation 6pt. Existing styles and themes keep their defaults.
- Include the originally planned v0.1.1 tabularray work in this unreleased v1.0.0: `\UseTblrLibrary{gradbars}` discovers optional `tblrlibgradbars.sty`, requiring tabularray 2025C+. Add scoped adapter defaults, public cell helpers and fixed-width G/H/N/D columns, with numeric/Heat/bar/comparison support, shared scales, unit formatting and longtblr examples.
- Add opt-in `gradtblr` presentation and native `style=matrix`. Suspend tagging through public trial hooks and verify real PDF descriptions for fixed/X cells without measurement duplicates. Install the optional adapter alongside the fifteen base modules; include it in documented-source extraction and isolated installation checks.
- Add scalar column aggregates (`count`, `sum`, `mean`, `min`, `max`) and one `\gradsummary` row with visible/full-data scopes. Missing values are skipped, zero is retained, and numeric summaries do not affect ranks or graphic ranges. Long tables display summaries once with the final data row.
- Add scoped `\gradscale` declarations and `scale group` references for standalone graphics and table columns. Explicit groups override drawing limits and reject conflicting automatic column scales.
- Add automatic-column `scale padding` percentages and `scale nice` bounds with zero anchors and outward 1/2/5 rounding. Preserve the original percent denominator when expanding a range; provide explicit `percent base` overrides.
- Add reusable academic, compact and dashboard table styles, independent blue/teal/violet/orange/forest/mono table themes, matching automatic header/summary fills and table font settings.
- Bind a loaded CSV directly to `gradtable` with `data=dataset` and per-column `source=header`; retain literal text, quoted commas, empty cells and configured missing tokens, with native multicolumn layout and `long=true` pagination.
- Add table/column `scale=fixed|column` and `include zero=true|false`; calculate shared ranges before measurement/ranking/pagination for scalar, pair, interval, signed-stack and spark columns. Column settings override table defaults.
- Support drawing ranges with any `min < max`, including positive-only and negative-only ranges; preserve zero-inclusive defaults and percent-label requirements. Define constant and all-missing fallbacks explicitly.
- Add native CSV table sorting, AND filters and row limits with `sort`, `order`, `filter` and `limit`; use raw decimal sorting, stable ties and missing-last ordering. Text fields support literal equality and character-order sorting.
- Add `scale scope=data|visible`, retaining full-data ranges by default while rankings refer to displayed rows. Selection does not modify the loaded dataset.

### Data Grouping and Sorting

- Add stable lexicographic `sort keys={column/ascending,column/descending}` over declared text/scalar columns. Retain `sort`/`order`, reject conflicting inputs, preserve raw numeric comparisons and input-order ties, and put missing values last for every key.
- Add `group by` for one declared CSV text column. Filter, sort globally and apply the global limit before grouping; groups follow first occurrence in the original CSV and preserve selected order internally. Retain empty groups with a configurable label and treat literal text missing tokens as distinct labels.
- Add `rank scope=group` for automatic or manual groups, retaining table-wide ranks by default, distinct-value ties and higher/lower metrics. Keep column/shared scales comparable across groups.
- Add one numeric summary per displayed group using existing column aggregates, `group summary scope=visible|data`, and a configurable summary label. Skip missing numbers, retain zero and preserve column formatting; overall summary scope is independent. Group headings stay with the first row, and group/overall summaries stay with the last row across pages.

### Graphics, Numerics, and Themes

- Resolve Issue #6 with `label align=cell`: inside/auto labels center across the full graphic content width independently of the filled segment or sign. Keep ordinary graphic alignment and overflow defaults unchanged; reserve space for left labels within allocated cells and diagnose insufficient widths.
- Add `label=left` for formatted labels before the track, baseline presets (`auto`, `text`, `center`, `bottom`) with `baseline shift`, and independent negative gradients through `negative fill`, `negative left color` and `negative right color`. Existing defaults remain unchanged.
- Add optional `formatter=siunitx` for standalone graphics and table/column defaults. Require explicit loading of siunitx v3; preserve builtin formatting by default. Map number format/precision to a documented SI subset and retain best-value bold math and second-value underlines.
- Add `number align=decimal` for number columns. Measure signed integer and fractional/exponent/unit portions across displayed data, group summaries and overall summaries; align decimal points using shared widths rather than formatted values as data. Scientific aligned displays use mantissas and powers of ten; display ties round away from zero. Explicit insufficient widths produce an error.
- Add semantic `unit code` with required readable `unit text`, alongside unchanged literal `unit`. Reject conflicting suffixes and semantic units on computed-percent labels. Count summaries suppress units; automatic graphic descriptions use raw values and readable unit text, without extra measurement tags.
- Add the compatible `research` preset table style with decimal number alignment, booktabs rules, centered headings, row padding and group spacing. Support all six existing table themes, missing values, grouped summaries and multipage layouts.
- Add `theme=violet|orange|forest`, pairing violet, warm-orange and forest-green gradients with matching pale tracks; expand the bilingual theme gallery and API reference to ten themes.
- Add `type=heat` and standalone `\gradheat`, continuous endpoint-color interpolation, lower-is-better reversal, automatic black/white text, neutral missing fill, grayscale printing, best/second-best marking and tagged-PDF alternative text.
- Add `heat palette=diverging`, `heat center` and `heat center color`; interpolate each side independently, support asymmetric ranges and boundary centers, and retain neutral missing fills and raw labels.
- Add `spark type=line|bar|winloss`, slot-width controls, win/loss/zero colors, zero-inclusive automatic bar ranges and raw-value labels for categorical win-loss plots.

### Accessibility and PDF Tagging

- Generate automatic alternative text for standalone graphics and legends when LaTeX PDF tagging is active. Descriptions retain raw values, units, scales, comparison differences, stack segments and subtotals, interval endpoints, and missing spark observations.
- Add `alt={...}` for context-specific descriptions, retaining compatibility with `/tikz/alt`.
- Add `accessibility=auto|artifact|off`; tagging remains opt-in through the document's `\DocumentMetadata` configuration.
- Suspend tagging during discarded table-measurement passes, preventing duplicate graphic descriptions in the PDF structure tree.
- Document tagging usage and limitations in both manuals and READMEs. Graphics inside an existing TikZ picture rely on the outer picture's description; document-wide PDF/UA conformance still requires separate validation.
- Verify the reported example and extended PDF structures with pdfLaTeX and XeLaTeX, plus 30 table regression cases.

### Documentation, Build, and Testing

- Add reproducible `gradbars.dtx`/`gradbars.ins` distribution sources, an l3doc source guide, a docstrip round-trip checker and migration/stability documentation. Keep editable runtime files in `sty/` and regenerate documented source after changes.
- Extend regression coverage for the model boundary, callback counts/scope, style recursion, invalid keys and the reference style. Add a Tagged PDF structure check for raw precision, explicit/outer alternative text, artifact/off behavior and measurement suppression; run it in CI with current TeX Live.
- Update bilingual manuals with independent tabularray chapters, README artwork and build metadata.
- Centralize manual code typography in a shared ttfamily definition and mark literal option/command prose as code. Keep bilingual Chapter sources, add library/API chapters, and connect l3build doc/ctan to the checked builders and the required gradbars_CTAN archive naming.
- Resolve the documentation typography issue from GitHub Issue #3: package names use sans-serif styling and code-facing material uses the shared monospaced definition.
- The cancelled v0.0.9 refactoring scope is included in this release. The tabularray integration and preset style originally planned for v0.1.1 are now included in v1.0.0, together with the stable API contract.
- Split the Chinese manual into 46 Chapter/*.tex files and the English manual into 32 Chapter/en/*.tex files. Main documents include each complete section; the builder prepares auxiliary directories and the archive validator checks included sources. Keep all examples and document the full/partial build workflow.
- Document TeX Live/tlmgr installation, package updates and information queries in both READMEs and manuals; distinguish repository versions from local releases and explain project-local file precedence.
- Accept decimal and e/E scientific literals through one shared numeric predicate in graphics, CSV operations, ranges, ranking and aggregates. Retain original input for calculation and descriptions. Reject expressions, locale separators, NaN/infinity and malformed exponents. Explicitly bound nonzero magnitudes to 1e-100 through 1e100 and document expl3's finite precision and input-length limits.
- Add precision/time and mixed-magnitude examples in the corresponding bilingual chapters, semantic-unit/tagging fixtures, scientific-equivalence assertions and rendered decimal-position checks. Keep the CTAN archive in gradbars_CTAN/gradbars-0.0.8.zip.
- Add algorithm-family and grouped-experiment datasets, bilingual examples in their functional chapters, group-statistic assertions and multipage verification. Existing styles and themes remain available; the next preset table style is scheduled for v0.0.8 after the second functional-theme update.
- Expand tests for summary statistics, empty/missing/filtered data, named-scale scope, padding and percent semantics, style/theme combinations, and multipage summaries. Add a checked CTAN release builder and bilingual examples in the corresponding feature chapters.
- Document the three interfaces in both READMEs, bilingual illustrated manuals and the API reference; add portable three-engine regression tests and CI coverage.
- Extend three-engine regression coverage with selection/range assertions, exact heat-color checks, signed and missing spark observations, sorted multipage tables and expected errors. Update each feature's existing chapter in both manuals.

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