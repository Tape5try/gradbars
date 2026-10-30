# gradbars 运行模块说明

GitHub 开发仓库在本目录保存 gradbars 的 22 个 `.sty` 运行文件；CTAN 源码包需先提取这些文件。使用时从 `gradbars.sty` 加载宏包，由入口管理内部模块与功能库；不要分别加载内部模块，也不要混用不同版本的文件。

## 入口与基础模块

| 文件 | 职责 |
| --- | --- |
| `gradbars.sty` | 宏包入口：解析 `libraries` 包选项，加载基础模块，注册功能库并按依赖加载，检查模块版本一致性。 |
| `gradbars-core.sty` | 核心运行逻辑与基本图形接口：作用域设置、样式、输入校验、标签与尺度处理，以及条形、比较条、区间、哑铃、bullet、类别图例和横向表头图例助手等。 |
| `gradbars-keys.sty` | 定义 `/gradbars` 键值选项及默认设置，包括尺寸、颜色、标签、尺度、打印和图形行为。 |
| `gradbars-numbers.sty` | 数值识别与格式化：科学计数输入、精度、百分比、单位、可选 siunitx 格式化及数字对齐支持。 |
| `gradbars-model.sty` | 内部数据模型：校验并归一化数值、量程、零点、起止位置及缺失状态，为布局与绘图提供数据。 |
| `gradbars-render-tikz.sty` | 默认 TikZ 渲染实现：根据内部模型和布局绘制条形路径、填充、轮廓、参考标记及标签等。 |
| `gradbars-tagging.sty` | 图形级无障碍支持：自动或显式替代文本、Figure 标记、artifact/off 模式及试排去重；不代表整份文档通过 PDF/UA 认证。 |
| `gradbars-accessible.sty` | 定义色觉友好的颜色角色、配色和主题，供图形、表格与图例共同使用。 |
| `gradbars-api.sty` | 公开扩展接口：库注册与加载、依赖和版本检查、自定义格式化器、图形类型及统一图形调用。 |
| `gradbars-backend.sty` | 公开标量绘图后端契约：后端注册、能力查询、只读数据与标签助手，以及原生后端回退；当前覆盖 bar/Heat。 |

## 功能库

通过 `\usegradbarslibrary{库名}` 加载。默认加载 `stack,spark,heat,csv,table`；`distribution,legend,reports` 按需加载。

| 文件 | 库名 | 职责 |
| --- | --- | --- |
| `gradbars-lib-stack.sty` | `stack` | 堆叠条形图：解析各分量，处理颜色、标签、缺失与打印表现，提供 `\gradstack`。 |
| `gradbars-lib-spark.sty` | `spark` | 微型趋势图：解析序列并绘制趋势线、端点和相关标记，提供 `\gradspark`。 |
| `gradbars-lib-heat.sty` | `heat` | Heat 单元格：按数值及顺序/发散色带计算底色，处理自动文字对比色与缺失色，提供 `\gradheat`。 |
| `gradbars-lib-csv.sty` | `csv` | CSV 数据加载、单元格访问和表格输出，以及普通表格收集列接口 `\gradbarscolumn`。 |
| `gradbars-lib-table.sty` | `table` | 原生数据表格的公开接口：声明列、行、分组、表头、样式、schema 与汇总，组织数据处理和排版流程。 |
| `gradbars-lib-distribution.sty` | `distribution` | 分布统计与箱线图：原始样本或预计算摘要、type 7 分位数、IQR、须及异常值，提供 `\gradboxplot`、`\gradboxsummary` 等。 |
| `gradbars-lib-legend.sty` | `legend` | 连续色阶、共享图例与参考符号；提供 `\gradheatlegend`、`\gradlegenddefine`、`\gradlegenduse` 和 `\gradreferencelegend`。 |
| `gradbars-lib-reports.sty` | `reports` | 领域报告预设：相关系数矩阵、消融实验、指标表的图形样式、表格样式和列助手；不自动推断显著性或综合评分。 |

`table` 依赖 `stack,spark,heat,csv`，`legend` 依赖 `heat`，`reports` 依赖 `table,legend`；加载器会自动补齐依赖。

