# Version 1 Stability Contract

This contract applies to the documented public interfaces of gradbars 1.2.3,
including the former local 1.3.0/1.4.0 plans and preserved 1.2.0, 1.1.1, 1.1.0 and 1.0.0 contracts.
It covers their arguments, option meaning, scope, library dependencies, data
semantics and documented errors. It does not promise identical PDF bytes,
font metrics across engines, compilation speed or private implementation names.

## Supported Environment

The supported baseline is LaTeX 2025-11-01 or newer with expl3 2025-12-29 or
newer and PGF/TikZ 3.1.11a or newer. pdfLaTeX, XeLaTeX and LuaLaTeX are supported
for PDF output. These requirements are based on the tested TeX Live installation
rather than the older, unverified 2020 minimum. Optional siunitx formatting
requires siunitx v3 loaded explicitly. Chinese manual builds require XeLaTeX and
ctex/Fandol. texlua, l3build and latexmk are build tools; no Python files are required.

## Stable Public Interfaces

| Family | Public interfaces |
| --- | --- |
| Settings | `\gradbarssetup`, its alias `\gradbarsset`, `\gradbarsstyle`, `\gradscale` |
| Graphics | `\gradbar`, `\gradsignedbar`, `\gradstack`, `\gradspark`, `\gradsparktarget`, `\gradsparkband`, `\gradsparkcompare`, `\gradheat`, `\gradcompare`, `\graddumbbell`, `\gradrange`, `\gradbullet`, `\gradintervals` |
| Numeric input | `\gradbarsparsenumber` (explicit, locally assigned canonical output) |
| Categories | `\gradbarscategory`, `\gradbarslegend`, `\gradtablelegend`, `\gradtablelegendhead` |
| CSV and existing tables | `\gradbarsloadcsv`, `\gradbarcsv`, `\gradbarscsvcell`, `\gradbarscsvstyle`, `\gradbarscsvtable`, `\gradbarscolumn` (including `*`), `\gradbarshead` |
| Native tables | `gradtable`, `\gradcolumn`, `\gradrow`, `\gradsummary`, `\gradgroup`, `\gradheader`, `\gradspan`, `\gradtablestyle`, `\gradtableschema`, `\graduseschema` |
| Library extensions | `\gradbarsdeclarelibrary`, `\usegradbarslibrary`, `\gradbarsiflibraryloaded` |
| Command declarations | `\gradbarsnewcommand` (v1.2.3) |
| Scalar extensions | `\gradbarsdeclaretype`, `\gradgraphic` |
| Formatter extensions | `\gradbarsdeclareformatter`, `\gradbarsformatnumber` |
| Optional tabularray integration | `\gradtblrsetup`, `\gradtblrcell`, `\gradbarTblr`, `\gradheatTblr`, `\gradnumberTblr`, `\gradcompareTblr`, G/H/N/D columns and `gradtblr` |

The [API reference](api.md) and bilingual manuals define arguments, native column
types, keys and defaults. `/gradbars` uses pgfkeys for graphic settings; package
loading options and typed table declarations retain their separate interfaces.
A pgfkeys `.store in` target is a macro, never an expl3 typed register. Internal
`gradbars@...`, `gradtable...`, `\__gradbars_...`, module file names and callback
implementation names are private.

## Loading and Precedence

Default loading includes the five feature libraries. `libraries=none` retains
core and the public API; explicit lists select features. `core` is always loaded.
`table` requires `stack`, `spark`, `heat` and `csv`, which each require core.
Register/load libraries in the preamble. Registrations are global; duplicate
names are errors and loading is idempotent. Names begin with a lower-case letter
and contain only lower-case letters, digits and hyphens.

Settings, graphic styles and per-call options follow ordinary TeX grouping.
Keys apply left to right: put explicit overrides after a style or theme.
A named scale group resolves the range after graphic options. Table defaults
precede column settings and drawing options; allocated dimensions and resolved
table scales are applied by the table adapter. Extensions do not change this
precedence implicitly.

