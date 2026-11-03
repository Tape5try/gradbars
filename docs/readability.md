# Readability and target trends / 可读性与目标趋势（v1.2.0）

These options are explicit. Existing legend layout and `text color=auto` retain
 their defaults. See the [complete example](examples/readability-target.tex)
and the [Chinese example](examples/readability-target-cn.tex).

## Legend labels

Load `\usegradbarslibrary{legend}`. `legend layout=legacy` is the default;
`legend layout=measured` measures each label's width, height and depth and packs
nonoverlapping horizontal rows or vertical columns with 4pt clearance. Tick
positions always use raw values. `width` remains the ramp length, not the whole
legend width: labels and columns may extend beyond it. Large fonts and long units
can require more space in the enclosing table/page. A vertical title clears the
highest label and the missing swatch clears the label rows.

```latex
\gradheatlegend[min=-2,max=8,heat palette=purple-teal,heat center=1,
  width=60mm,height=3mm,precision=1,unit={ pt},
  legend ticks={-2,0,1,4,8},legend layout=measured,
  legend duplicates=error]
```

`legend duplicates=off` is the default. `error` diagnoses duplicate **builtin
numeric labels**, naming both original ticks and suggesting higher precision or
fewer ticks. The check uses the builtin PGF numeric formatter (including percent
conversion and scientific mode), not a box-width or generic TeX-token comparison.
It never alters ticks, precision or raw values. `siunitx` and custom formatters
are opaque and explicitly rejected by this check; use `off` and inspect them.
Arbitrary custom units/fonts can also alter visible output: this is a numeric
label diagnostic, not universal visual equality detection.

Measured layout works with opaque formatters: each tick callback runs once,
under measurement-tagging suspension; the box is reused for output. Callbacks
must still be safe for normal TeX boxing. Legacy measurement/callback behavior
is unchanged. Shared definitions freeze both options; `\gradlegenduse` accepts
`legend layout` and `legend duplicates` overrides in addition to its older keys.

## Label-area contrast

`text contrast=center` remains the default. For rectangular scalar bars with
`text color=auto`, `text contrast=area` evaluates the actual internal main-label
box rather than its center. `contrast minimum=4.5` is the default target (valid
range 1–21); it is not inferred from font size. Label text/formatters must produce deterministic metrics. An explicit text color bypasses
automatic evaluation, preserving left-to-right theme/style overrides.

```latex
\gradbar[text color=auto,text contrast=area,contrast minimum=4.5,
  contrast failure=background,label=inside,label align=cell,
  rounded=0pt,height=3ex,min=-100,max=100]{75}
```

The model covers resolved positive/negative solid fills and sRGB gradients,
unfilled track, and a reference band's declared opacity over the track (or the declared canvas
within its 2pt vertical overhang). It
partitions the covered horizontal intervals at fill and band boundaries. Within
each gradient interval, 32 subintervals use RGB-channel bounds to enclose the
continuous luminance; this is conservative, not a point-sampling guarantee.
Black's lower contrast bound is `(Lmin+.05)/.05`; white's is
`1.05/(Lmax+.05)`. The better lower bound is chosen. Opposing channel gradients
may produce a slightly pessimistic bound. Vertical overflow and horizontal
portions outside the track include `contrast canvas=white` (default); set it to
the actual opaque page/cell background. The outer canvas is declared, not inferred.

If both colors fail, `contrast failure=warn` (default) emits an explicit bound
warning. `background` instead draws an opaque white padded panel with black
text. This resolves the modeled text/background contrast; it does not claim the
original ramp passed. An existing opaque print-label panel is evaluated as white, including over
patterns, corners and reference strokes it covers. Outside labels
retain existing behavior; `label=outside` is also a deliberate design alternative.

Inside area evaluation rejects non-scalar/compound shapes; without an existing
print panel it also rejects rounded corners, patterns and overlaid reference/error
strokes. It does not assess arbitrary TikZ
styles, inherited transparency/blend modes, custom drawing, glyph color changes,
font effects, color management or whole-document accessibility. Use an explicit
color/outside label or the old center mode for those cases. No PDF/UA or reader
certification is implied. Heat text and stack segment labels retain their older
algorithms. `bar-area` requires native TikZ; a third-party scalar backend needs
explicit `backend fallback=tikz`.

