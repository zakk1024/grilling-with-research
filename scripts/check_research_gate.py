#!/usr/bin/env python3
"""Research gate checker for grilling-with-research.

Usage: python3 check_research_gate.py <research_dir>

Checks (mirrors SKILL.md Step 1 — this script is that step's completion criterion):
  R1. every entry has all three fields: URL, tier, argument (non-empty).
  R2. mandatory coverage channels — GitHub (repo/issue/discussion), HN, Reddit —
      each carry >=1 source OR are covered by a searched-and-absent entry.
  R3. five-category coverage report (papers/arXiv, official docs/specs, code,
      community first-person, searched-and-absent); any category at zero -> gap.
  R4. an entry labelled 未讀全文 may not carry tier primary.

Exit 0 = pass. Exit 1 = violations listed on stdout.
"""
import re
import sys
from pathlib import Path

FIELD_URL = re.compile(r"^\s*[-*]\s*\*{0,2}URL\*{0,2}\s*[:：]\s*(\S+)", re.I | re.M)
FIELD_TIER = re.compile(r"^\s*[-*]\s*\*{0,2}tier\*{0,2}\s*[:：]\s*(\S.*)$", re.I | re.M)
FIELD_ARG = re.compile(r"^\s*[-*]\s*\*{0,2}(?:argument|論證)\*{0,2}\s*[:：]\s*(\S.*)$", re.I | re.M)
FIELD_CAT = re.compile(r"^\s*[-*]\s*\*{0,2}(?:cat|類別|分类)\*{0,2}\s*[:：]\s*(\S.*)$", re.I | re.M)
UNREAD = re.compile(r"未讀全文")
SAA_HEADING = re.compile(r"searched[- ]and[- ]absent", re.I)

CHANNELS = {
    "github": re.compile(r"github\.com", re.I),
    "hn": re.compile(r"news\.ycombinator\.com", re.I),
    "reddit": re.compile(r"reddit\.com", re.I),
}
CATEGORIES = {
    "papers (arXiv etc.)": re.compile(r"arxiv\.org|papers?\b", re.I),
    "official docs/specs": re.compile(
        r"readthedocs|docs?\.[a-z]+\.(io|ai|com)|agentskills\.io|jina\.ai|pricing|developers\.facebook|platform\.|\.dev\b|playwright\.dev", re.I),
    "code itself": re.compile(r"github\.com/[^/]+/[^/]+/(blob|commit|tree)/|\bcode\b", re.I),
    "community first-person": re.compile(
        r"github\.com/[^/]+/[^/]+/(issues|discussions)/|news\.ycombinator\.com|reddit\.com|threads\.com|x\.com/twitter\.com|community", re.I),
}


def parse_entries(text):
    """Split into (heading, body) entry blocks; entries = blocks with a URL field."""
    entries = []
    blocks = re.split(r"^#{2,3} ", text, flags=re.M)
    for b in blocks[1:]:
        heading, _, body = b.partition("\n")
        url = FIELD_URL.search(body)
        tier = FIELD_TIER.search(body)
        arg = FIELD_ARG.search(body)
        cat = FIELD_CAT.search(body)
        if url or tier or arg or cat:
            entries.append({"heading": heading.strip(), "url": url.group(1) if url else None,
                            "tier": (tier.group(1) if tier else "").strip().lower(),
                            "arg": (arg.group(1) if arg else "").strip(),
                            "cat": (cat.group(1) if cat else "").strip().lower(),
                            "unread": bool(UNREAD.search(body + heading)),
                            "saa": bool(SAA_HEADING.search(heading))})
    # searched-and-absent entries may not have a URL — catch heading-only blocks
    for b in blocks[1:]:
        heading, _, body = b.partition("\n")
        if SAA_HEADING.search(heading) and not any(e["heading"] == heading.strip() for e in entries):
            entries.append({"heading": heading.strip(), "url": None, "tier": "searched-and-absent",
                            "arg": body.strip(), "cat": "", "unread": False, "saa": True})
    return entries


CAT_KEYS = {"paper": "papers (arXiv etc.)", "papers": "papers (arXiv etc.)", "arxiv": "papers (arXiv etc.)",
            "docs": "official docs/specs", "official": "official docs/specs", "official docs": "official docs/specs",
            "docs/specs": "official docs/specs", "spec": "official docs/specs", "specs": "official docs/specs",
            "code": "code itself", "the code": "code itself", "code itself": "code itself",
            "community": "community first-person", "community first-person": "community first-person"}


def main():
    root = Path(sys.argv[1])
    files = sorted(root.glob("*.md"))
    if not files:
        print(f"GATE FAIL: no research files in {root}")
        return 1
    entries, violations = [], []
    for f in files:
        for e in parse_entries(f.read_text(encoding="utf-8")):
            e["file"] = f.name
            entries.append(e)
    n = len(entries)
    # R1: three fields
    for e in entries:
        if e["saa"]:
            if not e["arg"]:
                violations.append(f"R1 {e['file']}:{e['heading'][:40]} — searched-and-absent entry missing query/where/result")
            continue
        missing = [f for f in ("url", "tier", "arg") if not e[f]]
        if missing:
            violations.append(f"R1 {e['file']}:{e['heading'][:40]} — missing field(s): {','.join(missing)}")
    # R4: 未讀全文 cannot be primary
    for e in entries:
        if e["unread"] and e["tier"].startswith("primary"):
            violations.append(f"R4 {e['file']}:{e['heading'][:40]} — labelled 未讀全文 but tier primary")
    # R2: mandatory channels
    saa_text = " ".join(e["heading"] + " " + e["arg"] for e in entries if e["saa"])
    for name, pat in CHANNELS.items():
        hit = any(pat.search(e["url"] or "") for e in entries)
        covered = hit or pat.search(saa_text) or (name == "github" and re.search(r"github", saa_text, re.I))
        if not covered:
            violations.append(f"R2 channel '{name}' — zero sources and no searched-and-absent entry")
    # R3: five-category report
    print(f"entries total: {n}")
    for name, pat in CATEGORIES.items():
        count = sum(1 for e in entries if e["url"] and pat.search(e["url"]))
        saa_cover = any(e["saa"] and pat.search(e["heading"] + " " + e["arg"]) for e in entries)
        status = "OK" if (count or saa_cover) else "GAP"
        if status == "GAP":
            violations.append(f"R3 category '{name}' — zero coverage; search it or file a searched-and-absent entry")
        print(f"  {status:4} {name}: {count} sources" + (" (via searched-and-absent)" if saa_cover and not count else ""))
    saa_n = sum(1 for e in entries if e["saa"])
    print(f"  {'OK' if saa_n else 'GAP':4} searched-and-absent entries: {saa_n}")
    if not saa_n:
        violations.append("R3 no searched-and-absent entries at all — absences must be recorded, not assumed")
    if violations:
        print("\nVIOLATIONS:")
        for v in violations:
            print(" -", v)
        print("\nGATE: FAIL")
        return 1
    print("\nGATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