## Data and Callback Semantics

Raw numbers feed sorting, ranking, aggregation and automatic descriptions.
Formatting never becomes data. Decimal/scientific literals retain the documented
precision and magnitude bounds. Missing and zero are distinct. Signed stack
subtotals, ties, lower-is-better metrics, percent denominators, clipping and CSV
selection order retain their documented meaning.

Scalar callbacks receive one canonical numeric value or `NA`. `\gradbar` accepts
empty input as missing; `\gradgraphic` uses explicit `NA`. Custom scalar callbacks
do not add native table column types. Delegate to public drawing commands for
scales and tagging; the dispatcher adds no extra description. Builtin `bar` and
`heat` names cannot be replaced.

Formatters receive display value, precision and number-format mode. They render
only the number; the engine adds units or percent suffixes. The number helper
defaults to builtin formatting, preventing callback recursion. Custom output is
opaque and cannot use decimal alignment. Semantic `unit code` retains its
siunitx requirement. Missing values bypass formatter callbacks.

## Compatibility and Deprecation

Version 1 patches fix errors and documentation while preserving the contract.
Compatible options, libraries, graphics or presets use a new minor version.
Removal, changed defaults or changed data meaning requires a new major version.
A bug contradicting this contract may be fixed in a patch; the changelog must
describe any resulting numeric or visible output change.

