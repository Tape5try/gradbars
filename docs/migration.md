# Migrating from v2

Use `\gradbarssetup` and `\gradbar` for new documents.

| Old usage | Recommended replacement |
| --- | --- |
| `\gbar{blue}[white]{100}{70}` | `\gradbar[left color=blue,right color=white,unit={\%}]{70}` |
| `\cbl{100}{70}` | `\gradbar[theme=blue,unit={\%}]{70}` (new palette) |
| `\setscale{200}` | `\gradbarssetup{max=200}` |
| `\renewcommand{\barwidth}{2}` | `\gradbarssetup{width=2cm}` |
| `\renewcommand{\barheight}{0.5}` | `\gradbarssetup{height=.5cm}` |

The v2 `\shadebar`, `\gbar`, `\setscale`, size macros, and all 18 palette helpers
remain as deprecated compatibility entry points. They work in an existing
`tikzpicture` and now on their own. Their argument order and literal
raw-value-plus-percent labels are retained. Use the new API to distinguish
counts, percentage units, and fractions of a maximum.

Compatibility is not pixel-identical: rendering now uses an empty track,
square geometry without node minimum-size padding, true zero length, input
validation, and overflow clipping. It does not create the old named node `(a)`.
Documents referencing that node must supply their own coordinates.

The package no longer loads `ctex`. Chinese documents should select a suitable
class or load `ctex` themselves.

Nine original color names are now built in: `lightgreen`, `lightyellow`,
`lightblue`, `lightred`, `rose`, `skyblue`, `gold`, `lavender`, and `peach`.
They are xcolor names, not commands. `coral` and `mint` remain document-defined
if used directly. Three old gradient palettes are available through
`theme=lbyellow`, `theme=viblue`, and `theme=cyblu`.

New per-bar settings are local and do not redefine document-level `\value`,
`\leftcolor`, or `\rightcolor`.
