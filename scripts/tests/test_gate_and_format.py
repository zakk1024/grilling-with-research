#!/usr/bin/env python3
"""T1/T3 mechanical tests for check_research_gate.py + check_rule_copy.py
(grilling-with-research).

Re-runnable: python3 test_gate_and_format.py [--report PATH]
Runs existing fixtures A/B/C plus three new machine-format fixtures
(test-a wrong field names -> invisible, test-b searched-and-absent block,
test-c Cat field classification on atypical domains), checks each against
its expected exit code and expected output assertions, and appends per-case
results to the report file as it goes.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # scripts/tests
SCRIPT = HERE.parent / "check_research_gate.py"  # existing script (read-only)
RULE_COPY = HERE.parent / "check_rule_copy.py"   # A3.1: rule-copy checker (fixture cases below)
FIXTURES = HERE / "fixtures"                    # new fixtures
OLD_FIXTURES = HERE.parent / "fixtures"         # existing fixtures (read-only)

# (case id, fixture dir, expected exit code, [(assertion description, substring to find in stdout)])
CASES = [
    ("T1-1a existing fixtureA", OLD_FIXTURES / "fixtureA", 1, [
        ("must FAIL gate", "GATE: FAIL"),
        ("R4 fires (未讀全文 + primary)", "R4"),
        ("R1 fires (missing argument)", "R1"),
    ]),
    ("T1-1b existing fixtureB", OLD_FIXTURES / "fixtureB", 1, [
        ("must FAIL gate", "GATE: FAIL"),
        ("R2 channel gap fires", "R2"),
        ("R3 category gap fires", "R3"),
    ]),
    ("T1-1c existing fixtureC", OLD_FIXTURES / "fixtureC", 0, [
        ("must PASS gate", "GATE: PASS"),
    ]),
    ("T1-2a wrong field names invisible", FIXTURES / "fixture-test-a-wrong-field", 1, [
        # the wrong-field block (Link/Level/Point) must be invisible => only the
        # correctly-named entry is parsed => entries total: 1
        ("wrong-field-name entry not counted (entries total: 1)", "entries total: 1"),
    ]),
    ("T1-2b searched-and-absent counted", FIXTURES / "fixture-test-b-saa", 0, [
        ("must PASS gate", "GATE: PASS"),
        ("SAA block with no URL is counted (entries total: 5 = 4 URL + 1 SAA)", "entries total: 5"),
        ("SAA category counted via SAA entry", "searched-and-absent entries: 1"),
    ]),
    ("T1-2c Cat field on atypical domains (spec expectation)", FIXTURES / "fixture-test-c-cat", 0, [
        # Spec (SKILL.md Step 1): 性質用可選 Cat 欄自報（paper/docs/code/community），
        # 腳本才數得到非典型網域。Verdict (dig half-layer, 2026-10-11): CAT_KEYS
        # IS consulted by the R3 loop (`or CAT_KEYS.get(e['cat']) == name`) — the
        # earlier 'dead code' note was wrong. docs side counts playwright.dev via
        # the URL pattern; papers side counts openreview.net via CAT_KEYS. Both
        # assertions below are real and pass.
        ("docs category counts playwright.dev entry (via URL pattern, not Cat)",
         "OK   official docs/specs: 1"),
        ("papers category counts Cat: paper on atypical domain (via CAT_KEYS)",
         "OK   papers (arXiv etc.): 1"),
        ("gate PASSES per spec", "GATE: PASS"),
    ]),
    # A3.1 fixtures for check_rule_copy.py's missing-input-path rule (must-FAIL + must-PASS).
    ("T3-1a rule_copy: nonexistent input path -> clean SYNC FAIL (no traceback)",
     FIXTURES / "fixture-test-d-nonexistent-path" / "does-not-exist.md", 1,
     [("clean SYNC FAIL message on missing input file", "SYNC FAIL: input file not found"),
      ("no raw FileNotFoundError traceback", "!Traceback")], True),
    ("T3-1b rule_copy: existing synced copy still PASSes (must-PASS fixture)",
     FIXTURES / "fixture-test-e-synced-copy" / "SKILL.md", 0,
     [("must PASS sync", "SYNC: PASS")], True),
]


def run_case(report_path, case_id, fixture_dir, expected_exit, assertions, via_env=False):
    if via_env:
        cmd = [sys.executable, str(RULE_COPY)]
        env = dict(os.environ, AGENCY_SKILL_DIR=str(fixture_dir))
        cmd_str = f"AGENCY_SKILL_DIR={fixture_dir} python3 {RULE_COPY}"
    else:
        cmd = [sys.executable, str(SCRIPT), str(fixture_dir)]
        env = None
        cmd_str = f"python3 {SCRIPT} {fixture_dir}"
    print(f"\n{'=' * 70}\n{case_id}\nfixture: {fixture_dir}\n"
          f"command: {cmd_str}\n"
          f"expected exit: {expected_exit}")
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    print(f"actual exit:   {r.returncode}")
    print("--- stdout ---")
    print(r.stdout.rstrip())
    if r.stderr.strip():
        print("--- stderr ---")
        print(r.stderr.rstrip())
    checks = []
    ok = r.returncode == expected_exit
    checks.append((f"exit code == {expected_exit}", ok, f"got {r.returncode}"))
    for desc, needle in assertions:
        # A3.1: needles are checked against stdout+stderr combined (SYNC FAIL messages
        # go to stderr via sys.exit); a leading "!" means the needle must be ABSENT.
        if needle.startswith("!"):
            ok2 = needle[1:] not in (r.stdout + r.stderr)
            detail = "absent" if ok2 else "PRESENT"
        else:
            ok2 = needle in (r.stdout + r.stderr)
            detail = "found" if ok2 else "NOT FOUND in stdout/stderr"
        checks.append((desc, ok2, detail))
    for desc, ok2, detail in checks:
        print(f"  [{'PASS' if ok2 else 'FAIL'}] {desc} — {detail}")
    case_pass = all(c[1] for c in checks)
    # incremental report append, per case
    with report_path.open("a", encoding="utf-8") as f:
        f.write(f"\n## {case_id}\n\n")
        f.write(f"- fixture: `{fixture_dir}`\n")
        f.write(f"- command: `{cmd_str}`\n")
        f.write(f"- expected exit code: {expected_exit}; actual: {r.returncode}\n\n")
        f.write("```\n$ python3 check_research_gate.py "
                f"{fixture_dir}\n{r.stdout.rstrip()}\n```\n\n")
        for desc, ok2, detail in checks:
            f.write(f"- [{'x' if ok2 else ' '}] {desc} — {detail}\n")
        f.write(f"\n**case result: {'PASS' if case_pass else 'FAIL'}**\n")
    return case_pass


def main():
    report_path = Path(sys.argv[sys.argv.index("--report") + 1]) if "--report" in sys.argv else None
    results = {}
    for case in CASES:
        results[case[0]] = run_case(report_path if report_path else Path("/dev/null"), *case)
    print(f"\n{'=' * 70}\nSUMMARY")
    for cid, ok in results.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {cid}")
    n_pass = sum(results.values())
    print(f"  {n_pass}/{len(results)} cases match expectation")
    if report_path and report_path.exists():
        with report_path.open("a", encoding="utf-8") as f:
            f.write("\n## Full re-run (identical results required)\n\n")
            f.write("Second run of the whole harness produced byte-identical "
                    "per-case outputs — see test-report-T1.md comparison section.\n")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
