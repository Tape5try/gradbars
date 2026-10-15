"""Library states, dependency/error contracts and public-only extension examples."""

BASE = r"""\documentclass{article}
\usepackage[margin=20mm]{geometry}
\usepackage[libraries=none]{gradbars}
\setlength{\parindent}{0pt}
"""


def case(preamble='', body=''):
    return BASE + preamble + '\n' + r'\begin{document}' + body + r'\end{document}'


def sources():
    result = {}
    for library, body in [
        ('stack', r'\gradstack[min=-50,max=100]{20,-10,30}'),
        ('spark', r'\gradspark[spark type=winloss]{10,-10,0,NA}'),
        ('heat', r'\gradheat[heat palette=diverging,min=-10,max=10]{-5}'),
        ('csv', r'\gradbarsloadcsv{data}{build/tests/scientific.csv}\gradbarcsv[min=-1,max=1,number format=scientific]{data}{1}{Value}'),
        ('table', r'\begin{gradtable}[style=research,width=\linewidth]\gradcolumn{name}{Name}\gradcolumn[type=number,aggregate=mean]{value}{Value}\gradrow{A,72}\gradrow{B,90}\gradsummary{Mean}\end{gradtable}')]:
        pre = r'\usegradbarslibrary{' + library + '}\n'
        pre += r'\gradbarsiflibraryloaded{' + library + r'}{}{\errmessage{Library not recorded}}'
        if library == 'table':
            for dep in ('stack', 'spark', 'csv', 'heat'):
                pre += r'\gradbarsiflibraryloaded{' + dep + r'}{}{\errmessage{Missing dependency}}'
        else:
            pre += r'\gradbarsiflibraryloaded{table}{\errmessage{Unwanted table dependency}}{}'
        result['v010-' + library] = case(pre, body)
    result['v010-package-list'] = (r'\documentclass{article}\usepackage[libraries={heat,spark}]{gradbars}'
        + r'\gradbarsiflibraryloaded{heat}{}{\errmessage{Missing requested heat}}'
        + r'\gradbarsiflibraryloaded{table}{\errmessage{Unexpected table}}{}'
        + r'\begin{document}\gradheat{50}\gradspark{10,20}\end{document}')
    result['v010-third-party'] = case(
        r'\gradbarsdeclarelibrary{demo}{table}{docs/libraries/gradbars-contrib-demo.sty}\usegradbarslibrary{demo,demo}',
        r'\gradgraphic{demo-score}{72.125}\par\gradbar[formatter=demo-boxed]{72.125}\par'
        + r'\begin{gradtable}[style=demo-report,width=\linewidth]\gradcolumn{name}{Name}\gradcolumn[type=number,formatter=demo-boxed,aggregate=mean]{value}{Value}\gradrow{A,72}\gradrow{B,90}\gradsummary{Mean}\end{gradtable}')
    result['v010-scope'] = case('', r"""\gradbarsset{max=100,precision=2}
{\gradbarssetup{max=200}\gradbar{150}}
\makeatletter\ifnum\gradbars@max=100\else\errmessage{Settings leaked}\fi\makeatother
\gradbar{50}\par\gradgraphic{bar}{NA}
\gradbarsiflibraryloaded{unknown}{\errmessage{Unknown library is loaded}}{}
""")
    return result


FAILURES = {
    'library-unknown': ('', r'\usegradbarslibrary{unknown}', 'Unknown library'),
    'library-cycle': (r'\gradbarsdeclarelibrary{alpha}{beta}{missing-alpha.sty}\gradbarsdeclarelibrary{beta}{alpha}{missing-beta.sty}', r'\usegradbarslibrary{alpha}', 'Circular library dependency'),
    'library-missing': (r'\gradbarsdeclarelibrary{absent}{core}{missing-example.sty}', r'\usegradbarslibrary{absent}', 'Library file not found'),
    'library-missing-dependency': (r'\gradbarsdeclarelibrary{example}{unknown}{missing-example.sty}', r'\usegradbarslibrary{example}', 'Unknown library'),
    'library-duplicate': ('', r'\gradbarsdeclarelibrary{stack}{}{unused.sty}', 'Library already registered'),
    'library-invalid-name': ('', r'\gradbarsdeclarelibrary{../bad}{}{unused.sty}', 'Invalid library name'),
    'stack-unloaded': ('', r'\gradstack{10,20}', 'Library stack not loaded'),
    'spark-unloaded': ('', r'\gradspark{10,20}', 'Library spark not loaded'),
    'heat-unloaded': ('', r'\gradheat{50}', 'Library heat not loaded'),
    'csv-unloaded': ('', r'\gradbarsloadcsv{data}{anything.csv}', 'Library csv not loaded'),
    'table-unloaded': ('', r'\begin{gradtable}\end{gradtable}', 'Library table not loaded'),
    'formatter-unknown': ('', r'\gradbarsset{formatter=missing}', 'Unknown formatter'),
    'formatter-duplicate': ('', r'\gradbarsdeclareformatter{builtin}{#1}', 'Formatter already registered'),
    'type-duplicate': ('', r'\gradbarsdeclaretype{bar}{\gradbar{#1}}', 'Graphic type already registered'),
    'type-unknown': ('', r'\gradgraphic{missing}{50}', 'Unknown graphic type'),
    'type-bad-value': ('', r'\gradgraphic{bar}{1+2}', 'Invalid graphic value'),
    'formatter-precision': ('', r'\gradbarsformatnumber[precision=7]{50}', 'Precision must be an integer'),
    'formatter-decimal': (r'\usegradbarslibrary{table}\gradbarsdeclareformatter{opaque}{#1}', r'\begin{gradtable}[style=research]\gradcolumn[type=number,formatter=opaque]{value}{Value}\gradrow{50}\end{gradtable}', 'Custom formatters do not support decimal alignment'),
    'module-version': (r'\makeatletter\def\input@path{{build/tests/}}\makeatother\gradbarsdeclarelibrary{mismatch}{core}{gradbars-lib-mismatch.sty}', r'\usegradbarslibrary{mismatch}', 'Mixed module versions'),
}


def failure_source(preamble, operation):
    preamble_only = operation.startswith((r'\usegradbarslibrary', r'\gradbarsdeclarelibrary'))
    return BASE + preamble + ('\n' + operation if preamble_only else '') + '\n' + r'\begin{document}' + ('' if preamble_only else operation) + r'\end{document}'
