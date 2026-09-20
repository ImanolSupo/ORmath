# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Extract executable guide examples and compile them independently twice."""
import argparse
import re
from compile import ROOT, ENGINES, compile_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("all", *ENGINES), default="pdflatex")
    args = parser.parse_args()
    manual = (ROOT / "docs/ormath.tex").read_text(encoding="utf-8")
    blocks = re.findall(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", manual, re.S)
    quickstart = (ROOT / "examples/00-quickstart.tex").read_text(encoding="utf-8")
    quickstart = quickstart[quickstart.index("\\documentclass"):]
    if not blocks or blocks[0] != quickstart:
        raise RuntimeError("The first complete guide example differs from the standalone quickstart")
    for name in ("responsive-model", "tag-target", "summation-model"):
        fixture = (ROOT / f"examples/fixtures/{name}.tex").read_text(encoding="utf-8")
        fixture = fixture[fixture.index("\\begin{ormodel}"):]
        if fixture not in blocks:
            raise RuntimeError(f"Guide source differs from its rendered fixture: {name}")
    sources = []
    staging = ROOT / "tmp/manual-examples"
    staging.mkdir(parents=True, exist_ok=True)
    for index, block in enumerate(blocks, 1):
        if block.startswith("l3build check\n"):
            continue  # Explicitly described as shell commands in the guide.
        if "\\begin{document}" not in block:
            block = "\\documentclass[11pt]{article}\n\\usepackage{ormath}\n\\begin{document}\n" + block + "\\end{document}\n"
        source = staging / f"guide-{index:02d}.tex"
        source.write_text(block, encoding="utf-8")
        sources.append(source)
    if not sources:
        raise RuntimeError("No executable examples found in the guide")
    for engine in ENGINES if args.engine == "all" else (args.engine,):
        for source in sources:
            compile_source(source, engine, ROOT / "output/manual-examples" / engine)
    print(f"PASS {len(sources)} extracted guide examples")


if __name__ == "__main__":
    main()
