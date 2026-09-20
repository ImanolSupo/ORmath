# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Build every example and the guide twice; reject unexpected diagnostics."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ENGINES = ("pdflatex", "xelatex", "lualatex")
DIAGNOSTICS = re.compile(r"^!|Undefined control sequence|Overfull|Underfull|LaTeX Warning:|Package .+ Warning:|Font shape .+ undefined|Missing character:", re.MULTILINE)


def compile_source(source: Path, engine: str, output: Path, cwd: Path = ROOT) -> Path:
    executable = shutil.which(engine)
    if not executable:
        raise RuntimeError(f"Missing compiler: {engine}")
    output.mkdir(parents=True, exist_ok=True)
    command = [executable, "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape", f"-output-directory={output}", str(source)]
    for _ in range(2):
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", timeout=180)
        if result.returncode:
            raise RuntimeError(f"{engine}: {source.name}\n{result.stdout}")
    log = (output / f"{source.stem}.log").read_text(encoding="utf-8", errors="replace")
    problems = [line for line in log.splitlines() if DIAGNOSTICS.search(line)]
    if problems:
        raise RuntimeError(f"{engine}: {source.name}\n" + "\n".join(problems))
    pdf = output / f"{source.stem}.pdf"
    if not pdf.is_file():
        raise RuntimeError(f"No PDF produced: {pdf}")
    print(f"PASS {engine}: {source.name}", flush=True)
    return pdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("all", *ENGINES), default="pdflatex")
    args = parser.parse_args()
    sources = sorted((ROOT / "examples").glob("*.tex")) + [ROOT / "docs/ormath.tex"]
    for engine in ENGINES if args.engine == "all" else (args.engine,):
        for source in sources:
            compile_source(source, engine, ROOT / "output/pdf" / engine)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        raise SystemExit(str(error))
