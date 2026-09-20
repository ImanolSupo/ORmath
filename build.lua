-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
-- See NOTICE.md and MANIFEST.txt for work scope and maintenance.

module = "ormath"
sourcefiles = {"*.sty", "*.code.tex"}
installfiles = {"*.sty", "*.code.tex"}
checkengines = {"pdftex", "xetex", "luatex"}
stdengine = "pdftex"
checkruns = 2
testfiledir = "testfiles"
typesetfiles = {"docs/ormath.tex"}
typesetsuppfiles = {"examples/fixtures/planning-model.tex", "examples/fixtures/responsive-model.tex", "examples/fixtures/tag-target.tex", "examples/fixtures/summation-model.tex"}
typesetruns = 2
