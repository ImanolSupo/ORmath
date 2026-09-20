# Architecture

```text
User declaration
      ↓
Context check → parse options → validate semantics
      ↓
Semantic record (unexpanded mathematical tokens)
      ↓
Resolved visual configuration
      ↓
Available local width + measured components
      ↓
Layout strategy
      ↓
Rendering + standard LaTeX labels
```

## Files and responsibilities

`ormath.sty` contains the shared, organized implementation of the first vertical
slice. Its sections separate diagnostics, configuration, semantic records,
public commands, measurement, model rendering, declaration-block rendering, and
environment bindings. It loads the separate `ormath-input.code.tex` input adapter.
ORmath has one package id and one loader: `ormath`.

`build.lua` configures l3build for pdftex/xetex/luatex, two passes per test.
`testfiles/` holds regression input and reviewed expected logs.
`examples/fixtures/` contains a shared realistic semantic model and notation.
`scripts/compile.py` compiles examples/manual and rejects unexpected diagnostics;
`compile.ps1` remains a Windows alternative. `check_manual.py` compiles extracted
guide examples. `docs/ormath.tex` is the user manual. Build artifacts are ignored under `build/`,
`output/`, and `tmp/`.

## Public API and scoping

The environments create an ordinary LaTeX group. Begin code resolves their
configuration, clears local records, and binds short commands locally. End code
renders collected records. Global namespaced declaration commands check the
active environment and give a package error in the wrong context.

All collection, style resolution, measurement, and font/spacing changes are
local. Only standard equation counter increments and label writes intentionally
affect the document. Setup/style definitions use ordinary scoped assignments;
placing them at the top level makes them effective for following environments.
There is no persistent model registry, global margin change, or font selection.

## Semantic records

`\l__ormath_records_seq` stores seven separate, unexpanded fields:

1. kind (`set`, `parameter`, `variable`, `min`, `max`, `constraint`);
2. mathematical expression/symbol;
3. ordinary description text;
4. author-supplied index domain;
5. standard row label;
6. snapshot of resolved visual configuration (an expl3 property list);
7. variable mathematical type, separately from the index domain.

Set representations are validated and constructed from the declared symbol and
one optional representation key during collection. Arbitrary mathematics is
never parsed. The sequence is the model source of truth until rendering.
Stored tokens do not expand user notation macros; the semantics regression
asserts this explicitly. Environment title and model label remain separate.

## Configuration

Defaults, setup overrides, and named styles have separate property lists.
`ormath/config` parses visual keys into a temporary layer. Semantic key families
are separate, preventing styles from changing mathematical meaning.
`\__ormath_apply_layer:` applies a density preset first, followed by explicit
values. `\__ormath_resolve_layer:` inserts a named style beneath the current
layer. Styles cannot recurse. The environment configuration is saved before
element parsing; every element starts from it, preventing previous-row leakage.

Environment order: defaults → setup → named style → explicit environment options.
Element order: environment → optional element style → explicit element options.
An element style is restricted to properties actually consumed by rows.
Dimension validation occurs where a renderer consumes the dimension.

## Measurement and layout

Math is boxed with inherited fonts and display style inside amsmath `aligned`.
This permits explicit multiline input without requiring the outer layout API to
expose alignment columns. Available width is local `\linewidth` plus author-set
extensions; page geometry and journal identity never enter the decision.

Models share a measured marker reserve using every row's resolved font. Tag
measurement considers every upcoming ordinary equation value, including custom
formats such as Roman numbers; counter predictions are grouped and create no
labels or hyperlinks. A preparation pass boxes each expression/domain once and
caches the boxes locally, allocating private reusable registers only up to the
largest row count encountered. Rendering reuses them rather than evaluating
mathematics again to discover the model's natural width. Counter-sensitive math
sees the same preceding equation value as before this preparation pass.

For a tagged row, let W be local linewidth after explicit author extensions,
M the marker reserve and T that row's actual tag width. Auto tag preference is
clamp((W-M)/25, 0.75em, 2em), with a 0.5em fitting minimum. Auto domain preference
is 0.8em with a 0.3em minimum. Fit first with both minima reserved, then prefer
the tag separation by compressing the domain gap, and compress the tag gap if
needed. If expression + domain + both minimum gaps + T cannot fit W-M, move only
that domain below and recompute the tag separation beside the expression.
Explicit dimensions retain their values. Untagged rows reserve neither T nor a
tag gap. A below-domain line may use all W-M, independently of its first-line tag.

Each automatically tagged row supplies its natural right extent (first-line
content + fitted tag gap + actual tag width), capped to W-M for anchor selection.
Sort those extents and take the upper middle value C (the smaller value for a
two-row model). The common right edge is min(widest extent, C + max(2em, C/4)).
This simple bounded extension preserves a shared compact anchor without letting
one exceptional row determine the entire model width. A row extending beyond
the anchor keeps its own natural tag edge. Objectives participate with constraints.
Model numbering measures only the row actually bearing the model tag; notag
and numbering=none contribute no anchor candidates. Sharing adds alignment
padding within this bounded block, rather than stretching to unused page width.

