# ORmath 0.1.0 — proposed first release

Experimental toolkit for compact notation and mathematical optimization models.
This is a development package; no accepted public CTAN release exists yet.
ORmath is the sole package identity and loads with `\usepackage{ormath}`.

The initial API provides unified notation and lightweight model input alongside
structured commands. Definitions flow independently within the available width,
with left anchoring and hanging continuations. Models retain standard equation
numbering and references. Fonts and mathematical notation remain author-controlled.

The distribution includes a standalone quickstart, a compiled user guide,
full-page/two-column/minipage examples, a thirty-constraint pagination example,
API comparisons, and regression contracts for pdfLaTeX, XeLaTeX, and LuaLaTeX.
See [TEST-RESULTS.md](TEST-RESULTS.md) for actual execution and its limits.

The API is experimental. Arbitrary TeX parsing, automatic expression breaking,
model solving, and mathematical validation are outside the package's scope.
Publisher classes and all fonts are not certified. See the
[README](README.md) and [guide](docs/ormath.pdf) before adopting it.

Copyright 2026 Imanol Felix Supo Mamani; LPPL 1.3c, author-maintained.
Review this text and change the candidate wording to describe the actual
publication when it occurs.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
