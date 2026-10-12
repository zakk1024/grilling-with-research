#!/usr/bin/env python3
"""Rule-copy sync checker: agency-agents-thinking-grill vs grilling-with-research.

The agency skill embeds a verbatim COPY of the source-of-truth rules (COPY-START
to COPY-END). If they drift, the copy is stale and dispatch must not run.

Copy rule (what counts as copied): the skeleton's Step 1 paragraph lines
(the paragraphs between the '## Step 1 — Research (the gate)' heading and the
next heading), plus every Research Layer paragraph.

Usage: python3 check_rule_copy.py
Exit 0 = copy in sync. Exit 1 = drift (diff printed).
"""
import os
import re
import sys
from pathlib import Path

# ADR-0007: one convergence anchor. The skeleton resolves by self-location (this
# script lives in the skeleton repo); the overlay is the workspace repo's SKILL.md.
# NOTE: external users — change this to your local overlay path, or set the
# AGENCY_SKILL_DIR env var to it (ADR-0005: 外部使用者改這裡／設 env).
SKELETON = Path(__file__).resolve().parent.parent / "SKILL.md"
AGENCY = Path(os.environ.get("AGENCY_SKILL_DIR", "/Users/zakk/Desktop/Naval/Agency-agents thinking grill/SKILL.md"))  # 本機默認值


def read_text_checked(path):
    # A3.1: nonexistent input paths go through the script's own SYNC FAIL
    # message path (clean message + exit 1), not a raw FileNotFoundError traceback.
    if not path.is_file():
        sys.exit(f"SYNC FAIL: input file not found: {path}")
    return path.read_text(encoding="utf-8")


def paragraphs(path, lo=None, hi=None):
    text = read_text_checked(path)
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
    skel_text = read_text_checked(SKELETON)
    s1_start = skel_text.find("## Step 1 — Research")
    nxt = skel_text.find("\n## ", s1_start + 1)  # stop at the next heading — Step 1 is
    s1 = skel_text[s1_start:nxt if nxt >= 0 else len(skel_text)]  # followed by Research Layer, not Step 2 (ADR run 2 audit #4)
    step1 += [p.strip() for p in re.split(r"\n\s*\n", s1)
              if p.strip() and not p.startswith("#")
              and not p.startswith("Then add") and not p.startswith("Done when:")]
    rl = skel_text[skel_text.find("## Research Layer"):]
    rl = rl[:rl.find("\n## ")]
    step1 += [p.strip() for p in re.split(r"\n\s*\n", rl) if p.strip() and not p.startswith("#")]
    copy_text = read_text_checked(AGENCY)
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
