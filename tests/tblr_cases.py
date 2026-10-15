"""Tabularray loading, dimensions, label positions and multipage regressions."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PRE = r'''\documentclass{article}
\usepackage[margin=20mm]{geometry}
\usepackage{tabularray}
\UseTblrLibrary{gradbars,gradbars}
\setlength{\parindent}{0pt}
'''


def run(engine, compile_case):
    compile_case(engine, 'tblr-smoke', (ROOT / 'tests/tblr-smoke.tex').read_text(encoding='utf-8'), passes=2)
    compile_case(engine, 'tblr-edge', (ROOT / 'tests/tblr-edge.tex').read_text(encoding='utf-8'))
    compile_case(engine, 'tblr-contract', PRE + r'''
\makeatletter
\newsavebox{\probe}
\ExplSyntaxOn
\cs_new_eq:NN\probeBaseline\gradbarsResolveBaseline
\cs_set_protected:Npn\gradbarsResolveBaseline
  {\probeBaseline
   \str_if_eq:eeT{\gradbars@placement}{center}
     {\dim_compare:nNnT{\dim_abs:n{\gradbars@labelx-\gradbars@width/2}}>{.01pt}
       {\errmessage{Cell~label~is~not~centered}}}}
\ExplSyntaxOff
\makeatother
\gradtblrsetup{precision=3}
\gradtblrsetup{min=-10,max=10}
\begin{document}
\sbox{\probe}{\gradbarTblr[cell width=80pt]{-9.5}}
\ifdim\wd\probe=80pt\else\errmessage{Cell width changed}\fi
\sbox{\probe}{\gradbarTblr[cell width=80pt]{.001}}
\sbox{\probe}{\gradbarTblr[cell width=80pt]{NA}}
\sbox{\probe}{\gradbarTblr[cell width=80pt,label=left,label width=35pt]{-5}}
\ifdim\wd\probe=80pt\else\errmessage{Left label exceeds cell}\fi
{\gradtblrsetup{precision=1}\gradnumberTblr[cell width=80pt]{12.345}}
\gradnumberTblr[cell width=80pt]{12.345}
\gradtblrcell[cell width=80pt]{dumbbell}{-5/5}
\begin{tblr}{colspec={G{80pt} H{80pt}},cell{1}{1}={c=2}{c,cmd=}}
Spanning header & \\
-1 & NA\\
\end{tblr}
\end{document}
''')
    rows = ''.join('Row-%03d & %s\\\\\n' % (i, str(i % 19 - 9)) for i in range(1, 81))
    compile_case(engine, 'tblr-long', PRE + r'''
\gradtblrsetup{min=-10,max=10,precision=1}
\begin{document}
\begin{longtblr}[caption={Multipage integration}]{
  colspec={l G{70mm}},rowhead=1,row{1}={font=\bfseries},hlines}
Method & {Observation}\\
''' + rows + r'\end{longtblr}\end{document}', passes=2)
    text = subprocess.check_output(['pdftotext', '-layout', str(ROOT / 'build/tests' / engine / 'tblr-contract.pdf'), '-']).decode('utf-8')
    if '12.345' not in text or '12.3' not in text:
        raise RuntimeError(engine + ': formatter defaults did not accumulate or scope correctly')
    text = subprocess.check_output(['pdftotext', '-layout', str(ROOT / 'build/tests' / engine / 'tblr-long.pdf'), '-']).decode('utf-8')
    pages = [page for page in text.split('\f') if 'Row-' in page]
    if len(pages) < 2 or any('Observation' not in page for page in pages):
        raise RuntimeError(engine + ': missing repeated longtblr headers')
    if any(text.count('Row-%03d' % i) != 1 for i in range(1, 81)):
        raise RuntimeError(engine + ': duplicated or missing longtblr row')
    failures = {
        'bad-type': (PRE, r'\gradtblrcell[cell width=30mm]{absent}{1}', 'Unknown tblr graphic type'),
        'bad-pair': (PRE, r'\gradtblrcell[cell width=30mm]{compare}{1/2/3}', 'requires two values separated'),
        'bad-width': (PRE, r'\gradbarTblr[cell width=0pt]{1}', 'cell width must be positive'),
        'label-width': (PRE, r'\gradbarTblr[cell width=20pt,label=left,label width=30pt]{1}', 'must exceed label width'),
        'overflow': (PRE, r'\gradbarTblr[cell width=20pt,text={A very long label}]{1}', 'content exceeds cell width'),
        'bad-number': (PRE, r'\gradnumberTblr[cell width=80pt]{1+2}', 'Invalid cell value'),
        'unloaded': (r'\documentclass{article}\usepackage{gradbars}', r'\gradbarTblr{1}', 'Load the tabularray gradbars library'),
    }
    for name, (pre, body, error) in failures.items():
        compile_case(engine, 'tblr-' + name, pre + r'\begin{document}' + body + r'\end{document}', error)
    print(engine + ': tabularray dimensions, center/left labels, formats, longtblr and 7 expected errors passed', flush=True)
