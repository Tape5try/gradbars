"""Stable extension, settings and private model boundary regressions."""
from v010_cases import case


def sources():
    return {
        'v100-contract': case(r'''
\usegradbarslibrary{table}
\newcount\callbacks
\gradbarsdeclaretype{probe}{\global\advance\callbacks by1\relax\gradbar{#1}}
\gradbarsdeclareformatter{probe}{\gradbarsformatnumber[precision=#2,number format=#3]{#1}}
\gradbarsstyle{base}{color=teal,precision=2}
\gradbarsstyle{nested}{style=base,precision=3}
''', r'''
\gradbarsset{max=100,precision=1}
{\gradbarsset{style=nested}\gradgraphic[formatter=probe]{probe}{7.125}}\par
\gradgraphic{probe}{NA}\par
\ifnum\callbacks=2\else\errmessage{Scalar callback count changed}\fi
\makeatletter
\ifnum\gradbars@precision=1\else\errmessage{Style scope leaked}\fi
\ifnum\gradbars@max=100\else\errmessage{Range scope leaked}\fi
\makeatother
\begin{gradtable}[style=reference,width=\linewidth,theme=teal]
\gradcolumn{name}{Method}
\gradcolumn[type=number,aggregate=mean,options={precision=3}]{value}{Value}
\gradrow{A,-12.125}\gradrow{B,1.25}\gradrow{Pending,NA}\gradsummary{Mean}
\end{gradtable}
'''),
        'v100-model': case(r'''
\ExplSyntaxOn
\cs_new_eq:NN \test_render: \__gradbars_render_tikz:
\cs_set_protected:Npn \__gradbars_render_tikz:
  {\str_if_eq:eeF{\prop_item:Nn\l__gradbars_model_prop{raw-value}}{-25.125}
     {\errmessage{Raw~model~value~changed}}
   \fp_compare:nNnF{\prop_item:Nn\l__gradbars_model_prop{zero}}={.5}
     {\errmessage{Model~zero~changed}}
   \fp_compare:nNnF{\prop_item:Nn\l__gradbars_model_prop{end}}={.374375}
     {\errmessage{Model~endpoint~changed}}
   \test_render:}
\ExplSyntaxOff
''', r'''
\gradbar[min=-100,max=100,precision=0,label=left,baseline=text,
  negative left color=magenta!25,negative right color=magenta]{-25.125}
\ExplSyntaxOn
\prop_if_empty:NF\l__gradbars_model_prop{\errmessage{Model~state~leaked}}
\ExplSyntaxOff
'''),
    }


FAILURES = {
    'stable-unknown-key': ('', r'\gradbar[not-a-gradbars-key=1]{50}', 'I do not know the key'),
    'stable-style-cycle': (r'\gradbarsstyle{loop}{style=loop}', r'\gradbar[style=loop]{50}', 'Style nesting exceeds 32 levels'),
    'stable-style-unknown': ('', r'\gradbar[style=not-defined]{50}', 'Unknown style'),
    'stable-baseline': ('', r'\gradbar[baseline=not-defined]{50}', "Choice 'not-defined' unknown"),
    'stable-negative-fill': ('', r'\gradbar[negative fill=not-defined]{50}', "Choice 'not-defined' unknown"),
    'stable-formatter-name': ('', r'\gradbarsdeclareformatter{BadName}{#1}', 'Invalid formatter name'),
    'stable-type-name': ('', r'\gradbarsdeclaretype{BadName}{#1}', 'Invalid graphic type name'),
    'stable-empty-scalar': ('', r'\gradgraphic{bar}{}', 'Invalid graphic value'),
}
