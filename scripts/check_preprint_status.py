#!/usr/bin/env python3
"""Flag publications.bib preprint entries whose paper has since been published.

find_new_publications.py adds genuinely new papers but never revisits old
ones, so an @UNPUBLISHED bioRxiv/Research Square entry silently goes stale
once the paper clears peer review elsewhere -- its title, journal, and DOI
never change to match, and its PMID here (if any) is often just PubMed's own
index of the *preprint*, not the published article. See the Sheridan/
Zarrella/Sottnik/Stemm-Wolf fixes for what that looks like once it has
happened, and the Andersen2025-yl/Andersen2026-gl case for what happens when
find_new_publications.py adds the published paper as a new entry without
realizing an existing @UNPUBLISHED entry is the same paper -- the stale
preprint entry survives as a duplicate.

For every @UNPUBLISHED entry this tries three signals, in order:

  1. PubMed's own forward link. Once a preprint is peer reviewed, PubMed
     usually adds a `CommentsCorrections RefType="UpdateIn"` element to the
     *preprint's own* record naming the published PMID/journal/DOI -- exact,
     not fuzzy, and it covers Research Square and medRxiv as well as
     bioRxiv. The entry's own `pmid` field is used if present; otherwise the
     preprint's PMID is looked up by DOI, since most entries here predate
     that field being added.
  2. bioRxiv's own API, which links a bioRxiv DOI straight to its published
     DOI once the two are connected via Crossref. Only fires if (1) found
     nothing -- e.g. the preprint was never indexed in PubMed at all.
  3. A fuzzy match against every PubMed record already known for the lab's
     author search (the same query find_new_publications.py uses, run with
     the equivalent of --days 0), for preprints PubMed has no record of
     whatsoever. Matches on title word overlap plus shared author surnames,
     skipping any candidate itself hosted on a preprint server. This is the
     only probabilistic signal of the three, and the last resort.

This only reports; it never edits publications.bib. Turning a flagged entry
into the real fix means picking a new citekey (published year, same
lastname+suffix scheme as find_new_publications.cite_key), rewriting the
entry with the published byline/abstract/venue, deleting the old preprint's
content/publications/<slug> bundle, and running `pixi run import-pubs` --
and, per the Andersen case, checking whether find_new_publications.py has
already added the published version separately, in which case the fix is to
delete the stale entry rather than rewrite it. Enough judgment calls that
this is left to a human or an agent, not this script.

Usage:
    python scripts/check_preprint_status.py [--bib publications.bib]
                                             [--format text|markdown|json]
                                             [--min-similarity 0.55]
                                             [--min-author-overlap 2]

Exits 1 if anything is flagged (0 if the bib is clean), so CI can act on it.
Set NCBI_API_KEY / NCBI_EMAIL as find_new_publications.py does to raise the
E-utilities rate limit.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from find_new_publications import EUTILS, _get, fetch, search  # noqa: E402

BIORXIV_API = "https://api.biorxiv.org/details/biorxiv/{doi}"

# Substrings (lowercase) that mark a candidate PubMed record as itself a
# preprint, not a peer-reviewed publication -- never treat these as "the
# paper got published."
PREPRINT_MARKERS = (
    "biorxiv",
    "medrxiv",
    "research square",
    "ssrn",
    "authorea",
    "preprints.org",
    "arxiv",
)

STOPWORDS = {
    "a", "an", "the", "of", "in", "on", "for", "and", "or", "to", "is",
    "are", "by", "with", "from", "as", "at", "that", "this", "via", "using",
    "underlies", "underlie",
}


def norm_words(title: str) -> set[str]:
    words = re.sub(r"[^a-z0-9\s]", " ", title.lower()).split()
    return {w for w in words if w not in STOPWORDS and len(w) > 2}


def title_similarity(a: str, b: str) -> float:
    """Containment coefficient: robust to one title being a superset of the
    other, which is exactly what happens when a subtitle gets added/dropped
    between preprint and publication."""
    wa, wb = norm_words(a), norm_words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


def last_names_from_author_field(author_field: str) -> set[str]:
    names = set()
    for person in author_field.split(" and "):
        person = person.strip()
        if not person:
            continue
        last = person.split(",")[0].strip() if "," in person else person.split()[-1]
        last = re.sub(r"[^A-Za-z]", "", last)
        if last:
            names.add(last.lower())
    return names


def get_field(block: str, name: str) -> str:
    """One level of brace nesting (e.g. {DNA} inside a braced field) or a
    plain double-quoted value -- the two styles this file actually uses."""
    m = re.search(rf'{name}\s*=\s*\{{((?:[^{{}}]|\{{[^{{}}]*\}})*)\}}', block, re.S)
    if not m:
        m = re.search(rf'{name}\s*=\s*"([^"]*)"', block, re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def parse_unpublished(bib: str) -> list[dict]:
    entries = []
    for raw in re.split(r"\n(?=@)", bib):
        m = re.match(r"@UNPUBLISHED\{([^,]+),", raw)
        if not m:
            continue
        entries.append(
            {
                "key": m.group(1),
                "title": get_field(raw, "title"),
                "author": get_field(raw, "author"),
                "doi": get_field(raw, "doi"),
                "pmid": get_field(raw, "pmid"),
            }
        )
    return entries


def pmid_for_doi(doi: str) -> str | None:
    data = _get(f"{EUTILS}/esearch.fcgi", {"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"})
    idlist = json.loads(data)["esearchresult"].get("idlist", [])
    return idlist[0] if idlist else None


def update_in(pmid: str) -> dict | None:
    """PubMed's forward link from a preprint's own record to where it was
    published, if PubMed has recorded one."""
    xml = _get(f"{EUTILS}/efetch.fcgi", {"db": "pubmed", "id": pmid, "retmode": "xml"})
    root = ET.fromstring(xml)
    for art in root.iter("PubmedArticle"):
        cit = art.find(".//MedlineCitation")
        if cit is None or cit.findtext("PMID") != pmid:
            continue
        for cc in cit.findall(".//CommentsCorrectionsList/CommentsCorrections"):
            if cc.get("RefType") != "UpdateIn":
                continue
            source = (cc.findtext("RefSource") or "").strip()
            target_pmid = (cc.findtext("PMID") or "").strip()
            doi_match = re.search(r"10\.\S+?(?=\.?\s*$|\.?\s)", source)
            return {
                "pmid": target_pmid,
                "citation": source,
                "doi": doi_match.group(0).rstrip(".") if doi_match else "",
            }
    return None


def biorxiv_published_doi(doi: str) -> str | None:
    url = BIORXIV_API.format(doi=doi)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"  bioRxiv API error for {doi}: {exc}", file=sys.stderr)
        return None
    collection = data.get("collection") or []
    if not collection:
        return None
    published = collection[-1].get("published")
    return published if published and published != "NA" else None


def find_pubmed_match(
    entry: dict, records: list[dict], min_sim: float, min_overlap: int
) -> tuple[float, dict] | None:
    entry_names = last_names_from_author_field(entry["author"])
    best: tuple[float, dict] | None = None
    for rec in records:
        if entry["pmid"] and rec["pmid"] == entry["pmid"]:
            continue  # PubMed's own index of this same preprint, not a publication
        if entry["doi"] and rec["doi"].lower() == entry["doi"].lower():
            continue
        journal_l = rec["journal"].lower()
        if any(marker in journal_l for marker in PREPRINT_MARKERS):
            continue
        sim = title_similarity(entry["title"], rec["title"])
        if sim < min_sim:
            continue
        rec_names = {a.split(",")[0].strip().lower() for a in rec["authors"] if a}
        if len(entry_names & rec_names) < min_overlap:
            continue
        if not best or sim > best[0]:
            best = (sim, rec)
    return best


def audit(bib_path: str, min_sim: float, min_overlap: int) -> list[dict]:
    with open(bib_path, encoding="utf-8") as fh:
        bib = fh.read()

    entries = parse_unpublished(bib)
    print(f"{len(entries)} @UNPUBLISHED entries in {bib_path}", file=sys.stderr)

    flagged = []
    needs_fallback = []

    for entry in entries:
        result: dict = {"key": entry["key"], "title": entry["title"]}

        preprint_pmid = entry["pmid"] or (pmid_for_doi(entry["doi"]) if entry["doi"] else None)
        if preprint_pmid:
            upd = update_in(preprint_pmid)
            if upd:
                result["pubmed_update_in"] = {**upd, "preprint_pmid": preprint_pmid}
                flagged.append(result)
                continue

        if entry["doi"].startswith("10.1101/"):
            pub_doi = biorxiv_published_doi(entry["doi"])
            if pub_doi:
                result["biorxiv_published_doi"] = pub_doi
                flagged.append(result)
                continue

        needs_fallback.append((entry, result))

    if needs_fallback:
        pmids = search(0)
        print(f"{len(pmids)} PubMed records for the lab's author search (fallback pass)", file=sys.stderr)
        records = fetch(pmids)
        for entry, result in needs_fallback:
            match = find_pubmed_match(entry, records, min_sim, min_overlap)
            if match:
                sim, rec = match
                result["pubmed_fuzzy_match"] = {
                    "similarity": round(sim, 2),
                    "pmid": rec["pmid"],
                    "doi": rec["doi"],
                    "title": rec["title"],
                    "journal": rec["journal"],
                }
                flagged.append(result)

    return flagged


def render_text(flagged: list[dict]) -> str:
    if not flagged:
        return "No stale preprint entries found.\n"
    lines = [f"{len(flagged)} preprint entr{'y' if len(flagged) == 1 else 'ies'} may now be published:\n"]
    for item in flagged:
        lines.append(f"* {item['key']}  \"{item['title'][:80]}\"")
        if "pubmed_update_in" in item:
            u = item["pubmed_update_in"]
            lines.append(f"    PubMed's own preprint record (PMID {u['preprint_pmid']}) says it published as:")
            lines.append(f"      PMID {u['pmid']}: {u['citation']}")
        if "biorxiv_published_doi" in item:
            lines.append(f"    bioRxiv reports it published as: {item['biorxiv_published_doi']}")
        if "pubmed_fuzzy_match" in item:
            m = item["pubmed_fuzzy_match"]
            lines.append(
                f"    Possible PubMed match (title similarity {m['similarity']}): "
                f"PMID {m['pmid']}, {m['journal']}, doi:{m['doi']}"
            )
            lines.append(f"      \"{m['title'][:90]}\"")
        lines.append("")
    return "\n".join(lines)


def render_markdown(flagged: list[dict]) -> str:
    if not flagged:
        return "No stale preprint entries found in `publications.bib`.\n"
    lines = [
        f"Found {len(flagged)} `@UNPUBLISHED` entr{'y' if len(flagged) == 1 else 'ies'} in "
        "`publications.bib` that may now have a published, peer-reviewed version:\n",
    ]
    for item in flagged:
        lines.append(f"### `{item['key']}`")
        lines.append(f"> {item['title']}\n")
        if "pubmed_update_in" in item:
            u = item["pubmed_update_in"]
            lines.append(
                f"- PubMed's own record for this preprint "
                f"([PMID {u['preprint_pmid']}](https://pubmed.ncbi.nlm.nih.gov/{u['preprint_pmid']}/)) "
                f"says it published as [PMID {u['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{u['pmid']}/): "
                f"{u['citation']}"
            )
        if "biorxiv_published_doi" in item:
            lines.append(f"- bioRxiv reports this published as **{item['biorxiv_published_doi']}**")
        if "pubmed_fuzzy_match" in item:
            m = item["pubmed_fuzzy_match"]
            lines.append(
                f"- Possible PubMed match (title similarity {m['similarity']}): "
                f"[PMID {m['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{m['pmid']}/), "
                f"*{m['journal']}*, doi:{m['doi']}"
            )
            lines.append(f"  > {m['title']}")
        lines.append("")
    lines.append(
        "Fixing one of these means checking whether `find_new_publications.py` has already "
        "added the published version as a separate entry (delete the stale one if so), or "
        "otherwise updating the entry in place with the published byline/abstract/venue, "
        "renaming the citekey to the publication year, deleting the old "
        "`content/publications/<slug>` bundle, and running `pixi run import-pubs` -- see the "
        "Sheridan/Zarrella/Sottnik/Stemm-Wolf fixes for the pattern. This check does not edit "
        "`publications.bib` itself."
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default="publications.bib")
    ap.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    ap.add_argument("--min-similarity", type=float, default=0.55)
    ap.add_argument("--min-author-overlap", type=int, default=2)
    args = ap.parse_args()

    flagged = audit(args.bib, args.min_similarity, args.min_author_overlap)

    if args.format == "json":
        print(json.dumps(flagged, indent=2))
    elif args.format == "markdown":
        print(render_markdown(flagged))
    else:
        print(render_text(flagged))

    return 1 if flagged else 0


if __name__ == "__main__":
    raise SystemExit(main())
