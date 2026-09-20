# Local verification — 2026-09-20

Release candidate: ORmath **0.1.0**, Windows, MiKTeX 25.4, LaTeX kernel
2025-11-01, expl3 2025-11-06. Results below describe actual execution, not inferred
compatibility. This revision supersedes the initial eight-test/ten-source matrix.
No tag, release, CTAN upload, or publication occurred.

## Final commands and outcomes

Executed from the repository root:

```powershell
l3build check
python scripts/compile.py --engine all
python scripts/prepare_assets.py
python scripts/release.py inventory
python scripts/release.py check
python scripts/test_release.py
python scripts/release.py package
python scripts/release.py smoke
python scripts/compare-inputs.py
python scripts/compare-inputs.py --model-only
```

- `l3build check`: **PASS**. Thirteen tests, three engines, two runs each
  (39 engine/test combinations; 78 TeX passes).
- `scripts/compile.py --engine all`: **PASS**. Twenty examples and the manual,
  three engines, two runs each (63 documents; 126 TeX passes). The portable Python
  script was executed on Windows; Linux execution is not inferred.
- Final manual-only refresh: **PASS**, two additional passes under each of
  pdfLaTeX, XeLaTeX, and LuaLaTeX after adding the selected LPPL license, supplied attribution, and PDF metadata;
  all three final logs clean.
- `prepare_assets.py`: **PASS**, two pdfLaTeX passes each for the fourteen-page
  guide and one-page README preview; checked-in assets have source fingerprints.
- `l3build doc`: **PASS**, two pdfLaTeX passes for the renamed manual.
- Source-metric commands: **PASS**; tables and exact counting method in
  API-COMPARISON.md. Counts read actual checked-in fixtures.
- Release checks: **PASS**, 99 explicitly inventoried distribution files;
  required installation files, relative Markdown links, version/date, component
  notices, official license bytes, and source/asset fingerprints checked.
- Release gate regressions: **PASS**, eight disposable-tree cases covering valid
  contents, missing installation helper, stale preview, broken link, unresolved
  ownership, altered license, missing component notice, and excluded build clutter.
- Local source archive: **PASS**, sorted entries and fixed archive metadata;
  two builds from unchanged inputs produced identical SHA-256 hashes. The adjacent
  checksum and manifest describe the final archive, without machine-specific paths.
- Archive installation: **PASS**, manifest integrity and working-tree consistency
  checked; only the two installation files and quickstart copied to a temporary
  directory, then compiled twice with all three engines. Logs are retained under
  `output/release-smoke/<engine>/`. No root fixtures were needed.
- GitHub workflow and issue templates: YAML parsing **PASS** locally. Hosted
  workflow execution is unverified. CI contains no publication/upload step.

The manual refresh used each engine with
`-interaction=nonstopmode -halt-on-error -no-shell-escape`,
`-output-directory=output/pdf/<engine>`, and `docs/ormath.tex`, twice.
Its final logs were checked independently for errors, undefined controls,
over/underfull boxes, package/LaTeX warnings, missing glyphs, and unresolved refs.

Baselines reviewed during the preceding prototype cycle (not regenerated for
release preparation):

```powershell
l3build save -e pdftex cascade robustness input flow input-numbering
l3build save -e pdftex robustness flow input
l3build save -e pdftex input
l3build save -e pdftex input-numbering
```

Intermediate failures were corrected before the final suite. Saving expectations
alone did not establish PASS: the saved logs were reviewed, then the complete
three-engine suite rerun. No baseline contains a FAIL assertion or unexpected
TeX error. `diagnostics` intentionally records package errors and an overfull
expression; `input` deliberately records four package input errors for invalid
domains/context. Those are separate from clean example/manual builds.
The earlier engine-specific overflow baselines remain valid.

## Actual engine matrix

| Feature | pdfLaTeX | XeLaTeX | LuaLaTeX |
|---|---|---|---|
| Canonical ORmath loading | PASS | PASS | PASS |
| Structured sets/parameters/types/models | PASS | PASS | PASS |
| Unified notation and complete raw declarations | PASS | PASS | PASS |
| Top-level >= / <= and scoped in | PASS | PASS | PASS |
| Literal != / == / factorial-equality | PASS | PASS | PASS |
| Opaque groups, text, fractions, macros | PASS | PASS | PASS |
| Tuple memberships / malformed-domain diagnostics | PASS | PASS | PASS |
| Independent row flow / hanging continuation | PASS | PASS | PASS |
| Configuration cascade and grouping | PASS | PASS | PASS |
| Existing and new short-command restoration | PASS | PASS | PASS |
| Subsequent ordinary text/equation/align | PASS | PASS | PASS |
| Min/max sense, numbering, notag, standard refs | PASS | PASS | PASS |
| Hyperref reference integration | PASS | PASS | PASS |
| Roman numbering and mixed row fonts | PASS | PASS | PASS |
| Twenty examples plus manual | PASS | PASS | PASS |
| Thirty explicit constraint rows / pagination | PASS | PASS | PASS |
| Accented prose / inherited font | PASS | PASS | PASS |
| fontspec + unicode-math smoke test | NOT APPLICABLE | PASS | PASS |

Unicode-engine tests actually loaded fontspec/unicode-math with Latin Modern
Roman and Latin Modern Math, including the new input adapters. This is a smoke
test of these fonts, not a claim that all fonts and classes work.

