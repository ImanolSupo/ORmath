# ORmath design notes

## Public naming and teaching path — 2026-09-16

ORmath is the canonical project name and `ormath` the canonical package.
The implementation is in `ormath.sty`, with the input adapter in
`ormath-input.code.tex`. No compatibility loaders are retained because the
earlier package identity was never accepted for publication on CTAN.

The manual now starts with a complete lightweight example and a two-page path
through notation, index domains, objective senses, rows, and standard references.
Customization follows normal usage; the structured API is an explicitly advanced
metadata/element-control interface. Both APIs keep the existing records/renderer.
The responsive chapter renders one fixture at two widths, preserving a short
row inline while the longer row's domain moves below. No core features were added.

## Revision: flowing notation and an input prototype

Before implementation: evaluate `ornotation` with scoped `set`, `setdef`,
`param`, `var`, and a trailing `for`. Evaluate ordinary model math separated
by explicit `\\`, introduced by `minimize` or `maximize` and `st`.
Both inputs must collect the same records and use the existing renderer.
Retain structured declarations for explicit row options. Do not introduce
blank-line row parsing or change document catcodes.

Notation will measure each declaration separately. Render a colon, prose,
and an inline domain with no block-wide symbol/description/domain columns.
Try the configured gap, then a safe smaller gap, then a paragraph whose
continuation starts at the description. Move an atomic domain below only
when it cannot fit that continuation width. An unusually long prefix may
put its description below; it must not change neighboring rows. Keep the
current font unless the author explicitly chooses another size.

Prototype sugar is confined to top-level tokens in mathematical declarations
and model rows: `>=` and `<=`. Domain arguments additionally accept the
space-delimited word `in`. Preserve groups and macros without expansion.
Leave `!=` and `==` alone: `n!=k` already has a legitimate factorial meaning,
and `=` is shorter than `==`. Use `\\neq` explicitly. A starred `for` supplies
raw mathematics when a domain macro or an unusual condition needs it.

Compare bin packing, facility location, and multi-period planning with raw
amsmath and both package inputs, using identical mathematical rows. Test
references, unnumbered rows, grouping, punctuation, and all three engines.
Inspect PDFs at full width, in two columns, and in a narrow minipage before
making the final API recommendation. Later sections record results.

Result: the three equivalent source comparisons favor the lightweight candidate
by 14–19% in full-source characters against structured input, and 10–12% against
raw LaTeX. Structural commands and argument braces do not uniformly decrease;
the full tables and counting method are in API-COMPARISON.md. Recommend the
lightweight path as primary pre-release input, with structured metadata retained.
Exactly one renderer remains. Keep explicit row separators and native LaTeX
inside protected groups; reject !=/== shorthand and blank-line inference.

Rendered full/two-column/narrow pages confirm left anchoring, single-line short
definitions beside wrapped long ones, description-aligned continuations, and
no font shrinking. Default density is now compact (2pt row gap, 4pt outer gaps).
No punctuation is added except the colon separator; authored prose is literal.
Advanced generated real/integer domains use upright R/Z rather than bold letters.
The prior block-wide 38% threshold is obsolete and no longer implemented.

The domain adapter validates comma-separated memberships while shielding tuple
commas and brace groups. Starred domains accept raw conditions/macros. Standard
top-level labels and notag are collected before measurement; notag rows neither
reserve their own future equation value nor increment the equation counter.
Model labels refer to the first numbered row. Grouped manual breaks reach the
shared amsmath box after only the single outer protection group is removed.
The new tests also confirm max sense and restoration of pre-existing short names.

One artifact verification issue came from redefining label before a minipage:
amsmath's array/parbox restoration resets it there. The example now applies its
local label suppression inside the minipage. No installed amsmath file changed.

Initial inspection: the workspace contained no files. This is a local, pre-release
implementation; no remote, release, upload, or publisher integration is needed.

## Initial architecture review

Keep the recognizable `orsets`, `orparameters`, `orvariables`, and `ormodel`
environments. Provide namespaced commands and scoped short aliases. Store each
declaration as separate semantic fields plus a resolved visual configuration.
Resolve configuration before measurement; render only after collecting the model.
Use the actual local `\linewidth`, and standard equation counters/references.
Depend only on the modern LaTeX kernel and amsmath; do not select document fonts.

## Set defaults and mathematical safety

Problem: `\set{\mathcal C}{Customers}` does not imply
`\mathcal C=\{1,\ldots,|\mathcal C|\}`. Customers could have arbitrary identifiers.
The prompt's proposed default would invent semantics, conflicting with its
stronger rule against inventing mathematical meaning.

