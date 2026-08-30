---
name: grill-with-research
description: 整合版 grilling——先落盤有論證的研究，再開始逼問；邊問邊寫 glossary 與 ADR。手動召換。
disable-model-invocation: true
---

# Grill with Research

Interview relentlessly until shared understanding. Map the design as a **design tree**: every decision branches into the decisions that hang off it. Work the tree in **rounds** — the **frontier** is every decision answerable without guessing at answers not yet heard. Ask the whole frontier in one round, numbered, each with your recommended answer; wait for answers, recompute the frontier, ask the next round. A question that depends on an unsettled one belongs to a later round.

Three things this version adds to the base loop: a **research gate** before the first round (Step 1), **cited questions** (Step 2), and **docs written as you go** (Step 3).

## Step 0 — Bootstrap (decide by file existence, never by memory)

Check the current repo for `docs/agents/`. It exists → skip this step entirely. It doesn't → write it, showing the user the draft before writing:

- **Issue tracker** — GitHub remote → GitHub (`gh`). No remote / solo repo → local markdown under `.scratch/<feature>/`. Other trackers → ask the user for the workflow in one paragraph, record as prose. Record in `docs/agents/issue-tracker.md`.
- **Domain docs** — default single-context: root `CONTEXT.md` + `docs/adr/`. Record in `docs/agents/domain.md`.
- **Triage labels** — only if the `triage` skill is installed: ask once whether to keep defaults (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`); record in `docs/agents/triage-labels.md`.

Then add an `## Agent skills` block (one line per file) to whichever of `CLAUDE.md` / `AGENTS.md` exists; if neither, ask which to create — never create a second one.

Done when: every `docs/agents/*.md` above exists (minus skipped sections) and the Agent skills block points at them.

## Step 1 — Research (the gate)

Before the first round, enumerate every open decision that outside evidence could bear on. Then: one open question, one sub-agent dispatch. Each dispatch must return sources with **URLs** — a conclusion without a verifiable URL is marked unverified and never enters a question.

Every source lands in `research/<topic>.md` (append as it arrives) with three fields — **URL**, **tier** (primary: papers, specs, the code itself / secondary: blogs, retellings), and **argument**: one line on which open decision it bears on and how — which known trade-off it supports or contradicts. A citation without an argument has not landed.

**Searched-and-absent** entries are research output too and can carry a question. Fixed format: query terms, where searched (which sites/collections), result. That format is the target the next round can shoot at ("you didn't search X").

**Completion (consumption-based, not count-based):** every open question on the list carries either an argued citation or a searched-and-absent entry — plus a floor of at least 3 real sources or explicit absences. Only then does the first round open.

## Step 2 — Grilling rounds

Ask the whole frontier each round; each round the user's answers push the frontier outward. Fact-finding stays your job — never ask the user what you could look up yourself; a running sub-agent is an unsettled prerequisite, so only questions downstream of it wait.

- **Citation discipline** — from the first round after research lands, every round carries at least one question that could not exist without a source, with the source named in the question. Cite a secondary source → label it 轉述.
- **No manufactured tension** — a round may carry zero cited questions when it says why: "no source found contradicts the plan." Depth comes from contradictions; no contradiction, no question.
- **Restate before advancing** — after each confirmation, restate the locked decision in one line, so the transcript is self-verifying. Terse answers ("Q3: a") are normal.
- **Propagate corrections** — when the user corrects an earlier fact, explicitly revise every inference built on the old one and record the correction.
- **Label proposals honestly** — items the user confirmed verbatim vs items you proposed unchallenged: mark the latter *revisable* so they don't harden into decisions.
- **Doc hygiene** — read CONTEXT.md/ADR files before writing; patch, never overwrite — sibling sessions may be editing the same file.

## Step 3 — Domain docs (as things crystallise)

The moment a term is resolved, write it to `CONTEXT.md`; the moment a decision crystallises, offer an ADR. Don't batch.

- **Challenge against the glossary** — a term used against its definition gets called out immediately.
- **Sharpen fuzzy language** — propose one precise canonical term.
- **Discuss concrete scenarios** — invent edge-case scenarios that force precision about boundaries between concepts.
- **Cross-reference with code** — check whether the code agrees with what the user says; a contradiction gets surfaced.
- `CONTEXT.md` is a glossary and nothing else — no implementation details. `research/` is the evidence store; keep the two apart.
- **ADR only when all three hold:** hard to reverse, surprising without context, the result of a real trade-off. Any missing → skip the ADR.

## Finish

Done when the frontier is empty, every research question has landed evidence or a searched-and-absent entry, and every resolved term or decision is on disk. Do not act on the design until the user confirms shared understanding.
