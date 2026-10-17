#!/usr/bin/env python3
"""Stage the committed Word Lens packs as GitHub release assets (used by .github/workflows/release.yml).

Extracts every pack listed in the archive's word-lens-manifest.json, the manifest itself and the
attribution notice (as word-lens-ATTRIBUTION.md) from data/word-lens-packs.tar.xz into --out,
after checking that each pack matches the sha256 and size the manifest records and still parses
as a .lens file. Prints the number of staged files; exits non-zero on any mismatch and on archive
members the manifest does not list. --notes also writes release notes (a table of the packs).

    python3 scripts/stage_release_assets.py --out dist --notes dist-notes.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lens_format  # noqa: E402
from pack_archive import ARCHIVE_NAME, ATTRIBUTION_NAME, MANIFEST_NAME, read_archive  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
ATTRIBUTION_ASSET = "word-lens-ATTRIBUTION.md"


def release_notes(manifest: dict) -> str:
    lines = [
        "Word Lens gloss packs for CrossLingua (`.lens` format v%d). Devices download them from" % manifest["formatVersion"],
        "`releases/latest/download/`; sources and licences: `%s`." % ATTRIBUTION_ASSET,
        "",
        "| Pair | File | Size | Headwords | sha256 |",
        "|---|---|---:|---:|---|",
    ]
    for p in manifest["packs"]:
        lines.append(f"| {p['source']} → {p['target']} | `{p['file']}` | {p['bytes'] / 1e6:.2f} MB | "
                     f"{p['headwords']} | `{p['sha256'][:16]}…` |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=DATA)
    ap.add_argument("--out", required=True)
    ap.add_argument("--notes", help="also write release notes (Markdown) to this path")
    args = ap.parse_args(argv)

    members = read_archive(os.path.join(args.data, ARCHIVE_NAME))
    if MANIFEST_NAME not in members or ATTRIBUTION_NAME not in members:
        print("archive lacks the manifest or the attribution", file=sys.stderr)
        return 1
    manifest = json.loads(members[MANIFEST_NAME].decode("utf-8"))
    if manifest.get("formatVersion") != lens_format.FORMAT_VERSION:
        print(f"manifest formatVersion {manifest.get('formatVersion')} != {lens_format.FORMAT_VERSION}", file=sys.stderr)
        return 1
    listed = {p["file"] for p in manifest["packs"]}
    extra = set(members) - listed - {MANIFEST_NAME, ATTRIBUTION_NAME}
    if extra:
        print(f"archive members not in the manifest: {', '.join(sorted(extra))}", file=sys.stderr)
        return 1
    os.makedirs(args.out, exist_ok=True)
    staged = 0
    for pack in manifest["packs"]:
        data = members.get(pack["file"])
        if data is None or len(data) != pack["bytes"] or hashlib.sha256(data).hexdigest() != pack["sha256"]:
            print(f"{pack['file']}: missing or does not match the manifest", file=sys.stderr)
            return 1
        try:
            lens_format.LensFile(data)
        except ValueError as exc:
            print(f"{pack['file']}: {exc}", file=sys.stderr)
            return 1
        with open(os.path.join(args.out, pack["file"]), "wb") as f:
            f.write(data)
        staged += 1
    with open(os.path.join(args.out, MANIFEST_NAME), "wb") as f:
        f.write(members[MANIFEST_NAME])
    with open(os.path.join(args.out, ATTRIBUTION_ASSET), "wb") as f:
        f.write(members[ATTRIBUTION_NAME])
    if args.notes:
        with open(args.notes, "w", encoding="utf-8") as f:
            f.write(release_notes(manifest))
    print(staged + 2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
