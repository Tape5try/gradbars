"""Build the four real layouts and the unified manual with XeLaTeX.

Run from any directory: python scripts/build_manual.py
Requires XeLaTeX, ctex/Fandol and the standard LaTeX extra packages.
"""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "layouts"


def compile_tex(source, output, jobname=None, engine="xelatex"):
    command = [engine, "-interaction=nonstopmode", "-halt-on-error",
               f"-output-directory={output}"]
    if jobname:
        command.append(f"-jobname={jobname}")
    command.append(source.as_posix())
    for _ in range(2):
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        if result.returncode:
            print(result.stdout.decode("utf-8", errors="replace"))
            raise SystemExit(result.returncode)


def main():
    if not shutil.which("xelatex"):
        raise SystemExit("XeLaTeX was not found on PATH.")
    BUILD.mkdir(parents=True, exist_ok=True)
    version = re.search(r"\\ProvidesPackage\{gradbars\}\[[^\]]*?v([\d.]+)",
                        (ROOT / "gradbars.sty").read_text(encoding="utf-8")).group(1)
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


if __name__ == "__main__":
    main()