`\gradtablelegend[选项]{名称列表}` 与 `\gradtablelegendhead[选项]{标题}{名称列表}`
属于 core，`libraries=none` 即可使用，无需 `legend` 库。前者横向排列类别，后者在其上方居中放置普通文本标题。
`table legend` 默认 true，但仅显式调用助手才显示；false 隐藏类别行，标题仍保留且不留图例间距。
两者复用 `stack colors`、`\gradbarscategory` 和打印纹理，不推断阈值或改变条形颜色。
字体、色块大小、间距和边框的默认值与约束见 [图例接口](../docs/legends.md#horizontal-table-header-legends)。
普通 `\gradbarslegend` 和堆叠条的 `legend` 选项保持不变。

## 表格内部模块与 tabularray 适配

| 文件 | 职责 |
| --- | --- |
| `gradbars-table-data.sty` | 原生表格的内部数据处理，包括排名、最佳/次佳标记及列尺度等计算；由 `table` 库加载。 |
| `gradbars-table-layout.sty` | 原生表格的内部排版，负责列配置、尺寸、单元格呈现及表格布局；由 `table` 库加载。 |
| `tblrlibgradbars.sty` | tabularray 外部库入口：通过 `\UseTblrLibrary{gradbars}` 加载，提供专用列、`\gradtblrcell`、各类 `...Tblr` 助手及预设表格环境。 |
| `gradbars-tblr-tagging.sty` | tabularray 表格结构标记：显式启用 `\gradtblrtagging` 后提供表头关联、Table/TR/TH/TD、表内合并单元格及重复表头语义；由适配库加载。带重复表头/表尾的标记跨页表要求 LuaLaTeX，嵌套标记表和跨页合并单元格不在已验证范围内。 |

## 提取与安装

GitHub 开发仓库直接编辑本目录的 `.sty` 源码。CTAN 源码包使用 `.dtx/.ins`，不附带这些可提取的运行模块；在解压后的源码包根目录运行：

```sh
texlua scripts/unpack.lua
```

该命令会自动创建 `sty/` 及缺失的 README 标记，并从 `.dtx/.ins` 提取全部运行模块。直接运行 `tex gradbars.ins` 要求 `sty/` 目录及可读的 `sty/README.md` 标记同时存在；普通 TeX 不能自行创建缺失目录。CTAN 可能移除近乎空的 `sty/`，目录或标记缺失时均应使用 Lua 入口，仅自行创建目录不足以直接运行 `.ins`。

将全部 22 个 `.sty` 文件一起安装到 `TEXMFHOME/tex/latex/gradbars/`，或放到主 `.tex` 文件所在目录，无需 shell escape。

完整回归测试保留在 GitHub 的 `tests/`，不随 CTAN 源码包分发。源码包可运行 `l3build unpack` 和 `l3build doc`；`l3build check`、`scripts/check.lua` 和 `scripts/pdf-check.lua` 的完整检查需在 GitHub 开发仓库运行。

## 显式主题的正负配色 / Explicit signed themes

v1.1.1 开发版按要求为所有 11 个显式条形主题加入负值互补色，渐变两端分别取 RGB
互补色；纯色主题使用互补纯色。未显式选主题时保留默认负值浅红纯色。
主题后可覆盖负值端点，或用 `negative fill=solid,negative color=...` 覆盖纯色。
阈值和打印规则保持；完整对照见 [独立示例](../docs/examples/theme-complements.tex)。

All eleven explicit bar themes set complementary negative colors and matching
fill modes. The implicit default remains solid lightred. Put custom overrides
after the theme; solid overrides need `negative fill=solid` and `negative color`.

`\gradsignedbar[选项]{负值}{正值}` 为 core 内置命令，共用轨道和零线；
无需自行定义 TikZ 裁剪宏。两侧独立支持缺失值，误差可跨零点。
`\gradsignedbar[options]{negative}{positive}` is built into core; it shares one
track and zero line while preserving independent observations and error intervals.
See [the signed-bar API](../docs/api.md#two-signed-observations-on-one-track).
