"""Fixed-dataset comparison against the frozen v0.0.8 source (local baseline).

Run python scripts/benchmark.py --baseline build/baseline-v008
Copies/reads no installed gradbars files; PDF text must match for each engine.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import statistics
import shutil
import subprocess
import time
from build_release import metadata

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--engines', nargs='+', default=['pdflatex', 'xelatex', 'lualatex'])
    parser.add_argument('--runs', type=int, default=3)
    args = parser.parse_args()
    baseline = args.baseline.resolve()
    if not (baseline / 'gradbars.sty').is_file():
        raise SystemExit('Provide an extracted v0.0.8 gradbars.sty baseline directory.')
    source = r"""\documentclass{article}
\usepackage[margin=20mm]{geometry}
\usepackage{gradbars}
\setlength{\parindent}{0pt}
\begin{document}
\gradbar{72.125}\par
\gradstack[min=-50,max=100]{20,-10,30}\par
\gradspark{10,NA,50,-20}\par
\begin{gradtable}[width=\linewidth,long=true,theme=teal,caption={Fixed dataset}]
\gradcolumn{name}{Name}\gradcolumn[type=bar,aggregate=mean,mark=both]{value}{Value}
""" + '\n'.join(rf'\gradrow{{Row-{i:03d},{1+(i*37)%97}}}' for i in range(1, 81)) + r"""
\gradsummary{Mean}\end{gradtable}\end{document}
"""
    build = ROOT / 'build' / 'benchmark'
    build.mkdir(exist_ok=True)
    report = {'dataset_rows': 80, 'runs': args.runs, 'engines': {}}
    for engine in args.engines:
        timings, resources, texts = {}, {}, {}
        for name, directory, expected in [('v008', baseline, 'v0.0.8'), ('current', ROOT / 'sty', 'v' + metadata()[0])]:
            work = build / (engine + '-' + name)
            work.mkdir(exist_ok=True)
            for package in directory.glob('gradbars*.sty'):
                shutil.copy2(package, work / package.name)
            (work / 'benchmark.tex').write_text(source, encoding='utf-8')
            env = os.environ.copy()
            env['TEXINPUTS'] = '.' + os.pathsep
            cache = ROOT / 'build' / 'tests' / 'tex-cache'
            cache.mkdir(parents=True, exist_ok=True)
            env['TEXMFVAR'] = str(cache)
            env['TEXMFCACHE'] = str(cache)
            elapsed = []
            for _ in range(args.runs):
                start = time.perf_counter()
                result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', 'benchmark.tex'], cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                elapsed.append(time.perf_counter() - start)
                log = (work / 'benchmark.log').read_text(encoding='utf-8', errors='replace')
                if result.returncode or 'Overfull' in log or expected not in log:
                    raise RuntimeError(engine + '/' + name + '\n' + log[-3000:])
            texts[name] = subprocess.check_output(['pdftotext', '-layout', 'benchmark.pdf', '-'], cwd=work)
            resources[name] = {'pdf_bytes': (work / 'benchmark.pdf').stat().st_size,
                               'log_bytes': (work / 'benchmark.log').stat().st_size}
            timings[name] = statistics.median(elapsed)
        if texts['v008'] != texts['current']:
            raise RuntimeError('Baseline/current extracted PDF values differ: ' + engine)
        ratio = timings['current'] / timings['v008']
        report['engines'][engine] = {'seconds_median': timings, 'relative_time': ratio,
                                    'resources': resources, 'text_sha256': hashlib.sha256(texts['current']).hexdigest(),
                                    'resource_note': 'PDF/log sizes are diagnostic only; version/file metadata differ.'}
        print(engine, 'same rendered values;', f'median relative time {ratio:.2f}x', flush=True)
        if ratio > 2:
            raise RuntimeError('Review compilation regression greater than 2x: ' + engine)
    (build / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
