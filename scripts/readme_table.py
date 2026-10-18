#!/usr/bin/env python3
"""Regenerate the pack table in README.md from the archive's word-lens-manifest.json.

The table sits between `<!-- packs-table:begin -->` and `<!-- packs-table:end -->`. Run it after
anything that changes the archive (update_packs.py, import_packs.py); ci.yml runs it with --check,
which exits non-zero when the README is stale.

    python3 scripts/readme_table.py            # rewrite README.md if the table changed
    python3 scripts/readme_table.py --check    # exit 1 if README.md is stale
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pack_archive import ARCHIVE_NAME, MANIFEST_NAME, read_archive  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
BEGIN = "<!-- packs-table:begin -->"
END = "<!-- packs-table:end -->"


def pack_origin(pack: dict) -> str:
    """readest / derived / the importing tool, from the provenance fields the scripts record."""
    if pack.get("origin"):
        return pack["origin"].get("tool", "imported")
    if pack.get("derivedFrom"):
        return "derived"
    return "readest"


def origin_detail(pack: dict) -> str:
    origin = pack_origin(pack)
    if origin == "derived":
        return f"derived из {pack['derivedFrom']['pair']} (машинный перевод)"
    if origin == "readest":
        return "readest" + (" (определения на английском)" if pack["source"] == pack["target"] else "")
    profile = pack["origin"].get("profile")
    return origin + (f" (профиль {profile})" if profile else "")


def table(manifest: dict) -> str:
    packs = manifest["packs"]
    lines = [
        f"Пакетов: {len(packs)}, всего {sum(p['bytes'] for p in packs) / 1e6:.1f} MB.",
        "",
        "| Пара | Исходный | Перевод | Происхождение | Размер | Леммы | Записи (с формами) |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for p in packs:
        lines.append(f"| `{p['pair']}` | {p['source']} | {p['target']} | {origin_detail(p)} | "
                     f"{p['bytes'] / 1e6:.2f} MB | {p['headwords']} | {p['entries']} |")
    return "\n".join(lines) + "\n"


def render(readme: str, manifest: dict) -> str:
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise ValueError(f"README must contain exactly one {BEGIN} ... {END} block")
    head, _, rest = readme.partition(BEGIN)
    _, _, tail = rest.partition(END)
    return f"{head}{BEGIN}\n{table(manifest)}{END}{tail}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=os.path.join(REPO, "data"))
    ap.add_argument("--readme", default=os.path.join(REPO, "README.md"))
    ap.add_argument("--check", action="store_true", help="only report whether README.md is stale")
    args = ap.parse_args(argv)

    members = read_archive(os.path.join(args.data, ARCHIVE_NAME))
    manifest = json.loads(members[MANIFEST_NAME].decode("utf-8"))
    with open(args.readme, encoding="utf-8") as f:
        readme = f.read()
    updated = render(readme, manifest)
    if updated == readme:
        return 0
    if args.check:
        print(f"{os.path.relpath(args.readme)} is stale; run python3 scripts/readme_table.py", file=sys.stderr)
        return 1
    with open(args.readme, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"updated {os.path.relpath(args.readme)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
