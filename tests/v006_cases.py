"""Additional regression source for summaries, shared scales and table styles."""


def source(preamble):
    helpers = r"""\makeatletter\ExplSyntaxOn
\tl_new:N\l_vsix_checks_tl
\cs_new_eq:NN\vsixOriginalSummary\gradtableBuildSummary
\cs_set_protected:Npn\gradtableBuildSummary{\vsixOriginalSummary\tl_use:N\l_vsix_checks_tl}
\NewDocumentCommand\summarychecks{m}{\tl_set:Nn\l_vsix_checks_tl{#1}}
\NewDocumentCommand\assertsummary{m m}
  {\tl_set:Nx\l_tmpa_tl{\prop_item:Nn\l__gradtable_summary_values_prop{#1}}
   \str_if_eq:nnTF{#2}{NA}
     {\str_if_eq:VnF\l_tmpa_tl{NA}{\errmessage{Expected~missing~summary}}}
     {\fp_compare:nNnF{\l_tmpa_tl}={#2}{\errmessage{Incorrect~summary~statistic}}}}
\NewDocumentCommand\assertbasis{m m}
  {\group_begin:\gradtableConfigure{#1}
   \fp_compare:nNnF{\gradbarsPercentBase}={#2}{\errmessage{Changed~percent~basis}}\group_end:}
\NewDocumentCommand\assertgroup{m m m}
  {\group_begin:\gradbarssetup{min=-999,max=999,scale~group=#1}\gradbarsResolveScaleGroup
   \fp_compare:nNnF{\gradbars@min}={#2}{\errmessage{Incorrect~group~minimum}}
   \fp_compare:nNnF{\gradbars@max}={#3}{\errmessage{Incorrect~group~maximum}}\group_end:}
\ExplSyntaxOff\makeatother
"""
    body = [helpers]
    for operation, expected in [('count', '4'), ('sum', '4'), ('mean', '1'), ('min', '-3'), ('max', '5')]:
        body.append(rf"""\checks{{\assertrows{{5}}\assertcol{{value}}{{-3}}{{5}}}}
\summarychecks{{\assertsummary{{value}}{{{expected}}}}}
\begin{{gradtable}}[scale=column]
\gradcolumn{{name}}{{Item}}
\gradcolumn[type=bar,aggregate={operation},mark=both]{{value}}{{Value}}
\gradrow{{A,0}}\gradrow{{B,-3}}\gradrow{{C,2}}\gradrow{{D,NA}}\gradrow{{E,5}}
\gradsummary{{{operation}}}
\end{{gradtable}}\par\bigskip
""")
    for rows in ('', r'\gradrow{Missing,NA,NA,NA,NA,NA}'):
        body.append(r"""\checks{}
\summarychecks{\assertsummary{n}{0}\assertsummary{sum}{0}\assertsummary{mean}{NA}\assertsummary{min}{NA}\assertsummary{max}{NA}}
\begin{gradtable}[width=\linewidth,style=compact]
\gradcolumn{name}{Item}
\gradcolumn[type=number,aggregate=count]{n}{Count}
\gradcolumn[type=number,aggregate=sum]{sum}{Sum}
\gradcolumn[type=number,aggregate=mean]{mean}{Mean}
\gradcolumn[type=number,aggregate=min]{min}{Min}
\gradcolumn[type=number,aggregate=max]{max}{Max}
""" + rows + r"\gradsummary{Summary}\end{gradtable}\par\bigskip")
    body.append(r"""\gradbarsloadcsv{select}{build/tests/select.csv}
\checks{\assertrows{2}}
\summarychecks{\assertsummary{value}{65}}
\begin{gradtable}[data=select,sort=value,order=descending,limit=2]
\gradcolumn[source=Label]{label}{Label}
\gradcolumn[type=number,source=Score,aggregate=mean]{value}{Mean}
\gradsummary{Visible}
\end{gradtable}\par\bigskip
\summarychecks{\assertsummary{value}{185/7}}
\begin{gradtable}[data=select,sort=value,order=descending,limit=2]
\gradcolumn[source=Label]{label}{Label}
\gradcolumn[type=number,source=Score,aggregate=mean]{value}{Mean}
\gradsummary[scope=data]{All}
\end{gradtable}\par\bigskip
\summarychecks{}
\gradscale{shared}{min=-50,max=100}
\assertgroup{shared}{-50}{100}
{\gradscale{shared}{min=10,max=20}\assertgroup{shared}{10}{20}}
\assertgroup{shared}{-50}{100}
\gradbar[scale group=shared,min=-999,max=999]{-25}\par
\gradheat[scale group=shared,min=-999,max=999]{50}\par
\gradspark[spark range=fixed,scale group=shared]{-20,0,80}\par
\checks{\assertcol{value}{-50}{100}}
\begin{gradtable}[scale group=shared]
\gradcolumn{name}{Item}
\gradcolumn[type=bar,options={min=-999,max=999}]{value}{Value}
\gradrow{A,50}
\end{gradtable}\par\bigskip
""")
    ranges = [
        ('scale padding=10', ['63', '87'], 0, 95.7, 87),
        ('scale padding=10,scale nice=true', ['63', '87'], 0, 100, 87),
        ('scale padding=10', ['-30', '-10'], -33, 0, 0),
        ('include zero=false,scale padding=10', ['70', '90'], 68, 92, 90),
        ('scale padding=10,scale nice=true', ['-3', '5'], -4, 6, 5),
        ('scale nice=true', ['0', '0'], 0, 1, 1),
        ('scale nice=true', ['NA', 'NA'], 0, 1, 1),
        ('include zero=false,scale nice=true', ['7', '7'], 6.4, 7.6, 7.5),
        ('scale nice=true', ['.000003', '.000007'], 0, .000008, .000007),
        ('scale nice=true', ['300000', '700000'], 0, 800000, 700000),
    ]
    for options, rows, low, high, basis in ranges:
        body.append(rf"\checks{{\assertcol{{value}}{{{low}}}{{{high}}}\assertbasis{{value}}{{{basis}}}}}" + "\n"
                    + r"\begin{gradtable}[scale=column," + options + "]\n"
                    + r"\gradcolumn{name}{Item}\gradcolumn[type=number]{value}{Value}" + "\n"
                    + "\n".join(r"\gradrow{A," + value + "}" for value in rows)
                    + "\n" + r"\end{gradtable}\par\bigskip")
    for style in ('academic', 'compact', 'dashboard'):
        for theme in ('blue', 'teal', 'violet', 'orange', 'forest', 'mono'):
            body.append(r"\checks{}\summarychecks{\assertsummary{bar}{81}\assertsummary{heat}{2}}" + "\n"
                        + rf"\begin{{gradtable}}[style={style},theme={theme},width=\linewidth]" + "\n"
                        + r"\gradcolumn{name}{Method}\gradcolumn[type=bar,aggregate=mean]{bar}{Score}"
                        + r"\gradcolumn[type=heat,aggregate=count]{heat}{Heat}" + "\n"
                        + r"\gradrow{A,72,72}\gradrow{B,90,90}\gradsummary{Summary}\end{gradtable}\par\bigskip")
    body.append(r"""\checks{}
\summarychecks{\assertsummary{value}{40.5}}
\begin{gradtable}[long=true,width=\linewidth,style=compact,theme=teal,caption={Summary pages}]
\gradcolumn{name}{Method}\gradcolumn[type=number,aggregate=mean]{value}{Value}
""" + "\n".join(rf"\gradrow{{Row {i},{i}}}" for i in range(1, 81)) + r"""
\gradsummary{Final summary}
\end{gradtable}
\checks{}\summarychecks{}
\begin{gradtable}[scale=column,scale padding=10,scale nice=true]
\gradcolumn{name}{Item}
\gradcolumn[type=bar,aggregate=mean,options={value format=percent,percent base=100}]{value}{Percent}
\gradrow{A,63}\gradrow{B,87}\gradsummary{Mean}
\end{gradtable}
\begin{gradtable}[scale=column,scale padding=10,scale nice=true]
\gradcolumn{name}{Item}
\gradcolumn[type=heat,aggregate=mean,options={value format=percent}]{value}{Percent}
\gradrow{A,63}\gradrow{B,87}\gradsummary{Mean}
\end{gradtable}
""")
    return preamble + "\n".join(body) + r"\end{document}"


