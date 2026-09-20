# Input recommendation and visual review — 2026-09-16

Recommend `ornotation` and lightweight `ormodel` rows as the primary pre-release
input. Keep the structured environments as an advanced adapter to the same
records and renderer. The shorter source wins modestly on character count; it
does **not** win every source-complexity measure. The main benefit is removing
outer alignment work and measuring responsive definitions independently.

## Exact recommended syntax

```latex
\begin{ornotation}
  \set[size=n]{J}{Jobs}
  \setdef{M}{(j,t)\in J\times T}{Job-period pairs}
  \param{d_{jt}}{Demand}\for{j in J,t in T}
  \var{x_{jt} >= 0}{Production}\for{j in J,t in T}
  \var{y_{jt}\in\{0,1\}}{Setup indicator}\for{j in J,t in T}
\end{ornotation}
\begin{ormodel}[label=mod:packing]
  \minimize \sum_{b\in B}y_b \label{obj:bins} \\
  \st \sum_{b\in B}x_{ib}=1 \for{i in I} \label{con:assign} \\
  \sum_{i\in I}w_i x_{ib} <= C y_b \for{b in B} \\
  x_{ib}\in\{0,1\} \for{i in I,b in B} \notag
\end{ormodel}
```

`\maximize` supplies maximization; `\subjectto` is an alternative to `\st`.
Neither objective marker is a global short command. All prior meanings return
after the environment. Set symbols and complete variable declarations retain
the author's styling. `\var` does not infer or append a variable type.
Namespaced adapters `\orvar`, `\orsetdef`, and `\orfor` are available in the
same checked contexts. Existing namespaced structured declarations remain.

## Why this direction

The model row is ordinary mathematics with an explicit delimiter. There are no
outer `&` positions, per-constraint wrapper braces, or `label=` keys in the common
case. Standard row labels and `\notag` are collected before measurement, then
ordinary equation counters/references are used. A unified notation environment
reduces separate-environment boilerplate and expresses variable domains directly.
Explicit set size/definition metadata still avoids inventing set membership.

This is LaTeX with measured layout, not a new mathematical language. Native
`\sum`, subscripts, fractions, macros, and explicit amsmath breaks remain useful.
The thirty-constraint example makes the repeated-row experience reviewable;
its ten families are explicitly instantiated for three periods as a stress case.
Ordinary manuscript source would normally quantify those repeated families.

## Alternatives evaluated

| Input | Strength | Cost / decision |
|---|---|---|
| Structured declarations | Explicit metadata and per-row styling; existing compatibility | Repeated commands/options and braces; retain as advanced input |
| Lightweight scoped rows | Direct math, ordinary labels, fewer characters, no outer alignment | More small structural commands than raw; recommend primary |
| Raw amsmath align | Familiar, minimal argument braces, flexible alignment | Requires alignment tokens and manual layout adaptation; remains an escape hatch |
| Blank-line row separators | Visually natural source | Paragraph handling and macro structure are fragile; not implemented |
| Relation parsing or document-wide shorthand | Potentially more implicit syntax | Ambiguity and TeX interference; not implemented |

Both package inputs use exactly one layout/rendering path. Neither source style
changes the mathematical rows in the comparison fixtures.

## Actual source comparison

Measured by `python scripts/compare-inputs.py`, reading the checked-in nine
fixtures under `examples/comparison/`. All variants have identical descriptions,
mathematical declarations, constraints, objective sense, and label keys. The
comparison document supplies label prefixes so versions can coexist.
Counts include indentation, line endings normalized to LF, metadata, and the
notation/model environment wrappers, but omit the common document wrapper and
identical leading copyright/license notice. The script strips that exact notice;
it does not remove arbitrary comments or whitespace.
Brace counts are literal brace characters, including escaped mathematical
delimiters. Structural commands are the explicitly enumerated input/layout
commands in the script, not all mathematical macros. Alignment tokens count
individual `&` plus each `\\`; brackets count individual `[` and `]` characters.

| Model | Input | Characters | Structural commands | Braces | Option brackets | Alignment tokens | Lines |
|---|---|---:|---:|---:|---:|---:|---:|
| bin-packing | raw | 646 | 19 | 38 | 0 | 19 | 13 |
| bin-packing | structured | 718 | 19 | 82 | 16 | 0 | 19 |
| bin-packing | light | 581 | 24 | 78 | 0 | 4 | 15 |
| facility-location | raw | 819 | 21 | 42 | 0 | 19 | 14 |
| facility-location | structured | 891 | 20 | 96 | 20 | 0 | 20 |
| facility-location | light | 732 | 27 | 90 | 0 | 4 | 16 |
| planning | raw | 1898 | 40 | 140 | 0 | 48 | 26 |
| planning | structured | 1946 | 32 | 236 | 44 | 1 | 32 |
| planning | light | 1667 | 51 | 230 | 0 | 12 | 28 |

Light input saves approximately **19.1%, 17.8%, 14.3%** versus structured input,
and **10.1%, 10.6%, 12.2%** versus this raw LaTeX baseline. Its structural command
count and braces are higher than raw LaTeX, and physical source lines are slightly
more numerous. Raw notation here is a simple `\noindent` paragraph per definition;
it provides no measured hanging layout or domain fallback. These are three
specific models and formatting choices, not a universal typing-cost claim.

For the models alone, run `python scripts/compare-inputs.py --model-only`:

