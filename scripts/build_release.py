"""Create and validate the current gradbars CTAN archive (Python standard library).

Run after tests and python scripts/build_manual.py. Only the current version's
manuals are packaged; the independent v0.0.4 upload directory is never read.
Archives are written to gradbars_CTAN/gradbars-VERSION.zip, alongside a manifest.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent.parent
TEXT = {'.sty', '.tex', '.md', '.csv', '.py', '.lua', '.svg', '.bib', '.ins', '.dtx', '.lvt', '.tlg'}
DOC = TEXT | {'.pdf', '.png', '.jpg', '.jpeg'}


def metadata():
    text = (ROOT / 'sty' / 'gradbars.sty').read_text(encoding='utf-8')
    match = re.search(r'\\ProvidesPackage\{gradbars\}\[(\d{4})/(\d{2})/(\d{2}) v([\d.]+)', text)
    if not match:
        raise ValueError('Missing package version/date')
    return match.group(4), '-'.join(match.group(i) for i in (1, 2, 3))


def files_for(version):
    files = list((ROOT / 'sty').glob('*.sty'))
    files += [ROOT / name for name in ('LICENSE', 'README.md', 'README.en.md', 'CHANGELOG.md', 'build.lua', 'gradbars.dtx', 'gradbars.ins')]
    files += [ROOT / ('gradbars-manual' + language + '-v' + version + '.pdf') for language in ('', '-en')]
    files += [ROOT / ('gradbars-source-v' + version + '.pdf')]
    for directory in ('docs', 'tests'):
        files += [path for path in (ROOT / directory).rglob('*') if path.is_file()
                  and path.suffix.lower() in DOC and '__pycache__' not in path.parts
                  and path.name != 'ctan-upload.md']
    files += [ROOT / 'scripts' / name for name in ('build_manual.py', 'build_release.py', 'benchmark.py', 'check_release.py', 'build_source.py', 'check_tagging.py')]
    return sorted(set(files))


def check_payload(payload, version, date):
    required = ['sty/gradbars.sty', 'LICENSE', 'README.md', 'README.en.md', 'CHANGELOG.md',
                'gradbars.dtx', 'gradbars.ins', 'gradbars-source-v' + version + '.pdf',
                'gradbars-manual-v' + version + '.pdf', 'gradbars-manual-en-v' + version + '.pdf']
    for name in required:
        if name not in payload or not payload[name]:
            raise ValueError('Missing/empty release file: ' + name)
    package = payload['sty/gradbars.sty'].decode('utf-8')
    if date.replace('-', '/') + ' v' + version not in package:
        raise ValueError('Archive package metadata does not match')
    expected_modules = ['core', 'keys', 'numbers', 'model', 'render-tikz', 'tagging', 'api',
                        'lib-stack', 'lib-spark', 'lib-heat', 'lib-csv', 'lib-table', 'table-data', 'table-layout']
    for module in expected_modules:
        name = 'sty/gradbars-' + module + '.sty'
        if name not in payload:
            raise ValueError('Missing runtime module: ' + name)
        text = payload[name].decode('utf-8')
        if date.replace('-', '/') + ' v' + version not in text:
            raise ValueError('Module version/date mismatch: ' + name)
    adapter = 'sty/tblrlibgradbars.sty'
    if adapter not in payload or date.replace('-', '/') + ' v' + version not in payload[adapter].decode('utf-8'):
        raise ValueError('Missing or mismatched tabularray library: ' + adapter)
    changelog = payload['CHANGELOG.md'].decode('utf-8')
    if '## ' + version + ' — ' + date not in changelog:
        raise ValueError('CHANGELOG version/date mismatch')
    for manual in ('docs/gradbars-manual.tex', 'docs/gradbars-manual-en.tex'):
        if manual not in payload:
            raise ValueError('Missing manual source: ' + manual)
        text = payload[manual].decode('utf-8')
        uncommented = re.sub(r'(?m)(?<!\\)%[^\n]*', '', text)
        if re.search(r'\\includeonly\s*\{', uncommented):
            raise ValueError('Restore a full manual build before packaging: ' + manual)
        for chapter in re.findall(r'\\(?:include|input)\{([^{}]+)\}', text):
            filename = chapter if chapter.endswith('.tex') else chapter + '.tex'
            target = str(PurePosixPath(manual).parent / filename)
            if target not in payload:
                raise ValueError('Missing included chapter: ' + target)
    for name in ('README.md', 'README.en.md'):
        text = payload[name].decode('utf-8')
        if '**v' + version + ' ·' not in text:
            raise ValueError('README version mismatch: ' + name)
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if link.startswith(('https://', 'http://', 'mailto:', '#')):
                continue
            target = str(PurePosixPath(name).parent / link.split('#')[0])
            if target not in payload:
                raise ValueError('Broken archive link: ' + name + ' -> ' + link)
    for name, data in payload.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or not data:
            raise ValueError('Invalid archive path/file: ' + name)
        if path.suffix.lower() in TEXT and b'\r' in data:
            raise ValueError('Non-LF release text: ' + name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true', help='Validate an existing current-version archive')
    parser.add_argument('--validate-only', action='store_true', help='Validate the current payload without creating a zip')
    args = parser.parse_args()
    if args.check_only and args.validate_only:
        parser.error('--check-only and --validate-only are mutually exclusive')
    version, date = metadata()
    import subprocess
    import sys
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_source.py'), '--check'],
                   cwd=ROOT, check=True)
    for language in ('', '-en'):
        log = ROOT / 'build' / 'manual' / ('gradbars-manual' + language + '-v' + version + '.log')
        if log.exists():
            diagnostics = log.read_text(encoding='utf-8', errors='replace')
            if 'Overfull' in diagnostics or 'undefined references' in diagnostics.lower():
                raise ValueError('Fix manual layout/references before packaging: ' + str(log))
    output = ROOT / 'gradbars_CTAN'
    archive = output / ('gradbars-' + version + '.zip')
    if not args.check_only:
        payload = {}
        for path in files_for(version):
            if not path.is_file():
                raise ValueError('Build the current manuals before packaging: ' + str(path))
            data = path.read_bytes()
            if path.suffix.lower() in TEXT:
                data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
            payload[path.relative_to(ROOT).as_posix()] = data
        check_payload(payload, version, date)
        if args.validate_only:
            print(f'Validated {len(payload)} release files for v{version}; no archive created.')
            return
        output.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as stream:
            for name, data in payload.items():
                info = zipfile.ZipInfo('gradbars/' + name, (2000, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                stream.writestr(info, data)
    # Verify the actual archive, not just the original files.
    with zipfile.ZipFile(archive) as stream:
        names = stream.namelist()
        if len(names) != len(set(names)) or any(not name.startswith('gradbars/') for name in names):
            raise ValueError('Archive must contain one gradbars/ root without duplicates')
        if stream.testzip() is not None:
            raise ValueError('Archive CRC failure')
        payload = {name[len('gradbars/'):]: stream.read(name) for name in names}
    check_payload(payload, version, date)
    report = {'version': version, 'date': date, 'files': len(payload),
              'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'entries': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())}}
    (output / ('gradbars-' + version + '-manifest.json')).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(str(archive))
    print('Verified: version/date, ' + str(len(payload)) + ' files, README links, LF text, one archive root and CRC.')


if __name__ == '__main__':
    main()