FAILURES = {
    'unknown-group': (r'\gradbar[scale group=unknown]{50}', 'Unknown scale group'),
    'invalid-scale': (r'\gradscale{s}{min=10,max=10}', 'Scale max must be greater than min'),
    'empty-scale': (r'\gradscale{}{min=0,max=100}', 'Scale name must not be empty'),
    'group-auto': (r'\gradscale{s}{min=0,max=100}\begin{gradtable}[scale=column]\gradcolumn[type=bar,scale group=s]{a}{A}\gradrow{50}\end{gradtable}', 'Scale group requires'),
    'padding-negative': (r'\begin{gradtable}[scale padding=-1]\gradcolumn{a}{A}\end{gradtable}', 'Scale padding must be nonnegative'),
    'aggregate-text': (r'\begin{gradtable}\gradcolumn[aggregate=mean]{a}{A}\gradsummary{Mean}\end{gradtable}', 'Aggregate requires a scalar numeric column'),
    'aggregate-spark': (r'\begin{gradtable}\gradcolumn[type=spark,aggregate=mean]{a}{A}\end{gradtable}', 'Aggregate requires a scalar numeric column'),
    'summary-outside': (r'\gradsummary{Mean}', 'gradsummary requires gradtable'),
    'summary-double': (r'\begin{gradtable}\gradcolumn{a}{A}\gradsummary{First}\gradsummary{Second}\end{gradtable}', 'Only one summary row'),
    'summary-no-text': (r'\begin{gradtable}\gradcolumn[type=number,aggregate=mean]{a}{A}\gradrow{50}\gradsummary{Mean}\end{gradtable}', 'A summary label requires a text column'),
    'invalid-percent-base': (r'\gradbar[value format=percent,percent base=0]{50}', 'Percent base must be positive'),
}