| Model | Input | Characters | Structural commands | Braces | Option brackets | Alignment tokens | Lines |
|---|---|---:|---:|---:|---:|---:|---:|
| bin-packing | raw | 376 | 7 | 32 | 0 | 19 | 7 |
| bin-packing | structured | 376 | 7 | 38 | 10 | 0 | 7 |
| bin-packing | light | 337 | 13 | 38 | 0 | 4 | 7 |
| facility-location | raw | 438 | 7 | 36 | 0 | 19 | 7 |
| facility-location | structured | 438 | 7 | 42 | 10 | 0 | 7 |
| facility-location | light | 397 | 13 | 42 | 0 | 4 | 7 |
| planning | raw | 1033 | 16 | 110 | 0 | 48 | 14 |
| planning | structured | 1028 | 14 | 128 | 24 | 1 | 14 |
| planning | light | 914 | 27 | 128 | 0 | 12 | 14 |

The lightweight model saves roughly 9–11% in characters. The removed outer
alignment tokens and option keys, rather than fewer total commands, justify it.
Structured comparison variables use the original explicit `type=` metadata,
which generates the same declarations as raw and lightweight source.

## Easy-syntax feasibility

| Input | Result / boundary |
|---|---|
| `>=`, `<=` | Normalize to `\geq`, `\leq` at top level in `\var` and light model rows |
| `i in I,t in T` | Normalize space-delimited `in` only inside unstarred `\for` |
| `(i,j) in A,t in T` | Supported tuple membership; tuple commas are not clause separators |
| `i\in I,\;j\in J` | Native membership accepted and preserved |
| `!=` | Not implemented; use `\neq` |
| `n!=k`, `n! =k` | Preserve ordinary factorial followed by equality |
| `==` | Not implemented; write the shorter native `=` |
| `\frac{a>=b}{c<=d}`, `\text{in >=}` | Groups are preserved literally; write native operators inside them |
| `\mathrm{in}`, `\Cost_i`, custom macro arguments | Preserved without expansion by the adapter |
| `\for{j J}`, `\for{j in}`, `\for{j in J,k K}` | Package input error, not silent inference |
| `\for*{\Domain}`, `\for*{t>0}` | Raw-domain escape hatch; no membership parsing or normalization |
| Unicode prose / math fonts | Normal TeX/font handling; tested accents and Unicode math font setup |

Protection applies to braced arguments. Optional or unbraced macro arguments
cannot be inferred without interpreting arbitrary TeX: their top-level operators
can normalize. Use native operators or an outer brace group for literal input.

The bounded grammar checks one membership per comma-separated clause, protects
tuple parentheses and brace groups, and requires nonempty index/set parts. It
does not validate mathematical truth or expand a macro to discover membership.
Unusual conditions should use starred domains or the structured raw `for=` key.
No global active characters, catcode tricks, regex over user prose, or macro
expansion are used. Native LaTeX remains the safer language inside groups.

## Visual review

The inspected pdfLaTeX pages include examples 10–12 (full/two-column/55% local
width), all three lightweight real-model pages in comparison example 13,
both pages of example 14, and the narrower planning page in example 15.
The two-column PDF includes labeled bin packing with unnumbered type rows.
Further engine and manual review is recorded in TEST-RESULTS.md.

All notation starts at the local content edge. A row first tries its full prefix,
description, and inline quantifier, then reduces safe gaps before wrapping.
No wide symbol in another row consumes its description width. `B_t` and `a_j`
stay on one line beside long grouped-cost and inventory declarations. Wrapped
inventory prose aligns to the description. Domains are atomic unless explicitly
broken by the author, so a domain can occupy the next continuation line.
No automatic font reduction, default symbol styling, or separator period appears.

Defaults now use `density=compact`: 2pt additional row spacing, 4pt outer gaps,
and an 8pt prose-domain gap reducible to 3pt after a failed line fit. The colon
gap reduces from 3pt to 2pt. Existing named presets remain available. Models
retain semantic marker/expression/number alignment, anchored at the local left
edge; expression starts align without relation parsing or horizontal centering.
Thirty constraint rows paginate, with ordinary numbers and final references.

## Engine results

Actual final commands and matrix are recorded in TEST-RESULTS.md. Regression
contracts cover semantic storage, literal factorial/equality, protected groups,
malformed domains, aliases, per-row flow, normal font retention, max sense,
standard labels, `\notag`, and subsequent equation counters. Engine availability
alone is not counted as evidence. fontspec/unicode-math smoke tests load actual
Latin Modern fonts on XeTeX and LuaTeX.

## Implementation impact

The existing seven-field records, configuration cascade, model renderer,
counter/label integration, and alias package remain. Notation rendering replaces
block-wide columns with row measurement and flowing/hanging paragraphs. The
private resolved row flag `suppress-tag` carries `\notag`, and measurement skips
such rows without changing real counters. The input adapter is installed as
`ormath-input.code.tex`. `build.lua` now copies/installs it with the package.
There is no second package renderer or engine-specific mathematics path.

## Known risks and recommendation

The API is pre-release. `ormodel` captures its body, requires a literal leading
objective marker, and does not support verbatim or macro-generated row structure.
Include a complete environment when loading a model file. A grouped multiline
row shields its `\\` from row splitting; native operators inside that outer
group are required because groups are deliberately opaque. Individual rows are
indivisible when paginating. Very long unbreakable mathematics still needs author
breaks and produces width diagnostics. Math/prose measurement can evaluate user
content more than once; side effects inside arguments remain unsuitable.
Description punctuation is explicit author input, never parsed or restyled.

Adopt the lightweight input as the documented primary candidate now. Keep the
structured adapter for advanced options and compatibility. Treat shorthand and
the limited domain grammar as provisional conveniences, and gather manuscript
experience before declaring API stability. Reject implicit blank-line parsing,
`!=`/`==` sugar, automatic mathematical restyling, and blanket narrow-layout
stacking. No release or publication is part of this local work.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
