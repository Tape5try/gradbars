# Upgrading to the v1.1.0

No version-1 public command is removed or deprecated. Install all 22 matching
runtime modules together. Version 1.1.0 was released on 2026-10-25;
CTAN submission is separate from the GitHub release.

Existing documents retain their five-library default load list. To use new
standalone features, add `\usegradbarslibrary{distribution,legend}` in the
preamble. `distribution` depends on core; `legend` depends on core and Heat.
Native boxplot columns require the distribution library. New styles/palettes
are opt-in; existing numeric, missing, ranking and aggregation rules remain.

The tabularray adapter now also loads stack, spark and distribution, and defines
J/R/V/K/U/B in addition to G/H/N/D. Rename conflicting user-defined column names
before loading it. Spark and dumbbell marker stroke width is reserved inside the assigned
cell, including extrema at the scale endpoints; default spark/stack labels are suppressed, with explicit outside labels
still available. Bullet bands remain mandatory.

Tagged table structure is opt-in through `\gradtblrtagging`; it requires explicit
DocumentMetadata tagging. Short tagged tables work on all three engines.
Repeated tagged longtblr headers need LuaLaTeX and use artifact copies after
the first logical header. Per-page descriptions are an explicit opt-in that rebuilds header content with
fresh marked-content IDs. Multilevel Headers-ID associations are available
through explicit cell addresses, with invalid references and cycles diagnosed.
Do not treat this as a general PDF/UA certification or screen-reader test.

See [distributions.md](distributions.md), [legends.md](legends.md) and
[accessibility.md](accessibility.md) for full definitions and verified boundaries.

Constant automatic ranges preserve the established +/-0.5 expansion. If both
endpoints collapse at the approximately 16-digit numeric limit, the corrected
path uses a bounded 5% interval instead of producing a zero-width scale. This
also applies to native column ranges with include zero=false.

The optional starred form `\gradbarscolumn*` extends the existing csv-library
collector with inside/cell-centered labels and literal blank preservation.
`\gradbarshead` supplies ordinary-table text headings. Unstarred columns retain
their existing behavior; no new dependency or default library is introduced.

The reports library is opt-in. Backend registration uses schema 1 for scalar
bar/Heat callbacks; default rendering remains tikz. Install the new backend and
reports modules with the matching entry/API modules. See backends.md and reports.md.
