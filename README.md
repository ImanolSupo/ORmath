# ORmath

*Typesetting mathematical optimization models and notation.*

> Write the model. Let ORmath handle the layout.

ORmath is a lightweight, responsive LaTeX toolkit for writing and typesetting
mathematical optimization models. It keeps ordinary LaTeX mathematics while
reducing repetitive layout work and adapting notation and models to the
available width.

```latex
\begin{ornotation}
  \set[size=n]{I}{Products}
  \param{c_i}{Unit profit}\for{i in I}
  \param{u_i}{Capacity}\for{i in I}
  \var{x_i >= 0}{Production}\for{i in I}
\end{ornotation}
\begin{ormodel}
  \maximize \sum_{i\in I} c_i x_i \\
  \st x_i <= u_i \for{i in I} \label{capacity}
\end{ormodel}
```

![Real ORmath output: compact, left-anchored definitions and a numbered production model.](docs/images/quickstart.png)

**Experimental version 0.1.0.** The API may change. ORmath typesets models;
it does not solve them or validate their mathematical correctness.

## Install and try

Use a current LaTeX distribution (kernel 2022-06-01 or newer). The package's only
external package dependency is `amsmath`.

1. Copy **both** [ormath.sty](ormath.sty) and
   [ormath-input.code.tex](ormath-input.code.tex) beside your document.
2. Add `\usepackage{ormath}` to its preamble.
3. Compile twice to resolve equation references.

For a complete first example, put [00-quickstart.tex](examples/00-quickstart.tex)
beside those two files and run:

```text
pdflatex 00-quickstart.tex
pdflatex 00-quickstart.tex
```

XeLaTeX and LuaLaTeX also work with the tested examples. In a repository checkout,
run `pdflatex examples/00-quickstart.tex` twice from the root. Advanced examples
use shared fixtures, so compile them from the root too. The only supported loader
is `ormath`.

## What it handles

- Compact notation: declaration, colon, description, and domain share a line
  whenever they fit. Each row adapts independently, with hanging continuations.
- Left-anchored models with objective, constraint, domain, and equation-number
  alignment at full page, two-column, and minipage widths.
- Ordinary `\label`, `\ref`, `\eqref`, and `\notag`, with row, model, or no numbering.
- Scoped short commands, plus setup, named styles, and explicit font/spacing options.
- An advanced structured API for metadata and element-level control.

Optional indexed summations reduce repeated membership syntax:

```latex
\begin{ormodel}
  \minimize \Sum{i in I,j in J_i} c_{ij}x_{ij} \\
  \st \Sum{(i,j) in A where c_{ij}>0} y_{ij} <= M
\end{ormodel}
```

One `\Sum` produces one symbol over the complete domain. Write
`\Sum{i in I}\Sum{j in J}` for two nested symbols. The optional single `where`
condition is ordinary math, not prose; use `\land`, `\neq` and native operators.
`\Sum*{...}` supplies raw subscript math, including `\substack`. The short alias
is local to `ormodel` and restores any external meaning. Public `\orsum` and
`\orsum*` also work in ordinary math and structured expressions; standard `\sum`
is unchanged. See [22-indexed-summations.tex](examples/22-indexed-summations.tex)
and the manual for examples and grammar limits.

The lightweight API is recommended for ordinary paper writing; the structured
API is optional. Both feed the same semantic representation and renderer.

Mathematical styling stays yours: `J` remains `J`, and `\mathcal J` remains
`\mathcal J`. Plain sets do not acquire inferred members. Raw variable declarations
render the complete expression you supply, without adding an implicit type.

## Lightweight API

Begin lightweight models with `\minimize` or `\maximize`, separate rows with
explicit `\\`, and introduce constraints with `\st` or `\subjectto`.
Blank lines are whitespace, not constraint separators.

`\for{j in J,t in T}` is a small membership grammar. Native mathematics such as
`\for{j\in J,t\in T}` is accepted too; tuple memberships are supported. Use
`\for*{<native math>}` for arbitrary conditions. Top-level `>=` and `<=` are
conveniences in raw variable declarations and lightweight model rows. Inside
braced groups, keep native LaTeX operators. `!=` and `==` are not aliases;
`n!=k` retains its ordinary factorial/equality meaning.

Short names are local to ORmath environments. See the
[user guide](docs/ormath.pdf) for options, structured commands, and numbering.

Model domains use `domain-gap=auto`: normally 0.8em, reduced toward 0.3em when
space is tight. If that row still cannot fit, its domain moves below; neighboring
short rows keep their domains inline. `domain-gap=1em` or `10pt` fixes the gap.
Use `domain-position=right` or `below` to force placement. A semicolon is
inserted by default; `domain-separator={,}` changes it and `{}` disables it.
A literal trailing comma, semicolon, or period already in the expression wins.
Existing notation flow and fonts are preserved.

Equation tags also adapt automatically: the model infers a compact shared anchor
from its measured rows and local width. A much longer row keeps its own nearby
tag without spreading out short neighbors. Tag gaps respond to width and font
size, compress with domain gaps, and remain bounded; available width is not
space that must be filled. When a domain moves below, its tag stays on the
expression line. No minipage or two-column flag is needed for this behavior.

Use `tag-gap=0.8em`, `2em`, or `12pt` for an exact row-local separation.
Use `tag-position=right` for conventional publisher-style right-edge numbering.
Both keys work in setup, named styles, model options and structured row options.
The defaults are `tag-gap=auto,tag-position=auto`; numbering and references are
unchanged.

## Examples and documentation

| Start here | Purpose |
|---|---|
| [Quickstart](examples/00-quickstart.tex) | Complete, small document |
| [Wide notation](examples/10-easy-notation.tex) | Default definition flow |
| [Two-column notation](examples/11-easy-two-column.tex) | Independent row adaptation |
| [Narrow notation](examples/12-easy-narrow.tex) | Hanging continuations |
| [Thirty constraints](examples/14-thirty-constraints.tex) | Model pagination and references |
| [Adaptive tags](examples/19-adaptive-tags.tex) | Shared anchors, outliers, narrow domains and overrides |
| [User guide PDF](docs/ormath.pdf) / [source](docs/ormath.tex) | Public API and limitations |

All example sources are in [examples](examples). For implementation background,
see [architecture](ARCHITECTURE.md), [API comparisons](API-COMPARISON.md), and
[executed verification results](TEST-RESULTS.md).

## Current limits

ORmath is not an arbitrary TeX parser and does not automatically break long
mathematical expressions. Nested environments, verbatim content, and
macro-generated row structure are outside the lightweight parser's supported
scope. An indivisible multiline row cannot split across pages; continuation
headings are not repeated. Measurement can evaluate material more than once,
so avoid side effects in mathematical content.

Older kernels, arbitrary publisher classes, and all font families have not been
verified. Tested fonts and engines are recorded in [TEST-RESULTS.md](TEST-RESULTS.md).

## Contribute

Bug reports are most useful with a minimal complete document, the available
width, and compiler/distribution versions. See [CONTRIBUTING.md](CONTRIBUTING.md)
for development and visual review. From the repository root:

```text
l3build check
python scripts/compile.py --engine all
```

The local suite covers three engines. A GitHub Actions workflow is prepared,
but has not been run on hosted runners. See [CHANGELOG.md](CHANGELOG.md) for changes.

## License

Copyright 2026 Imanol Felix Supo Mamani. Distributed under the
LaTeX Project Public License, version 1.3c. See [LICENSE](LICENSE) and
[NOTICE.md](NOTICE.md) for the work's scope and maintenance status.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
