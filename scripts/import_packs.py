#!/usr/bin/env python3
"""Merge externally built Word Lens packs (e.g. from ua-dict) into data/word-lens-packs.tar.xz.

The input directory holds the .lens files plus two fragments, as ua-dict's ./build.sh writes them
to dist/wordlens/:

    word-lens-manifest.fragment.json   {"formatVersion": 1, "packs": [<manifest entries>]}
    ATTRIBUTION.fragment.md            "# <title>" and one "- `<file>`: <attribution>" line per pack

Dry run by default; --apply writes the archive and ATTRIBUTION.md. Same-pair entries are replaced,
everything else is carried over. The attribution goes into a `<!-- <name>:begin -->` ...
`<!-- <name>:end -->` section of ATTRIBUTION.md (replaced on re-import), which update_packs.py
keeps when it regenerates the file; --remove PAIR drops a pack again.

    python3 scripts/import_packs.py --packs ../ua-dict/dist/wordlens            # show the plan
    python3 scripts/import_packs.py --packs ../ua-dict/dist/wordlens --apply    # write
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lens_format  # noqa: E402
from pack_archive import ARCHIVE_NAME, ATTRIBUTION_NAME, MANIFEST_NAME, read_archive, write_archive  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "data")
MANIFEST_FRAGMENT = "word-lens-manifest.fragment.json"
ATTRIBUTION_FRAGMENT = "ATTRIBUTION.fragment.md"
PACK_FILE = re.compile(r"^word-lens-[a-z]{2,3}-[a-z]{2,3}\.lens$")


def merge_section(text: str, name: str, section: str | None) -> str:
    """Replace (or append, or with section=None remove) the `name` section of ATTRIBUTION.md."""
    begin, end = f"<!-- {name}:begin -->", f"<!-- {name}:end -->"
    if begin in text and end in text:
        head, _, rest = text.partition(begin)
        _, _, tail = rest.partition(end)
        text = head.rstrip("\n") + "\n" + tail.lstrip("\n")
    if section is None:
        return text.rstrip("\n") + "\n"
    return text.rstrip("\n") + "\n\n" + f"{begin}\n{section.rstrip()}\n{end}\n"


def section_text(fragment_md: str, entries: list[dict]) -> str:
    title = next((ln[2:].strip() for ln in fragment_md.splitlines() if ln.startswith("# ")), "Imported packs")
    per_pack = [ln for ln in fragment_md.splitlines() if ln.startswith("- `")]
    lines = [f"## {title}", ""]
    for e in entries:
        origin = e.get("origin") or {}
        detail = []
        if origin.get("profile"):
            detail.append(f"{origin['profile']} profile")
        if origin.get("sources"):
            detail.append("sources: " + ", ".join(origin["sources"]))
        lines.append(f"- `{e['file']}`" + (f" ({'; '.join(detail)})" if detail else ""))
    lines += ["", "Per-pack attribution strings (shown on the device):", ""] + per_pack
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--packs", help="directory with the .lens files and the two fragments")
    ap.add_argument("--name", help="attribution section name (default: origin.tool of the packs)")
    ap.add_argument("--remove", help="comma-separated pairs to drop from the archive instead")
    ap.add_argument("--data", default=DATA, help="directory holding the pack archive (default: data/)")
    ap.add_argument("--attribution", default=os.path.join(REPO, ATTRIBUTION_NAME),
                    help="plain-text copy of ATTRIBUTION.md (default: the repository root)")
    ap.add_argument("--apply", action="store_true", help="write the archive and ATTRIBUTION.md")
    args = ap.parse_args(argv)
    if bool(args.packs) == bool(args.remove):
        ap.error("pass exactly one of --packs and --remove")

    archive_path = os.path.join(args.data, ARCHIVE_NAME)
    members = read_archive(archive_path)
    if MANIFEST_NAME not in members:
        print(f"{archive_path}: no manifest inside; refusing", file=sys.stderr)
        return 2
    manifest = json.loads(members[MANIFEST_NAME].decode("utf-8"))
    by_pair = {p["pair"]: p for p in manifest["packs"]}
    attribution = members.get(ATTRIBUTION_NAME, b"").decode("utf-8")

    if args.remove:
        for pair in (p.strip() for p in args.remove.split(",") if p.strip()):
            entry = by_pair.pop(pair, None)
            if entry is None:
                print(f"{pair}: not in the archive", file=sys.stderr)
                return 2
            if "readest" in entry or "derivedFrom" in entry:
                print(f"{pair}: a Readest pack; update_packs.py owns it", file=sys.stderr)
                return 2
            members.pop(entry["file"], None)
            print(f"remove {entry['file']}")
        if args.name:
            attribution = merge_section(attribution, args.name, None)
    else:
        with open(os.path.join(args.packs, MANIFEST_FRAGMENT), encoding="utf-8") as f:
            fragment = json.load(f)
        if fragment.get("formatVersion") != manifest["formatVersion"]:
            print(f"format version mismatch: packs {fragment.get('formatVersion')} vs archive "
                  f"{manifest['formatVersion']}", file=sys.stderr)
            return 2
        entries = fragment["packs"]
        name = args.name or next((e.get("origin", {}).get("tool") for e in entries if e.get("origin")), None)
        if not name or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            print("no usable section name; pass --name", file=sys.stderr)
            return 2
        for entry in entries:
            prev = by_pair.get(entry["pair"])
            if prev and ("readest" in prev or "derivedFrom" in prev):
                print(f"{entry['pair']}: a Readest pack of that pair exists; refusing to replace it", file=sys.stderr)
                return 2
            if not PACK_FILE.match(entry["file"]) or entry["file"] != f"word-lens-{entry['source']}-{entry['target']}.lens":
                print(f"{entry['file']}: unexpected file name", file=sys.stderr)
                return 2
            with open(os.path.join(args.packs, entry["file"]), "rb") as f:
                image = f.read()
            if len(image) != entry["bytes"] or hashlib.sha256(image).hexdigest() != entry["sha256"]:
                print(f"{entry['file']}: sha256/size do not match the fragment; rebuild it", file=sys.stderr)
                return 2
            try:
                lens_format.LensFile(image)
            except ValueError as exc:
                print(f"{entry['file']}: {exc}", file=sys.stderr)
                return 2
            print(f"{'replace' if prev else 'add'} {entry['file']}: {entry.get('headwords')} headwords, "
                  f"{entry.get('entries')} records, {entry['bytes']} bytes")
            by_pair[entry["pair"]] = entry
            members[entry["file"]] = image
        with open(os.path.join(args.packs, ATTRIBUTION_FRAGMENT), encoding="utf-8") as f:
            attribution = merge_section(attribution, name, section_text(f.read(), entries))

    manifest["packs"] = sorted(by_pair.values(), key=lambda p: p["pair"])
    members[MANIFEST_NAME] = (json.dumps(manifest, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    members[ATTRIBUTION_NAME] = attribution.encode("utf-8")
    total = sum(p["bytes"] for p in manifest["packs"])
    print(f"the archive would hold {len(manifest['packs'])} packs, {total / 1e6:.1f} MB unpacked")
    if not args.apply:
        print("dry run: nothing written (use --apply)")
        return 0
    changed = write_archive(archive_path, members)
    with open(args.attribution, "w", encoding="utf-8") as f:
        f.write(attribution)
    print(f"archive {'rewritten' if changed else 'unchanged'}: {os.path.relpath(archive_path, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
