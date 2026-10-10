---
name: grilling-with-research
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

Every source lands in `research/<topic>.md` in the designated run workspace — glossary, ADRs, and research deliverables all live in one repo; a reference must never point across a repo at something that can move. Only when no workspace is designated does it land in the skill's own repo. Append as it arrives, with three fields — **URL**, **tier** (primary: papers (arXiv etc.), specs/official docs, the code itself, first-person community posts (GitHub issues/discussions, HN/Reddit OPs & comments — the author reporting their own run) / secondary: blogs, retellings, aggregator summaries), and **argument**: one line on which open decision it bears on and how — which known trade-off it supports or contradicts. A citation without an argument has not landed. A source carries a decision only after full extraction; snippet-only sources stay secondary, labelled 未讀全文.

**必搜範圍（mandatory coverage）**：每次運行的研究範圍必須包含 GitHub（repo/issues/discussions）、HN、Reddit 三個管道——各至少一條來源，或一條 searched-and-absent。五類第一層（論文／官方文件／代碼／社群親身發言／searched-and-absent）逐類清點，缺哪類補哪類或留 absents 記錄。管道按來源網域數，類別按來源性質數——性質用可選 `Cat:` 欄自報（paper/docs/code/community），腳本才數得到非典型網域（如 playwright.dev 屬官方文件）。開場前跑 `scripts/check_research_gate.py <research_dir>`——腳本退出碼 0 才開第一輪。腳本本身要先過 fixture 自測（每條規則至少一個必 FAIL 的 fixture＋一個必 PASS）；它對真實數據報 FAIL 時，先跑 fixture 分清是腳本 bug 還是數據真有洞，再動數據。

**機读格式（腳本 parse 的格式，寫錯欄名＝條目 invisible）**：每條來源一個 `## 標題` 區塊，欄位逐行：`- URL:`、`- Tier:`（primary／secondary＋未讀全文標記）、`- Argument:`（或「論證」）、可選 `- Cat:`。searched-and-absent 區塊免 URL，用固定三行：查詢詞／搜了哪裡／結果。fixture 在 `scripts/fixtures/`。

**Searched-and-absent** entries are research output too and can carry a question. Fixed format: query terms, where searched (which sites/collections), result. That format is the target the next round can shoot at ("you didn't search X").

**Completion (consumption-based, not count-based):** every open question on the list carries either an argued citation or a searched-and-absent entry — plus a floor of at least 3 real sources or explicit absences. Only then does the first round open.

## Research Layer（runtime routing，ADR-0004）

三條道。搜尋 → 宿主原生搜尋工具（顯式默認、可覆寫；降級序：自建 SearXNG → 廠商免費 key）。已登入的平台 → 平台 CLI（Agent-Reach 路徑）。普通 URL → 下面的階梯。搜尋回傳小結果集；抓取才產生上下文；兩筆預算分開計。

升級階梯——默認最便宜層（HTTP fetch，輸出轉正文 markdown，只回抽取結果）。觸發器：空結果、challenge 頁、登入牆。一次只升一層。升上瀏覽器層時：預設關資源＋擋廣告＋重用 session；單發腳本，不進 per-step loop（每步 loop 在本地 context 預算下是 10⁵ tokens 起跳）。

環境事實先實測再引用——建議依賴「本機有 X」時，先測（which／config／實 call），測試輸出留檔進 `research/`。

**Scrapling 觸發規則（ADR-0006 裁決，執行腳本預先寫死，觸發當場不再決策）**：平时不裝、不常駐。三種情況才升上來裝：抓取回空內容、challenge 頁、登入牆。執行腳本：`uv tool install "scrapling[all]"` → `scrapling install`（它拉自己的瀏覽器依賴，不復用本機 playwright）→ MCP 掛 `scrapling-mcp`（stdio）。PyPI 裝法要顯式鎖 `scrapling` 本名（山寨名在隔壁）。驗證看內容，不只看狀態碼——它會靜默失敗（回 200 但內容空）。enterprise Cloudflare 是天花板，升到頂也繞不過。

## Step 2 — Grilling rounds

Ask the whole frontier each round; each round the user's answers push the frontier outward. Fact-finding stays your job — never ask the user what you could look up yourself; a running sub-agent is an unsettled prerequisite, so only questions downstream of it wait. No cap on questions per round — the frontier is whatever it is.

