#!/usr/bin/env python3
"""Assemble the client-pinned standards files from the structured source articles.

Shipped coop clients read ONLY the three v1-pinned files (standards/sql.md,
standards/dax.md, standards/semantic-model.md) and retrieve sections by
heading match. This script rebuilds those files from the source articles
under SQL/, Power BI/, and Technology/. Never hand-edit the pinned files.

Usage:
    python3 scripts/assemble.py          # rebuild the pinned files
    python3 scripts/assemble.py --check  # verify the pinned files are current (no writes)

Exit codes: 0 = ok (or current, with --check), 1 = missing source, 2 = drift detected (--check).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# article (relative to repo root) -> pinned file. Order within each list is
# the section order in the pinned file: articles with distinctive, non-generic
# titles go first, or broad topic words crowd them out of the 6-chunk budget.
MAP = {
    "standards/sql.md": [
        "SQL/SQL Formatting.md",
        "SQL/Silver/Overview.md",
        "SQL/Gold/Stored Procedures.md",
        "SQL/Gold/Fact Tables.md",
        "SQL/Gold/Dimension Tables.md",
        "SQL/Gold/Views.md",
        "Technology/Fabric/Fabric Warehouse.md",
    ],
    "standards/dax.md": [
        "Power BI/Semantic Model/DAX.md",
        "Power BI/Semantic Model/Measures.md",
    ],
    "standards/semantic-model.md": [
        "Power BI/File Types.md",
        "Power BI/Reports/App Deployment.md",
        "Power BI/Reports/Page Formatting.md",
        "Power BI/Reports/Visuals.md",
        "Power BI/Semantic Model/M Query.md",
        "Power BI/Semantic Model/Composite Models.md",
        "Power BI/Semantic Model/Fact Tables.md",
        "Power BI/Semantic Model/Relationships.md",
        "Power BI/Semantic Model/Tables.md",
    ],
}

HEADER = (
    "<!-- ASSEMBLED from structured articles by scripts/assemble.py.\n"
    "     Edit the source article under SQL/, Power BI/, or Technology/ and re-run\n"
    "     `python3 scripts/assemble.py`. Do not hand-edit sections here. -->\n\n"
)

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)


def body_without_front_matter(path):
    text = path.read_text(encoding="utf-8")
    return FRONT_MATTER.sub("", text).strip()


def first_heading(path, body):
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise SystemExit(f"error: {path}: source article has no '# ' title heading")


def build(out_rel):
    parts = []
    for src_rel in MAP[out_rel]:
        src = ROOT / src_rel
        if not src.is_file():
            raise SystemExit(f"error: missing source article: {src_rel}")
        body = body_without_front_matter(src)
        first_heading(src, body)
        parts.append(body)
    return HEADER + "\n\n".join(parts) + "\n"


def main():
    check_only = "--check" in sys.argv[1:]
    drift = []
    for out_rel in MAP:
        assembled = build(out_rel)
        out = ROOT / out_rel
        if check_only:
            current = out.read_text(encoding="utf-8") if out.is_file() else None
            if current != assembled:
                drift.append(out_rel)
            continue
        out.write_text(assembled, encoding="utf-8")
        print(f"assembled {out_rel} <- {len(MAP[out_rel])} articles")
    if check_only:
        if drift:
            print("stale (re-run scripts/assemble.py): " + ", ".join(drift))
            raise SystemExit(2)
        print("pinned files are current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
