"""Compile a tagged fixture and inspect PDF structure, not just visible text.

Development dependency: pypdf. Requires a tagging-capable LaTeX distribution.
"""
from pathlib import Path
import argparse
import os
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def figure_descriptions(reader):
    result = []
    root = reader.trailer['/Root'].get('/StructTreeRoot')
    if root is None:
        raise RuntimeError('PDF has no structure tree')
    visited = set()

    def walk(node):
        if hasattr(node, 'get_object'):
            node = node.get_object()
        if isinstance(node, list):
            for child in node:
                walk(child)
        elif isinstance(node, dict):
            identity = id(node)
            if identity in visited:
                return
            visited.add(identity)
            if str(node.get('/S')) == '/Figure':
                result.append(str(node.get('/Alt', '')))
            if '/K' in node:
                walk(node['/K'])
    walk(root)
    return result


def main():
    try:
        from pypdf import PdfReader
    except ImportError:
        raise SystemExit('Install the development dependency: python -m pip install pypdf')
    parser = argparse.ArgumentParser()
    parser.add_argument('--engines', nargs='+', default=['pdflatex', 'xelatex', 'lualatex'])
    args = parser.parse_args()
    build = ROOT / 'build' / 'tagging'
    env = os.environ.copy()
    env['TEXINPUTS'] = 'sty' + os.pathsep
    cache = ROOT / 'build' / 'tests' / 'tex-cache'
    cache.mkdir(parents=True, exist_ok=True)
    env['TEXMFVAR'] = str(cache)
    env['TEXMFCACHE'] = str(cache)
    for engine in args.engines:
        out = build / engine
        out.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            run = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error',
                                  '-output-directory=' + str(out), str(ROOT / 'tests' / 'v100-tagged.tex')],
                                 cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if run.returncode:
                raise RuntimeError(engine + ' tagging compile failed:\n' + run.stdout.decode('utf-8', errors='replace')[-5000:])
        descriptions = figure_descriptions(PdfReader(out / 'v100-tagged.pdf'))
        expected = ['Value: 12.345.', 'Explicit stable description.', 'Whole stable picture.',
                    'Value: 82.', 'Value: 94.']
        tagged = [text for text in descriptions if text]
        if len(tagged) != len(expected) or any(sum(part in text for text in tagged) != 1 for part in expected):
            raise RuntimeError(engine + ': missing or duplicated Figure descriptions: ' + repr(descriptions))
        if len(descriptions) > 6 or any('56.78' in text or '67.89' in text for text in tagged):
            raise RuntimeError(engine + ': artifact/off or measurement suppression failed')
        print(engine + ': five unique Figure descriptions; raw precision, outer alt and measurement suppression passed', flush=True)
        for _ in range(2):
            run = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error',
                                  '-output-directory=' + str(out), str(ROOT / 'tests' / 'tblr-tagged.tex')],
                                 cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if run.returncode:
                raise RuntimeError(engine + ' tblr tagging compile failed:\n' + run.stdout.decode('utf-8', errors='replace')[-5000:])
        descriptions = figure_descriptions(PdfReader(out / 'tblr-tagged.pdf'))
        expected = ['Value: 1.234.', 'Heat cell: -2.345', 'Value: missing.',
                    'Heat cell: 0 ', 'Value: 4.567.', 'Value: -5.678.', 'Explicit cell description.']
        tagged = [text for text in descriptions if text]
        if len(tagged) != 7 or any(sum(part in text for text in tagged) != 1 for part in expected):
            raise RuntimeError(engine + ': duplicated or missing tblr descriptions: ' + repr(descriptions))
        if len(descriptions) > 8 or any('7.891' in text or '8.912' in text for text in tagged):
            raise RuntimeError(engine + ': tblr artifact/off behavior changed')
        print(engine + ': seven unique tblr Figure descriptions; fixed/X widths and measurement suppression passed', flush=True)


if __name__ == '__main__':
    main()
