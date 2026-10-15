"""Scientific input equivalence and decimal anchors, including group summaries."""


def source(preamble, si=False):
    if si:
        preamble = preamble.replace(r'\usepackage{gradbars}', r'\usepackage{siunitx}\usepackage{gradbars}')
    helpers = r"""\makeatletter\ExplSyntaxOn
\tl_new:N\l_veight_checks_tl
\cs_new_eq:NN\veightOriginalDecimals\gradtableMeasureDecimals
\cs_set_protected:Npn\gradtableMeasureDecimals{\veightOriginalDecimals\tl_use:N\l_veight_checks_tl}
\NewDocumentCommand\decimalchecks{m}{\tl_set:Nn\l_veight_checks_tl{#1}}
\NewDocumentCommand\assertnumericprop{m m m}
  {\fp_compare:nNnF{\prop_item:cn{l__gradtable_#1_prop}{#2}}={#3}{\errmessage{Incorrect~#1~#2}}}
\NewDocumentCommand\assertdecimal{m m}
  {\group_begin:\gradtableConfigure{#1}\hbox_set:Nn\l_tmpa_box{\gradtableNumber{#2}}
   \fp_compare:nNnT{abs(\dim_to_fp:n{\box_wd:N\l_tmpa_box-\prop_item:Nn\l__gradtable_decimal_left_prop{#1}-\prop_item:Nn\l__gradtable_decimal_right_prop{#1}})}>{.01}
     {\errmessage{Decimal~cell~does~not~match~column~anchors}}
   \dim_compare:nNnF{\prop_item:Nn\l__gradtable_decimal_left_prop{#1}}>{0pt}{\errmessage{No~decimal~left~anchor}}
   \group_end:}
\NewDocumentCommand\assertparts{m m m m}
  {\group_begin:\pgfkeys{/gradbars,precision=2,number~format=#1}\gradbarsDecimalParts{#2}
   \fp_compare:nNnF{\l__gradbars_decimal_value_fp}={#3}{\errmessage{Incorrect~display~rounding}}
   \int_compare:nNnF{\l__gradbars_decimal_exponent_int}={#4}{\errmessage{Incorrect~exponent}}
   \group_end:}
\gradbarsIfNumber:nF{1e100}{\errmessage{Rejected~upper~boundary}}
\gradbarsIfNumber:nF{-1E-100}{\errmessage{Rejected~lower~boundary}}
\gradbarsIfNumber:nT{1e101}{\errmessage{Accepted~overflow}}
\gradbarsIfNumber:nT{1e-101}{\errmessage{Accepted~underflow}}
\gradbarsIfNumber:nT{NaN}{\errmessage{Accepted~NaN}}
\ExplSyntaxOff\makeatother
\assertparts{fixed}{1.125}{1.13}{0}
\assertparts{fixed}{-1.125}{-1.13}{0}
\assertparts{scientific}{9.995e3}{1}{4}
\assertparts{scientific}{1e-3}{1}{-3}
\assertparts{scientific}{0}{0}{0}
"""
    formatter = 'siunitx' if si else 'builtin'
    bodies = [helpers]
    for rows in ([r'A,0.001,0.002', r'B,-0.0025,0.004', r'C,NA,0'],
                 [r'A,1e-3,2E-3', r'B,-2.5E-3,4e-3', r'C,NA,0e9']):
        bodies.append(r"\checks{\assertcol{v}{-.0025}{.001}\assertcol{w}{0}{.004}}" + '\n'
                      + r"\decimalchecks{\assertnumericprop{best}{v}{.001}\assertnumericprop{second}{v}{-.0025}\assertnumericprop{summary_values}{v}{-.00075}\assertdecimal{v}{-.0025}}" + '\n'
                      + r'\begin{gradtable}[style=research,theme=teal,scale=column,width=\linewidth,formatter=' + formatter + ']\n'
                      + r'\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=mean,mark=both,options={precision=6}]{v}{Value}' + '\n'
                      + r'\gradcolumn[type=heat]{w}{Heat}' + '\n'
                      + '\n'.join(r'\gradrow{' + row + '}' for row in rows)
                      + r'\gradsummary{Mean}\end{gradtable}\par\bigskip' + '\n')
    bodies.append(r"""\checks{}\decimalchecks{}
\gradbarsloadcsv{scientific}{build/tests/scientific.csv}
\decimalchecks{\assertcell{1}{1}{B}\assertcell{2}{1}{A}\assertcell{3}{1}{C}
\assertnumericprop{group_best}{1/value}{.001}\assertnumericprop{group_best}{2/value}{-.0025}
\assertnumericprop{group_summary_values}{1/value}{.001}\assertdecimal{value}{.001}}
\begin{gradtable}[data=scientific,width=\linewidth,style=research,theme=violet,scale=column,
  group by=family,rank scope=group,group summary=true,sort keys={value/descending,time/ascending},formatter="""
                  + formatter + r""" ]
\gradcolumn[source=Name]{name}{Name}\gradcolumn[source=Family]{family}{Family}
\gradcolumn[type=number,source=Value,mark=both,aggregate=mean,options={precision=4,number format=scientific}]{value}{Value}
\gradcolumn[type=number,source=Time,aggregate=count]{time}{Time}
\gradsummary{Overall}\end{gradtable}\par\bigskip
\decimalchecks{}\checks{\assertrows{2}\assertcell{1}{1}{B}\assertcell{2}{1}{A}}
\begin{gradtable}[data=scientific,style=research,width=\linewidth,filter={value>=1E-3},sort=time]
\gradcolumn[source=Name]{name}{Name}\gradcolumn[type=number,source=Value,options={precision=4}]{value}{Value}
\gradcolumn[type=number,source=Time]{time}{Time}\end{gradtable}\par\bigskip
\checks{\assertcol{pair}{0}{400}\assertcol{stack}{-100}{500}\assertcol{spark}{-.002}{.001}}
\begin{gradtable}[width=\linewidth,style=compact,scale=column]
\gradcolumn[type=dumbbell]{pair}{Pair}\gradcolumn[type=stack]{stack}{Stack}\gradcolumn[type=spark]{spark}{Spark}
\gradrow{2e2/4E2,{-1e2,2E2,3e2},{1e-3,NA,-2E-3}}\end{gradtable}\par\bigskip
\decimalchecks{}\checks{}
\begin{gradtable}[style=research,width=\linewidth,theme=mono,formatter=""" + formatter + r""" ]
\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=sum,mark=both,options={precision=2,number format=grouped}]{value}{Value}
\gradrow{A,-12345.125}\gradrow{B,1.995}\gradrow{C,0}\gradrow{Missing,NA}\gradsummary{Sum}
\end{gradtable}\par\bigskip
\gradscale{tiny}{min=-1E-2,max=1e-2}
\gradbar[scale group=tiny,number format=scientific]{1e-3}\par
\gradheat[scale group=tiny,number format=scientific]{-2.5E-3}\par
\graddumbbell[min=0,max=1e6,number format=scientific]{2e5}{8E5}\par
\gradrange[min=0,max=1e6,number format=scientific,range point=5e5]{2e5}{8E5}\par
\gradstack[min=-1e3,max=1e3,number format=scientific]{2e2,-3E2,4e2}\par
\gradspark[number format=scientific]{1e-4,-2e-4,0,NA}\par
\gradspark[spark type=bar,number format=scientific]{1e-4,-2e-4,0,NA}\par
\gradspark[spark type=winloss]{1e-4,-2e-4,0,NA}\par
\gradbar[min=0,max=1e100,number format=scientific]{1e100}\par
\gradbar[min=0,max=1e-100,number format=scientific]{1e-100}\par
""")
    for theme in ('blue', 'teal', 'violet', 'orange', 'forest', 'mono'):
        bodies.append(r'\decimalchecks{}\checks{}\begin{gradtable}[style=research,width=\linewidth,theme=' + theme + ',formatter=' + formatter + r''',group summary=true]
\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=mean,mark=both,options={precision=3}]{value}{Value}
\gradcolumn[type=heat,aggregate=count]{heat}{Heat}
\gradgroup{Group}\gradrow{A,-12.125,10}\gradrow{B,1.25,20}\gradrow{Missing,NA,NA}\gradsummary{Overall}
\end{gradtable}\par\bigskip
''')
    if si:
        bodies.append(r"""\gradbar[formatter=siunitx,precision=3,unit code={\milli\second},unit text={milliseconds}]{12.3456}\par
\graddumbbell[formatter=siunitx,compare label=percent,unit code={\milli\second},unit text={milliseconds}]{20}{30}\par
\begin{gradtable}[style=research,width=\linewidth,formatter=siunitx,theme=forest,group summary=true]
\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=count,options={unit code={\milli\second},unit text={milliseconds},precision=3}]{time}{Time}
\gradgroup{First}\gradrow{A,1.25e1}\gradrow{B,NA}\gradsummary{Count}\end{gradtable}\par
""")
    return preamble + '\n'.join(bodies) + r'\end{document}'


