# v1.2.2 measurement record / 测量记录

Measured 2026-11-07 on Linux x86_64, TeX Live 2026. Fixed local v1.2.1 development snapshot versus v1.2.2; the baseline was not a published GitHub tag.
120 rows, 12 groups, three marked numeric columns, three processes per engine. Baseline and candidate ran sequentially; no concurrent compilation benchmark. First processes are recorded separately, without flushing OS/font caches.
Timings are TeX elapsed seconds, excluding process startup and OS peak memory. Rank timing repeats the operation five times. Subsequent median uses runs 2 and 3; this small sample does not establish a general performance guarantee.
原始运行目录为 `build/benchmark/v121/` 与 `build/benchmark/v122/`，含完整基线/候选源码、日志和结果；目录不上传。基线为本地快照，不能用不存在的 v1.2.1 标签代替。请保留该目录以重测历史基线；新源码可按性能说明独立测量。

| Engine | Rank before (s) | Rank after (s) | Reduction |
| --- | --- | --- | --- |
| pdflatex | 10.860534 | 7.147407 | 34.19% |
| xelatex | 10.527512 | 6.994507 | 33.56% |
| lualatex | 10.419868 | 6.940933 | 33.39% |

Only the ranking workload improves by about one third. This is not whole-document compile speed. Parsing, statistics and measurement remain separate; no parser/statistics cache is introduced based on these results.

## Baseline

```csv
engine,run,process_state,phase,seconds
pdflatex,1,first,parse-1000,3.528809
pdflatex,1,first,stats-20,1.444412
pdflatex,1,first,bar-total-20,0.269806
pdflatex,1,first,rank-5,10.714813
pdflatex,1,first,measure,2.263168
pdflatex,2,subsequent,parse-1000,3.471069
pdflatex,2,subsequent,stats-20,1.463669
pdflatex,2,subsequent,bar-total-20,0.270111
pdflatex,2,subsequent,rank-5,10.915390
pdflatex,2,subsequent,measure,2.270233
pdflatex,3,subsequent,parse-1000,3.517548
pdflatex,3,subsequent,stats-20,1.471558
pdflatex,3,subsequent,bar-total-20,0.277069
pdflatex,3,subsequent,rank-5,10.805679
pdflatex,3,subsequent,measure,2.270706
xelatex,1,first,parse-1000,3.421951
xelatex,1,first,stats-20,1.449768
xelatex,1,first,bar-total-20,0.267181
xelatex,1,first,rank-5,10.481110
xelatex,1,first,measure,2.239670
xelatex,2,subsequent,parse-1000,3.377457
xelatex,2,subsequent,stats-20,1.418549
xelatex,2,subsequent,bar-total-20,0.266708
xelatex,2,subsequent,rank-5,10.527802
xelatex,2,subsequent,measure,2.195969
xelatex,3,subsequent,parse-1000,3.398636
xelatex,3,subsequent,stats-20,1.413254
xelatex,3,subsequent,bar-total-20,0.264282
xelatex,3,subsequent,rank-5,10.527222
xelatex,3,subsequent,measure,2.207855
lualatex,1,first,parse-1000,3.493713
lualatex,1,first,stats-20,1.409409
lualatex,1,first,bar-total-20,0.261230
lualatex,1,first,rank-5,10.398193
lualatex,1,first,measure,2.427368
lualatex,2,subsequent,parse-1000,3.434387
lualatex,2,subsequent,stats-20,1.393982
lualatex,2,subsequent,bar-total-20,0.254791
lualatex,2,subsequent,rank-5,10.436966
lualatex,2,subsequent,measure,2.185349
lualatex,3,subsequent,parse-1000,3.454330
lualatex,3,subsequent,stats-20,1.398193
lualatex,3,subsequent,bar-total-20,0.260956
lualatex,3,subsequent,rank-5,10.402771
lualatex,3,subsequent,measure,2.206497
```

Runtime/data identities (MD5, identification only):

```text
gradbars-accessible.sty e2c23a2c96f07858b61fc959f5e114f1
gradbars-api.sty 21ebb228ad211a5ed5b2f131e1eaecab
gradbars-backend.sty 0b2365d2e96d50d711b0d8c5afe72281
gradbars-core.sty a1dffb862a6b97bc203d61d3c9d8ad88
gradbars-keys.sty 81e8aa766f0d32c19e1f0458c3e795d9
gradbars-lib-csv.sty 8f280c0c88576dcdba5c6364f2301eb5
gradbars-lib-distribution.sty 5801236bf24cfb080d69e386ba9909bd
gradbars-lib-heat.sty 374940939331f6530cdec0b2c5a08ea8
gradbars-lib-legend.sty c0645f894f8a05bc421cb90efc99c240
gradbars-lib-pgfplotstable.sty 2863cd5e68d7aa4b87aa631273836fa2
gradbars-lib-reports.sty 2f6b8c96b65b02bab069ced7f4de4af4
gradbars-lib-spark.sty 4500aff9bea36c98124ca26db4aae09b
gradbars-lib-stack.sty 3169f999f67c3dd3dae8a19781cae6a2
gradbars-lib-table.sty 1f90404187c539ef88aace29498912a0
gradbars-model.sty 2f4ca03a9c103a76684fc4051e074e08
gradbars-numbers.sty 5881f49360f5c02a69084bea7ffc6a76
gradbars-render-tikz.sty f79d2e1f3b1dd1a5343568910d3f3d49
gradbars-table-data.sty 05965423053ce903d7bb7d205a6e50d7
gradbars-table-layout.sty cfaba4a1c16b4aeea5d967578dba7734
gradbars-tagging.sty 7be92417129e994942d2de3b54147fcc
gradbars-tblr-tagging.sty 81c79cc77c22b3ad547884c9ea7334b3
gradbars.sty 7e20f727338a43d2357f79ffec6e347b
tblrlibgradbars.sty d3465cb2aee02e2dd52f6366e8f87743
data 96b9d54317c459e6da275f6f6b6c950c
```

