# Color, printing and table semantics

The opt-in `palette=accessible` uses seven colors from the Okabe-Ito Color
Universal Design recommendation: blue #0072B2, orange #E69F00, teal #009E73,
purple #CC79A7, sky #56B4E9, vermillion #D55E00 and yellow #F0E442.
Color values and redundant coding guidance are attributed to
[Masataka Okabe and Kei Ito](https://jfly.uni-koeln.de/color/).
No third-party image or implementation is incorporated. The package's original
implementation is MIT licensed. A palette name is not accessibility certification.

`theme=accessible` selects a solid blue bar, pale track, automatic label contrast and vermillion negative
role. `palette=accessible` additionally selects stack colors/textures, threshold,
comparison, spark and Heat roles. Heat has `heat palette=accessible-sequential`
and `accessible-diverging` (vermillion/white/blue). Native tables accept
`theme=accessible`; labels and numbers must remain visible. Color does not encode
missingness by itself. Category palettes cycle after seven entries, so add
category names and registered patterns when the set is larger.

Existing `print` remains opt-in and follows the ordinary left-to-right override
rules. It supplies monochrome fills, patterned bars/stacks and white label
backgrounds. Box plots retain median strokes, caps and hollow outlier circles.
Shared legends use the same print configuration. Thin lines can disappear in
low-resolution prints; enlarge the row or graphic when necessary.

Heat uses computed sRGB luminance to select black or white labels. For bar
inside labels use `text color=auto`; outside labels should remain black on a
light page. For gradients the existing center estimate is not a worst-case
contrast guarantee: use solid fills or print-label backgrounds where text spans
multiple colors. `scripts/accessible.lua` records contrast samples and
produces a grayscale comparison; simulated deficiencies are design checks only.

Automatic descriptions retain unrounded numbers, missing observations, unit text,
scale, metric direction, and the full distribution definition/list of outliers.
Descriptions are not silently truncated. Use a deliberate `alt={...}` and supply
an adjacent full data table when a long sample list would be burdensome.
`text` only changes the visible label, not its semantic value.

The verified tagging toolchain is TeX Live 2026 with LaTeX 2026-06-01, expl3
2026-09-09, tagpdf 1.0h (2026-10-08) and tabularray 2025C. This records the
actual test environment rather than promising untested tagging backends.

## Explicit tabularray structure

After `\UseTblrLibrary{gradbars}`, opt in **inside a local group before a table**:

```latex
\DocumentMetadata{tagging=on,lang=en-US} % before documentclass
% ... in the document:
{\gradtblrtagging{head rows=1,row headers={1},caption={Measured scores}}
\begin{tblr}{colspec={l G{30mm}}}
{Method} & {Score}\\
A & 42\\
\end{tblr}}
```

`head rows` defaults to 1; 0 disables column headers. `row headers={...}` is an
explicit list of 1-based column indices. `caption` is visible tagged text,
attached as Caption under the same Table; use this instead of native captions
when requiring the tested structure. Scope=Column/Row/Both and explicit
RowSpan/ColSpan attributes describe header roles and merged cells. Rows are
allocated in logical order before tabularray builds its repeated boxes. Data
cells contain text or their own Figure descriptions, not extra logical rows.
The package does not activate global document tagging.

Short tagged tblr works with pdfLaTeX, XeLaTeX and LuaLaTeX. Tagged longtblr with
repeated row headers/footers requires **LuaLaTeX**; after the first physical page,
repeated boxes have their marked-content attributes reset to artifact. Thus the
first logical header is described once and each real data row remains unique.
The compatibility adapter uses isolated private output hooks for this reset,
checked against the installed tabularray; it is not a public backend protocol.
`header repeat=artifact` is the default. `header repeat=describe` rebuilds header
content for each physical page with fresh marked-content IDs beneath the same
logical TH cells. It repeats header source code, so keep header callbacks free of
external side effects. Logical data rows and header cells are not duplicated. Ordinary untagged longtblr remains
available on all engines. Keep header rows and merged cells within the normal
tabularray pagination constraints. Nested tagged tables are not supported.

Explicit associations use `cell headers={3/2={1/2,2/2,3/1},...}`. Each key is a
1-based row/column cell address, and the value lists its header addresses. This
also works between header cells for multilevel hierarchies. `header cells={3/3}`
marks an irregular header outside the declared header rows/columns. The adapter
uses the real TH structure IDs in `/Headers`, rejects unknown/covered cells,
non-TH references and cycles, and retains the default Scope/span attributes.

The verified scope is Table/TR/TH/TD hierarchy, ordered logical rows, simple and
spanning headers with Scope, explicit multilevel Headers-ID associations,
graphic/text cells, caption, and both LuaLaTeX repeated-header modes.
Cross-page spanning cells and screen-reader behavior in specific external viewers
are not certified. PDF/UA compliance of an entire
document requires separate validation. The structural checks do not substitute
for a real assistive-technology review.