### Question format (interactive)

One round = prose layer + one interactive question form (e.g. Hermes' `clarify` tool; any agent's equivalent). The prose layer carries the argument; the form carries only the answers. Structure:

1. **Restate line(s) in prose** — every locked decision from prior rounds, one line each, before the new questions.
2. **Each question in prose**: a concrete scenario with a real trade-off first — abstract questions ("how big should the buffer be?") don't qualify here. Then any citation the question needs, inline in the prose, tier-labeled (secondary sources marked as reported). Every option carries pros AND cons; the recommendation states its reason.
3. **The form** collects answers: one entry per question, options max 4, the recommended answer listed FIRST (the UI marks it), an "Other" free-text row on every question so the user can escalate a tier or add a thought. The most radical option must be IN the option set — never silently narrow the range.
4. **Searched-and-absent questions get no options** — they render as an open-ended field (no choices): they want the user's judgment, not a pick from a menu.
5. **Dependency rule**: a question whose wording depends on an unanswered question stays out of this round's form.
6. **Degraded path**: on an agent with no interactive form tool, fall back to plain text — `❓ **Qn** - **title**: body` + `➡ recommendation` lines, accepting terse answers ("Q3: a").

Example shape:

```
(locked: Q14 — research phase is non-blocking.)

❓ **Q15 - buffer size**: when KV budget drops to 6G, a 512K context
forces q4 quantization — [paper X §4.2] (primary) says the trade-off
is real.

<form>
  Q15: ○ (recommended) 256K, no precision hit
       ○ 512K, accept q4
       ○ dynamic scheduling, complexity up
       ○ radical: cut to 128K for headroom
       ○ Other → free text
  Q16 (no source — nothing found contradicting): open field
</form>
```

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

## 驗證紀律（多尺場次適用的常駐規則，10 條）

逼問場裡有多個獨立執行者（人或 agent）跑量測時：

- **自報數不入帳**——任何自己報的數字要有獨立實作覆核過才算數；實務上每次收斂後錯的都是沒被交叉核驗的自報數。獨立複現要連執行環境路徑一起報。
- **計數器要連統計口徑一起報**——大小寫規則（副檔名 `.PNG`）、單位制（MB vs MiB）寫進憑據，否則兩把尺物理收斂會被當成發分歧；判「分歧」前先對齊口徑。
- **開給別人工作的單要兩個獨立觀察（不同環境）**——單人在自己的環境上單人觀察＝證據等級不及格，可能測到的是自己的探針。
- **預測寫死在盤上之後才派工，落空不改寫**；曲線整跑結束前不准讀數、中場不蓋章。
- **預填的合規欄位不算過閘**——照口頭答覆填綠的欄位正是規則要防的東西；閘要的是一張文件實體。權利的正當行使（owner 裁決跳過）可以，但要留痕：欄位加注「口頭裁決＋日期＋文件在哪」。
- **裁決權限以擁有權為界**——決策者能裁他擁有的東西（雙向門）；不屬於他的東西（第三方版權）只有文件證據過得了閘，他的簽字無效。
- **寫死在 repo 裡可重跑的測試才是憑據**；測試腳本的環境前提（port、啟動根目錄）是憑據的一部分，寫進文件裡。渲染驗收要驗實效（真解碼／狀態真的變），DOM 存在只是代理指標——人眼判與代理判打架時以實測為準。
- **數符號要數真呼叫，不數字串出現**——grep 數燈會把註解裡的符號計入（註解寫了 M2 就多一盞燈）；比對兩個殼／兩份表的題號時，只數真正的斷言呼叫。
- **聲稱「已落地／已補齊」之前先看盤**——先 commit 再報 hash，先 `git status` 乾淨再報連跑成績；話講在實物前面就是順序債，同一形態犯兩次就要升級成常駐規則。
- **「補齊／對齊」類工單要雙向核**——改完從兩個方向各數一次差集（A−B 與 B−A），單邊補齊不算補齊。

## Finish

Done when the frontier is empty, every research question has landed evidence or a searched-and-absent entry, and every resolved term or decision is on disk. Do not act on the design until the user confirms shared understanding.
