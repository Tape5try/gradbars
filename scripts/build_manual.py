"""Build the four real layouts and the unified manual with XeLaTeX.

Run from any directory: python scripts/build_manual.py
Requires XeLaTeX, ctex/Fandol and the standard LaTeX extra packages.
"""
from pathlib import Path
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "layouts"


def compile_tex(source, output, jobname=None, engine="xelatex"):
    output.mkdir(parents=True, exist_ok=True)
    # LaTeX include writes per-section .aux files using the include's directory.
    # TeX does not create these directories itself, even with -output-directory.
    for include in re.findall(r'\\include\{([^{}]+)\}', source.read_text(encoding='utf-8')):
        relative = Path(include)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe include path: ' + include)
        (output / relative.parent).mkdir(parents=True, exist_ok=True)
        # Modern LaTeX can resolve input@path before naming the include's aux.
        # Manuals are found through docs/, so prepare that resolved path too.
        source_directory = source.resolve().parent.relative_to(ROOT)
        (output / source_directory / relative.parent).mkdir(parents=True, exist_ok=True)
    command = [engine, "-interaction=nonstopmode", "-halt-on-error",
               f"-output-directory={output}"]
    if jobname:
        command.append(f"-jobname={jobname}")
    command.append(source.as_posix())
    environment = os.environ.copy()
    environment['TEXINPUTS'] = 'sty' + os.pathsep + environment.get('TEXINPUTS', '') + os.pathsep
    for _ in range(2):
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, env=environment)
        if result.returncode:
            print(result.stdout.decode("utf-8", errors="replace"))
            raise SystemExit(result.returncode)


def main():
    if not shutil.which("xelatex"):
        raise SystemExit("XeLaTeX was not found on PATH.")
    BUILD.mkdir(parents=True, exist_ok=True)
    version = re.search(r"\\ProvidesPackage\{gradbars\}\[[^\]]*?v([\d.]+)",
                        (ROOT / "sty" / "gradbars.sty").read_text(encoding="utf-8")).group(1)
    print('Building README overview...', flush=True)
    overview_build = ROOT / 'build' / 'overview'
    compile_tex(ROOT / 'docs' / 'images' / 'overview.tex', overview_build, engine='pdflatex')
    converter = shutil.which('pdftocairo')
    if not converter:
        raise SystemExit('pdftocairo is required to regenerate the README SVG.')
    subprocess.run([converter, '-svg', (overview_build / 'overview.pdf').relative_to(ROOT).as_posix(),
                    f'docs/images/overview-v{version}.svg'], cwd=ROOT, check=True)
    for name in ("twocolumn", "longtable", "grayscale", "slides"):
        print(f"Building {name}...", flush=True)
        compile_tex(ROOT / "docs" / "layouts" / f"{name}.tex", BUILD)
        shutil.copy2(BUILD / f"{name}.pdf", ROOT / "docs" / "layouts" / f"{name}.pdf")
    print(f"Building manual v{version}...", flush=True)
    manual_build = ROOT / "build" / "manual"
    manual_build.mkdir(parents=True, exist_ok=True)
    compile_tex(ROOT / "docs" / "gradbars-manual.tex", manual_build,
                f"gradbars-manual-v{version}")
    try:
        shutil.copy2(manual_build / f"gradbars-manual-v{version}.pdf",
                     ROOT / f"gradbars-manual-v{version}.pdf")
    except PermissionError:
        raise SystemExit("Manual compiled successfully. Close the root PDF in its viewer "
                         f"before replacing it. New PDF: {manual_build / f'gradbars-manual-v{version}.pdf'}")
    print(ROOT / f"gradbars-manual-v{version}.pdf")
    print(f"Building English manual v{version}...", flush=True)
    compile_tex(ROOT / "docs" / "gradbars-manual-en.tex", manual_build,
                f"gradbars-manual-en-v{version}", engine="pdflatex")
    shutil.copy2(manual_build / f"gradbars-manual-en-v{version}.pdf",
                 ROOT / f"gradbars-manual-en-v{version}.pdf")
    print(ROOT / f"gradbars-manual-en-v{version}.pdf")
    print("Building the l3doc source guide...", flush=True)
    subprocess.run([os.sys.executable, str(ROOT / 'scripts' / 'build_source.py'), '--check'],
                   cwd=ROOT, check=True)
    compile_tex(ROOT / 'gradbars.dtx', manual_build,
                f'gradbars-source-v{version}', engine='pdflatex')
    shutil.copy2(manual_build / f'gradbars-source-v{version}.pdf',
                 ROOT / f'gradbars-source-v{version}.pdf')


if __name__ == "__main__":
    main()
