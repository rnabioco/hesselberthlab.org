#!/usr/bin/env python3
"""Point publication author entries at lab member profiles.

BibTeX carries display strings, so one person arrives under several spellings —
"Jay R Hesselberth", "J R Hesselberth", "J Hesselberth". Hugo turns each into
its own taxonomy term, so a lab member's page lists only the papers that happen
to use one spelling: before this script Jay's page showed 8 of his 86 papers
and Erika Lasda's showed none of her 3.

Rewriting a lab member's entry to their `data/authors/<slug>.yaml` slug makes
HugoBlox resolve the profile: the byline renders the display name and links to
the right page, and every paper lands there. Authors with no profile are left
exactly as they are.

`academic import` regenerates content/publications/ from the .bib and would
undo this, so it runs as part of `pixi run import-pubs`, and in the nightly
publications workflow, immediately after the import.

    python scripts/normalize_authors.py [--check]

--check reports what would change and exits 1 if anything would, for CI.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUTHORS = ROOT / "data" / "authors"
PUBS = ROOT / "content" / "publications"


def roster() -> dict[str, tuple[str, str]]:
    """slug -> (given, family) for everyone with a profile."""
    out = {}
    for f in sorted(AUTHORS.glob("*.yaml")):
        name = (yaml.safe_load(f.read_text()) or {}).get("name") or {}
        given, family = name.get("given"), name.get("family")
        if given and family:
            out[f.stem] = (given, family)
    return out


def match(author: str, people: dict[str, tuple[str, str]]) -> str | None:
    """Map one author string to a profile slug, or None.

    Requires the family name to match and the given name to be either the full
    first name or its initial. Family name alone is not enough: the roster has
    a Li, and the publications also carry Xueni Li, Yize Li and Frances S Li.
    """
    parts = author.replace(".", "").split()
    if len(parts) < 2:
        return None
    given, family = parts[0], parts[-1]
    for slug, (rg, rf) in people.items():
        if family.lower() != rf.lower():
            continue
        if given.lower() == rg.lower() or given.lower() == rg[0].lower():
            return slug
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report changes without writing; exit 1 if any")
    args = ap.parse_args()

    people = roster()
    if not people:
        print("No profiles in data/authors/", file=sys.stderr)
        return 1

    changed, edits = 0, []
    for f in sorted(PUBS.glob("*/index.md")):
        text = f.read_text()
        head, sep, rest = text.partition("---\n")[2].partition("\n---")
        fm = yaml.safe_load(head) or {}
        authors = fm.get("authors") or []
        new = []
        touched = False
        for a in authors:
            slug = match(a, people) if isinstance(a, str) else None
            if slug and a != slug:
                edits.append((f.parent.name, a, slug))
                new.append(slug)
                touched = True
            else:
                new.append(a)
        if not touched:
            continue
        changed += 1
        if args.check:
            continue
        # rewrite only the authors block, leaving the rest of the front matter
        # byte-identical rather than round-tripping the whole file through yaml
        block = "authors:\n" + "".join(f"- {x}\n" for x in new)
        text = re.sub(r"^authors:\n(?:- .*\n)+", block, text, count=1, flags=re.M)
        f.write_text(text)

    seen = {}
    for _, was, now in edits:
        seen.setdefault((was, now), 0)
        seen[(was, now)] += 1
    for (was, now), n in sorted(seen.items(), key=lambda kv: -kv[1]):
        print(f"  {was:<26} -> {now:<20} {n:>3} paper(s)")
    verb = "would change" if args.check else "changed"
    print(f"{verb} {changed} publication(s), {len(edits)} author entries")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
