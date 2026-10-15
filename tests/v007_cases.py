"""Numeric assertions for stable sorting, group boundaries, ranks and statistics."""

COLS = r"""\gradcolumn[source=Name]{name}{Name}
\gradcolumn[source=Group]{family}{Group}
\gradcolumn[type=number,source=Score,mark=both,aggregate=mean]{score}{Score}
\gradcolumn[type=number,source=Time,mark=both,aggregate=count,options={better=lower}]{time}{Time}
"""
LOAD = r"\gradbarsloadcsv{groups}{build/tests/groups.csv}"


def source(preamble):
    helpers = r"""\ExplSyntaxOn
\tl_new:N\l_vseven_checks_tl
\cs_new_eq:NN\vsevenOriginalMeasure\gradtableMeasureSummary
\cs_set_protected:Npn\gradtableMeasureSummary{\vsevenOriginalMeasure\tl_use:N\l_vseven_checks_tl}
\NewDocumentCommand\groupchecks{m}{\tl_set:Nn\l_vseven_checks_tl{#1}}
\NewDocumentCommand\assertprop{m m m}
 {\tl_set:Nx\l_tmpa_tl{\prop_item:cn{l__gradtable_#1_prop}{#2}}
  \str_if_eq:eeF{\l_tmpa_tl}{#3}{\errmessage{Incorrect~#1~at~#2:~\l_tmpa_tl~vs~#3}}}
\NewDocumentCommand\assertstat{m m}
 {\fp_compare:nNnF{\prop_item:Nn\l__gradtable_group_summary_values_prop{#1}}={#2}
   {\errmessage{Incorrect~group~summary~#1}}}
\ExplSyntaxOff
"""
    body = [helpers, LOAD]

    def case(options, checks, after="", cols=COLS, data="data=groups,"):
        body.append(r"\checks{}\groupchecks{" + checks + "}\n"
                    + r"\begin{gradtable}[width=\linewidth," + data + options + "]\n"
                    + cols + after + r"\end{gradtable}\par\bigskip" + "\n")

    # Global lexicographic order: equal scores break by time, missing values last.
    case("sort keys={score/descending,time/ascending}",
         r"\assertcell{1}{1}{D}\assertcell{2}{1}{B}\assertcell{3}{1}{C}\assertcell{4}{1}{A}\assertcell{5}{1}{NAgroup}\assertcell{6}{1}{Empty}\assertcell{7}{1}{E}\assertcell{8}{1}{F}\assertcell{9}{1}{G}")
    case("sort keys={score/ascending,time/descending}",
         r"\assertcell{1}{1}{E}\assertcell{2}{1}{Empty}\assertcell{3}{1}{NAgroup}\assertcell{4}{1}{A}\assertcell{5}{1}{B}\assertcell{6}{1}{C}\assertcell{7}{1}{D}\assertcell{8}{1}{G}\assertcell{9}{1}{F}")
    case("sort keys={family/descending,time/ascending}",
         r"\assertcell{1}{1}{NAgroup}\assertcell{9}{1}{Empty}")
    # Group order from CSV's first occurrence; reorder selected rows only after global limit.
    case("group by=family,rank scope=group,group summary=true,sort keys={score/descending,time/ascending}",
         r"\assertrows{9}\assertcell{1}{1}{D}\assertcell{2}{1}{A}\assertcell{3}{1}{F}"
         r"\assertcell{4}{1}{B}\assertcell{5}{1}{C}\assertcell{6}{1}{E}\assertcell{7}{1}{G}"
         r"\assertprop{group_best}{1/score}{30}\assertprop{group_second}{1/score}{10}"
         r"\assertprop{group_best}{2/score}{20}\assertprop{group_second}{2/score}{0}"
         r"\assertprop{group_best}{2/time}{2}\assertprop{group_second}{2/time}{4}"
         r"\assertprop{group_labels}{3}{(ungrouped)}\assertprop{group_labels}{4}{NA}"
         r"\assertprop{group_ends}{3}{1}\assertprop{group_ends}{7}{2}"
         r"\assertstat{1/score}{20}\assertstat{2/score}{40/3}\assertstat{1/time}{3}\assertstat{2/time}{4}")
    case("group by=family,group summary=true,sort keys={score/descending,time/ascending},limit=3",
         r"\assertrows{3}\assertcell{1}{1}{D}\assertcell{2}{1}{B}\assertcell{3}{1}{C}"
         r"\assertstat{1/score}{30}\assertstat{2/score}{20}\assertprop{best}{score}{30}",
         r"\gradsummary{Overall}")
    case("group by=family,group summary=true,group summary scope=data,sort=score,order=descending,limit=3",
         r"\assertstat{1/score}{20}\assertstat{2/score}{40/3}")
    case("group by=family,group summary=true,sort=score,order=descending,limit=3",
         r"\assertstat{1/score}{30}\assertstat{2/score}{20}\assertprop{summary_values}{time}{9}",
         r"\gradsummary[scope=data]{All data}")
    case("group by=family,group summary=true,filter={score<=20},sort=score,order=descending",
         r"\assertrows{6}\assertcell{1}{1}{A}\assertcell{2}{1}{B}\assertcell{3}{1}{C}"
         r"\assertstat{1/score}{10}\assertstat{2/score}{40/3}")
    case("group by=family,rank scope=group,group summary=true,filter={score>100}", r"\assertrows{0}")
    case("group by=family,rank scope=group,group summary=true,filter={family=B,score=NA}",
         r"\assertrows{1}\assertprop{group_summary_values}{2/score}{NA}\assertstat{2/time}{1}")
    case("group by=family,group missing label={No family},group summary=true,filter={family=}",
         r"\assertrows{1}\assertprop{groups}{1}{No family}\assertstat{3/score}{5}")
    manual = r"\gradgroup{One}\gradrow{A,A,-5,0}\gradrow{B,A,0,NA}\gradgroup{Two}\gradrow{C,B,3,1}\gradrow{D,B,NA,2}\gradsummary{Overall}"
    case("rank scope=group,group summary=true,rules=grid",
         r"\assertprop{group_best}{1/score}{0}\assertprop{group_second}{1/score}{-5}"
         r"\assertstat{1/score}{-2.5}\assertstat{2/score}{3}\assertstat{1/time}{1}\assertstat{2/time}{2}"
         r"\assertprop{group_ends}{2}{1}\assertprop{group_ends}{4}{2}", manual, data="")
    case("rank scope=group,group summary=true,rules=none",
         r"\assertprop{groups}{1}{(ungrouped)}\assertstat{1/score}{1}\assertstat{2/score}{2}",
         r"\gradrow{A,A,1,0}\gradgroup{Named}\gradrow{B,B,2,1}", data="")
    for operation, result in [('count', 2), ('sum', -5), ('mean', -2.5), ('min', -5), ('max', 0)]:
        cols = (r"\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=" + operation + r"]{score}{Score}")
        case("group summary=true,style=compact,theme=mono", rf"\assertstat{{1/score}}{{{result}}}",
             r"\gradgroup{Repeated}\gradrow{A,-5}\gradrow{B,0}\gradrow{C,NA}"
             r"\gradgroup{Repeated}\gradrow{D,NA}", cols=cols, data="")
    body.append(r"\gradbarsloadcsv[missing={missing}]{literal}{build/tests/group-literal.csv}")
    case("group by=family,group summary=true,rank scope=group",
         r"\assertrows{4}\assertprop{group_labels}{1}{\detokenize{Family, one}}"
         r"\assertprop{group_labels}{2}{missing}\assertprop{group_labels}{3}{(ungrouped)}"
         r"\assertstat{1/score}{15}\assertprop{group_summary_values}{2/score}{NA}\assertstat{3/score}{0}",
         data="data=literal,")
    return preamble + "\n".join(body) + r"\end{document}"


