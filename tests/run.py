"""Run from any directory: python tests/run.py [--engine xelatex].

Requires a TeX installation. Poppler's pdftotext enables PDF label assertions.
Only the Python standard library is used. Generated files stay under build/.
"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INVALID = {
    "zero-max": (r"\gradbar[max=0]{10}", "Max must be greater than zero"),
    "negative-max": (r"\gradbar[max=-10]{0}", "Max must be greater than zero"),
    "negative-value": (r"\gradbar{-1}", "Negative values require a negative min"),
    "invalid-value": (r"\gradbar{hello}", "Invalid value"),
    "invalid-max": (r"\gradbar[max=abc]{10}", "Invalid max"),
    "invalid-precision": (r"\gradbar[precision=1.5]{10}", "Precision must be"),
    "zero-width": (r"\gradbar[width=0pt]{10}", "Width must be positive"),
    "zero-height": (r"\gradbar[height=0pt]{10}", "Height must be positive"),
    "overflow-error": (r"\gradbar[max=10,overflow=error]{11}", "Value exceeds range"),
    "positive-min": (r"\gradbar[min=5]{10}", "Min must be zero or negative"),
    "invalid-min": (r"\gradbar[min=abc]{10}", "Invalid min"),
    "signed-percent": (r"\gradbar[min=-10,value format=percent]{5}", "Percent format requires min=0"),
    "below-min": (r"\gradbar[min=-10,overflow=error]{-11}", "Value exceeds range"),
    "target-range": (r"\gradbar[target=101]{50}", "Target must lie within range"),
    "target-invalid": (r"\gradbar[target=foo]{50}", "Invalid target"),
    "negative-error": (r"\gradbar[error=-1]{50}", "Error magnitudes must be nonnegative"),
    "error-overflow": (r"\gradbar[error=20,overflow=error]{90}", "Error upper endpoint exceeds range"),
    "threshold-count": (r"\gradbar[thresholds={60}]{50}", "Thresholds must contain two values"),
    "threshold-order": (r"\gradbar[thresholds={80,60}]{50}", "Thresholds must be strictly increasing"),
    "threshold-colors": (r"\gradbar[thresholds={60,80},threshold colors={red,blue}]{50}", "Threshold colors must contain three colors"),
    "negative-radius": (r"\gradbar[rounded=-1pt]{50}", "Rounded radius must be nonnegative"),
}


def compile_tex(engine, source, output):
    command = [engine, "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", "-output-directory=" + output.relative_to(ROOT).as_posix(),
               source.relative_to(ROOT).as_posix()]
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=90)
    log_path = output / (source.stem + ".log")
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    if not log:
        log = result.stdout.decode(errors="replace")
    return result.returncode, log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=["xelatex"],
                        default="xelatex")
    parser.add_argument("--require-pdf-text", action="store_true")
    args = parser.parse_args()
    if not shutil.which(args.engine):
        sys.exit("Missing TeX engine: " + args.engine)
    output = ROOT / "build" / args.engine
    output.mkdir(parents=True, exist_ok=True)
    passed = 0
    sources = [ROOT / "tests/smoke.tex", ROOT / "tests/semantics.tex",
               ROOT / "tests/effects.tex", ROOT / "tests/geometry.tex"]
    sources += sorted((ROOT / "examples").glob("*.tex"))
    for source in sources:
        code, log = compile_tex(args.engine, source, output)
        if code or "Overfull" in log or "Missing character" in log:
            print(log[-6000:])
            sys.exit("FAIL: " + source.name)
        if source.stem == "semantics":
            assert "bar clipped, label unchanged" in log
        else:
            assert "Package gradbars Warning" not in log
        print("PASS", args.engine, source.name)
        passed += 1
    for name, (body, expected) in INVALID.items():
        source = output / (name + ".tex")
        source.write_text("\\documentclass{article}\n\\usepackage{gradbars}\n"
                          "\\begin{document}\n" + body + "\n\\end{document}\n",
                          encoding="utf-8")
        code, log = compile_tex(args.engine, source, output)
        normalized = re.sub(r"\s+", "", log)
        if code == 0 or re.sub(r"\s+", "", expected) not in normalized:
            print(log[-4000:])
            sys.exit("FAIL: expected diagnostic for " + name)
        print("PASS", args.engine, name, "(expected error)")
        passed += 1
    if shutil.which("pdftotext"):
        result = subprocess.run(["pdftotext", "-layout", str(output / "semantics.pdf"), "-"],
                                stdout=subprocess.PIPE, check=True)
        text = result.stdout.decode("utf-8")
        expected_labels = {
            "RAW": r"50\.0", "PERCENT": r"25\.0%", "UNIT": r"50\.0\s*ms",
            "LARGE": r"87\s*500", "CUSTOM": r"eight of ten",
            "ZERO": r"0\.0%", "OVERFLOW": r"125\.0%",
        }
        for name, expected in expected_labels.items():
            assert re.search(name + r":\s*" + expected + r"\s*(?:\n|$)", text), (name, text)
        print("PASS", args.engine, "PDF labels (7 assertions)")
        passed += 1
        effects = subprocess.run(["pdftotext", str(output / "effects.pdf"), "-"],
                                 stdout=subprocess.PIPE, check=True).stdout.decode("utf-8")
        for label in ["-35.0", "-25.0", "-10.0", "-5.0", "100.0"]:
            assert label in effects, ("Missing signed or end label", label)
        print("PASS", args.engine, "Signed and end labels (5 assertions)")
        passed += 1
    elif args.require_pdf_text:
        sys.exit("Missing pdftotext; install Poppler.")
    else:
        print("SKIP PDF label assertions: pdftotext is not installed")
    print(f"{passed} checks passed for {args.engine}")


if __name__ == "__main__":
    main()
