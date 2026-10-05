# Changelog

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
