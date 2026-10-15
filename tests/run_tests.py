"""Compile data, scale, heat and spark regressions with each TeX engine (stdlib only).

Run: python tests/run_tests.py
Optional: python tests/run_tests.py --engines pdflatex xelatex
Outputs are kept in build/tests; no shell escape or external data is needed.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import v006_cases
import v007_cases
import v008_cases
import v010_cases
import v100_cases

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "tests"
PREAMBLE = r"""\documentclass{article}
\usepackage[margin=20mm]{geometry}
\usepackage{gradbars}
\setlength{\parindent}{0pt}
\makeatletter
\ExplSyntaxOn
\cs_new_eq:NN\testOriginalRanges\gradtableAutoRanges
\tl_new:N\l_test_checks_tl
\cs_set_protected:Npn\gradtableAutoRanges
  {\testOriginalRanges\tl_use:N\l_test_checks_tl}
\NewDocumentCommand\checks{m}{\tl_set:Nn\l_test_checks_tl{#1}}
\NewDocumentCommand\assertcol{m m m}
  {\group_begin:\gradtableConfigure{#1}
   \fp_compare:nNnF{\gradbars@min}={#2}{\errmessage{Incorrect~minimum~for~#1}}
   \fp_compare:nNnF{\gradbars@max}={#3}{\errmessage{Incorrect~maximum~for~#1}}
   \group_end:}
\NewDocumentCommand\assertrows{m}
  {\int_compare:nNnF{\seq_count:N\l__gradtable_rows_seq}={#1}{\errmessage{Incorrect~CSV~row~count}}}
\NewDocumentCommand\assertcell{m m m}
  {\clist_set:Nx\l_tmpa_clist{\seq_item:Nn\l__gradtable_rows_seq{#1}}
   \tl_set:Nx\l_tmpa_tl{\clist_item:Nn\l_tmpa_clist{#2}}
   \str_if_eq:eeF{\tl_to_str:V\l_tmpa_tl}{\tl_to_str:n{#3}}{\errmessage{Incorrect~selected~cell}}}
\NewDocumentCommand\assertheat{m m m}
  {\group_begin:\gradbarssetup{#1}\gradbarsHeatColor{#2}
   \convertcolorspec{named}{gradbarsHeatCell}{rgb}\testActualRGB
   \convertcolorspec{named}{#3}{rgb}\testExpectedRGB
   \clist_set:Nx\l_tmpa_clist{\testActualRGB}\clist_set:Nx\l_tmpb_clist{\testExpectedRGB}
   \int_step_inline:nn{3}
     {\fp_compare:nNnT{abs(\clist_item:Nn\l_tmpa_clist{##1}-\clist_item:Nn\l_tmpb_clist{##1})}>{.0002}
       {\errmessage{Incorrect~heat~interpolation}}}\group_end:}
\ExplSyntaxOff
\makeatother
\begin{document}
"""


def table(options, columns, rows, checks):
    return (r"\checks{" + checks + "}\n" + r"\begin{gradtable}[" + options + "]\n"
            + columns + "\n" + "\n".join(r"\gradrow{" + row + "}" for row in rows)
            + "\n" + r"\end{gradtable}\par\bigskip" + "\n")


def regression_source():
    body = []
    scalar = r"\gradcolumn[type=heat]{value}{Value}"
    cases = [
        ("", ["70", "90", "NA"], 0, 90),
        ("", ["-30", "-10", "NA"], -30, 0),
        (",include zero=false", ["70", "90", "NA"], 70, 90),
        (",include zero=false", ["-30", "-10", "NA"], -30, -10),
        ("", ["-8", "12"], -8, 12),
        ("", ["7", "7"], 0, 7),
        (",include zero=false", ["7", "7"], 6.5, 7.5),
        (",include zero=false", ["-7", "-7"], -7.5, -6.5),
        ("", ["0", "0"], 0, 1),
        (",include zero=false", ["0", "0"], -.5, .5),
        ("", ["NA", "NA"], 0, 1),
        (",include zero=false", ["NA", "NA"], 0, 1),
        ("", [], 0, 1),
    ]
    for options, rows, low, high in cases:
        body.append(table("scale=column" + options, scalar, rows,
                          rf"\assertcol{{value}}{{{low}}}{{{high}}}"))
    body.append(table("scale=column,graphic width=25mm,label width=12mm",
                      r"\gradcolumn[type=stack]{stack}{Stack}" "\n"
                      r"\gradcolumn[type=compare]{pair}{Pair}" "\n"
                      r"\gradcolumn[type=interval]{interval}{Interval}",
                      ["{20,30,-10},40/60,30/40/70", "{5,10,-40},NA/80,NA"],
                      r"\assertcol{stack}{-40}{50}\assertcol{pair}{0}{80}\assertcol{interval}{0}{70}"))
    body.append(table("scale=column,include zero=false",
                      r"\gradcolumn[type=spark]{spark}{Trend}",
                      ["{70,NA,90}", "{75,80,NA}"], r"\assertcol{spark}{70}{90}"))
    body.append(table("scale=column",
                      r"\gradcolumn[type=bar,scale=fixed,options={min=-50,max=100}]{fixed}{Fixed}" "\n"
                      r"\gradcolumn[type=heat,include zero=false,options={min=0,max=200}]{auto}{Auto}",
                      ["10,70", "20,90"], r"\assertcol{fixed}{-50}{100}\assertcol{auto}{70}{90}"))
    body.append(r"""\gradbarsloadcsv[missing={missing}]{special}{build/tests/special.csv}
\checks{\assertrows{4}\assertcol{score}{0}{90}\assertcol{same}{70}{90}}
\begin{gradtable}[data=special,scale=column,width=\linewidth]
\gradcolumn[source=Label]{label}{Label}
\gradcolumn[type=bar,source=Score]{score}{Score}
\gradcolumn[type=heat,source=Score,include zero=false]{same}{Same}
\end{gradtable}
\checks{}
\gradbarsloadcsv{empty}{build/tests/empty.csv}
\begin{gradtable}[data=empty,scale=column]
\gradcolumn[source=Label]{label}{Label}
\gradcolumn[type=heat,source=Score]{score}{Score}
\end{gradtable}
\gradtablestyle{auto}{scale=column,include zero=false}
\gradtableschema{heat}{\gradcolumn[type=heat,mark=both,options={better=lower}]{value}{Heat}}
\begin{gradtable}[style=auto]
\graduseschema{heat}
\gradrow{70}\gradrow{90}\gradrow{70}\gradrow{NA}
\end{gradtable}
\gradbarsloadcsv{longdata}{build/tests/long.csv}
\checks{\assertrows{90}\assertcol{Score}{0}{90}}
\begin{gradtable}[data=longdata,long=true,width=\linewidth,scale=column,caption={CSV pages}]
\gradcolumn[source=Label]{label}{Label}
\gradcolumn[type=heat]{Score}{Score}
\end{gradtable}
\checks{}
\gradheat[min=-10,max=10]{-10}\gradheat[min=-10,max=10]{0}\gradheat[min=-10,max=10]{10}\par
\gradheat[print]{50}\gradheat[label=none]{75}\gradheat{NA}\par
\gradheat[heat low color=white,heat high color=red,heat text color=black,height=5ex]{75}\par
\begin{tikzpicture}\gradheat[min=70,max=90]{80}\end{tikzpicture}
""")
    return PREAMBLE + "\n".join(body) + r"\end{document}"


def extensions_source():
    columns = (r"\gradcolumn[source=Label]{label}{Label}" "\n"
               r"\gradcolumn[type=heat,source=Score]{score}{Score}" "\n"
               r"\gradcolumn[source=Group]{group}{Group}")
    cases = [
        ("sort=score,order=descending", 9, [(1, "Zed"), (2, "Bravo"), (3, "Charlie"), (8, "Delta"), (9, "Golf")], -5, 100),
        ("sort=score", 9, [(1, "Foxtrot"), (2, "Echo"), (5, "Bravo"), (6, "Charlie"), (9, "Golf")], -5, 100),
        ("sort=label,order=descending", 9, [(1, "Zed"), (8, "Alpha"), (9, "")], -5, 100),
        ("sort=score,order=descending,limit=3", 3, [(1, "Zed"), (2, "Bravo"), (3, "Charlie")], -5, 100),
        ("filter={group=A},sort=score,order=descending,limit=2", 2, [(1, "Charlie"), (2, "")], -5, 100),
        ("filter={group=A},sort=score,order=descending,limit=2,scale scope=visible", 2, [(1, "Charlie"), (2, "")], 0, 30),
        ("filter={score>=10,score<=30,group=A}", 3, [(1, "Alpha"), (2, "Charlie"), (3, "")], -5, 100),
        ("filter={score=NA}", 2, [(1, "Delta"), (2, "Golf")], -5, 100),
        ("filter={score!=NA}", 7, [(1, "Alpha"), (7, "")], -5, 100),
        ("filter={score=30.0}", 2, [(1, "Bravo"), (2, "Charlie")], -5, 100),
        ("filter={score!=30}", 5, [(1, "Alpha"), (5, "")], -5, 100),
        ("filter={label=}", 1, [(1, "")], -5, 100),
        ("filter={score>200},scale scope=visible", 0, [], 0, 1),
        ("filter={score>200}", 0, [], -5, 100),
        ("filter={score<0}", 1, [(1, "Foxtrot")], -5, 100),
    ]
    body = [r"\gradbarsloadcsv{select}{build/tests/select.csv}"]
    for options, count, cells, low, high in cases:
        checks = rf"\assertrows{{{count}}}\assertcol{{score}}{{{low}}}{{{high}}}"
        checks += "".join(rf"\assertcell{{{row}}}{{1}}{{{value}}}" for row, value in cells)
        body.append(table("data=select,scale=column,width=\\linewidth," + options, columns, [], checks))
    body.append(r"""\checks{}
\gradbarsloadcsv[missing={missing}]{special}{build/tests/special.csv}
\checks{\assertrows{1}\assertcell{1}{2}{70}}
\begin{gradtable}[data=special,filter={{label=Comma, quote "yes"}}]
\gradcolumn[source=Label]{label}{Label}
\gradcolumn[type=number,source=Score]{score}{Score}
\end{gradtable}
\checks{}
\assertheat{heat palette=diverging,min=-50,max=100}{-50}{gradbarsOrange}
\assertheat{heat palette=diverging,min=-50,max=100}{0}{white}
\assertheat{heat palette=diverging,min=-50,max=100}{100}{gradbarsTeal}
\assertheat{heat palette=diverging,min=-50,max=100}{-25}{gradbarsOrange!50!white}
\assertheat{heat palette=diverging,min=-50,max=100}{50}{gradbarsTeal!50!white}
\assertheat{heat palette=diverging,min=20,max=80,heat center=50}{50}{white}
\assertheat{heat palette=diverging,min=0,max=100}{0}{white}
\assertheat{heat palette=diverging,min=-50,max=0}{0}{white}
\assertheat{heat palette=diverging,min=-50,max=100,better=lower}{-50}{gradbarsTeal}
\assertheat{heat palette=diverging,min=-50,max=100,print}{-50}{black!75}
\assertheat{heat palette=diverging,min=-50,max=100,print}{100}{black!75}
\gradspark[spark type=bar]{0,0,NA}\par
\gradspark[spark type=bar]{-10,-20,-30}\par
\gradspark[spark type=bar]{10,20,30}\par
\gradspark[spark type=bar]{NA,NA}\par
\gradspark[spark type=bar]{25}\par
\gradspark[spark type=bar,spark range=fixed,min=-40,max=40]{-30,0,30,NA}\par
\gradspark[spark type=winloss]{20,-100,0,NA}\par
\gradspark[spark type=winloss,spark range=fixed,min=10,max=20]{-100,100,0}\par
\gradspark[spark type=winloss]{NA,NA}\par
\gradspark[spark type=winloss,print]{20,-10,0}\par
\gradspark[spark type=bar,print,spark bar width=1]{20,-10,0}\par
\begin{tikzpicture}\gradspark[spark type=bar]{10,-10,0}\end{tikzpicture}\par
""")
    body.append(table("data=longdata,long=true,scale=column,sort=Score,order=descending,limit=80,caption={Sorted CSV pages},width=\\linewidth",
                      r"\gradcolumn[source=Label]{label}{Label}" "\n" r"\gradcolumn[type=heat]{Score}{Score}", [],
                      r"\assertrows{80}\assertcol{Score}{0}{90}\assertcell{1}{2}{90}\assertcell{80}{2}{11}"))
    return PREAMBLE + "\n".join([r"\gradbarsloadcsv{longdata}{build/tests/long.csv}"] + body) + r"\end{document}"


FAILURES = {
    "unknown-data": (r"\begin{gradtable}[data=unknown]\gradcolumn{a}{A}\end{gradtable}", "Unknown CSV dataset"),
    "unknown-source": (r"\gradbarsloadcsv{data}{build/tests/special.csv}\begin{gradtable}[data=data]\gradcolumn[source=unknown]{a}{A}\end{gradtable}", "Unknown CSV column"),
    "mixed-rows": (r"\gradbarsloadcsv{data}{build/tests/special.csv}\begin{gradtable}[data=data]\gradcolumn[source=Label]{a}{A}\gradrow{manual}\end{gradtable}", "cannot also contain manual rows"),
    "invalid-number": (r"\begin{gradtable}[scale=column]\gradcolumn[type=heat]{a}{A}\gradrow{bad}\end{gradtable}", "Auto scale requires decimal"),
    "heat-range": (r"\gradheat[min=10,max=10]{10}", "Max must be greater than min"),
    "heat-overflow": (r"\gradheat[overflow=error]{101}", "Heat value exceeds range"),
    "heat-precision": (r"\gradheat[precision=7]{50}", "Precision must be an integer"),
    "heat-percent": (r"\gradheat[min=70,max=90,value format=percent]{80}", "Percent format requires min=0"),
    "bar-range": (r"\gradbar[min=10,max=10]{10}", "Max must be greater than min"),
    "heat-center": (r"\gradheat[heat palette=diverging,min=10,max=20,heat center=0]{15}", "Heat center must lie within range"),
    "heat-center-text": (r"\gradheat[heat palette=diverging,heat center=bad]{50}", "Invalid heat center"),
    "spark-width": (r"\gradspark[spark type=bar,spark bar width=0]{10,20}", "Spark bar width must be in"),
    "winloss-percent": (r"\gradspark[spark type=winloss,value format=percent]{10,-10}", "Win-loss does not support percent"),
    "selection-manual": (r"\begin{gradtable}[sort=a]\gradcolumn{a}{A}\gradrow{Text}\end{gradtable}", "require a CSV data source"),
    "selection-unknown": (r"\gradbarsloadcsv{data}{build/tests/select.csv}\begin{gradtable}[data=data,sort=unknown]\gradcolumn[source=Label]{a}{A}\end{gradtable}", "Unknown selection column"),
    "filter-text-order": (r"\gradbarsloadcsv{data}{build/tests/select.csv}\begin{gradtable}[data=data,filter={a>Alpha}]\gradcolumn[source=Label]{a}{A}\end{gradtable}", "Text filters support only"),
    "filter-bad-value": (r"\gradbarsloadcsv{data}{build/tests/select.csv}\begin{gradtable}[data=data,filter={a>bad}]\gradcolumn[type=number,source=Score]{a}{A}\end{gradtable}", "Invalid filter value"),
    "filter-bad-syntax": (r"\gradbarsloadcsv{data}{build/tests/select.csv}\begin{gradtable}[data=data,filter={a}]\gradcolumn[source=Label]{a}{A}\end{gradtable}", "Filter requires column operator value"),
    "negative-limit": (r"\begin{gradtable}[limit=-1]\gradcolumn{a}{A}\end{gradtable}", "Limit must be a nonnegative"),
}


def compile_case(engine, name, source, expected_error=None, passes=1):
    tex = BUILD / (name + ".tex")
    with tex.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(source)
    output = BUILD / engine
    output.mkdir(exist_ok=True)
    environment = os.environ.copy()
    environment['TEXINPUTS'] = 'sty' + os.pathsep + environment.get('TEXINPUTS', '') + os.pathsep
    environment['max_print_line'] = '1000'
    if engine == 'lualatex':
        cache = BUILD / 'tex-cache'
        cache.mkdir(exist_ok=True)
        environment['TEXMFVAR'] = str(cache)
        environment['TEXMFCACHE'] = str(cache)
    for _ in range(passes):
        result = subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error",
                                 "-output-directory=" + str(output), str(tex)], cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=environment)
        log = result.stdout.decode("utf-8", errors="replace")
        if expected_error:
            if result.returncode == 0 or expected_error not in " ".join(log.split()):
                raise RuntimeError(f"{engine}/{name}: expected {expected_error}\n{log[-4000:]}")
        elif result.returncode or "Package gradbars Warning" in log or "Overfull" in log:
            raise RuntimeError(f"{engine}/{name} failed:\n{log[-5000:]}")


def main():
    import tblr_cases
    parser = argparse.ArgumentParser()
    parser.add_argument("--engines", nargs="+", default=["pdflatex", "xelatex", "lualatex"])
    parser.add_argument('--tblr-only', action='store_true')
    args = parser.parse_args()
    BUILD.mkdir(parents=True, exist_ok=True)
    if args.tblr_only:
        for engine in args.engines:
            tblr_cases.run(engine, compile_case)
        return
    (BUILD / "special.csv").write_text(
        'Score,Label\n70,"Comma, quote ""yes"""\n90,100% & \\undefinedcommand\nmissing,\n,""\n', encoding="utf-8")
    (BUILD / "empty.csv").write_text("Label,Score\n", encoding="utf-8")
    (BUILD / "long.csv").write_text("Label,Score\n" + "".join(f"Row {i},{i}\n" for i in range(1, 91)), encoding="utf-8")
    (BUILD / "select.csv").write_text("Label,Score,Group\nAlpha,10,A\nBravo,30,B\nCharlie,30,A\nDelta,,A\nEcho,0,B\nFoxtrot,-5,A\nGolf,NA,B\nZed,100,B\n,20,A\n", encoding="utf-8")
    (BUILD / "groups.csv").write_text("Name,Group,Score,Time\nA,A,10,5\nB,B,20,4\nC,B,20.0,4.0\nD,A,30,2\nE,B,0,2\nF,A,NA,1\nG,B,NA,9\nEmpty,,5,6\nNAgroup,NA,5,5\n", encoding="utf-8")
    (BUILD / "group-long.csv").write_text("Name,Family,Value\n" + "".join(
        f"Row-{i:03d},Family-{(i-1)//40+1},{i}\n" for i in range(1, 81)), encoding="utf-8")
    (BUILD / "group-literal.csv").write_text('Name,Group,Score,Time\nA,"Family, one",10,1\nB,missing,missing,2\nC,"Family, one",20,3\nD,,0,4\n', encoding="utf-8")
    (BUILD / "scientific.csv").write_text('Name,Family,Value,Time\nA,First,1e-3,4\nB,First,.001,2\nC,Second,-2.5E-3,3\nD,Second,NA,NA\n', encoding='utf-8')
    (BUILD / 'gradbars-lib-mismatch.sty').write_text(r'\ProvidesPackage{gradbars-lib-mismatch}[2026/10/09 v0.0.8 Test mismatched module]' + '\n' + r'\endinput' + '\n', encoding='utf-8')
    smoke = (ROOT / "tests" / "p0-smoke.tex").read_text(encoding="utf-8")
    for engine in args.engines:
        if not shutil.which(engine):
            raise SystemExit(f"Required engine not found: {engine}")
        compile_case(engine, "p0-smoke", smoke)
        compile_case(engine, "regression", regression_source(), passes=2)
        compile_case(engine, "extensions-smoke", (ROOT / "tests" / "extensions-smoke.tex").read_text(encoding="utf-8"))
        compile_case(engine, "extensions-regression", extensions_source(), passes=2)
        compile_case(engine, "v006-smoke", (ROOT / "tests" / "v006-smoke.tex").read_text(encoding="utf-8"))
        compile_case(engine, "v006-regression", v006_cases.source(PREAMBLE), passes=2)
        compile_case(engine, "v007-smoke", (ROOT / "tests" / "v007-smoke.tex").read_text(encoding="utf-8"))
        compile_case(engine, "v007-regression", v007_cases.source(PREAMBLE), passes=2)
        compile_case(engine, "v007-long", v007_cases.long_source(PREAMBLE), passes=2)
        compile_case(engine, "v008-smoke", (ROOT / 'tests' / 'v008-smoke.tex').read_text(encoding='utf-8'))
        compile_case(engine, "v008-builtin", v008_cases.source(PREAMBLE), passes=2)
        compile_case(engine, "v008-siunitx", v008_cases.source(PREAMBLE, si=True), passes=2)
        compile_case(engine, "v008-long", v008_cases.long_source(PREAMBLE), passes=2)
        compile_case(engine, "v008-alignment", (ROOT / 'tests' / 'v008-alignment.tex').read_text(encoding='utf-8'), passes=2)
        for name in ('v010-minimal', 'v010-smoke', 'issue-v010'):
            compile_case(engine, name, (ROOT / 'tests' / (name + '.tex')).read_text(encoding='utf-8'))
        for name, source in v010_cases.sources().items():
            compile_case(engine, name, source)
        for name, source in v100_cases.sources().items():
            compile_case(engine, name, source)
        tblr_cases.run(engine, compile_case)
        if shutil.which('pdftotext'):
            result = subprocess.run(['pdftotext', '-layout', str(BUILD / engine / 'v007-long.pdf'), '-'], stdout=subprocess.PIPE, check=True)
            pages = result.stdout.decode('utf-8').split('\f')
            for last_row in ('Row-040', 'Row-080'):
                page = next(page for page in pages if last_row in page)
                if 'GROUP SUMMARY' not in page:
                    raise RuntimeError('Group summary separated from last data row: ' + last_row)
            for family, first_row in [('Family-1', 'Row-001'), ('Family-2', 'Row-041')]:
                page = next(page for page in pages if first_row in page)
                if not any(line.strip() == family for line in page.splitlines()):
                    raise RuntimeError('Group heading separated from first row: ' + family)
            text = ''.join(pages)
            if text.count('GROUP SUMMARY') != 2 or text.count('OVERALL SUMMARY') != 1:
                raise RuntimeError('Duplicated/missing multipage summaries')
            if 'OVERALL SUMMARY' not in next(page for page in pages if 'Row-080' in page):
                raise RuntimeError('Overall summary separated from final group')
            verify_research_pages(engine)
        for name, (body, error) in dict(FAILURES, **v006_cases.FAILURES, **v007_cases.FAILURES, **v008_cases.FAILURES).items():
            compile_case(engine, name, PREAMBLE + body + r"\end{document}", error)
        for name, (body, error) in v008_cases.SI_FAILURES.items():
            compile_case(engine, name, PREAMBLE.replace(r'\usepackage{gradbars}', r'\usepackage{siunitx}\usepackage{gradbars}') + body + r"\end{document}", error)
        for name, (pre, operation, error) in v010_cases.FAILURES.items():
            compile_case(engine, name, v010_cases.failure_source(pre, operation), error)
        for name, (pre, operation, error) in v100_cases.FAILURES.items():
            compile_case(engine, name, v010_cases.failure_source(pre, operation), error)
        print(f"{engine}: modules, public APIs and existing regressions; {len(FAILURES)+len(v006_cases.FAILURES)+len(v007_cases.FAILURES)+len(v008_cases.FAILURES)+len(v010_cases.FAILURES)+len(v008_cases.SI_FAILURES)+len(v100_cases.FAILURES)} expected failures passed", flush=True)


def verify_research_pages(engine):
    result = subprocess.run(['pdftotext', '-layout', str(BUILD / engine / 'v008-long.pdf'), '-'], stdout=subprocess.PIPE, check=True)
    pages = result.stdout.decode('utf-8').split('\f')
    text = ''.join(pages)
    if text.count('Summary') != 1 or text.count('Final summary') != 1:
        raise RuntimeError('Duplicated/missing research summaries')
    page = next(page for page in pages if 'Row-080' in page)
    if 'Summary' not in page or 'Final summary' not in page:
        raise RuntimeError('Research summary separated from final row')
    page = next(page for page in pages if 'Row-001' in page)
    if 'Research group' not in page:
        raise RuntimeError('Research group heading separated from first row')


if __name__ == "__main__":
    main()
