# Developing gradbars v1.1.1

This release freezes the documented extension interfaces under the
[version 1 stability contract](stability.md). Private
commands (`gradbars@...`, `gradtable...`, `__gradbars_...`) and variables are
implementation details; they are not an extension contract.

## Runtime structure

The twenty-two matching runtime modules, including optional feature libraries and tabularray adapters, are stored in `sty/`. The builders and tests add
this directory to the TeX search path; l3build installs its contents as package
files. The contributed example remains in `docs/libraries/`.

| File | Responsibility |
| --- | --- |
| gradbars.sty | Package options and default library selection |
| gradbars-core.sty | Scoped defaults, numeric/geometry orchestration, common scalar/comparison frontends and opt-in assembled table-header legends |
| gradbars-keys.sty | Basic `/gradbars` pgfkeys family; feature keys live with their implementation |
| gradbars-numbers.sty | Shared decimal/scientific validation, numeric formatting and units |
| gradbars-model.sty | Validated input, normalized model and coordinate projection |
| gradbars-render-tikz.sty | TikZ drawing and label primitives |
| gradbars-tagging.sty | Alternative descriptions and measurement-tag suspension |
| gradbars-api.sty | Settings alias, semantic version guard, library registry and public extension callbacks |
| gradbars-backend.sty | Public scalar backend registry, capabilities and scoped schema-1 records |
| gradbars-lib-reports.sty | Optional correlation, ablation and metrics recipes |
| gradbars-lib-stack.sty | Signed-stack parsing and drawing |
| gradbars-lib-spark.sty | Series parsing and line/bar/win-loss rendering |
| gradbars-lib-heat.sty | Sequential/diverging heat-cell renderer |
| gradbars-lib-csv.sty | Literal CSV I/O and collected table columns |
| gradbars-lib-table.sty | Column/schema declarations and table frontend |
| gradbars-table-data.sty | Table selection, ranges, ranks, grouping and aggregates |
| gradbars-table-layout.sty | Table measurement, alignment, headers, layout and pagination |
| gradbars-accessible.sty | Opt-in color roles; no default style change |
| gradbars-lib-distribution.sty | Type-7 statistics, observed whiskers and box plots |
| gradbars-lib-legend.sty | Shared explicit configurations and semantic legends |
| gradbars-tblr-tagging.sty | Opt-in Table/TR/TH/TD and Lua repeat suppression |
| tblrlibgradbars.sty | Optional tabularray library, cell widths, dedicated columns and trial-tagging hooks |

The default package loads all five feature libraries. `libraries=none` loads
only the shared engine and API. `table` depends on `stack`, `spark`, `heat` and
`csv`; all feature libraries depend on `core`. No library implicitly loads
siunitx. Internal table helpers are loaded by `table`, not separate public libraries.
The loader detects unknown names, missing files, cycles and repeated loads.
Native modules must match the entry package version. Library loading and library
registration belong in the preamble because feature libraries may require packages.

## Settings and data contracts

`\gradbarsset{...}` calls the same scoped pgfkeys engine as `\gradbarssetup`.
Settings follow TeX groups and keys are applied left to right. Table/column
declarations retain their typed expl3 keys and existing precedence: table defaults,
column settings, drawing `options`, explicit named scale/range resolution and final
allocated widths. Package `libraries` affects availability, not data semantics.

The numeric parser retains the v0.0.8 bounds and roughly 16-digit arithmetic.
CSV text remains literal character data. Original row values feed selection,
ranking and aggregation; formatting results are never parsed as input. Geometry
receives resolved ranges and validated values. Layout collects widths without
tagging measurements; rendering emits real graphic descriptions once.

## Public-only third-party library

```latex
\usepackage[libraries=none]{gradbars}
\gradbarsdeclarelibrary{demo}{table}{docs/libraries/gradbars-contrib-demo.sty}
\usegradbarslibrary{demo}
```

The three arguments are a lower-case name, a comma-separated dependency list and
a TeX-searchable `.sty` filename. Names use letters, digits and hyphens and start
with a letter. Registration is global and duplicates are errors. Library loading
is idempotent. See [the complete example](libraries/gradbars-contrib-demo.sty).

