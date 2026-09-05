#!/usr/bin/env python3
"""Rewrite publication front matter into HugoBlox's structured shape.

`academic import` writes the journal as one markdown string:

    publication: '*J. Clin. Invest.*'

HugoBlox now wants the parts separately, and warns once per page until it
gets them:

    publication:
      name: J. Clin. Invest.
      volume: '136'
      issue: '12'
      pages: e200857
      publisher: American Society for Clinical Investigation

The parts are already in the page bundle's own cite.bib, so this reads them
back out rather than trying to unpick the display string. Pages whose bib has
nothing beyond the journal still get the structured shape with just a name,
which is enough to silence the warning and lets the volume arrive later
without another migration.

It also moves a top-level `doi` under `hugoblox.ids`, which the importer
writes flat and the theme deprecates.

    python scripts/structure_publications.py [--check]

--check reports what would change and exits 1 if anything would, for CI.
Runs as part of `pixi run import-pubs`, after the author normalisation, since
`academic import` regenerates both shapes every time it runs.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBS = ROOT / "content" / "publications"

# journal -> name is the display string; the rest map straight through.
BIB_TO_PUB = {"journal": "name", "volume": "volume", "number": "issue",
              "pages": "pages", "publisher": "publisher"}


def bib_fields(text: str) -> dict[str, str]:
    """Pull top-level `key = value` pairs out of a single BibTeX entry.

    Values span lines and come brace-wrapped, quote-wrapped or bare, so this
    tracks the delimiter rather than matching a line at a time.
    """
    body = text[text.index("{") + 1:] if "{" in text else text
    out, i, n = {}, 0, len(body)
    while i < n:
        m = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*").search(body, i)
        if not m:
            break
        key, i = m.group(1).lower(), m.end()
        if i >= n:
            break
        if body[i] in "{\"":
            close, depth, i = ("}" if body[i] == "{" else "\""), 1, i + 1
            start = i
            while i < n and depth:
                if body[i] == "\\":
                    i += 2
                    continue
                if close == "}" and body[i] == "{":
                    depth += 1
                elif body[i] == close:
                    depth -= 1
                i += 1
            value = body[start:i - 1]
        else:
            start = i
            while i < n and body[i] not in ",\n":
                i += 1
            value = body[start:i]
        out[key] = re.sub(r"\s+", " ", value).strip().strip(",").strip()
    return out


def structured(page: pathlib.Path, flat: str) -> dict[str, str] | None:
    """Build the structured mapping for one page, or None to leave it alone."""
    name = flat.strip().strip("'\"").strip()
    name = re.sub(r"^\*(.*)\*$", r"\1", name).strip()
    if not name:
        return None

    bib = page.parent / "cite.bib"
    fields = bib_fields(bib.read_text(encoding="utf-8")) if bib.exists() else {}

    pub: dict[str, str] = {}
    for bib_key, pub_key in BIB_TO_PUB.items():
        value = fields.get(bib_key, "")
        # The bib's journal is the display name only when the page agrees with
        # it; a hand-edited front matter wins.
        if pub_key == "name":
            pub["name"] = name
        elif value:
            # BibTeX writes a page range as `742--753`; that is a typographic
            # en dash, not two hyphens, and the theme prints it verbatim.
            if pub_key == "pages":
                value = re.sub(r"-{2,}", "\u2013", value)
            pub[pub_key] = value
    return pub


def rewrite(text: str, page: pathlib.Path) -> str | None:
    """Return the rewritten file, or None if nothing needs doing."""
    changed = False

    flat = re.search(r"^publication: (?!\s*$)(.+)$", text, re.M)
    if flat:
        pub = structured(page, flat.group(1))
        if pub:
            block = yaml.safe_dump({"publication": pub}, sort_keys=False,
                                   allow_unicode=True, default_flow_style=False,
                                   width=10**6)
            text = text[:flat.start()] + block.rstrip("\n") + text[flat.end():]
            changed = True

    # The importer writes `doi` at the top level; the theme wants it nested,
    # which is where every hand-checked page already has it.
    doi = re.search(r"^doi: (.+)$", text, re.M)
    if doi and "hugoblox:" not in text:
        value = doi.group(1).strip()
        text = text[:doi.start()] + text[doi.end() + 1:]
        head, sep, rest = text.rpartition("\n---")
        text = f"{head.rstrip()}\nhugoblox:\n  ids:\n    doi: {value}\n{sep}{rest}"
        changed = True
    elif doi:
        text = text[:doi.start()] + text[doi.end() + 1:]
        changed = True

    return text if changed else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report changes without writing; exit 1 if any")
    args = ap.parse_args()

    changed = []
    for f in sorted(PUBS.glob("*/index.md")):
        new = rewrite(f.read_text(encoding="utf-8"), f)
        if new is None:
            continue
        changed.append(f.parent.name)
        if not args.check:
            f.write_text(new, encoding="utf-8")

    for name in changed:
        print(f"  {name}")
    verb = "would restructure" if args.check else "restructured"
    print(f"{verb} {len(changed)} publication(s)")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
