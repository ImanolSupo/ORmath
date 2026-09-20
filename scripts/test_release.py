# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Exercise real release gates on disposable copies of the distribution."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import release


class ReleaseGates(unittest.TestCase):
    def setUp(self):
        staging = release.ROOT / "tmp/release-tests"
        staging.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=staging)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for source in release.files():
            destination = self.root / source.relative_to(release.ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())

    def check(self, review=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return release.check(review, self.root)

    def test_current_distribution(self):
        self.check()

    def test_missing_installation_helper(self):
        (self.root / "ormath-input.code.tex").unlink()
        with self.assertRaisesRegex(RuntimeError, "Missing or unsafe distribution file"):
            self.check()

    def test_stale_preview(self):
        with (self.root / "docs/preview.tex").open("a", encoding="utf-8") as stream:
            stream.write("\n% changed source\n")
        with self.assertRaisesRegex(RuntimeError, "Stale asset or source fingerprint"):
            self.check()

    def test_broken_documentation_link(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[missing](missing-document.md)\n")
        with self.assertRaisesRegex(RuntimeError, "Broken link"):
            self.check()

    def test_unresolved_ownership_requires_explicit_review(self):
        path = self.root / "release.json"
        meta = json.loads(path.read_text(encoding="utf-8"))
        meta["copyright_holder"] = None
        path.write_text(json.dumps(meta), encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Publication gate"):
            self.check()
        self.check(review=True)

    def test_modified_license_is_rejected(self):
        with (self.root / "LICENSE").open("a", encoding="utf-8") as stream:
            stream.write("altered terms\n")
        with self.assertRaisesRegex(RuntimeError, "License text"):
            self.check()

    def test_missing_component_notice_is_rejected(self):
        path = self.root / "examples/00-quickstart.tex"
        text = path.read_text(encoding="utf-8")
        path.write_text("\n".join(text.splitlines()[2:]) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Missing component license notice"):
            self.check()

    def test_build_clutter_excluded(self):
        for name in ("output/private.tex", "tmp/secret.tex", "docs/generated.log", "scripts/__pycache__/hidden.py"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("not for distribution", encoding="utf-8")
        selected = {p.relative_to(self.root).as_posix() for p in release.files(self.root)}
        self.assertNotIn("output/private.tex", selected)
        self.assertNotIn("tmp/secret.tex", selected)
        self.assertNotIn("docs/generated.log", selected)
        self.assertNotIn("scripts/__pycache__/hidden.py", selected)
        self.check()


if __name__ == "__main__":
    unittest.main(verbosity=2)