### Scalar graphic callbacks

```latex
\gradbarsdeclaretype{score}{\gradbar[color=teal,rounded=1pt]{#1}}
\gradgraphic[max=100]{score}{72.125}
```

The callback receives one validated numeric value in canonical floating-point
notation, or `NA`. Options are scoped around the callback and inherited by public
graphics. `bar` and `heat` are reserved builtin renderer names; `heat` still requires
its library. Custom types are standalone scalar frontends, not additional native
`gradcolumn` types. List/compound data and inference of arbitrary callback endpoints
are outside this first interface. Delegate to public graphics for their geometry
and tagging; the dispatcher itself adds no second picture or description.

### Numeric formatter callbacks

```latex
\gradbarsdeclareformatter{boxed}{%
  \fbox{\gradbarsformatnumber[precision=#2,number format=#3]{#1}}}
\gradbar[formatter=boxed]{72.125}
```

Arguments are display value, precision and number-format mode. Display value
already includes any requested computed-percent conversion. Render only the
number; the engine appends a literal unit or percent suffix. The helper defaults
to builtin formatting and accepts builtin/siunitx, precision and number-format
overrides, so it can be used without callback recursion. `builtin` and `siunitx`
are reserved. Custom formatters work in graphics and non-decimal-aligned number
columns; their output is opaque and cannot use `number align=decimal`. Semantic
`unit code` retains its existing siunitx requirement.

## Build and validation

Run the complete development checks from a GitHub checkout, which includes
`tests/`:

```sh
l3build check
texlua tests/maintenance.lua
texlua scripts/docs-check.lua
texlua scripts/check.lua
l3build doc
l3build ctan
```

`l3build check` runs seven semantic groups under three engines, extracting runtime
modules from the documented source and comparing them with `sty/`. The static
regression corpus in `tests/cases/` is replayed by `texlua scripts/check.lua`;
expected failures must fail with their declared diagnostics. Run
`texlua scripts/pdf-check.lua` to inspect actual Tagged PDF Figure alternatives,
measurement suppression and table spans/scopes through TeX Live's pdfe library.

