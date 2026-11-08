# v1.2.2 performance / 性能与稳定性

## 本版范围

v1.2.2 优先优化分组报告与多列排名。原实现为提取组内最佳值、次佳值，对同一组完整计算两次排名；现在一次计算后同时保存两项结果。表级排名及组内并列、第二个不同数值、缺失和 higher/lower 含义保持不变。父组/叶组沿用同一实现。

本版没有增加公开选项、运行依赖、跨调用缓存或轻量后端。分组结果只用于当前表格，不复用排版盒子，不缓存 formatter 输出，也不关闭校验或 PDF 标记。数字解析和 type-7 统计先测量，不因本次优化而引入缓存。

## 重建基准

本次测量的环境、前后对照、90 个原始阶段样本及源码/数据身份见[测量记录](performance-v1.2.2.md)。排名阶段约三分之一的下降仅适用于该固定负载，不代表整份文档编译提速。

从仓库根目录运行现有 TeX Live 的 texlua，无需 Python、shell escape 或新运行依赖：

```sh
texlua scripts/benchmark.lua --output=build/benchmark/current --runs=3
```

默认三引擎、120 行、12 组、3 个带排名的数值列，含并列、缺失及 higher/lower；每次排名阶段重复 5 次以降低计时噪声。可选参数：

```sh
texlua scripts/benchmark.lua --runtime=sty --output=build/benchmark/large --rows=240 --groups=24 --runs=5 pdflatex
```

`--runtime` 指向同一版本的完整 23 模块目录；输出使用独立的相对目录。行数限定 12–600，组数 1–行数，重复次数 2–10。比较前后版本时，分别提供两套完整源码目录，使用相同参数与引擎，顺序执行，不并发跑其他编译负载。不要用修改过的单个模块混装基线。

输出包含源码副本 `runtime/`、逐文件及数据 MD5 身份 `snapshot.txt`、生成数据/TeX、每次编译 stdout/log/PDF、逐样本 `measurements.csv` 和中位数 `results.md`。MD5 用于识别测量输入，不用于安全验证。

- 时间来自 TeX elapsed timer，每秒 65536 ticks，不包括进程启动；不同引擎结果分别比较。
- 首次进程与后续进程分开记录；不清空操作系统或字体缓存，因此不能称为严格冷启动。报告后续样本中位数，并保留所有样本。
- 独立记录 1000 次显式数值解析、20 次样本统计、5 次排名和一次表格测量；20 次数据条的总路径包含解析、布局与 TikZ，不是纯绘图耗时。这些阶段负载不同，不能相加作为总耗时或比例。
- 不跨平台猜测进程峰值内存；脚本未测量 OS 内存，记录这一限制。耗时不是接口保证，不预先承诺固定百分比或秒级结果。

验收使用语义断言、错误回归、实际 PDF 和分页检查，计时结果不能替代正确性验证。新增用例 [v122-ranking.tex](../tests/cases/v122-ranking.tex) 独立核对并列/次佳、负值、零、缺失、方向与 CSV 重载后的隔离，并检查每组不重复执行整套排名。

静态与 PDF 检查脚本也将 Lua 字体缓存放在各自 `build/` 子目录，不修改全局 TeX 环境；这类工具缓存不同于宏包运行时缓存。

## English

Version 1.2.2 removes duplicate group-ranking work: a single pass supplies both the best and second distinct values. Table/parent/leaf ranking semantics, missing values, ties, higher/lower directions, interfaces and defaults remain unchanged. No cross-call cache, formatter/box cache, new dependency or lightweight backend is introduced.

Static/PDF runners keep Lua font caches in their build directories without changing global TeX configuration. These tool caches are distinct from package runtime caches.

Run `texlua scripts/benchmark.lua --output=build/benchmark/current --runs=3` from the repository root. Defaults are 120 rows, 12 groups, three marked numeric columns and all three engines. Optional `--runtime`, `--rows`, `--groups`, `--runs` and engine arguments select a complete runtime and bounded workload. Run baseline and candidate sequentially with identical parameters and distinct output directories.

The output preserves runtime/data identities, generated inputs, individual compilation logs, all samples and subsequent-run medians. Measurements use the TeX elapsed timer (65536 ticks/second), excluding process startup. First versus subsequent processes does not mean flushed OS/font caches. Separate parsing, statistics, ranking and table measurement workloads are reported; the complete bar path includes parsing/layout/TikZ and is not a pure drawing measurement. Do not sum these phases or infer workload shares. OS peak memory is not measured. Correctness, PDF structure and pagination remain independent acceptance gates; timing is not a performance guarantee.
