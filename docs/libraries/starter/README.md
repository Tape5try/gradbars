# Third-party library starter

Copy this directory, rename the file/package/library and all `starter-*` names,
and edit the callback bodies. The starter is [MIT-licensed](../../../LICENSE); include the full MIT notice from the project-root LICENSE when copying this
template, and add your authorship/version information to your derived library.

Load a locally installed or development gradbars 1.1.0 or newer, then register:

```latex
\usepackage[libraries=none]{gradbars}
\gradbarsdeclarelibrary{starter}{table}{gradbars-contrib-starter.sty}
\usegradbarslibrary{starter}
```

Keep the `.sty` beside the document or in TEXMF. The dependency list is part of
the caller's registration. The library checks that its declared table dependency is already loaded.
For direct preamble loading, load table first; prefer registry-based loading. Repeated loading
through the registry is idempotent. Registration/loading belong in the preamble.

`gradbarsversion` and `gradbarsrequireversion` expose and check semantic package
versions; backend record schema version is a separate `gradbarsbackendversion`.
No private variables or callbacks are used. The scalar callback accepts one
validated number or NA; the formatter receives value/precision/number-format.
The style only selects existing table options. The backend example delegates
native drawing through the public continuation, retaining geometry, labels and
tagging. It supplies no second drawing implementation.

Run, from this directory or anywhere:

```sh
texlua check-starter.lua --gradbars-root /absolute/path/to/gradbars
```

Omit `--gradbars-root` when testing a user-installed release. The checker uses
TeX Live's texlua runtime and the three TeX engines; no Python files are needed. It compiles in temporary
directories, checks repeated loading and real output, and verifies that an
unsupported required version fails. The checker runs all three engines before publication.

Before publishing, document your own commands, options, units, range and missing
rules, supported engines, required libraries, minimum gradbars version and license.
Add numerical/semantic assertions for your extension's actual behavior; successful
compilation alone is not sufficient for a new statistical algorithm. Test PDF
structure when adding descriptions. Do not claim compatibility with private
model fields or native gradcolumn type registration; those are outside this API.

See [backend contract](../../backends.md), [developer reference](../../developer.md)
and [version-1 stability contract](../../stability.md).