For the explicitly requested v1.1.1 development update, the opt-in
`\gradtablelegend` and `\gradtablelegendhead` commands and their documented
`/gradbars` keys are an additive exception to the usual minor-release policy.
This does not change that policy for subsequent work. They are available in
core, render only when explicitly called, and preserve existing loading,
category mappings, bar colors, stack legends and data semantics. Their title
is ordinary text outside the category Figure; existing accessibility/backend
rules continue to apply. See [the table-legend contract](legends.md#horizontal-table-header-legends).

For this same unreleased v1.1.1 development update, the maintainer explicitly
requested complementary negative colors for all eleven explicitly selected bar
themes. This is a documented visual exception: themes now reset both signs,
including negative endpoints and fill mode. Without an explicit theme, the
historical solid lightred negative default remains. Left-to-right overrides, grouping,
print and threshold precedence, positive colors and data semantics remain.
See [the theme and signed-observation interfaces](api.md). This exception does not relax the
major-version rule for other default changes.

The explicitly requested built-in `\gradsignedbar[options]{negative}{positive}`
is also an additive exception for this unreleased development update. It is in
core, renders two independent signed observations on one track, preserves the
scalar `\gradbar` contract and uses native compound backend kind `signed-bar`.
Its exact bounds, missing-value and label rules are in [the API](api.md).

A deprecated public interface remains available throughout version 1. Its
replacement and migration example are documented before removal in a later major
version. No public interface is deprecated in 1.0.0. Private functions may change
without notice. Install all matching modules together; mixing versions is
unsupported and diagnosed by the loader.

## Accessibility and Integration Boundaries

`alt` replaces the raw-data description. `text` changes the visible label only.
`accessibility=artifact` marks decoration; `off` leaves tagging to surrounding
code. An outer TikZ picture owns the whole-picture description. Table measurement
suspends tags to avoid duplicate descriptions. These features do not certify a
complete table or document as PDF/UA conformant.

PGF/TikZ remains the sole supplied drawing implementation. Schema-1 scalar backend
registration and read-only records are public; private model storage remains
private. See [the backend contract](backends.md). Unsupported compound/legend
requests require explicit native fallback.
The optional tabularray 2025C+ adapter loads with `\UseTblrLibrary{gradbars}`;
its documented commands and columns are stable. It does not load with the five
native feature libraries, modify ordinary tblr defaults, or add native table
statistics to tblr. Header text must be protected from numeric column commands.
The opt-in `\gradtblrtagging` interface supplies Table/TR/TH/TD, Scope/span and
explicit multilevel Headers-ID associations; short tagged tables are tested on
all three engines. Tagged longtblr with repeated headers or footers requires
LuaLaTeX, with artifact or explicitly described repeated-header modes. Nested
tagged tables and cross-page spanning cells remain outside the verified scope;
structural tests do not certify screen-reader behavior or whole-document PDF/UA
conformance. See [accessibility.md](accessibility.md) for the exact boundaries.
pgfplots and pgfplotstable may contain ordinary inline graphics but have no
dedicated supplied adapter.

## Version 1.1 additions

Distribution and shared-legend commands, new native boxplot columns, accessible
styles/palettes, new tabularray helpers/columns and explicit table-tagging settings
are covered by their documented contracts in [distributions.md](distributions.md),
[legends.md](legends.md) and [accessibility.md](accessibility.md). Unsupported
combinations are diagnosed. Private tagging hooks and viewer-level behavior are
not a universal table-tagging protocol. No interface is deprecated in 1.1.0.

## Domain and contributor interfaces

The opt-in reports commands/styles are documented in [reports.md](reports.md).
The semantic version query/guard and schema-1 backend commands are public.
The [starter](libraries/starter/README.md) uses public interfaces only.

## Version 1.2 additions

All [readability options](readability.md) are explicit. Legacy legend layout and center-point contrast remain defaults. The spark-target entry has independent reference data and fixed/named scale requirements; it does not relax old spark diagnostics or create new scalar table records. Unsupported area rendering and opaque duplicate checks are diagnosed.

## v1.3.0 / v1.4.0 explicit additions

[Regional input](regional-input.md) is an opt-in helper/CSV scalar-column layer; strict existing inputs do not guess separators. Normalization precedes existing selection, scales, ranking and aggregation; output formatters never provide data.

[Two-level CSV grouping](hierarchical-tables.md) is a separate entry with structured parent/leaf paths. Legacy single-level group keys retain their meaning. Global selection precedes grouping; parent/leaf ranks use selected raw values, summaries have independent explicit scopes, and neither adds hidden per-group scales.

[Fixed-band and endpoint/trend compositions](trend-compositions.md) require explicit ranges and preserve NA positions. New native backend kinds require native support or explicit TikZ fallback; schema stays 1. Native trendcompare columns are compound inputs, not arbitrary scalar adapters. Pagination keeps apply when each indivisible chain fits the page. No expanded PDF/UA Table claim is made.

## v1.2.1 adapters and metric contract

The maintainer requests actual version 1.2.1 for the former 1.5.0/1.6.0 plans,
retaining the earlier local planned features. Public numeric version comparisons
use 1.2.1. This is an explicit numbering exception, not a general patch feature policy.

New [column declarations](column-adapters.md) are scoped and separate from old
standalone types. Table callbacks require fixed/repeatable layout and no external
side effects; this admission rule does not retroactively constrain independent
callbacks. New [pgfplotstable cells](pgfplotstable.md) are optional and preserve
the host reader/header contract, without claiming native CSV safety or table tags.

New [report metric declarations](report-metrics.md) are scoped, explicit and
scalar. They freeze range/group identity, unit, direction and numeric formatting;
no role-based computation, implicit units or conversion is introduced. Raw values
remain authoritative for selection/ranks/summaries, count suppresses units. History
is positional; final NA remains current missing. Rug multiplicity/type-7 statistics
are preserved with an explicit 2048-position limit. Each combination has one Figure;
measurement creates no duplicates. Prior unbound report commands/defaults remain.

## v1.2.3 extension compatibility

`\gradbarsnewcommand` follows local scope and existing frontend semantics; opt-in
label positioning retains legacy modes. Numeric pairs use a separate global
registry and scoped record version 1, without adding fields to scalar backend
schema 1. Standard native pair columns are explicit, scoped declarations; old
scalar columns do not acquire compound input. The default five libraries and
numeric meanings remain unchanged. See [command declarations](api.md#command-declarations)
and the [pair contract](pair-extensions.md).
