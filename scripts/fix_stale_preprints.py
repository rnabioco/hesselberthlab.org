#!/usr/bin/env python3
"""Apply the fixes check_preprint_status.py can find without human judgment.

For each flagged @UNPUBLISHED entry, one of two things can happen -- but
which one is safe to do unsupervised depends on the signal:

  * Its published PMID is already in publications.bib under a different
    entry (find_new_publications.py added it separately, as happened with
    Andersen2025-yl/Andersen2026-gl) -- the stale entry is deleted outright,
    and any `preview`/`selected` fields it had are carried over to the
    surviving entry if that entry doesn't already have them. This is safe
    even off a fuzzy title/author match, since it never invents new
    bibliographic data -- it only recognizes that a PMID already sitting in
    the file is the same paper as the preprint, which a human can verify at
    a glance in the PR diff.
  * Otherwise the entry is rewritten in place as the real @ARTICLE, in the
    same raw style find_new_publications.to_bibtex() produces for brand new
    papers (this does not attempt the fuller manual polish -- stripped
    copyright boilerplate, added ISSN/PMC/month -- of a hand-done fix; see
    the Sheridan/Zarrella/Sottnik/Stemm-Wolf commits for that). Its citekey
    is renamed to the publication year via the same scheme
    find_new_publications.cite_key() uses for new entries, and any
    `preview`/`selected` fields are carried forward. This only happens for
    an exact signal -- PubMed's own CommentsCorrections/UpdateIn link, or
    bioRxiv's publication-tracking API -- never for a bare fuzzy match,
    since fabricating a whole new entry from a probabilistic guess is not
    safe to do unsupervised.

Either way the entry's old content/publications/<slug> bundle is deleted
(matched by which bundle's cite.bib contains the old citekey, since the
slug academic generates from a key isn't worth re-deriving) -- run
`pixi run import-pubs` afterward to regenerate it under the new key.

A fuzzy match that doesn't resolve to a PMID already in the file is left
untouched; re-running check_preprint_status.py afterward will still flag it
for a human to look at (see that script's own issue-filing path).

Usage:
    python scripts/fix_stale_preprints.py [--bib publications.bib]
                                           [--summary fix-summary.md]

Exits 1 if it changed anything (0 if there was nothing to fix), so CI can
tell whether to open a PR.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_preprint_status import audit, get_field, pmid_for_doi  # noqa: E402
from find_new_publications import cite_key, fetch, to_bibtex  # noqa: E402


def split_entries(bib: str) -> list[str]:
    """Whole top-level entries, each starting at its own '@' and running up
    to (not including) the next -- lossless: "".join(split_entries(x)) == x.
    """
    return re.split(r"(?<=\n)(?=@)", bib)


def entry_key(chunk: str) -> str | None:
    m = re.match(r"@\w+\{([^,]+),", chunk)
    return m.group(1) if m else None


def add_fields(entry_text: str, extra: dict[str, str]) -> str:
    if not extra:
        return entry_text
    insert = "".join(f',\n  {k:<8} = "{v}"' for k, v in extra.items())
    new_text, n = re.subn(r"\n\}\n\Z", insert + "\n}\n", entry_text)
    return new_text if n else entry_text


def carried_fields(old_chunk: str, skip_if_present_in: str = "") -> dict[str, str]:
    extra = {}
    for field in ("preview", "selected"):
        val = get_field(old_chunk, field)
        if val and not get_field(skip_if_present_in, field):
            extra[field] = val
    return extra


def delete_content_bundle(key: str) -> str | None:
    for cite_path in glob.glob("content/publications/*/cite.bib"):
        with open(cite_path, encoding="utf-8") as fh:
            if re.search(rf"@\w+\{{{re.escape(key)},", fh.read()):
                bundle = os.path.dirname(cite_path)
                shutil.rmtree(bundle)
                return bundle
    return None


def resolve_target_pmid(item: dict) -> tuple[str | None, str]:
    """Return (pmid, signal_name). The signal matters downstream: a fuzzy
    match is only ever auto-applied when it turns out to point at a PMID
    already in the bib under another entry (see apply_fixes) -- inventing a
    brand new @ARTICLE entry from a probabilistic match is not safe to do
    unsupervised, but recognizing a duplicate that already exists is."""
    if "pubmed_update_in" in item:
        return item["pubmed_update_in"]["pmid"] or None, "pubmed_update_in"
    if "biorxiv_published_doi" in item:
        return pmid_for_doi(item["biorxiv_published_doi"]), "biorxiv_published_doi"
    if "pubmed_fuzzy_match" in item:
        return item["pubmed_fuzzy_match"]["pmid"] or None, "pubmed_fuzzy_match"
    return None, ""


def apply_fixes(bib_path: str) -> list[dict]:
    with open(bib_path, encoding="utf-8") as fh:
        bib = fh.read()

    flagged = audit(bib_path, min_sim=0.55, min_overlap=2)

    chunks = split_entries(bib)
    results = []

    for item in flagged:
        old_key = item["key"]
        index = next((i for i, c in enumerate(chunks) if entry_key(c) == old_key), None)
        if index is None:
            continue
        old_chunk = chunks[index]

        target_pmid, signal = resolve_target_pmid(item)
        if not target_pmid:
            continue  # left for check_preprint_status.py's report to surface

        existing_index = next(
            (i for i, c in enumerate(chunks) if i != index and re.search(rf'pmid\s*=\s*[{{"]{target_pmid}[}}"]', c)),
            None,
        )

        if existing_index is None and signal == "pubmed_fuzzy_match":
            # Only a probabilistic title/author match, and nothing already in
            # the bib to confirm it against -- too risky to fabricate a new
            # entry from this alone. Leave it for a human.
            continue

        if existing_index is not None:
            # find_new_publications.py already added the published version
            # separately (e.g. Andersen2025-yl/Andersen2026-gl) -- the stale
            # entry is just a duplicate now.
            surviving_key = entry_key(chunks[existing_index])
            extra = carried_fields(old_chunk, chunks[existing_index])
            if extra:
                chunks[existing_index] = add_fields(chunks[existing_index], extra)
            del chunks[index]
            results.append(
                {
                    "key": old_key,
                    "action": "removed_duplicate",
                    "surviving_key": surviving_key,
                    "pmid": target_pmid,
                }
            )
            continue

        records = fetch([target_pmid])
        if not records:
            results.append({"key": old_key, "action": "skipped", "reason": f"could not fetch PMID {target_pmid}"})
            continue
        rec = records[0]

        taken = {entry_key(c) for c in chunks if entry_key(c)}
        new_key = cite_key(rec, taken)
        new_entry = add_fields(to_bibtex(rec, new_key), carried_fields(old_chunk))
        chunks[index] = new_entry + "\n"
        results.append(
            {
                "key": old_key,
                "action": "updated",
                "new_key": new_key,
                "pmid": target_pmid,
                "journal": rec.get("journal", ""),
                "title": rec.get("title", ""),
            }
        )

    if any(r["action"] != "skipped" for r in results):
        with open(bib_path, "w", encoding="utf-8") as fh:
            fh.write("".join(chunks))
        for r in results:
            if r["action"] in ("updated", "removed_duplicate"):
                bundle = delete_content_bundle(r["key"])
                r["deleted_bundle"] = bundle

    return results


def render_summary(results: list[dict]) -> str:
    changed = [r for r in results if r["action"] != "skipped"]
    if not changed:
        return "No stale preprint entries could be fixed automatically.\n"
    lines = [f"Fixed {len(changed)} stale preprint entr{'y' if len(changed) == 1 else 'ies'} in `publications.bib`:\n"]
    for r in changed:
        if r["action"] == "updated":
            lines.append(
                f"- `{r['key']}` -> `{r['new_key']}`: published in *{r['journal']}* "
                f"([PMID {r['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/))\n"
                f"  > {r['title']}"
            )
        elif r["action"] == "removed_duplicate":
            lines.append(
                f"- `{r['key']}` removed -- already present as `{r['surviving_key']}` "
                f"(PMID {r['pmid']})"
            )
        lines.append("")
    lines.append(
        "Generated by `scripts/fix_stale_preprints.py`. Rewriting a stale entry only "
        "happens on an exact match (PubMed's own preprint-to-publication link, or "
        "bioRxiv's tracking API); removing one as a duplicate can also come from a "
        "fuzzy title/author match, since that only requires confirming a PMID already "
        "in the file, not inventing new bibliographic data. `pixi run import-pubs` has "
        "already regenerated the affected publication pages in this PR. Please skim "
        "the diff before merging."
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default="publications.bib")
    ap.add_argument("--summary", help="write a markdown summary of what changed to this path")
    args = ap.parse_args()

    results = apply_fixes(args.bib)
    changed = [r for r in results if r["action"] != "skipped"]

    print(render_summary(results))
    if args.summary:
        with open(args.summary, "w", encoding="utf-8") as fh:
            fh.write(render_summary(results))

    return 1 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
