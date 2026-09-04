#!/usr/bin/env python3
"""Append newly published lab papers to publications.bib.

Queries PubMed for the lab's authors, skips anything already in the file by
PMID or DOI, and appends BibTeX entries in the style the file already uses.
Writes nothing and exits 0 when there is nothing new, so the calling workflow
simply finds a clean tree and opens no pull request.

Usage:
    python scripts/find_new_publications.py [--bib publications.bib] [--days 0]

--days 0 searches the whole record; the nightly job uses a window instead so a
single run cannot flood the file after a long gap.

Set NCBI_API_KEY to raise the E-utilities rate limit. NCBI asks for a contact
address, which comes from NCBI_EMAIL.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# Authors whose papers belong on the site. Keep in step with the lab roster.
AUTHOR_TERMS = ['"Hesselberth JR"[Author]']

TOOL = "hesselberthlab-site"


def _get(url: str, params: dict) -> bytes:
    params = {k: v for k, v in params.items() if v}
    params.setdefault("tool", TOOL)
    if os.environ.get("NCBI_EMAIL"):
        params.setdefault("email", os.environ["NCBI_EMAIL"])
    if os.environ.get("NCBI_API_KEY"):
        params.setdefault("api_key", os.environ["NCBI_API_KEY"])
    full = f"{url}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(full, timeout=60) as r:
                return r.read()
        except Exception as exc:  # noqa: BLE001 - retry any transport error
            if attempt == 3:
                raise
            print(f"  retrying after {exc}", file=sys.stderr)
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def norm_title(s: str) -> str:
    """Collapse to letters and digits so wrapping and punctuation do not matter."""
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def existing_ids(bib: str) -> tuple[set[str], set[str], set[str], set[str]]:
    """Return (pmids, dois, keys, normalised titles) already in the file.

    Titles matter because the older hand-curated entries predate consistent
    pmid fields, so PMID and DOI alone let a paper in twice.
    """
    pmids = set(re.findall(r'pmid\s*=\s*"(\d+)"', bib))
    dois = {d.lower() for d in re.findall(r'doi\s*=\s*"([^"]+)"', bib)}
    keys = set(re.findall(r"^@\w+\{([^,]+),", bib, re.M))
    titles = {
        norm_title(re.sub(r"\s+", " ", m))
        for m in re.findall(r'title\s*=\s*"([^"]*)"', bib, re.S)
    }
    return pmids, dois, keys, titles


def search(days: int) -> list[str]:
    term = " OR ".join(AUTHOR_TERMS)
    data = _get(
        f"{EUTILS}/esearch.fcgi",
        {
            "db": "pubmed",
            "term": term,
            "retmax": "500",
            "retmode": "json",
            "datetype": "edat",
            "reldate": str(days) if days else None,
        },
    )
    return json.loads(data)["esearchresult"].get("idlist", [])


def _text(node, path: str) -> str:
    found = node.find(path)
    return "".join(found.itertext()).strip() if found is not None else ""


def fetch(pmids: list[str]) -> list[dict]:
    out: list[dict] = []
    for i in range(0, len(pmids), 100):
        chunk = pmids[i : i + 100]
        xml = _get(
            f"{EUTILS}/efetch.fcgi",
            {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"},
        )
        root = ET.fromstring(xml)
        for art in root.iter("PubmedArticle"):
            cit = art.find(".//MedlineCitation")
            a = cit.find(".//Article")
            if a is None:
                continue
            authors = []
            for au in a.findall(".//Author"):
                last, initials = _text(au, "LastName"), _text(au, "Initials")
                if last:
                    authors.append(f"{last}, {' '.join(initials)}".strip().rstrip(","))
            ids = {
                el.get("IdType"): (el.text or "").strip()
                for el in art.findall(".//ArticleId")
            }
            pages = _text(a, ".//Pagination/MedlinePgn")
            out.append(
                {
                    "pmid": _text(cit, "PMID"),
                    "doi": ids.get("doi", ""),
                    "title": re.sub(r"\s+", " ", _text(a, "ArticleTitle")).rstrip("."),
                    "authors": authors,
                    "journal": _text(a, ".//Journal/ISOAbbreviation")
                    or _text(a, ".//Journal/Title"),
                    "year": _text(a, ".//JournalIssue/PubDate/Year")
                    or _text(a, ".//ArticleDate/Year"),
                    "volume": _text(a, ".//JournalIssue/Volume"),
                    "number": _text(a, ".//JournalIssue/Issue"),
                    "pages": pages.replace("-", "--") if pages else "",
                    "abstract": re.sub(
                        r"\s+", " ", _text(a, ".//Abstract")
                    ),
                }
            )
        time.sleep(0.4)
    return out


def cite_key(rec: dict, taken: set[str]) -> str:
    """Paperpile-ish key: LastnameYear-xx, stable per PMID."""
    last = (rec["authors"][0].split(",")[0] if rec["authors"] else "Anon")
    last = re.sub(r"[^A-Za-z]", "", last) or "Anon"
    year = rec["year"] or "undated"
    alpha = "abcdefghijklmnopqrstuvwxyz"
    n = int(rec["pmid"] or 0)
    suffix = alpha[n % 26] + alpha[(n // 26) % 26]
    key = f"{last}{year}-{suffix}"
    while key in taken:
        suffix = alpha[(alpha.index(suffix[0]) + 1) % 26] + suffix[1]
        key = f"{last}{year}-{suffix}"
    taken.add(key)
    return key


def wrap(field: str, value: str, width: int = 74) -> str:
    """Match the hanging-indent layout of the existing entries."""
    pad = " " * 14
    words, lines, cur = value.split(), [], ""
    for w in words:
        if cur and len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    body = f"\n{pad}".join(lines)
    return f'  {field:<8} = "{body}"'


def to_bibtex(rec: dict, key: str) -> str:
    lines = [f"@ARTICLE{{{key}"]
    lines.append(wrap("title", rec["title"]))
    if rec["authors"]:
        lines.append(wrap("author", " and ".join(rec["authors"])))
    if rec["abstract"]:
        lines.append(wrap("abstract", rec["abstract"]))
    for field in ("journal", "volume", "number", "pages", "year", "doi", "pmid"):
        val = rec.get(field, "")
        if not val:
            continue
        if field in ("volume", "number", "year"):
            lines.append(f"  {field:<8} =  {val}")
        else:
            lines.append(wrap(field, val))
    return ",\n".join(lines) + "\n}\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default="publications.bib")
    ap.add_argument("--days", type=int, default=0)
    args = ap.parse_args()

    bib_path = args.bib
    with open(bib_path, encoding="utf-8") as fh:
        bib = fh.read()
    pmids, dois, keys, titles = existing_ids(bib)
    print(f"{len(pmids)} PMIDs already in {bib_path}")

    found = search(args.days)
    print(f"PubMed returned {len(found)} records")
    new_ids = [p for p in found if p not in pmids]
    if not new_ids:
        print("Nothing new.")
        return 0

    records = fetch(new_ids)
    additions = []
    for rec in records:
        if rec["doi"] and rec["doi"].lower() in dois:
            continue
        if not rec["title"] or norm_title(rec["title"]) in titles:
            continue
        additions.append(to_bibtex(rec, cite_key(rec, keys)))
        print(f"  + {rec['pmid']}  {rec['title'][:70]}")

    if not additions:
        print("Nothing new after DOI and title de-duplication.")
        return 0

    with open(bib_path, "a", encoding="utf-8") as fh:
        fh.write("\n\n" + "\n\n".join(a.rstrip() for a in additions) + "\n")
    print(f"Appended {len(additions)} entries to {bib_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