Graphic `style=readable` selects an accessible solid theme, rectangular 3ex
track, small centered internal label, area evaluation and background fallback.
Later keys override it. Native table `style=readable` selects the accessible
theme, small type, 1.6 row stretch, 8pt column gaps, 3pt row padding and a 22mm
outside-label slot; columns retain their normal labels and data semantics. To
use internal panels, explicitly put `style=readable` in a bar column's `options`.

## One combination: spark line plus target

```latex
\gradscale{completion}{min=0,max=100}
\gradsparktarget[scale group=completion,unit={\%},precision=0]
  {20,35,NA,60,75}{70}
```

`\gradsparktarget[graphic options]{series}{target}` belongs to `spark` (loaded by
default). It requires `spark type=line` and `spark range=fixed` or a named scale.
The target is a separate numeric reference within the explicit range, drawn as
one dashed horizontal line using `target color`. It is never an observation,
never included in extrema/statistics, and never fills a missing observation.
The ordinary `target` bar option remains rejected, even on this command.

`NA` retains its equally spaced position and breaks the line. Constant and
single-point series use the explicit range. All-missing series retain the target
and describe missing data. Existing point/last-label/font/unit/clipping options
apply to observations; the final position determines the label, even when missing.
The target cannot be clipped outside the range. Automatic alternative text
separates observations, vertical range and reference; `alt`/artifact/off/embedded
picture rules retain one semantic graphic. The kind `spark-target` uses native
TikZ, with explicit fallback required for third-party scalar backends.

Use it directly in ordinary `tabular` cells. It is not a new native `gradtable`
column, CSV record type or tabularray helper; unknown types/keys are diagnosed.
Existing scalar CSV bindings remain scalar. The old `\gradspark` still rejects
bar targets. A varying reference band or arbitrary composition is outside v1.2.0.

## 中文说明

- 图例库新增 `legend layout=measured`：按文字盒的宽、高、深分配多行或多列，
  刻度位置仍取原始值；旧默认 `legacy` 保持。图例总宽可超过色带长度，需给页面留空间。
- `legend duplicates=error` 对内建数字格式化后的重复标签报错，指出原始刻度并建议提高
  精度或减少刻度；默认 `off`。不自动改值或删刻度，不将盒宽或任意 TeX token 当作视觉等价。
  siunitx/自定义格式化器属于不透明输出，开启此检查会明确报错；测量布局仍可使用它们，
  每个刻度只调用一次格式化器。共享定义保存新选项，使用时可局部覆盖。
- `text contrast=area` 只在内部主标签且 `text color=auto` 时启用；默认仍为中心点估计。
  按标签实际盒与正负填充、轨道、参考带交集计算 sRGB 相对亮度界，每段渐变细分 32 个区间，
  用各通道范围保守包围连续变化，并比较黑字/白字的最不利对比度。默认目标 4.5，可设 1–21。
  大字号不自动降低目标。显式文字颜色保持覆盖顺序并跳过自动评估。
- 默认失败策略 `contrast failure=warn` 报警；`background` 使用不透明白底黑字，
  不声称原渐变已经达标。标签越出轨道时采用 `contrast canvas` 声明的底色（默认白色），
  宏包不推断真实单元格底色。复合图形不在此模型内并有诊断；没有已有打印白底面板时，圆角、纹理及覆盖的参考/误差线也会诊断。已有打印白底面板按白色评估，其覆盖的图案与线条不参与底色评估。
  外层透明度、混合模式、自定义绘图、字体效果及整份 PDF 的无障碍认证不在评估范围。
- 图形 `style=readable` 启用内部白底回退；原生表格同名预设采用较宽列距、行距和外部标签槽，
  单列内部标签需显式设置 `options={style=readable}`。两个预设均不改变数值语义。
- `\gradsparktarget[选项]{序列}{目标}` 是本版唯一新增的组合，属于默认加载的 spark 库。
  必须显式固定范围或命名尺度、使用折线，目标在范围内。目标线是参考，不参与观测统计。
  NA 保留位置并断线，全缺失仍可显示目标，描述明确说明数据缺失。标签来自最后位置，
  不回退寻找有效值；替代文本区分范围、序列和目标。
- 旧 `\gradspark` 的目标选项错误保持；新命令同样不接受条形 `target` 键。
  可直接嵌入普通表格，未新增 CSV 复合记录、原生列类型或 tabularray 助手。
  第三方标量后端须显式回退 TikZ。中英文手册和上述独立示例给出可编译用法。
