# Updating to v1.1.1 / 升级到 v1.1.1

Version/date: **1.1.1 2026-10-27**. This is a development snapshot;
no v1.1.1 GitHub Release or CTAN release has been published.
Install all 22 matching runtime modules together.

Existing public interfaces, default library selection and raw-data rules are unchanged.
Two opt-in table-legend helpers have been added at the maintainer's request. Existing
documents retain their missing/zero distinction, ranges, percentages, ranking,
aggregation, units and explicit backend fallback semantics. Backend schema stays 1;
third-party libraries requiring 1.1.0 do not need a new minimum solely for this patch.

## Assembled table legends

`\gradtablelegend[options]{names}` draws a horizontal category row.
`\gradtablelegendhead[options]{title}{names}` centers a title above that row.
Both are in core, including `libraries=none`. Set `table legend=false` to hide
the swatches; the header helper retains the title without an extra row gap.
The default is true, but a legend appears only where a helper is explicitly called.
Reuse `stack colors` and category registrations; no numeric thresholds are inferred
and no existing bar colors change. See [configuration](legends.md) and the
[complete service-response example](examples/service-response-legend.tex).

## Complementary theme colors / 主题互补色

At the maintainer's request, explicitly selecting any of the eleven bar themes
now sets complementary negative colors and the corresponding gradient/solid mode.
RGB channels are inverted individually; gradient endpoint order is unchanged.
For example, this now uses orange/brown negative endpoints instead of lightred:

```latex
\gradbar[min=-50,max=50,error=8,theme=blue]{-24}
```

To restore the former negative appearance, put this override after the theme:

```latex
\gradbar[min=-50,max=50,error=8,theme=blue,
  negative fill=solid,negative color=lightred]{-24}
```

This is an explicitly requested visual exception for the unreleased development
version. Without an explicit theme the default stays solid lightred. Themes reset
both negative endpoints and mode; later custom endpoint overrides still work.
Positive endpoint overrides do not automatically recalculate negative colors.
`accessible` uses a complementary negative fill rather than the former vermillion
role; that new fill is not an Okabe-Ito palette member. Thresholds, print rules,
geometry, uncertainty and raw-data semantics are preserved.

本次按要求为全部 11 个显式条形主题设置负值互补色，RGB 各通道取反；渐变两端分别取反，
左右顺序不变，纯色主题使用互补纯色。上述代码不再需要手工指定负值端点。
这是尚未发布开发版中的明确外观变化；未选主题时负值默认浅红纯色保持。
主题后用 `negative fill=solid,negative color=lightred` 恢复原有外观，
或显式指定负值渐变两端。主题会重置负值端点和模式；后续正值端点修改不联动重算负值。
`accessible` 的负值由原朱红色改为互补色，该互补色不属于 Okabe-Ito 七色角色。
阈值、打印、误差、量程和数据语义保持。

## Built-in signed pairs / 内置正负同轨命令

Use `\gradsignedbar[min=-50,max=50,error=8,theme=blue]{-24}{24}` in core.
It replaces the example's custom `\signedtheme` macro and fixed-width clips.
No old scalar call needs changing. Each argument may independently be missing;
errors may cross zero. See [the complete contract](api.md#two-signed-observations-on-one-track).

新增 core 内置命令 `\gradsignedbar[选项]{负值}{正值}`，直接展示正负同轨主题，
无需复制示例裁剪宏。两侧值、缺失与误差保持独立，原有 `\gradbar` 无需迁移。

## Ordinary table baselines / 普通表格基线

Issue #4's original table still uses the legacy `baseline=auto`. Select
`baseline=text` explicitly to align bar labels with ordinary numeric cells;
this already works in v1.1.0. A version upgrade alone does not change the mode.
See the [complete reproduction](examples/baseline-alignment.tex).

issue #4 原例未指定基线模式，因此保留旧默认 `auto`；在设置中加入
`baseline=text` 才启用文字基线对齐，该选项在 v1.1.0 中已存在。
本次补足原始表格示例和实际排版位置验证，不改默认值，也不要求手动升降图形。

## Extraction and validation

From a CTAN source directory containing `gradbars.dtx` and `gradbars.ins`, run:

```sh
texlua scripts/unpack.lua
```

The Lua entry recreates the runtime directory and marker as needed, then extracts
all modules into `sty/`. Follow the documented direct-TeX diagnostic if the output
directory is missing. No shell escape or root-level runtime modules are required.

Use the GitHub development checkout for full regressions. A CTAN source package
that omits `tests/` can unpack and build documentation, but cannot run the missing
regression corpus. Bilingual chapters use `-cn`/`-en` names; the contributed checker
is `docs/libraries/starter/check-starter.lua`.

## Visible legend change

Continuous Heat legends contain 256 sampled base-color strips with fine
semitransparent white separators in both orientations and print mode. Compared
with the published 1.1.0 ramp, the texture is visibly different; the underlying
color function, scale, ticks, units and descriptions remain the same. The lines
are decorative and do not indicate bins or categories.

## 中文说明

开发版日期为 2026-10-27，尚未发布 v1.1.1 GitHub Release 或 CTAN 版本。升级时整套替换 22 个运行模块，
已有接口、默认库列表、数值与缺失语义均保持；后端 schema 仍为 1。
仅要求 1.1.0 功能的第三方库无需因为本次补丁提高最低版本要求。

按本次要求增加 core 内置的横向类别图例 `\gradtablelegend` 和标题组合
`\gradtablelegendhead`；在正文或表头显式调用才显示。设置 `table legend=false`
隐藏色块行并保留标题，恢复用 `table legend=true`，不留隐藏行间距。
配色复用 `stack colors` 和类别注册；不自动判定服务状态或改变数据条颜色。

CTAN 源码包缺失 `sty/` 或 README 标记时，使用上述 Lua 入口自动重建并提取。
完整回归在含 `tests/` 的开发仓库运行；精简源码包只能进行其实际包含的解包与文档检查。
中英文章节保留 `-cn`/`-en` 后缀，第三方模板检查器使用 `check-starter.lua`。

连续 Heat 图例保留当前工作区的半透明白色细纹，水平、纵向及打印模式均适用。
与已发布的 1.1.0 相比，图例外观有变化，但底色插值、尺度、刻度、单位与替代文本不变；
分隔线不表示分类或分箱。
