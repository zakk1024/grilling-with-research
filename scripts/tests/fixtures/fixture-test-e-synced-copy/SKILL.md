COPY-START

Before the first round, enumerate every open decision that outside evidence could bear on. Then: one open question, one sub-agent dispatch. Each dispatch must return sources with **URLs** — a conclusion without a verifiable URL is marked unverified and never enters a question.

Every source lands in `research/<topic>.md` in the designated run workspace — glossary, ADRs, and research deliverables all live in one repo; a reference must never point across a repo at something that can move. Only when no workspace is designated does it land in the skill's own repo（本機預設，外部使用者改指自己的 workspace）. Append as it arrives, with three fields — **URL**, **tier** (primary: papers (arXiv etc.), specs/official docs, the code itself, first-person community posts (GitHub issues/discussions, HN/Reddit OPs & comments — the author reporting their own run) / secondary: blogs, retellings, aggregator summaries), and **argument**: one line on which open decision it bears on and how — which known trade-off it supports or contradicts. A citation without an argument has not landed. A source carries a decision only after full extraction; snippet-only sources stay secondary, labelled 未讀全文.

**必搜範圍（mandatory coverage）**：每次運行的研究範圍必須包含 GitHub（repo/issues/discussions）、HN、Reddit 三個管道——各至少一條來源，或一條 searched-and-absent。五類第一層（論文／官方文件／代碼／社群親身發言／searched-and-absent）逐類清點，缺哪類補哪類或留 absents 記錄。管道按來源網域數，類別按來源性質數——性質用可選 `Cat:` 欄自報（paper/docs/code/community），腳本才數得到非典型網域（如 playwright.dev 屬官方文件）。無 pytest 也可直跑（受支持路徑）：測試腳本 self-contained，直接 `python3 scripts/tests/test_gate_and_format.py` 跑即可。開場前跑 `scripts/check_research_gate.py <research_dir>`——腳本退出碼 0 才開第一輪。腳本本身要先過 fixture 自測（每條規則至少一個必 FAIL 的 fixture＋一個必 PASS）；它對真實數據報 FAIL 時，先跑 fixture 分清是腳本 bug 還是數據真有洞，再動數據。

**機读格式（腳本 parse 的格式，寫錯欄名＝條目 invisible）**：每條來源一個 `## 標題` 區塊，欄位逐行：`- URL:`、`- Tier:`（primary／secondary＋未讀全文標記）、`- Argument:`（或「論證」）、可選 `- Cat:`。searched-and-absent 區塊免 URL，用固定三行：查詢詞／搜了哪裡／結果。fixture 在 `scripts/fixtures/`。

**Searched-and-absent** entries are research output too and can carry a question. Fixed format: query terms, where searched (which sites/collections), result. That format is the target the next round can shoot at ("you didn't search X").

**Completion (consumption-based, not count-based):** every open question on the list carries either an argued citation or a searched-and-absent entry — plus a floor of at least 3 real sources or explicit absences. Only then does the first round open.

三條道。搜尋 → 宿主原生搜尋工具（顯式默認、可覆寫；降級序：自建 SearXNG → 廠商免費 key）。已登入的平台 → 平台 CLI——本機已裝 Agent-Reach 時載入 `references/agent-reach.md` 命令卡路由（Twitter/X、B站、Reddit 等）。普通 URL → 下面的階梯。搜尋回傳小結果集；抓取才產生上下文；兩筆預算分開計。

升級階梯——默認最便宜層（HTTP fetch，輸出轉正文 markdown，只回抽取結果）。觸發器：空結果、challenge 頁、登入牆。一次只升一層。升上瀏覽器層時：預設關資源＋擋廣告＋重用 session；單發腳本，不進 per-step loop（每步 loop 在本地 context 預算下是 10⁵ tokens 起跳）。

環境事實先實測再引用——建議依賴「本機有 X」時，先測（which／config／實 call），測試輸出留檔進 `research/`。

**Scrapling 觸發規則（ADR-0006 裁決，執行腳本預先寫死，觸發當場不再決策）**：平时不裝、不常駐。三種情況才升上來裝：抓取回空內容、challenge 頁、登入牆。執行腳本：`uv tool install "scrapling[all]"` → `scrapling install`（它拉自己的瀏覽器依賴，不復用本機 playwright）→ MCP 掛 `scrapling-mcp`（stdio）。PyPI 裝法要顯式鎖 `scrapling` 本名（山寨名在隔壁）。驗證看內容，不只看狀態碼——它會靜默失敗（回 200 但內容空）。enterprise Cloudflare 是天花板，升到頂也繞不過。

COPY-END
