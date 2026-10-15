# Migrating to gradbars 1.0.0

Version 1.0.0 establishes the [version 1 stability contract](stability.md).
Existing graphic and native-table calls retain their defaults and data semantics.
No public command has been removed or renamed.

## Install the Complete Module Set

Install the fifteen `sty/gradbars*.sty` files and optional `sty/tblrlibgradbars.sty`
together. The new private model
module is required even for basic bars. Replacing the entry file alone is
insufficient. A project-local older copy takes precedence over TeX Live; check
the log for every gradbars module version.

The verified environment is LaTeX 2025-11-01+, expl3 2025-12-29+ and PGF/TikZ
3.1.11a+. Update older distributions before using the supported stable
configuration. The old 2020 minimum was not backed by the current suite and is
replaced with the tested requirement. siunitx v3 remains explicitly optional.

## Preserve Existing Loading and Settings

```latex
\usepackage{gradbars} % full feature loading
\gradbarssetup{max=100,precision=1}
\gradbar{72.4}
```

Minimal and selected loading remain available in the preamble:

```latex
\usepackage[libraries=none]{gradbars}
\usegradbarslibrary{stack,spark}
```

`\gradbarsset` remains an alias for `\gradbarssetup`. Settings follow groups and
keys apply left to right. No change is required for `label=left`, baseline
presets or negative gradients from the 0.1.0 development cycle.

## Stable Registrations

Library, scalar type and formatter registrations from 0.1.0 are now stable with
the same arguments. Existing public-only contributed libraries need no changes.
Private variables and internal module layout are excluded. Opaque formatters
still reject decimal alignment; custom scalar types remain separate from native
table column types.

The optional `style=reference` table style adds centered headers, booktabs rules,
decimal number alignment, row stretch 1.25 and column separation 6pt. It does not
change any existing style or force a color theme.

## Source and Build Workflow

Keep editable runtime changes in `sty/`, then run:

```sh
python scripts/build_source.py
python scripts/build_source.py --check
l3build check
python tests/run_tests.py
python scripts/check_tagging.py
python scripts/build_manual.py
```

`gradbars.dtx` and `gradbars.ins` are generated distribution sources. The source
check extracts every module with docstrip and compares it with `sty/`. Do not
edit both copies independently. `tex gradbars.ins` extracts a matching module
set for users without Python. The source guide uses l3doc; the bilingual
illustrated manuals retain their chapter files.

Tagged PDF inspection needs the development dependency `pypdf` and a current
tagging-capable LaTeX installation. It checks real structure-tree descriptions,
raw precision, explicit/outer descriptions and measurement suppression.

CTAN packaging remains a separate explicit step through `l3build ctan` or
`python scripts/build_release.py`. Updating sources and manuals does not refresh
any existing zip automatically. Dedicated tabularray integration is included
in 1.0.0: load `\UseTblrLibrary{gradbars}` with tabularray 2025C+ in the preamble.
Existing ordinary `\gradbar` calls inside `tblr` retain their behavior. Adopt
`\gradbarTblr`, G/H/N/D columns or `\gradtblrcell` to allocate cell widths and
center labels with `label align=cell`. Protect header text with braces. Existing
custom G/H/N/D column names must be renamed before loading the adapter.
`gradtblr` and native `style=matrix` are optional presets, not changed defaults.

Without creating a zip, run `python scripts/build_release.py --validate-only`
and `python scripts/check_release.py --source-tree` to validate the complete
payload and compile a separately copied installation with all three engines.
