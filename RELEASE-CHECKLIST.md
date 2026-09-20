# First-release review

Everything in this preparation remains local. These are owner review steps,
not authorization for automated publication.

## Required decisions

- [x] Owner selected LPPL 1.3c and confirmed Imanol Felix Supo Mamani as
  copyright holder and Current Maintainer. The official license text and
  author-maintained notice are included; review their scope before distribution.
- [ ] Confirm the proposed version `0.1.0` and tag `v0.1.0`.
- [x] Record the supplied attribution in [CITATION.md](CITATION.md).
- [ ] Add the eventual repository URL when it exists. No DOI or repository
  address was invented.
- [ ] Review the README example, preview, installation steps, limitations, and
  [release notes](RELEASE-NOTES.md); replace candidate wording at publication.

## Local validation

Python 3.10+ is required for repository scripts, not for using the package.
Run from the repository root with the compilers in PATH:

```text
l3build check
python scripts/compile.py --engine all
l3build doc
python scripts/check_manual.py --engine all
python scripts/prepare_assets.py
python scripts/release.py inventory
python scripts/release.py check
python scripts/test_release.py
python scripts/release.py package
python scripts/release.py smoke
```

`prepare_assets.py` additionally requires Poppler's `pdftoppm`. It recompiles
the guide and real TeX preview and records source/asset fingerprints. Inspect
the rendered result after any relevant source change. `release.py check`
rejects missing installation files, stale assets, inconsistent metadata, broken
relative Markdown links, and unresolved licensing. `inventory` refreshes
MANIFEST.txt when distribution files are added or removed. `package` writes a sorted,
deterministic source archive, manifest, and SHA-256 checksum to `output/release/`.
`smoke` installs only the two required package files and the quickstart from that
archive into a separate directory and compiles twice with each engine.

For review while licensing is unresolved, use `check --review`,
`package --review`, and `smoke --review`. The archive is named `-review.zip` and
embeds a review-only notice. This exception does not constitute a license grant.

- [ ] Confirm all commands pass for the final source tree and inspect the PDFs.
- [ ] Check the archive's manifest and checksum; test the extracted installation.
- [ ] Review the source archive for private information and intended attribution.
- [ ] Review the prepared GitHub workflow. Hosted CI and Linux/TeX Live have not
  been executed during local Windows/MiKTeX verification.

Local preparation completed the regression/example matrix, guide/preview review,
eight release-gate tests, YAML parsing, archive reproducibility, and extracted
three-engine installation. Actual results are in [TEST-RESULTS.md](TEST-RESULTS.md).
The unchecked boxes above remain the owner's final review, not unfinished builds.

## Later, only after owner approval

Repository creation, remote configuration, pushes, tags, public releases, CTAN,
Overleaf, and external documentation publication are outside this task. No such
operation has been performed. A public repository and hosted CI can be reviewed
by the owner after the license and attribution decisions are complete.

<!-- Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c. See NOTICE.md and MANIFEST.txt for work scope and maintenance. -->