def long_source(preamble):
    rows = '\n'.join(rf'\gradrow{{Row-{i:03d},' + ('-1.25e-3' if i % 2 else '1.25e1') + '}' for i in range(1, 81))
    return (preamble + r'\begin{gradtable}[long=true,style=research,width=\linewidth,theme=teal,group summary=true,rank scope=group,caption={Research pages}]'
            + r'\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=mean,mark=both,options={precision=4,number format=scientific}]{value}{Value}'
            + r'\gradgroup{Research group}' + rows + r'\gradsummary{Final summary}\end{gradtable}\end{document}')


FAILURES = {
    'scientific-incomplete': (r'\gradbar{1e}', 'Invalid value'),
    'scientific-overflow': (r'\gradbar{1e101}', 'Invalid value'),
    'scientific-underflow': (r'\gradbar{1e-101}', 'Invalid value'),
    'scientific-huge-exponent': (r'\gradbar{1e99999}', 'Invalid value'),
    'scientific-nan': (r'\gradbar{NaN}', 'Invalid value'),
    'scientific-expression': (r'\gradbar{1+2}', 'Invalid value'),
    'scientific-comma': (r'\gradbar{1,234}', 'Invalid value'),
    'siunitx-missing': (r'\gradbar[formatter=siunitx]{50}', 'requires loading siunitx v3'),
    'siunitx-table-missing': (r'\begin{gradtable}[formatter=siunitx]\gradcolumn[type=number]{a}{A}\gradrow{NA}\end{gradtable}', 'requires loading siunitx v3'),
    'siunitx-unit-builtin': (r'\gradbar[unit code={ms},unit text={milliseconds}]{50}', 'Unit code requires formatter'),
    'decimal-graphic': (r'\begin{gradtable}\gradcolumn[type=bar,number align=decimal]{a}{A}\gradrow{50}\end{gradtable}', 'Decimal alignment requires a number column'),
    'decimal-width': (r'\begin{gradtable}[style=research]\gradcolumn{name}{Name}\gradcolumn[type=number,width=1mm]{a}{A}\gradrow{X,123.45}\end{gradtable}', 'Decimal column width too narrow'),
}

SI_FAILURES = {
    'unit-no-text': (r'\gradbar[formatter=siunitx,unit code={\second}]{50}', 'Unit code requires readable unit text'),
    'unit-conflict': (r'\gradbar[formatter=siunitx,unit={s},unit code={\second},unit text={seconds}]{50}', 'Use unit or unit code'),
    'unit-percent': (r'\gradbar[formatter=siunitx,value format=percent,unit code={\second},unit text={seconds}]{50}', 'Percent labels cannot use unit code'),
}