Decision: an unspecified set displays its symbol and description. `size=n`
explicitly requests `\{1,\ldots,n\}`; `elements` and `definition` are alternatives.
An explicit `size=|\mathcal C|` reproduces the proposed indexed representation.
This adds no ceremony for a plain set and makes the stronger declaration visible.
Evidence that could change this: a separate, explicitly indexed-set abstraction.

## Command names and scope

Decision: retain the provisional short names locally and expose `\orset`,
`\orparameter`, `\orvariable`, `\orobjective`, and `\orconstraint` globally.
All declaration commands check their context. Namespaced commands provide a safe
escape hatch when a document already uses a short name. Environment grouping
restores the previous short-command meanings, including pre-existing definitions.
Alternatives: global short commands (collision risk), namespaced-only commands
(less readable for long models). Change this if real integration reveals surprises.

## Configuration cascade and order

Decision: defaults < explicit global setup < named style < environment options
< element options. Every layer applies density presets first and explicit spacing
second, regardless of key order. Styles contain visual keys only and do not nest.
Element styles resolve above the environment, with element keys applied last.
Global setup follows ordinary TeX grouping; at document top level it is global in
effect, but a setup inside a group remains scoped. No hidden assignments escape.
Alternative: immediately executing keys left-to-right makes `density` accidentally
erase explicit gaps. Tests must cover both orders and each cascade level.

## Responsive rendering

Decision: measure components independently and align expression starts. Reserve
width for objective/subject-to markers and equation numbers, then move domains
below expressions when needed. Descriptions use a measured symbol column in wide
contexts and a stacked layout in narrow ones. Never parse relations in arbitrary
math. Explicit `\\` inside an expression is the manual multiline escape hatch.
Automatic font size preserves the surrounding size. No whole-model scaling.
Warn when even a stacked expression or domain exceeds the available width.
Alternative: automatic math token splitting is fragile and out of scope.
Evidence that could change this: real fixtures requiring relation alignment or
safe, author-supplied breakpoints beyond explicit multiline input.

## Numbering and unresolved questions

Decision: `numbering=rows` uses the ordinary equation counter (default);
`numbering=model` numbers the model once; `numbering=none` is unnumbered.
Labels use standard `\label`, `\ref`, and `\eqref`. A model label in rows mode
refers to the first row. Labels with numbering=none are diagnosed.
Open: optional subequation numbering, relation-aligned syntax without parsing,
multi-page model blocks, and typographic objectives with author-supplied breaks.

## License

During initial prototyping, licensing and identity were left unresolved.
For release preparation, the owner selected LPPL 1.3c and supplied
Imanol Felix Supo Mamani as copyright holder and Current Maintainer.
The work is author-maintained; LICENSE, NOTICE.md, and MANIFEST.txt define
the grant and scope. This decision does not authorize publication.

## Evidence from the first usability and visual review

The shared production-routing body contains one four-term objective and eleven
constraints, with conditional arc sums, tuple domains, inventory superscripts,
continuous quantities, integer shipments, and binary setups. It needs no outer
align environment, display-spacing settings, margin wrapper, or per-row visual
options. Its four explicit objective lines are authored once and reused at all
three widths. This is substantially less layout ceremony than the motivating
manual align/adjustwidth pattern. Short names and consistent `for` keys remain
easy to read; no naming change beyond the safe set default is warranted yet.

Visual review exposed title orphans despite clean logs. The renderer now boxes
the title with its first row; the remaining model can paginate between rows.
The manual keeps code listings indivisible. Auto moves the balance domain below
in two-column/minipage contexts and retains it at the side in a wide context.
Declaration domains can likewise trigger stacked layout and accept explicit breaks.
Font/number measurement uses every row's resolved size and every upcoming number,
because the widest Roman number need not be the final one.

Eight regressions run under all three target engines. Unicode-engine smoke tests
actually load fontspec and unicode-math with Latin Modern. Clean example/manual
builds are separate from deliberately invalid diagnostic fixtures. See
TEST-RESULTS.md for the executed commands and explicit results.

Remaining usability issue: multiline objectives still expose amsmath break/alignment
tokens. A future semantic continuation command or author-supplied breakpoint key
should be evaluated using real long objectives, without parsing arbitrary math.
Labeled subequations, relation alignment, repeatable page headers, finer description
column control, and variable membership notation remain open visual/API questions.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
