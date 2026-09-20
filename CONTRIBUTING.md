# Contributing to ORmath

Start with a minimal complete TeX example that explains the modeling or layout
problem. Include the available width, package version, compiler, and distribution.
For proposals, show the source you want to write and the output you expect.
The API is experimental; improvements should keep ordinary mathematics intact.
Contributions should be compatible with the project's LPPL 1.3c license.
See [NOTICE.md](NOTICE.md) for copyright and maintenance details.

## Tools

- A current LaTeX distribution with pdfLaTeX, XeLaTeX, LuaLaTeX, amsmath, and l3build.
- Python 3.10+ for portable repository scripts; no Python is needed by the package.
- Optional PowerShell 7 for `scripts/compile.ps1`.
- Optional fontspec/unicode-math and Latin Modern fonts for modern-font smoke tests.
- Poppler `pdftoppm` for visual inspection.

## Run from the repository root

```powershell
l3build check
python scripts/compile.py --engine all
python scripts/check_manual.py --engine all
python scripts/check_aliases.py
python scripts/test_release.py
```

Use `--engine pdflatex`, `xelatex`, or `lualatex` for a focused example/manual build.
The script runs each source twice and fails on unresolved references, unexpected
warnings, missing glyphs, font-shape warnings, and over/underfull boxes.
PDFs and complete compiler logs are under `output/pdf/<engine>/`.
Do not run two l3build processes concurrently: they share and clear `build/test/`.

Manual compilation without PowerShell:

```text
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape docs/ormath.tex
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape docs/ormath.tex
```

Compile examples similarly, from the root so shared fixtures resolve. `l3build
doc` is an additional manual-build path; example compilation remains a separate
command so visual/log verification is explicit.

## Tests and baselines

`testfiles/*.lvt` exercise contracts rather than mirroring implementation details.
`*.tlg` contain reviewed expected results. Add a regression for a real bug or
public behavior, then save a baseline after inspecting the actual output:

```powershell
l3build save -e pdftex test-name
l3build check test-name
```

Use engine-specific baselines only for justified engine differences, such as a
deliberately overfull diagnostic fixture's font metrics. Never save a `FAIL`
assertion, unexpected TeX error, or missing glyph as a successful baseline.
Saving a log is not verification; rerun `l3build check` afterward.

The diagnostic test intercepts only expected message entry points to record
diagnostic identifiers. Ordinary TeX errors are retained. The clean compilation
script provides complementary checks of real user-facing message behavior.

## Implementation conventions

Internal functions: `\__ormath_...`. Local data: `\l__ormath_...`.
Default/setup/style stores: `\g__ormath_...` (setup/styles still follow ordinary
TeX scope). Public commands use `or...` names, with locally bound short aliases.
Keep parsing, validation, storage, style resolution, measurement, and rendering
separate. Preserve user math tokens without expansion. Do not infer membership,
indices, relation operators, or objective semantics from arbitrary TeX.

Before changing an API, describe the usability problem, compare alternatives,
and record the decision and change criteria in DESIGN-NOTES.md. Update README,
manual option documentation, examples, regressions, and CHANGELOG together.

## Visual review

Render the latest PDF, then inspect all relevant pages:

```powershell
pdftoppm -r 120 -png output/pdf/pdflatex/06-two-column.pdf tmp/two-column
```

Check title placement, objective hierarchy, line alignment, spacing, domains,
equation numbers, descriptions, page breaks, and surrounding text. A clean log
does not establish visual quality. Record actual results in TEST-RESULTS.md.
Never claim an engine passed unless it was run.

## Preview and release maintenance

Run `python scripts/prepare_assets.py` after changing package output or the guide.
This updates the checked-in PDF, README image, and fingerprint manifest. Inspect
the new render before committing these assets. Publication preparation is
described in [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md). The prepared CI workflow
checks each engine separately; it does not publish artifacts or documentation.

For local environment troubleshooting and the exact tested platform, see
[TEST-RESULTS.md](TEST-RESULTS.md). Avoid introducing machine-specific font or
cache configuration into distributed package files.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
