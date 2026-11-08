# Changelog

## 1.2.2 — 2026-11-07

GitHub source delivery; no release tag, GitHub Release or CTAN submission.

- Compute each group's best and second distinct values in one ranking pass instead of two, preserving table/parent/leaf ranking, ties, missing values and higher/lower directions. No public API, default or numeric meaning changes.
- Add a bounded TeX/Lua benchmark with immutable runtime/data identities, individual samples, first/subsequent process measurements and phase medians for parsing, statistics, ranking, measurement and the complete bar path. Do not claim flushed OS caches, pure drawing timings or measured OS peak memory.
- Add regression assertions for distinct ranks, negative/zero/missing values, group isolation and CSV reloads. Retain existing hierarchy, pagination and PDF checks. No cross-call or formatter/box cache is added.
- Keep static/PDF runner Lua font caches under their build directories so restricted environments do not require a writable global TeX cache; benchmark runs also use a local cache.
- Synchronize all 23 runtime modules and bilingual documentation; see [performance notes](docs/performance.md).

## 1.2.1 — 2026-11-07

Local development only. The maintainer explicitly requested this patch-numbered
feature snapshot: it includes the former v1.5.0/v1.6.0 roadmap scopes, retaining
the prior local v1.3.0/v1.4.0 implementation. Those labels were local plans, not
separately published releases. No GitHub upload, tag, Release or CTAN archive/submission.

- Add explicit, scoped native scalar column adapters with declared raw selection/rank/aggregate capabilities, standard frontend proxies, fixed-box dimensions and a repeatable measurement contract. Preserve independent scalar callback behavior.
- Add an optional pgfplotstable library for body-cell bars, heat and numbers, protected host headers, explicit missing mappings and total width checks. Keep the original default library list.
- Add one raw distribution composition: box plus every valid sample rug, duplicates retained, type-7/IQR statistics unchanged, explicit 2048-position bound, no summary-only input.
- Add scoped report metric declarations and explicit standalone/native bindings, frozen units/direction/format/range/group identity, source binding at use, raw statistics and preserved count semantics.
- Add one report composition: final-position current bar plus complete history trend, with no fallback at final NA, shared metric/range/unit, explicit panel budgets and one combined Figure. History is not scalar summary data.
- Compare resolved shared-legend signatures without re-expanding formatting macros, avoiding false conflicts for identical unit macros. Freeze explicit metric percent denominators as part of numeric formatting.
- Add three table presets, public-only extensions, bilingual manuals/examples and numeric/error/PDF/pagination tests. All 23 runtime modules are v1.2.1; backend schema remains 1.


## Former 1.4.0 plan — 2026-11-07

Local development update only; not uploaded to GitHub/CTAN and not released.

- Add explicit CSV `group levels={parent,leaf}` with structured literal paths, source-appearance group order, parent/leaf ranks and independent visible/data summaries. Preserve global selection order and old single-level behavior.
- Add the hierarchical native-table preset and actual-page longtable checks for heading/summary keep chains across four rule modes.
- Add `\gradsparkcompare` and native `type=trendcompare`: same-series first/last dumbbell plus full trend, shared value range/unit, explicit panel dimensions and missing-endpoint semantics, one Figure alternative.
- Synchronize bilingual manuals, standalone project review/longtable examples and API/stability/developer contracts. All 22 runtime modules are v1.4.0; backend schema stays 1.

## Former 1.3.0 plan — 2026-11-07

Implemented locally as part of the v1.4.0 development snapshot; not published separately.

- Add `\gradbarsparsenumber` and opt-in CSV scalar-column decimal/grouping rules. Validate grouping, then reuse the strict canonical validator before geometry/selection/statistics; text fields, CSV safety, units and output formatting remain independent.
- Add `\gradsparkband` for a line series with a fixed reference interval and explicit range. Reference bounds do not become observations or an inferred confidence interval.
- Add the regional native-table preset, bilingual purchase/circulation examples and input/error/scope regressions. Existing scalar and spark input defaults remain.

## 1.2.0 — 2026-11-03

Development snapshot; repository update only, without a GitHub Release or CTAN package/submission.

- Add opt-in measured continuous-legend layouts and builtin numeric duplicate diagnostics, shared-legend overrides, and one formatter call per measured tick. Preserve legacy two-row layout by default.
- Add opt-in conservative label-area contrast bounds for rectangular scalar bars, declared canvas and band compositing, explicit failure warnings or white panels. Preserve center estimation and explicit color precedence; document unsupported rendering effects.
- Add exactly one combination, `\gradsparktarget[options]{series}{target}`, with fixed/named scales, separate reference semantics, missing-position preservation, one Figure description and explicit native backend fallback. The old spark target error remains.
- Gate CTAN archives, release artifacts and publication to explicit tag builds; ordinary branch pushes run tests and documentation builds only.
- Add readable graphic/native-table presets, bilingual executable examples/manuals and numerical, error, callback and actual-PDF regressions. Synchronize all 22 modules at v1.2.0; backend schema remains 1.

## 1.1.1 — 2026-10-27

Development snapshot; no v1.1.1 release has been published.

- Clarify issue #4: ordinary numeric cells align with graphic labels only after explicitly selecting `baseline=text`, already supported in v1.1.0; the legacy `auto` default is preserved. Add the exact minimal table and output-position regressions rather than treating a version upgrade as an automatic alignment fix.
- Add explicitly requested core `\gradsignedbar[options]{negative}{positive}` with a shared track/zero, independent missing values and uncertainty, combined formatted labels, one automatic Figure description and explicit scalar-backend fallback. Rebuild all theme galleries using the built-in command.
- At the maintainer's explicit request, all eleven explicitly selected bar themes now set complementary negative colors (RGB channel inversion), with gradient/solid modes matching the theme. This visibly changes themed negatives; unthemed defaults remain solid lightred. Retain left-to-right custom overrides, threshold/print precedence and numeric semantics; include a full signed gallery and migration examples.
- Preserve all public interfaces, the five-library default load list and existing numeric, missing-value, ranking and aggregation semantics. Synchronize all 22 runtime module versions.
- Add the explicitly requested opt-in `\gradtablelegend` horizontal category row and `\gradtablelegendhead` title/legend assembly. The scoped `table legend` switch hides the row without leaving a gap below the title; colors, typography, swatches, spacing and borders are configurable. Reuse category mappings, print patterns, alternative text and explicit backend fallback; retain older vertical and automatic stack legends.
- Add bilingual complete table examples for course completion, library borrowing channels, building energy use and production-batch dimensions, with independently compilable sources using existing interfaces.
- Make source extraction and l3build unpacking work when the CTAN source archive no longer contains `sty/` or its README marker. Keep direct plain-TeX extraction diagnostics explicit when the output directory is unavailable.
- Separate the development regression suite from source packages that omit `tests/`; do not report an empty package check as a successful regression run.
- Preserve source timestamps, normalize CTAN archive permissions, reject unwanted paths, repeated filenames and duplicate contents, and record the MIT package / CC BY-SA 4.0 adapted-example license scopes in upload metadata.
- Keep the existing bilingual chapter suffixes and starter-checker rename, repair stale migration links, and correct the documented tagging/backend support boundaries. Add maintenance and documentation-reference checks.
- Continuous Heat legends retain the current worktree's decorative semitransparent white separators between 256 sampled color strips, in both orientations and print mode. This changes the visible ramp texture compared with v1.1.0; the underlying Heat interpolation, scale, ticks and alternative text remain unchanged. The separators are not category or bin boundaries.

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
