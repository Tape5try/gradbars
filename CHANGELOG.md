# Changelog

## 3.1.0 — 2026-10-02

- Add clamped rounded corners, data-unit targets, three-band conditional colors,
  and endpoint labels with inward adjustment at track edges.
- Support signed bars with explicit min/max and a visible zero baseline.
- Add symmetric/asymmetric error whiskers, clipping warnings, and strict errors.
- Expand the XeLaTeX manual to 22 numbered examples and test geometry,
  threshold equality, signed labels, tiny bars, and invalid options.


## 3.0.0 — 2026-10-01

- Add three built-in gradients (lbyellow, viblue, cyblu), nine public colors,
  and a color key for solid fills.
- Use XeLaTeX as the documented and tested workflow.
- Remove presentation-only paragraph commands from manual examples.
- Add a unified, 10-page Chinese illustrated manual with 14 numbered examples,
  live output/source comparisons, a linked contents page, and a key reference.

- Add `\gradbar` and scoped `\gradbarssetup` with key-value configuration.
- Render directly in table cells, prose, and existing TikZ pictures.
- Add blue, teal, solid, and gray themes; configurable dimensions and labels.
- Separate raw values, units, computed percentages, and custom labels.
- Draw true zero values; validate numeric input, ranges, and precision.
- Warn and clip overflow, or reject it under a strict policy.
- Remove the forced `ctex` dependency; expose the selected nine-color palette.
- Preserve v2 command entry points with migration notes for rendering changes.
- Add three complete examples, bilingual READMEs, regression tests, and CI.
