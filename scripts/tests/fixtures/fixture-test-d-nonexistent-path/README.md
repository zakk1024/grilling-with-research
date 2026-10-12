# fixture-test-d — rule_copy must-FAIL fixture

Input path `does-not-exist.md` intentionally does NOT exist (dir holds only this README).
Rule under test: check_rule_copy.py must answer a missing input file with its own
clean `SYNC FAIL: input file not found: <path>` message and exit 1 — never a raw
FileNotFoundError traceback. Harness case: T3-1a.