def long_source(preamble):
    return (preamble + r"""\gradscale{pages}{min=0,max=100}
\gradbarsloadcsv{pages}{build/tests/group-long.csv}
\begin{gradtable}[data=pages,long=true,width=\linewidth,style=compact,theme=teal,
  group by=family,group summary=true,group summary label={GROUP SUMMARY},rank scope=group,
  sort keys={value/ascending},caption={Grouped pages}]
\gradcolumn[source=Name]{name}{Name}
\gradcolumn[source=Family]{family}{Family}
\gradcolumn[type=heat,source=Value,mark=both,aggregate=mean,scale group=pages]{value}{Value}
\gradsummary{OVERALL SUMMARY}
\end{gradtable}\end{document}""")


FAILURES = {
    "multi-sort-conflict": (LOAD + r"\begin{gradtable}[data=groups,sort=score,sort keys={score/descending}]" + COLS + r"\end{gradtable}", "Use sort or sort keys"),
    "multi-sort-syntax": (LOAD + r"\begin{gradtable}[data=groups,sort keys={score}]" + COLS + r"\end{gradtable}", "Sort keys require column/direction"),
    "multi-sort-direction": (LOAD + r"\begin{gradtable}[data=groups,sort keys={score/up}]" + COLS + r"\end{gradtable}", "Sort key direction must be"),
    "multi-sort-unknown": (LOAD + r"\begin{gradtable}[data=groups,sort keys={unknown/ascending}]" + COLS + r"\end{gradtable}", "Unknown selection column"),
    "multi-sort-manual": (r"\begin{gradtable}[sort keys={name/ascending}]" + COLS + r"\gradrow{A,A,1,1}\end{gradtable}", "require a CSV data source"),
    "group-by-numeric": (LOAD + r"\begin{gradtable}[data=groups,group by=score]" + COLS + r"\end{gradtable}", "Group by requires a text column"),
    "group-by-manual": (r"\begin{gradtable}[group by=family]" + COLS + r"\gradrow{A,A,1,1}\end{gradtable}", "require a CSV data source"),
    "group-by-unknown": (LOAD + r"\begin{gradtable}[data=groups,group by=unknown]" + COLS + r"\end{gradtable}", "Unknown selection column"),
    "group-by-conflict": (LOAD + r"\begin{gradtable}[data=groups,group by=family]" + COLS + r"\gradgroup{Manual}\end{gradtable}", "Do not combine group by"),
    "group-summary-ungrouped": (r"\begin{gradtable}[group summary=true]" + COLS + r"\gradrow{A,A,1,1}\end{gradtable}", "Group statistics require"),
    "group-rank-ungrouped": (r"\begin{gradtable}[rank scope=group]" + COLS + r"\gradrow{A,A,1,1}\end{gradtable}", "Group statistics require"),
}
