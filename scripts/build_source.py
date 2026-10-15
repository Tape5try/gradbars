"""Generate/check the documented source and verify docstrip round trips.

The maintainable sources live in sty/. Generated gradbars.dtx/gradbars.ins are
reproducible distribution sources; do not edit their generated module sections.
"""
from pathlib import Path
import argparse
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def normalized(text):
    return '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'


def generated_sources():
    modules = sorted((ROOT / 'sty').glob('*.sty'))
    entry = (ROOT / 'sty' / 'gradbars.sty').read_text(encoding='utf-8')
    date, version = re.search(r'\\ProvidesPackage\{gradbars\}\[([\d/]+) v([\d.]+)', entry).groups()
    dtx = [r'% \iffalse', r'%<*driver>', r'\documentclass{l3doc}',
           r'\OnlyDescription', r'\begin{document}', r'\DocInput{gradbars.dtx}',
           r'\end{document}', r'%</driver>', r'% \fi',
           r'% \title{\textsf{gradbars}: documented source}',
           r'% \author{SuFan (Tape5try)}', '% \\date{v' + version + ' / ' + date + '}',
           r'% \maketitle', r'% \input{docs/source-guide.tex}', r'% \StopEventually{}']
    ins = [r'\input docstrip.tex', r'\keepsilent', r'\askforoverwritefalse',
           r'\nopreamble', r'\nopostamble', r'\generate{']
    for path in modules:
        tag = ('entry' if path.stem == 'gradbars' else
               path.stem[len('gradbars-'):] if path.stem.startswith('gradbars-') else path.stem)
        dtx += ['% \\section{\\texttt{' + path.name + '}}', r'%    \begin{macrocode}']
        dtx += ['%<' + tag + '>' + line for line in normalized(path.read_text(encoding='utf-8')).splitlines()]
        dtx += [r'%    \end{macrocode}']
        ins += [r'  \file{' + path.name + r'}{\from{gradbars.dtx}{' + tag + '}}']
    ins += ['}', r'\endbatchfile']
    return modules, {'gradbars.dtx': '\n'.join(dtx) + '\n',
                     'gradbars.ins': '\n'.join(ins) + '\n'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Reject stale generated source')
    args = parser.parse_args()
    modules, generated = generated_sources()
    for name, text in generated.items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or normalized(path.read_text(encoding='utf-8')) != text:
                raise SystemExit('Stale documented source: run python scripts/build_source.py')
        else:
            with path.open('w', encoding='utf-8', newline='\n') as handle:
                handle.write(text)
    engine = shutil.which('tex')
    if not engine:
        raise SystemExit('TeX is required to verify docstrip extraction.')
    work = ROOT / 'build' / 'source-check'
    work.mkdir(parents=True, exist_ok=True)
    for name in generated:
        shutil.copy2(ROOT / name, work / name)
    result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', 'gradbars.ins'],
                            cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise SystemExit(result.stdout.decode('utf-8', errors='replace'))
    for path in modules:
        extracted = work / path.name
        if not extracted.is_file() or normalized(extracted.read_text(encoding='utf-8')) != normalized(path.read_text(encoding='utf-8')):
            raise SystemExit('Docstrip extraction differs from runtime: ' + path.name)
    print(f'Documented source matches all {len(modules)} runtime modules; docstrip round trip passed.')


if __name__ == '__main__':
    main()
