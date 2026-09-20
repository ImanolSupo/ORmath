# Changelog

## Unreleased

- Rename the package to ORmath with the sole loader `ormath`, move the runtime
  implementation and input module to that identity, and remove legacy loaders
  and alias-only tests.

- Add public `\orsum` and model-local `\Sum` indexed summation shorthand,
  with one operator per command, shared membership parsing, an optional single
  mathematical `where` condition, and starred raw subscripts.
- Cover operator semantics, token preservation, diagnostics, scope restoration,
  and isolated package loading with summation regressions and examples.

- Add responsive `tag-gap=auto` and a compact shared anchor for objective and
  constraint tags, with local handling of unusually long rows.
- Add exact tag-gap dimensions and conventional `tag-position=right`, following
  the existing setup/style/environment/structured-row cascade.
- Fit domain and tag gaps jointly against local width; retain tags beside the
  expression when domains continue below. Preserve numbering and references.
- Use bounded automatic model domain gaps and configurable semicolon separators
  in the coordinated fitting pass.
- Cover responsive tags with regression contracts, visual fixtures, and manual
  examples; split semantic regression records to avoid platform log wrapping.

## 0.1.0 — 2026-09-16 (rejected CTAN submission; never published)

- Reorganized the guide around a self-contained two-page lightweight workflow,
  a visual width comparison, scannable option tables, and an advanced API section.
- Documented ORTeX and ORmath as aliases of canonical ORLaTeX; added the thin
  `ormath` loader and independent/duplicate-loading regression and smoke tests.
- Added executable guide-example extraction and compilation checks.

- Prepared a concise README with a compiled preview and standalone quickstart.
- Added portable example builds, local release checks and packaging, isolated
  installation verification, contributor templates, and a prepared CI workflow.
- Added review notes/checklist and source fingerprints for the compiled guide
  and preview. Confirmed LPPL 1.3c and copyright/maintenance attribution.

- Revised notation defaults to left-anchored colon-separated flowing lines with
  independent row measurement, safe gap reduction, and hanging continuations.
- Changed default density to compact; removed automatic block-wide stacking and
  bold generated real/integer domain letters.
- Prototyped unified notation, complete raw variable declarations, scoped
  lightweight model rows, trailing domains, standard labels, and notag.
- Added bounded membership grammar and protected top-level inequality shorthand;
  factorial/equality, nested groups, macros, and user prose remain literal.
- Added six examples, nine equivalent API-comparison fixtures, reproducible
  source metrics, three more regression contracts, and updated recommendations.

- Added semantic sets, parameters, variables, objectives, and constraints with
  scoped short commands and namespaced alternatives.
- Added explicit indexed/enumerated/defined set representations; plain sets
  preserve unspecified membership.
- Added consistent index domains, four variable types, standard equation labels,
  and row/model/none numbering.
- Added setup, named styles, deterministic density presets and configuration
  cascade, local font/spacing control, and explicit width extensions.
- Added width-aware domain placement and adaptive symbol-description blocks.
- Added nine examples, a shared realistic planning model at three widths, user
  manual, contributor/architecture/design documentation, and l3build regressions.
- Recorded design questions. No publication or API-stability promise is made.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