## Candidate

```csv
engine,run,process_state,phase,seconds
pdflatex,1,first,parse-1000,3.553787
pdflatex,1,first,stats-20,1.475357
pdflatex,1,first,bar-total-20,0.271088
pdflatex,1,first,rank-5,7.174423
pdflatex,1,first,measure,2.251251
pdflatex,2,subsequent,parse-1000,3.486511
pdflatex,2,subsequent,stats-20,1.449554
pdflatex,2,subsequent,bar-total-20,0.267868
pdflatex,2,subsequent,rank-5,7.168701
pdflatex,2,subsequent,measure,2.230347
pdflatex,3,subsequent,parse-1000,3.499329
pdflatex,3,subsequent,stats-20,1.443359
pdflatex,3,subsequent,bar-total-20,0.267258
pdflatex,3,subsequent,rank-5,7.126114
pdflatex,3,subsequent,measure,2.224655
xelatex,1,first,parse-1000,3.380676
xelatex,1,first,stats-20,1.429916
xelatex,1,first,bar-total-20,0.262573
xelatex,1,first,rank-5,7.036850
xelatex,1,first,measure,2.189438
xelatex,2,subsequent,parse-1000,3.482803
xelatex,2,subsequent,stats-20,1.459503
xelatex,2,subsequent,bar-total-20,0.261307
xelatex,2,subsequent,rank-5,7.018158
xelatex,2,subsequent,measure,2.230881
xelatex,3,subsequent,parse-1000,3.372818
xelatex,3,subsequent,stats-20,1.411148
xelatex,3,subsequent,bar-total-20,0.260391
xelatex,3,subsequent,rank-5,6.970856
xelatex,3,subsequent,measure,2.189621
lualatex,1,first,parse-1000,3.434158
lualatex,1,first,stats-20,1.402786
lualatex,1,first,bar-total-20,0.260254
lualatex,1,first,rank-5,6.833801
lualatex,1,first,measure,2.179123
lualatex,2,subsequent,parse-1000,3.400940
lualatex,2,subsequent,stats-20,1.399277
lualatex,2,subsequent,bar-total-20,0.266205
lualatex,2,subsequent,rank-5,6.955978
lualatex,2,subsequent,measure,2.190536
lualatex,3,subsequent,parse-1000,3.382309
lualatex,3,subsequent,stats-20,1.383987
lualatex,3,subsequent,bar-total-20,0.262314
lualatex,3,subsequent,rank-5,6.925888
lualatex,3,subsequent,measure,2.207550
```

Runtime/data identities (MD5, identification only):

```text
gradbars-accessible.sty 052d5cce78671cdd6842aaac0044ed48
gradbars-api.sty 8d6349057fa354dc303cd2fd3b9b6f3b
gradbars-backend.sty dc04a33a697f3807d28f10340a80e1da
gradbars-core.sty 73d0333eb2443c5687fdbf20bb4bf109
gradbars-keys.sty bf6a52b2b4dea3d0a3913ee5efd984aa
gradbars-lib-csv.sty cd7cb0adfdbd261a006ef03f027560db
gradbars-lib-distribution.sty 2ca78c025622b90ac8000f3f9b6bca13
gradbars-lib-heat.sty 4216b03c6a662e837cb0b337ee069314
gradbars-lib-legend.sty 25cb121a7d1a68dbabf35f1789480f37
gradbars-lib-pgfplotstable.sty 57f62ec7c6dad071e25dc5b510b3b535
gradbars-lib-reports.sty d7e9aea9bafaeab885ee097601b42f7c
gradbars-lib-spark.sty 21fbd00c8f7322d8d2aee2c371b1250e
gradbars-lib-stack.sty 4e95bd806901820fbfdd9185197a3d8b
gradbars-lib-table.sty b83fc36b8f962d0fea9748813769c650
gradbars-model.sty fcc9a26dcfa825645a825b47470309cf
gradbars-numbers.sty d342c78df2f94b57f528da612a7422f7
gradbars-render-tikz.sty 989dd0fe7a29073cc1650cf5c46986f6
gradbars-table-data.sty 777ea129a190c474f1276bd405d8a5a1
gradbars-table-layout.sty fa1c49ab91f5a5b379390fc0433d1a05
gradbars-tagging.sty 8dc49a852575b9c93b70907378807072
gradbars-tblr-tagging.sty db2faf80a545912a450621cbeeb8494e
gradbars.sty 123843ad6f1efb4ce4a4c5cc58ca2d6e
tblrlibgradbars.sty 72adec5b449252d64e7fbcf464cd7fe5
data 96b9d54317c459e6da275f6f6b6c950c
```

## Engine versions

- pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026)
- XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026)
- This is LuaHBTeX, Version 1.24.0 (TeX Live 2026)

No fixed improvement is promised for other data, machines or future runs. Correctness/PDF/page checks are reported separately. / 其他负载不承诺同等提速，正确性与 PDF/分页检查单独验收。
