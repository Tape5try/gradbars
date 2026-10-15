# Version 1 Stability Contract

This contract applies to the documented public interfaces of gradbars 1.0.0.
It covers their arguments, option meaning, scope, library dependencies, data
semantics and documented errors. It does not promise identical PDF bytes,
font metrics across engines, compilation speed or private implementation names.

## Supported Environment

The supported baseline is LaTeX 2025-11-01 or newer with expl3 2025-12-29 or
newer and PGF/TikZ 3.1.11a or newer. pdfLaTeX, XeLaTeX and LuaLaTeX are supported
for PDF output. These requirements are based on the tested TeX Live installation
rather than the older, unverified 2020 minimum. Optional siunitx formatting
requires siunitx v3 loaded explicitly. Chinese manual builds require XeLaTeX and
ctex/Fandol. Python, pypdf and l3build are development tools only.

## Stable Public Interfaces

| Family | Public interfaces |
| --- | --- |
| Settings | `\gradbarssetup`, its alias `\gradbarsset`, `\gradbarsstyle`, `\gradscale` |
| Graphics | `\gradbar`, `\gradstack`, `\gradspark`, `\gradheat`, `\gradcompare`, `\graddumbbell`, `\gradrange`, `\gradbullet`, `\gradintervals` |
| Categories | `\gradbarscategory`, `\gradbarslegend` |
| CSV and existing tables | `\gradbarsloadcsv`, `\gradbarcsv`, `\gradbarscsvcell`, `\gradbarscsvstyle`, `\gradbarscsvtable`, `\gradbarscolumn` |
| Native tables | `gradtable`, `\gradcolumn`, `\gradrow`, `\gradsummary`, `\gradgroup`, `\gradheader`, `\gradspan`, `\gradtablestyle`, `\gradtableschema`, `\graduseschema` |
| Library extensions | `\gradbarsdeclarelibrary`, `\usegradbarslibrary`, `\gradbarsiflibraryloaded` |
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

PGF/TikZ remains the sole supplied backend. The model/backend boundary is private.
The optional tabularray 2025C+ adapter loads with `\UseTblrLibrary{gradbars}`;
its documented commands and columns are stable. It does not load with the five
native feature libraries, modify ordinary tblr defaults, or add native table
statistics to tblr. Header text must be protected from numeric column commands;
repeated graphic headers and complete tagged table structure are outside the
tested accessibility scope. pgfplots and pgfplotstable may contain ordinary
inline graphics but have no dedicated supplied adapter.
