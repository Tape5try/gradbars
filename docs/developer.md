# Developing gradbars v1.0.0

This release freezes the documented extension interfaces under the
[version 1 stability contract](stability.md). Private
commands (`gradbars@...`, `gradtable...`, `__gradbars_...`) and variables are
implementation details; they are not an extension contract.

## Runtime structure

Fifteen base runtime modules and optional `tblrlibgradbars.sty` are stored in `sty/`. The builders and tests add
this directory to the TeX search path; l3build installs its contents as package
files. The contributed example remains in `docs/libraries/`.

| File | Responsibility |
| --- | --- |
| gradbars.sty | Package options and default library selection |
| gradbars-core.sty | Scoped defaults, numeric/geometry orchestration, common scalar and comparison frontends |
| gradbars-keys.sty | Basic `/gradbars` pgfkeys family; feature keys live with their implementation |
| gradbars-numbers.sty | Shared decimal/scientific validation, numeric formatting and units |
| gradbars-model.sty | Validated input, normalized model and coordinate projection |
| gradbars-render-tikz.sty | TikZ drawing and label primitives |
| gradbars-tagging.sty | Alternative descriptions and measurement-tag suspension |
| gradbars-api.sty | Settings alias, library registry and public extension callbacks |
| gradbars-lib-stack.sty | Signed-stack parsing and drawing |
| gradbars-lib-spark.sty | Series parsing and line/bar/win-loss rendering |
| gradbars-lib-heat.sty | Sequential/diverging heat-cell renderer |
| gradbars-lib-csv.sty | Literal CSV I/O and collected table columns |
| gradbars-lib-table.sty | Column/schema declarations and table frontend |
| gradbars-table-data.sty | Table selection, ranges, ranks, grouping and aggregates |
| gradbars-table-layout.sty | Table measurement, alignment, headers, layout and pagination |
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

```sh
l3build check
python tests/run_tests.py
l3build doc
l3build ctan
```

`l3build check` runs three-engine semantic log regressions in an isolated staging
tree containing the runtime modules. The existing Python suite preserves detailed
range/color/statistic/position assertions and expected errors. `l3build doc` and
`l3build ctan` delegate to the existing checked builders, retaining Chapter includes
and `gradbars_CTAN/gradbars-VERSION.zip`. Set `GRADBARS_PYTHON` if Python is not
available as `python`. Modern tagging fixtures require a tagging-capable LaTeX
installation; ordinary operation requires no tagging setup.

For a fixed-dataset timing and value comparison, extract a v0.0.8 `.sty` baseline:

```sh
python scripts/benchmark.py --baseline path/to/v0.0.8
```

The report records median compilation time, PDF/log sizes and an identical PDF-text
hash per engine. Sizes include version/file metadata and are diagnostic. Timing
greater than twice the baseline requires investigation rather than automatic acceptance.

The supported minimum is LaTeX 2025/11/01, expl3 2025/12/29 and PGF/TikZ 3.1.11a.
The tested baseline is TeX Live 2025 with current updates; CI uses a current
TeX Live container rather than an older operating-system TeX package. The usual table
dependencies remain required for corresponding features. SI formatting requires
siunitx v3, and the package never installs or loads it automatically. Wider old
distribution compatibility should be claimed only after running the same suite.

## Model and backend boundary

`gradbars-model.sty` owns validation and normalized geometry preparation.
`\l__gradbars_model_prop` is a private per-call snapshot with raw-value, min,
max, zero, start, stop, end, shape and missing fields. Positions are normalized
after clipping; raw-value is retained separately for semantics. Colors and
formatted text are resolved independently of numeric input. The snapshot is
local and cannot leak between graphics.

`\__gradbars_render:` prepares the model before invoking
`\__gradbars_render_tikz:`. Projection to physical dimensions runs in the drawing
font/coordinate context, preserving existing em/ex behavior. The TikZ backend
consumes validated values and resolved positions; it does not parse raw scalar
input. Compound library drawing helpers and table measurement remain private.
This boundary reserves a future backend without exposing its internal fields
as a version-1 extension API. Public scalar callbacks delegate to public graphics.

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
`python scripts/build_source.py`. Use `--check` to reject drift and verify
docstrip extraction of every module. The l3doc driver builds a source guide;
the manuals continue using bilingual chapter sources. Run
`python scripts/check_tagging.py` with development dependency pypdf to inspect
actual PDF Figure descriptions and check measurement suppression in all engines.