`l3build doc` uses latexmk for convergence and stages chapter sources, data and
layout PDFs. `l3build ctan` uses the native target, runs the l3build tests, builds
documentation and produces `gradbars-ctan.zip`. Run
`texlua scripts/release.lua --verify` and `texlua scripts/install-check.lua` to
inspect that ZIP and compile after source extraction in a clean directory.
The CTAN source archive omits `tests/`, so `l3build check`, `scripts/check.lua`
and `scripts/pdf-check.lua` there do not provide the full development regression
suite. Use `l3build unpack` and `l3build doc` to extract and rebuild the supplied
source package; use the GitHub checkout for the full checks.
No Python files or generated runtime modules enter the CTAN source ZIP.
PDFs and archives are ignored by Git and published through Release/CI artifacts.
See [upload and release configuration](#release-configuration).

## Model and backend boundary

`gradbars-model.sty` owns validation and normalized geometry preparation.
`\l__gradbars_model_prop` is a private per-call snapshot with raw-value, min,
max, zero, start, stop, end, shape and missing fields. Positions are normalized
after clipping; raw-value is retained separately for semantics. Colors and
formatted text are resolved independently of numeric input. The snapshot is
local and cannot leak between graphics.

`\__gradbars_render:` prepares the model, then dispatches through the public
backend contract. Default tikz follows the native path without creating a public
record. Selected custom scalar backends receive a scoped schema-1 snapshot, not
access to private model storage. Heat uses the same negotiation after validation.
Compound and legend kinds require native rendering or explicit fallback.
Projection preserves existing em/ex behavior. See [backends.md](backends.md)
for the exact public fields, capabilities, label helper and continuation rules.

Use [the independent starter](libraries/starter/README.md) to create a library.
It includes source, example, semantic version guard and a three-engine checker.
`\gradbarsversion` reports the package version; `\gradbarsrequireversion{1.1.0}`
checks a minimum semantic version. [Domain reports](reports.md) demonstrate
recipes built from existing graphic/table interfaces without inferring statistics.

## tabularray adapter

`\UseTblrLibrary{gradbars}` uses tabularray's standard external `tblrlibgradbars.sty`
discovery. This is separate from the five native feature libraries and does not
change their default load list. tabularray 2025C+ is optional. The adapter uses
public column definitions, `cmd`, `\linewidth` and trial hooks; it does not patch
tabularray internals. `hook`/varwidth keeps natural-width trials consistent.
Trial tagging is suspended for the whole table and resumed before actual output.

Cell commands inherit graphic settings, then adapter initial defaults
(`baseline=text,label=inside,label align=cell`), scoped accumulated
`\gradtblrsetup` settings and call options. Allocated dimensions apply last.
G/H/N/D columns pass an explicit content width; Q/X cells use the local line
width, falling back to the configured graphic width during paper-wide natural
trials. Left/outside labels reserve slots; dumbbells reserve marker extents.
Oversized content is diagnosed unless the user permits overflow. The full-width
cell box centers its content without scaling text or changing raw values.

Number cells use the shared parser and label formatter without range clipping
or a Figure wrapper. Pair cells accept reference/current or lower/upper; whole
NA/empty input means both endpoints are missing. Custom opaque formatters retain
their normal restrictions. `gradtblr` is an opt-in styled environment; native
`style=matrix` uses the existing table style registry. Neither provides automatic
CSV selection, ranking or aggregates for tblr.

`gradbars.dtx`/`gradbars.ins` are generated from `sty/` by
`texlua scripts/source.lua`. Use `--check` to reject drift and verify
docstrip extraction of every module. The l3doc driver builds a source guide;
the manuals continue using bilingual chapter sources. From the source-package
root, `texlua scripts/unpack.lua` creates `sty/` if needed and extracts all 22
modules without shell escape. Plain `tex gradbars.ins` also writes there, but
requires both an existing `sty/` directory and its readable `sty/README.md`
marker. If either is missing, use the Lua entry above; creating the directory
alone is insufficient. The l3build unpack stage creates this layout and stages
the extracted modules for checks and typesetting. Isolated installation checks
cover a missing `sty/` and reject root `.sty` files. In the GitHub checkout, run
`texlua scripts/pdf-check.lua` with TeX Live pdfe to inspect
actual PDF Figure descriptions and check measurement suppression in all engines.

The two new native libraries are opt-in: distribution depends on core; legend
depends on core and heat. Run `texlua scripts/check.lua` and `texlua scripts/pdf-check.lua`
for independent rational-reference statistics and actual PDF structure checks.
Palette design evidence is described in [accessibility](accessibility.md); CVD previews are not a certification.
The table-tagging adapter isolates the private repeated-box reset and requires
LuaLaTeX for repeated tagged longtblr headers. Do not extend this with unverified
PDF literal rewrites for the other engines.

## Release configuration

The GitHub source tree does not track UPLOAD-RESTRICTIONS.md, README.ctan.md,
gradbars.dtx or gradbars.ins. The first two are local maintainer files;
l3build and CI generate the documented sources from the tracked sty/ modules.
The CTAN README is derived from README.en.md and receives source-installation
instructions. Clean GitHub checkouts support l3build check/doc/ctan without the
local maintainer files. CTAN source packages support extraction and documentation
rebuilds without those files; full regression checks require the GitHub `tests/`
directory.

Branch pushes and pull requests run tests and create CI artifacts. A stable
vVERSION tag matching finalized metadata publishes the verified ZIP and PDFs to
GitHub Release. For subsequent CTAN submission, configure the repository secret
CTAN_EMAIL and repository variables CTAN_UPLOAD=true, CTAN_ANNOUNCEMENT and
optionally CTAN_NOTE. The CTAN job submits the same verified ZIP with l3build
upload. Future planned dates and unreleased README states block stable releases.
No task here rewrites Git history or publishes a release merely by editing files.