## Regression coverage

- `load-scope`: canonical loader, surrounding text/layout state, subsequent
  ordinary math font, ordinary equation/align counter behavior.
- `semantics`: unexpanded records, explicit/plain set representations, indexed
  parameters, four structured variable types, objective and constraint metadata.
- `cascade`: compact default, setup/style/environment/element precedence, order
  independence, element style override, sibling reset, grouped setup.
- `responsive`: measured model domains, local narrow width, forced right/below,
  both objective senses.
- `numbering`: rows/model/none, standard references and hyperref, two-pass writes.
- `diagnostics`: contexts/options/styles, set conflicts, invalid objectives,
  labels, negative dimensions and deliberately excessive mathematics.
- `fonts`: accented Spanish/French and inherited font, old/new input, actual
  fontspec/unicode-math on Unicode engines.
- `robustness`: empty/conflicting models, counter-safe measurement, Roman widths,
  row font reserves, local long-domain wrapping, explicit multiline domains.
- `input`: controlled inequalities, literal factorial/equality, grouped fraction
  arguments and text, unchanged prose, unexpanded math/domain macros, tuple
  indices, missing membership/set, malformed second clause, scoped new aliases.
- `flow`: short-long-short-long-short rows at 195pt; only long rows wrap, hanging
  continuations use their own prefix, normal 10pt font remains unchanged.
- `input-numbering`: protected manual row breaks, first objective notag, first
  numbered model reference, later notag, standard labels, subsequent counter,
  max sense, model/none modes, restored objective/subject-to names, hyperref.

## Visual review and artifacts

All final second-pass example/manual logs contain no unexpected package errors,
warnings, unresolved references, missing glyphs, or over/underfull boxes. The
compile script rejects these diagnostics rather than suppressing them.

Rendered with Poppler `pdftoppm` at a 1200–1400px page scale and inspected in this
revision: pdfLaTeX examples 10–12; comparison pages 1, 2, 3, 6, 9; both thirty-row
pages; narrow planning page; legacy two-column and minipage planning examples;
all eight manual pages; XeLaTeX and LuaLaTeX examples 11 and 12. After the final
manual punctuation cleanup, its changed page 4 was rendered and inspected again.
The earlier development cycle inspected all original nine example PDFs.

Observed: local left anchoring; flowing colon-separated definitions; no shared
empty columns; short capacity/resource declarations remain one line beside long
grouped definitions; hanging prose aligns at the description; atomic domains
move to a continuation line when needed; no font reduction; authored mathematical
styling retained. Models keep semantic marker/expression/domain/number alignment,
standard refs, and left anchoring. The thirty-row model paginates and ends with
reference (31). The manual narrow example is now left anchored too.

Two authoring issues were fixed: a missing paragraph boundary around the manual
minipage and label suppression placed before a minipage (amsmath restores label
there). The latter is now scoped inside it. No installed package code changed.

Generated PDFs/logs: `output/pdf/pdflatex/`, `output/pdf/xelatex/`, and
`output/pdf/lualatex/` (21 example/guide PDFs per engine; pdflatex also has the
preview). The checked-in guide is `docs/ormath.pdf`; the README image is
`docs/images/quickstart.png`. `build/doc/ormath.pdf` is the l3build documentation
output; use the checked-in or freshly compiled guide for the release candidate.
Release preparation also inspected the final README preview and changed manual
pages 1 and 8: attribution, version, license text, build commands, and spacing
are legible with no clipping. Its PDF title/author metadata matches the guide.

Temporary rendered review images under `tmp/pdfs/` are removed after inspection;
final PDFs and compiler/regression logs remain. Metrics script and source fixtures
remain reviewable under `scripts/` and `examples/comparison/`.

## Local environment issue resolved

The first restricted MiKTeX invocation could not initialize its normal cache.
Running the local tools with approved normal permissions resolved that.
The initial LuaLaTeX font database scan then failed before package code ran with
`Unsupported UNC path encountered`. A plain article reproduced the environment
failure. The following scratch configuration successfully initialized the cache:

```ini
[db]
location-precedence = texmf
[run]
log-level = 4
```

The exact successful engine smoke command was:

```powershell
# Working directory: tmp/lua-check
lualatex -interaction=nonstopmode -halt-on-error -no-shell-escape smoke.tex
```

After initialization, final suite/example/manual commands ran normally from the
root without a root font config or a change to the package's font policy. The
ordinary MiKTeX font caches were populated; no installed font/package source was
patched. Scratch evidence remains under `tmp/lua-check/`.

## Limits of verification

No arbitrary TeX parser or automatic expression breaking is implemented. Long
objectives require explicit authored breaks. Models align expression starts,
not relations. Multiline rows cannot split across pages; continuation headings
are not repeated. Extremely narrow widths and overlong unbreakable domains can
still overflow and are diagnosed. The fixture illustrates package usability;
ORmath does not validate the optimization model's mathematical correctness.
Nested environments, subequations, arbitrary publisher classes, all font families,
and older kernels have not been verified. LPPL 1.3c, copyright holder, and Current
Maintainer were confirmed by the owner during release preparation. Hosted CI,
Linux/TeX Live, CTAN packaging, and Overleaf upload were not performed. No tag or
release was created.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
