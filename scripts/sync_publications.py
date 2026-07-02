#!/usr/bin/env python3
"""
Sync peer-reviewed publications from an ORCID profile into publications.json.

- Reads the existing publications.json (your curated us / nepal / other lists).
- Fetches the public work list from the ORCID API.
- Adds any publication NOT already present (matched by DOI or by title) to the
  "other" bucket with empty tags, for you to categorise and tag.
- NEVER edits or removes anything already in the file, so your hand-tuned
  titles, journals, and tags are preserved.

Usage:
    ORCID_ID=0000-0002-1091-328X python3 scripts/sync_publications.py
    python3 scripts/sync_publications.py --orcid 0000-0002-1091-328X

Exit code 0 always; the calling workflow decides what to do with the git diff.
"""

import argparse
import datetime
import difflib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBS_PATH = os.path.join(ROOT, "publications.json")

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+", re.IGNORECASE)


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


def norm_doi(d):
    return (d or "").strip().lower().rstrip(".")


def load_existing():
    with open(PUBS_PATH, encoding="utf-8") as f:
        return json.load(f)


def known_keys(data):
    """Return the DOIs and the normalised titles already present in the file."""
    dois, titles = set(), []
    for bucket in ("us", "nepal", "other"):
        for pub in data.get(bucket, []):
            titles.append(norm_title(pub.get("title")))
            for m in DOI_RE.findall(pub.get("link", "")):
                dois.add(norm_doi(m))
    return dois, titles


def common_prefix_len(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def is_duplicate(pub_title, pub_doi, known_dois, known_titles):
    """
    True if this publication already exists. ORCID often stores the full canonical
    title while the curated list uses a shorter form, so exact matching misses them.
    We therefore also treat it as a match when the two normalised titles share a
    long common prefix (>=60% of the shorter one) or are highly similar overall.
    """
    if pub_doi and norm_doi(pub_doi) in known_dois:
        return True
    nt = norm_title(pub_title)
    if not nt:
        return False
    for kt in known_titles:
        if not kt:
            continue
        if nt == kt:
            return True
        shorter = min(len(nt), len(kt))
        cpl = common_prefix_len(nt, kt)
        if cpl >= 25 and shorter and cpl / shorter >= 0.60:
            return True
        if difflib.SequenceMatcher(None, nt, kt).ratio() >= 0.85:
            return True
    return False


def fetch_orcid_works(orcid):
    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                               "User-Agent": "mukeshadhikari.com-pub-sync"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def parse_work(summary):
    """Extract a normalised publication dict from one ORCID work-summary."""
    title = (((summary.get("title") or {}).get("title") or {}).get("value") or "").strip()
    if not title:
        return None

    journal = ((summary.get("journal-title") or {}) or {}).get("value") or ""

    year = ""
    pub_date = summary.get("publication-date") or {}
    if pub_date and pub_date.get("year"):
        year = (pub_date["year"] or {}).get("value") or ""

    doi, link = "", ""
    ext = ((summary.get("external-ids") or {}).get("external-id")) or []
    for e in ext:
        if (e.get("external-id-type") or "").lower() == "doi":
            doi = norm_doi(e.get("external-id-value"))
            link = ((e.get("external-id-url") or {}) or {}).get("value") or ""
            break
    if not link and doi:
        link = f"https://doi.org/{doi}"
    if not link:
        link = ((summary.get("url") or {}) or {}).get("value") or ""

    return {"title": title, "journal": journal.strip(), "year": str(year),
            "link": link, "doi": doi, "tags": []}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orcid", default=os.environ.get("ORCID_ID", "").strip())
    args = ap.parse_args()
    if not args.orcid:
        sys.exit("No ORCID iD. Set ORCID_ID env var or pass --orcid 0000-0000-0000-0000")

    data = load_existing()
    known_dois, known_titles = known_keys(data)

    try:
        payload = fetch_orcid_works(args.orcid)
    except Exception as e:  # network / API hiccup: leave the file untouched
        print(f"ORCID fetch failed ({e}); no changes made.", file=sys.stderr)
        return

    added = []
    for group in payload.get("group", []):
        summaries = group.get("work-summary") or []
        if not summaries:
            continue
        pub = parse_work(summaries[0])
        if not pub:
            continue
        if is_duplicate(pub["title"], pub["doi"], known_dois, known_titles):
            continue
        # New publication — record its keys so we don't add near-duplicates twice.
        known_titles.append(norm_title(pub["title"]))
        if pub["doi"]:
            known_dois.add(norm_doi(pub["doi"]))
        # Drop the internal doi field from the stored record (link carries it).
        pub.pop("doi", None)
        data.setdefault("other", []).append(pub)
        added.append(pub["title"])

    if not added:
        print("Up to date — no new publications found.")
        return

    data["updated"] = datetime.date.today().isoformat()
    with open(PUBS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Added {len(added)} new publication(s) to the 'other' bucket:")
    for t in added:
        print(f"  - {t}")


if __name__ == "__main__":
    main()
