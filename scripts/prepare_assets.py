# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Regenerate the checked-in guide and README image from real TeX output."""
import hashlib
import json
import shutil
import subprocess
from compile import ROOT, compile_source


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise RuntimeError("Install Poppler (pdftoppm) to regenerate the preview.")
    output = ROOT / "output/pdf/pdflatex"
    guide = compile_source(ROOT / "docs/ormath.tex", "pdflatex", output)
    preview = compile_source(ROOT / "docs/preview.tex", "pdflatex", output)
    shutil.copyfile(guide, ROOT / "docs/ormath.pdf")
    images = ROOT / "docs/images"
    images.mkdir(parents=True, exist_ok=True)
    subprocess.run([renderer, "-scale-to", "1400", "-singlefile", "-png", str(preview), str(images / "quickstart")], check=True, timeout=60)
    inputs = ["ormath.sty", "ormath-input.code.tex", "docs/ormath.tex", "docs/preview.tex", "examples/fixtures/planning-model.tex", "examples/fixtures/responsive-model.tex", "examples/fixtures/tag-target.tex", "examples/fixtures/summation-model.tex", "scripts/prepare_assets.py"]
    assets = ["docs/ormath.pdf", "docs/images/quickstart.png"]
    manifest = {"inputs": {p: digest(ROOT / p) for p in inputs}, "assets": {p: digest(ROOT / p) for p in assets}}
    (ROOT / "docs/assets.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("PASS regenerated guide, preview, and source fingerprints")


if __name__ == "__main__":
    main()
