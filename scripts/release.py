# Copyright 2026 Imanol Felix Supo Mamani. Licensed under LPPL 1.3c.
# See NOTICE.md and MANIFEST.txt for work scope and maintenance.

"""Local release checks, deterministic source packaging, and extracted-install tests.

No network, Git, repository creation, or publication operations are performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile
import zipfile
from compile import ROOT, ENGINES, compile_source

TOP = (
    "ormath.sty", "ormath-input.code.tex", "build.lua",
    "README.md", "LICENSE", "NOTICE.md", "MANIFEST.txt", "CHANGELOG.md", "CONTRIBUTING.md",
    "ARCHITECTURE.md", "DESIGN-NOTES.md", "API-COMPARISON.md", "TEST-RESULTS.md",
    "RELEASE-NOTES.md", "RELEASE-CHECKLIST.md", "CITATION.md", "release.json",
    ".gitignore", ".gitattributes", ".editorconfig",
)
DIRECTORIES = {
    "docs": {".tex", ".pdf", ".png", ".json"},
    "examples": {".tex"}, "testfiles": {".tex", ".lvt", ".tlg"},
    "scripts": {".py", ".ps1"}, ".github": {".yml", ".md"},
}
LPPL_SHA256 = "3d262cdf34dafa6955f703c634a8c238ec44109bc8dd6ef34fb7aa54809f7e66"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files(root=ROOT):
    selected = [root / p for p in TOP]
    for directory, extensions in DIRECTORIES.items():
        selected.extend(p for p in (root / directory).rglob("*") if p.is_file() and p.suffix in extensions and "__pycache__" not in p.parts)
    for path in selected:
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise RuntimeError(f"Missing or unsafe distribution file: {path.name}")
    return sorted(selected, key=lambda p: p.relative_to(root).as_posix())


def check(review=False, root=ROOT):
    selected = files(root)
    meta = json.loads((root / "release.json").read_text(encoding="utf-8"))
    if not re.fullmatch(r"\d+\.\d+\.\d+", meta["version"]):
        raise RuntimeError("Release version must be a numeric x.y.z version")
    if meta["proposed_tag"] != "v" + meta["version"] or meta["status"] != "experimental":
        raise RuntimeError("Inconsistent candidate metadata")
    source = (root / "ormath.sty").read_text(encoding="utf-8")
    pattern = r"\{" + re.escape(meta["date"]) + r"\}\s*\{" + re.escape(meta["version"]) + r"\}"
    if not re.search(pattern, source):
        raise RuntimeError("Version/date mismatch: ormath.sty")
    for name in ("README.md", "CHANGELOG.md", "RELEASE-NOTES.md", "docs/ormath.tex"):
        if meta["version"] not in (root / name).read_text(encoding="utf-8"):
            raise RuntimeError(f"Version missing: {name}")
    readme = (root / "README.md").read_text(encoding="utf-8")
    snippet = re.search(r"```latex\n(.*?)\n```", readme, re.S)
    if not snippet or snippet[1] not in (root / "examples/00-quickstart.tex").read_text(encoding="utf-8"):
        raise RuntimeError("README example differs from the compiled quickstart")
    for path in selected:
        if path.suffix == ".md":
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if re.match(r"[a-zA-Z][\w+.-]*:", target) or target.startswith("#"):
                    continue
                relative = target.split("#")[0]
                if relative and not (path.parent / relative).exists():
                    raise RuntimeError(f"Broken link in {path.name}: {target}")
    manifest = json.loads((root / "docs/assets.json").read_text(encoding="utf-8"))
    for group in ("inputs", "assets"):
        for name, expected in manifest[group].items():
            if digest((root / name).read_bytes()) != expected:
                raise RuntimeError(f"Stale asset or source fingerprint: {name}; run prepare_assets.py")
    if not (root / "docs/ormath.pdf").read_bytes().startswith(b"%PDF-"):
        raise RuntimeError("Guide is not a PDF")
    if not (root / "docs/images/quickstart.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Preview is not a PNG")
    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    pending = not meta.get("license") or not meta.get("copyright_holder") or not meta.get("maintainer") or "License decision pending" in license_text
    if not pending:
        if meta["license"] != "LPPL-1.3c" or digest((root / "LICENSE").read_bytes()) != LPPL_SHA256:
            raise RuntimeError("License text and selected identifier do not agree")
        notice = (root / "NOTICE.md").read_text(encoding="utf-8")
        if meta["copyright_holder"] not in notice or meta["maintainer"] not in notice or meta.get("maintenance_status") != "author-maintained":
            raise RuntimeError("Copyright/maintainer metadata differs from NOTICE.md")
        for path in selected:
            if path.suffix in {".sty", ".tex", ".lvt", ".py", ".ps1", ".lua", ".yml"}:
                text = path.read_text(encoding="utf-8")
                if ("Copyright 2026 " + meta["copyright_holder"]) not in text or "Licensed under LPPL 1.3c" not in text:
                    raise RuntimeError(f"Missing component license notice: {path.name}")
    listed = (root / "MANIFEST.txt").read_text(encoding="utf-8").splitlines()
    actual = [p.relative_to(root).as_posix() for p in selected]
    if listed != actual:
        raise RuntimeError("MANIFEST.txt differs from distribution files; run inventory")
    if pending:
        if not review:
            raise RuntimeError("Publication gate: license and copyright holder remain unresolved. Use --review only for a private review bundle.")
        print("REVIEW ONLY: licensing/ownership unresolved; no distribution grant")
    print(f"PASS release file checks: {len(selected)} files")
    return meta, selected


def archive_name(meta, review):
    return f"ormath-{meta['version']}" + ("-review" if review else "")


def package(review=False):
    meta, selected = check(review)
    name = archive_name(meta, review)
    prefix = f"ormath-{meta['version']}/"
    output = ROOT / "output/release"
    output.mkdir(parents=True, exist_ok=True)
    payloads = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in selected}
    if review:
        payloads["REVIEW-ONLY.txt"] = b"Private review candidate. No publication has occurred. Resolve licensing and attribution before distribution.\n"
    manifest = {"name": meta["name"], "version": meta["version"], "review_only": review,
                "files": {p: {"bytes": len(data), "sha256": digest(data)} for p, data in sorted(payloads.items())}}
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    payloads["MANIFEST.json"] = manifest_data
    archive = output / f"{name}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(prefix + path, (2026, 9, 20, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    (output / f"{name}.manifest.json").write_bytes(manifest_data)
    (output / f"{name}.sha256").write_text(f"{digest(archive.read_bytes())}  {archive.name}\n", encoding="utf-8")
    print(f"PASS local archive: {archive.name}")
    return archive


def smoke(review=False):
    meta, _ = check(review)
    archive = ROOT / "output/release" / (archive_name(meta, review) + ".zip")
    prefix = f"ormath-{meta['version']}/"
    staging = ROOT / "tmp/release-smoke"
    staging.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        manifest = json.loads(bundle.read(prefix + "MANIFEST.json"))
        expected = {prefix + p for p in manifest["files"]} | {prefix + "MANIFEST.json"}
        if set(bundle.namelist()) != expected or len(bundle.namelist()) != len(expected):
            raise RuntimeError("Unexpected or duplicate archive entries")
        for name, record in manifest["files"].items():
            data = bundle.read(prefix + name)
            if digest(data) != record["sha256"] or len(data) != record["bytes"]:
                raise RuntimeError(f"Archive integrity mismatch: {name}")
        current = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files()}
        for name, data in current.items():
            if bundle.read(prefix + name) != data:
                raise RuntimeError(f"Archive differs from working source: {name}; rebuild package")
        with tempfile.TemporaryDirectory(prefix="install-", dir=staging) as directory:
            install = Path(directory)
            for name in ("ormath.sty", "ormath-input.code.tex", "examples/00-quickstart.tex"):
                (install / Path(name).name).write_bytes(bundle.read(prefix + name))
            for engine in ENGINES:
                compile_source(install / "00-quickstart.tex", engine, ROOT / "output/release-smoke" / engine, cwd=install)
    print("PASS archive integrity and isolated two-file installation on three engines")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inventory", "check", "package", "smoke"))
    parser.add_argument("--review", action="store_true", help="Permit unresolved licensing only for local review")
    args = parser.parse_args()
    if args.command == "inventory":
        paths = sorted(set(TOP) | {p.relative_to(ROOT).as_posix() for d, ext in DIRECTORIES.items() for p in (ROOT / d).rglob("*") if p.is_file() and p.suffix in ext and "__pycache__" not in p.parts})
        (ROOT / "MANIFEST.txt").write_text("\n".join(paths) + "\n", encoding="utf-8")
        print(f"PASS updated inventory: {len(paths)} files")
    else:
        {"check": check, "package": package, "smoke": smoke}[args.command](args.review)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error))
