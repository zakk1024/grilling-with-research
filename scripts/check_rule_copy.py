#!/usr/bin/env python3
"""Rule-copy sync checker: agency-agents-thinking-grill vs grilling-with-research.

The agency skill embeds a verbatim COPY of the source-of-truth rules (COPY-START
to COPY-END). If they drift, the copy is stale and dispatch must not run.

Copy rule (what counts as copied): the skeleton's Step 1 paragraph lines
(the paragraph after '## Step 1 — Research (the gate)' heading up to the next
blank line), the mandatory-coverage paragraph, the machine-format paragraph,
the searched-and-absent paragraph, and the three Research Layer paragraphs.

Usage: python3 check_rule_copy.py
Exit 0 = copy in sync. Exit 1 = drift (diff printed).
"""
import re
import sys
from pathlib import Path

SKELETON = Path("/Users/zakk/.hermes/profiles/naval/skills/grilling-with-research/SKILL.md")
AGENCY = Path("/Users/zakk/.hermes/profiles/naval/skills/agency-agents-thinking-grill/SKILL.md")


def paragraphs(path, lo=None, hi=None):
    text = path.read_text(encoding="utf-8")
    if lo:
        i = text.find(lo)
        if i < 0:
            sys.exit(f"DRIFT FAIL: marker '{lo}' not in {path.name}")
        text = text[i:]
    if hi:
        j = text.find(hi)
        if j >= 0:
            text = text[:j]
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if lo and paras:
        paras = paras[1:]  # drop the heading/anchor line itself
    return paras


def copy_lines(path):
    text = path.read_text(encoding="utf-8")
    i = text.find("COPY-START"); j = text.find("COPY-END")
    if i < 0 or j < 0:
        sys.exit("SYNC FAIL: COPY-START/COPY-END markers missing in agency SKILL.md")
    block = text[i + len("COPY-START"):j]
    lines = [l for l in block.splitlines() if l.strip() and not l.startswith("（") and "逐字副本" not in l]
    return lines


def main():
    # reverse direction: every copyable rule paragraph in the skeleton must be in the copy.
    # copyable = Step 1 paragraphs (minus Step-0 plumbing lines) + every Research Layer paragraph.
    step1 = []
    skel_text = SKELETON.read_text(encoding="utf-8")
    s1 = skel_text[skel_text.find("## Step 1 — Research"):]
    s1 = s1[:s1.find("## Step 2")]
    step1 += [p.strip() for p in re.split(r"\n\s*\n", s1)
              if p.strip() and not p.startswith("#")
              and not p.startswith("Then add") and not p.startswith("Done when:")]
    rl = skel_text[skel_text.find("## Research Layer"):]
    rl = rl[:rl.find("\n## ")]
    step1 += [p.strip() for p in re.split(r"\n\s*\n", rl) if p.strip() and not p.startswith("#")]
    copy_text = AGENCY.read_text(encoding="utf-8")
    ci = copy_text.find("COPY-START"); cj = copy_text.find("COPY-END")
    if ci < 0 or cj < 0:
        sys.exit("SYNC FAIL: COPY-START/COPY-END markers missing in agency SKILL.md")
    copy_block = copy_text[ci:cj]
    ok = True
    for p in step1:
        if p not in copy_block:
            print(f"DRIFT: skeleton rule paragraph missing from copy:\n  {p[:80]}...")
            ok = False
    # forward direction: every copy line must exist verbatim in the skeleton
    skeleton_lines = set()
    for p in step1:
        for l in p.splitlines():
            if l.strip():
                skeleton_lines.add(l.strip())
    copy_lines = [l.strip() for l in copy_block.splitlines()
                  if l.strip() and "COPY-START" not in l and "COPY-END" not in l and "逐字副本" not in l]
    for l in copy_lines:
        if l not in skeleton_lines:
            print(f"DRIFT: copy line not verbatim in skeleton:\n  {l[:80]}")
            ok = False
    print(f"copyable skeleton paragraphs: {len(step1)}, copy lines: {len(copy_lines)}")
    print("SYNC: PASS" if ok else "SYNC: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
