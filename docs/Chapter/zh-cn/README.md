# 中文手册章节

编译入口为 `docs/gradbars-manual.tex`，不要单独编译章节。当前对应 v1.2.3。

主文件只维护全书配置与固定章节入口；新增功能的说明、参数、效果和源码写入所属章节。
优先扩充现有章节；确需新增独立章节或调整主文件时，先确认目录方案。

## 1. 快速开始

| 章节文件 | 内容 |
| --- | --- |
| [install-cn.tex](install-cn.tex) | 安装与快速开始 |

## 2. 共同基础

| 章节文件 | 内容 |
| --- | --- |
| [values-cn.tex](values-cn.tex) | 数值语义与边界 |
| [settings-cn.tex](settings-cn.tex) | 统一设置、覆盖顺序与作用域 |
| [styles-cn.tex](styles-cn.tex) | 命名样式与缺失值 |
| [number-format-cn.tex](number-format-cn.tex) | 数字格式与区间背景 |
| [research-numbers-cn.tex](research-numbers-cn.tex) | 科研数字列与语义单位 |

## 3. 图形详解

| 章节文件 | 内容 |
| --- | --- |
| [selection-cn.tex](selection-cn.tex) | 选型指南 |
| [signed-bars-cn.tex](signed-bars-cn.tex) | 正负双向条与误差标记 |
| [compare-cn.tex](compare-cn.tex) | 双层对比条、棒棒糖与浮动区间 |
| [dumbbell-cn.tex](dumbbell-cn.tex) | 哑铃对比图 |
| [change-cn.tex](change-cn.tex) | 对比变化标注 |
| [references-cn.tex](references-cn.tex) | 多重参考与区间对比 |
| [stack-cn.tex](stack-cn.tex) | 堆叠条 |
| [stack-legend-cn.tex](stack-legend-cn.tex) | 堆叠图例与分段标签 |
| [spark-cn.tex](spark-cn.tex) | 迷你趋势图：折线、柱形与 win-loss |
| [distribution-cn.tex](distribution-cn.tex) | 微型箱线图与分布摘要 |
| [boxrug-cn.tex](boxrug-cn.tex) | 箱线图与全部原始样本 |
| [heat-cn.tex](heat-cn.tex) | Heat 色阶单元格 |

## 4. 表格实战

| 章节文件 | 内容 |
| --- | --- |
| [tabular-cn.tex](tabular-cn.tex) | 在已有 tabular 中使用图形 |
| [table-cn.tex](table-cn.tex) | 专属数据表格：gradtable |
| [table-graphics-cn.tex](table-graphics-cn.tex) | 更多图形列 |
| [table-alignment-cn.tex](table-alignment-cn.tex) | 表格对齐与线条样式 |
| [table-width-cn.tex](table-width-cn.tex) | 按总宽度分配列宽 |
| [headers-cn.tex](headers-cn.tex) | 多级表头与跨列标题 |
| [groups-cn.tex](groups-cn.tex) | 分组行与最优值标记 |
| [summaries-cn.tex](summaries-cn.tex) | 汇总行与统计范围 |
| [longtable-cn.tex](longtable-cn.tex) | 跨页表格与重复表头 |

## 5. 数据与报告

| 章节文件 | 内容 |
| --- | --- |
| [csv-cn.tex](csv-cn.tex) | CSV 数据导入 |
| [regional-cn.tex](regional-cn.tex) | 显式地区输入与固定参考带 |
| [column-scales-cn.tex](column-scales-cn.tex) | 自动列尺度与零点基准 |
| [hierarchy-cn.tex](hierarchy-cn.tex) | 两级报告与首末趋势 |
| [report-metrics-cn.tex](report-metrics-cn.tex) | 报告级指标与当前值趋势卡 |
| [reports-cn.tex](reports-cn.tex) | 领域报告预设 |
| [table-definitions-cn.tex](table-definitions-cn.tex) | 复用表格样式与列定义 |
| [complete-examples-cn.tex](complete-examples-cn.tex) | 完整案例（统一章节入口） |

## 6. 外观与交付

| 章节文件 | 内容 |
| --- | --- |
| [themes-cn.tex](themes-cn.tex) | 主题与内置颜色 |
| [labels-cn.tex](labels-cn.tex) | 标签、尺寸与正文内嵌 |
| [collision-cn.tex](collision-cn.tex) | 智能标签与数值列 |
| [rounded-targets-cn.tex](rounded-targets-cn.tex) | 圆角、目标线与条尾标签 |
| [overflow-cn.tex](overflow-cn.tex) | 越界指示与点标记 |
| [conditional-colors-cn.tex](conditional-colors-cn.tex) | 条件配色 |
| [quality-cn.tex](quality-cn.tex) | 指标优劣方向 |
| [categories-cn.tex](categories-cn.tex) | 语义配色与稳定类别纹理 |
| [patterns-cn.tex](patterns-cn.tex) | 黑白纹理填充 |
| [presets-cn.tex](presets-cn.tex) | 四套排版预设 |
| [table-themes-cn.tex](table-themes-cn.tex) | 报告与黑白表格主题 |
| [legends-cn.tex](legends-cn.tex) | 表头类别图例、连续色阶与共享图例 |
| [readability-cn.tex](readability-cn.tex) | 可读性与目标趋势 |
| [layouts-cn.tex](layouts-cn.tex) | 真实排版案例 |
| [accessibility-cn.tex](accessibility-cn.tex) | Tagged PDF 与替代文本 |

## 7. 高级集成与参考

| 章节文件 | 内容 |
| --- | --- |
| [libraries-cn.tex](libraries-cn.tex) | 按需加载库与公开扩展接口；自定义命令分步教程（参数形式、数据映射、配色尺寸、标签定位、作用域与表格） |
| [tabularray-cn.tex](tabularray-cn.tex) | tabularray 集成与单元格标签对齐 |
| [adapters-cn.tex](adapters-cn.tex) | 显式列适配与 pgfplotstable 集成 |
| [extensions-cn.tex](extensions-cn.tex) | 第三方库模板、公开后端与独立数值对契约 |
| [faq-cn.tex](faq-cn.tex) | 常见问题 |
| [reference-cn.tex](reference-cn.tex) | 参数速查与使用限制 |

## 完整案例子文件

以下文件由 `complete-examples-cn.tex` 按顺序 `input`，作为同一章的小节；主文件不再分别包含。

| 文件 | 案例 |
| --- | --- |
| [example-models-cn.tex](example-models-cn.tex) | 模型对比 |
| [example-overview-cn.tex](example-overview-cn.tex) | 数据集概览 |
| [example-comparisons-cn.tex](example-comparisons-cn.tex) | 前后对比与目标评价 |
| [example-trends-cn.tex](example-trends-cn.tex) | 等间隔趋势汇总 |
| [example-scenarios-cn.tex](example-scenarios-cn.tex) | 教学、借阅、节能与质控 |
| [example-palettes-cn.tex](example-palettes-cn.tex) | 主题与标签总览 |
| [example-contributions-cn.tex](example-contributions-cn.tex) | 收支贡献与黑白打印 |
| [example-metrics-cn.tex](example-metrics-cn.tex) | 社区服务站办理质量对照 |
