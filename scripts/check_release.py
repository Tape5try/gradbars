"""Compile the release payload in an isolated package directory."""
from pathlib import Path, PurePosixPath
import argparse
import os
import subprocess
import zipfile
from build_release import ROOT, metadata, check_payload, files_for, TEXT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-tree', action='store_true', help='Check an isolated payload without requiring or creating a zip')
    args = parser.parse_args()
    version, date = metadata()
    archive = ROOT / 'gradbars_CTAN' / ('gradbars-' + version + '.zip')
    target = ROOT / 'build' / 'install-check' / (version + ('-source' if args.source_tree else ''))
    target.mkdir(parents=True, exist_ok=True)
    if args.source_tree:
        payload = {}
        for path in files_for(version):
            data = path.read_bytes()
            if path.suffix.lower() in TEXT:
                data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
            name = path.relative_to(ROOT).as_posix()
            payload[name] = data
        check_payload(payload, version, date)
        for name, data in payload.items():
            path = target / 'gradbars' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    else:
        payload = {}
        with zipfile.ZipFile(archive) as stream:
            for name in stream.namelist():
                part = PurePosixPath(name)
                if part.is_absolute() or '..' in part.parts or not name.startswith('gradbars/'):
                    raise ValueError('Invalid archive entry: ' + name)
                data = stream.read(name)
                path = target / Path(*part.parts)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                payload[name[len('gradbars/'):]] = data
    check_payload(payload, version, date)
    work = target / 'gradbars'
    text = r"""\documentclass{article}
\usepackage[margin=20mm]{geometry}
\usepackage[libraries=table]{gradbars}
\usepackage{tabularray}
\UseTblrLibrary{gradbars}
\gradbarsdeclarelibrary{demo}{table}{docs/libraries/gradbars-contrib-demo.sty}
\usegradbarslibrary{demo}
\setlength{\parindent}{0pt}
\begin{document}
\gradstack[min=-50,max=100]{20,-10,30}\par
\gradspark{10,NA,20}\par
\gradheat{50}\par
\gradgraphic{demo-score}{72.125}\par
\gradbarsloadcsv{results}{docs/data/precision-time.csv}
\begin{gradtable}[data=results,style=demo-report,width=\linewidth]
\gradcolumn[source=Method]{name}{Method}
\gradcolumn[type=number,source=Score,aggregate=mean,formatter=demo-boxed]{score}{Score}
\gradsummary{Mean}\end{gradtable}
\begin{gradtblr}{colspec={G[min=-10,max=10]{30mm} H{30mm} N{30mm}}}
{Bar} & {Heat} & {Number}\\
-5 & 50 & 12.345\\
\end{gradtblr}
\end{document}
"""
    (work / 'install.tex').write_text(text, encoding='utf-8')
    for engine in ('pdflatex', 'xelatex', 'lualatex'):
        output = work / engine
        output.mkdir(exist_ok=True)
        env = os.environ.copy()
        env['TEXINPUTS'] = 'sty' + os.pathsep + '.' + os.pathsep
        cache = ROOT / 'build' / 'tests' / 'tex-cache'
        cache.mkdir(parents=True, exist_ok=True)
        env['TEXMFVAR'] = str(cache)
        env['TEXMFCACHE'] = str(cache)
        result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + engine, 'install.tex'], cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = (output / 'install.log').read_text(encoding='utf-8', errors='replace')
        if result.returncode or 'Overfull' in log or 'v' + version not in log:
            raise RuntimeError(engine + ': isolated runtime failed\n' + log[-3500:])
        print(engine + ': isolated runtime/data/contributed-library compile passed', flush=True)


if __name__ == '__main__':
    main()