Manual tag-gap uses an exact row-local separation, bypassing the common anchor.
tag-position=right explicitly puts the tag at W-M (the outer right edge after
the marker); in that mode tag-gap is a fitting reservation. Both controls follow
the ordinary setup/style/environment/structured-element cascade. Tags stay on
the expression's first baseline when domains move below. Literal separators are
added only with domains, and authored trailing comma/semicolon/period wins.
Forced wide/right domain layouts and stacked/below layouts remain escape
hatches. No automatic shrinking, class detection or arbitrary token splitting.

Declaration blocks measure each expression, prose, and index domain separately.
They try a colon-separated flowing line at the configured gap, then safe smaller
gaps, then a hanging paragraph using that row's prefix width. No maximum symbol
width is shared across rows. Only a domain too wide for the continuation is
placed below; an unusually long prefix or explicit stacked layout can put prose
below the prefix. Default density is compact, and no automatic font reduction
occurs. Literal prose punctuation and mathematical symbol styling are preserved.
For notation, domain-gap=auto resolves to the existing density-based prose/domain gap.
Domains support the same explicit aligned breaks as model-row mathematics.
Descriptions wrap as ordinary paragraphs. Oversize mathematical boxes remain
visible and are diagnosed rather than silently scaled.

Rendering uses a zero-width adjustment inside a paragraph box with the original
linewidth, so intentional extensions do not trigger spurious paragraph overflow.
Content overflow still produces normal TeX diagnostics. A title is boxed together
with the first row to prevent orphans at a page boundary. Each model row is
indivisible internally but the model can paginate between subsequent rows.

## Referencing

Rows use `\refstepcounter{equation}` and ordinary `\label`; models in model mode
step the same counter once. In rows mode the model label shares the first numbered row's
number. Hyperref uses the standard counter integration, without a parallel label
system. Number measurement changes the counter only inside a group, without
creating hyperlinks or real counter increments.

## Input adapters

`ormath-input.code.tex` is installed with the package. It adds `ornotation`,
raw `orvar`, `orsetdef`, and a trailing `orfor` that replaces the last record's
domain without expanding any fields. A body-captured `ormodel` detects literal
leading `minimize`/`maximize`; other bodies execute the structured collector.
Explicit top-level `\\` delimit lightweight rows. Nested groups shield breaks.
A token scanner preserves groups and macros, extracts top-level `for`, `label`,
and `notag`, and collects the same seven-field record. No second renderer exists.
The private resolved-config flag `suppress-tag` represents a lightweight notag;
it is not a public style key. Number measurement skips suppressed rows, as does
counter advancement. A single outer expression group is unwrapped only when
boxing mathematics, so protected manual breaks reach amsmath.

Top-level token replacements normalize >= and <=; domains additionally replace
the space-delimited word in. Nested groups and macros are never rewritten or
expanded. A bounded domain scan validates comma-separated membership clauses,
treating tuple parentheses and brace groups as protected comma contexts. It
rejects missing membership, indices, sets, or unbalanced tuple parentheses;
it does not interpret set mathematics or expand macros.
Starred domains bypass it. Factorial/equality remain literal: there is no != or
== shorthand. Captured bodies do not support verbatim or macro-generated row
structure. Full included model environments and macros inside mathematics work.

Indexed summations live in the existing input adapter module. `\orsum` is a
public mathematical operator; `ormodel` binds `\Sum` locally before collection
and rendering. No model record fields or responsive-layout decisions are added.
The command consumes only its starred flag and braced specification, then emits
one ordinary `\sum` with a subscript. It never consumes the summand.

The normal path separates the optional literal space-delimited `where` before
passing memberships to the same token scanner and clause validator used by
`\for`. Brace groups are opaque and parenthesized membership commas are
protected. The shared validator can collect clauses for summation without
altering stored `\for` output or its diagnostics. Summation clauses join with
`comma + \;`, followed by `:\,` and the optional condition. Condition commas
are never fed to membership splitting; only existing safe inequality
normalization applies. Macros are not expanded to find grammar. Literal `in`
after `where`, empty conditions and repeated `where` are errors. Raw subscripts
bypass the parser entirely. Explicit nested commands emit explicit nested sums.

Parsing state is grouped by each operator, avoiding interference with row/domain
collection or nested operators. Collision tests verify both an existing and an
undefined external `\Sum` are restored after the model. Dimension comparisons
against native LaTeX verify operator count, raw escapes and untouched summands.

## Diagnostics and tests

Package diagnostics cover invalid context, unknown option/style, nested styles,
set representation conflicts, objective count, incompatible labels, negative
dimensions, empty blocks, nesting, and oversized math.

Regressions assert semantic storage, style cascade/order, short-alias restoration,
surrounding text/layout state, subsequent math fonts, ordinary equation/align
behavior, width adaptation, numbering/references with hyperref, and multilingual
font smoke tests. Diagnostic tests deliberately provoke package errors and one
overfull expression; these expected logs are distinct from clean example builds.
Engine-specific diagnostic baselines preserve legitimate font-metric differences.
Robustness tests additionally cover empty models, contradictory objective senses,
mixed row fonts, nonmonotonic Roman-number widths, and multiline notation domains.

LaTeX NFSS selects math font sizes lazily, sometimes with global internal cache
updates. Isolation tests verify the *next ordinary math* has the restored font
size rather than manipulating NFSS internals or expecting an unused math-font
register to update before the next formula.

When adding a feature, change semantic parsing/storage before layout/rendering,
add a meaningful regression and visual example, then update the manual. Split
the source into physical modules only when the responsibilities become harder
to navigate in one file.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
