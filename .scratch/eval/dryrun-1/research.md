# Research — OpenCLI vs Playwright 做 agent 瀏覽器自動化，誰當默認？

開放決策（本題唯一決策）：agent 的默認瀏覽器執行層選 OpenCLI（CLI/adapter-first，agent 調命令）還是 Playwright（直驱瀏覽器庫/MCP），混合如何分層。

規則執行記錄：搜尋 6/6 次、全文擷取 2/3 次（未超算）。凡只從搜尋摘要取得者標 tier secondary＋未讀全文；只有全文擷取過的才准 primary。

## OpenCLI AGENTS.md（代碼即文件）
- URL: https://github.com/jackwener/OpenCLI/blob/303872b7978e0f7bb99ecbb21f5fb25ee0585ac9/AGENTS.md
- tier: primary（已全文擷取）
- argument: 支持「確定性優先」分層——官方架構文件寫明 PUBLIC pipeline adapters 根本不啟動瀏覽器，只有 COOKIE/HEADER/INTERCEPT/UI 策略才掛瀏覽器 session；即 OpenCLI 的默認路徑是免瀏覽器的確定性命令，瀏覽器是升級層。

## OpenCLI repo README（wuyoscar fork，與 jackwener 同源）
- URL: https://github.com/wuyoscar/OpenCLI
- tier: secondary（未讀全文，僅搜尋摘要）
- argument: 支持 OpenCLI 當默認：主張「一個界面統一三種自動化」＋重用已登入 Chrome（登入態复用是本題關鍵決策變數），並提供 agent skills 入口。

## OpenCLI 深度評測（含 vs browser-use 對比）
- URL: https://guancyxx.cn/en/blog/opencli-deep-dive-comparison
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持混合分層：常規抽取用內建 adapter（零 LLM token、確定性），新互動才升級到瀏覽器原語——正是本題「默認」的第三答案（分層而非二選一）。

## Playwright 官方 release notes
- URL: https://playwright.dev/docs/release-notes
- tier: primary（已全文擷取）
- argument: 官方文件證實 Playwright 已內建 `npx playwright mcp` 與 `playwright-cli`，並為 agent/報告器加 structured step params——反駁「Playwright 只為人類測試存在」的強版主張：官方自己也把 agent 入口當產品面。

## Playwright agent 測試的 waiting/locator 反模式（stevekinney course note）
- URL: https://github.com/stevekinney/stevekinney.net/blob/main/courses/self-testing-ai-agents/the-waiting-story.md
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持「Playwright 當默認」的穩定性論證：agent 生成 Playwright 代碼的头号失败模式是手動 waitForTimeout/networkidle，auto-retrying assertion 模型是結構性解法——確定性框架的等待語義是 agent 直驱模式缺的東西。

## invisible_playwright 反偵測清單（Playwright 生態）
- URL: https://github.com/feder-cr/invisible_playwright/blob/9833d053fa308bc048d12a0b81312bc298076576/docs/playwright-detected-as-bot.md
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 反駁「Playwright 直接用就夠」：反偵測取決於整機指紋/環境一致性（software renderer、時區-IP 錯配），不是 JS 層 stealth 插件能補——若默认層要碰防爬站點，Playwright 需額外層，OpenCLI 重用真實登入 Chrome 迴避了這一層。

## Loom repo README（agent-first browser runtime，反方直接證詞）
- URL: https://github.com/mentiora-ai/loom
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 反駁 Playwright 當默認：明文主張「Playwright 是為人測自己的站造的」——agent 需要 replay 可重放的 hash chain、typed errors、per-session budget，這些 Playwright 原生不提供。

## agent-skills-hub browser-automation SKILL.md
- URL: https://github.com/agent-skills-hub/agent-skills-hub/blob/main/skills/browser-automation/SKILL.md
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持 Playwright 當默認：「Playwright won the framework war」——生態、debug 工具、test runner 是量產可靠度來源（社区共識性轉述，非一手運行報告）。

## HN: Fetch-MCP thread（Playwright MCP 的 cookie 缺口）
- URL: https://news.ycombinator.com/item?id=43419713
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 反駁裸 Playwright 當默認：留言直指「playwright doesn't use your cookies」，工作區做法是 CDP attach 已登入 Chrome——即登入態必須靠外部層解決，这正是 OpenCLI Browser Bridge 的存在理由。

## HN: Playwriter——單 execute 工具＋重用現有 Chrome tab
- URL: https://news.ycombinator.com/item?id=46068108
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持確定性/低 context 優先：單工具 reduces context bloat、重用現有 browser 省資源——與 Reddit mcp 條的 114K-token 論證同向。

## Reddit r/WebScrapingInsider: Browser Use vs Playwright in 2026（官方 AMA 轉述）
- URL: https://www.reddit.com/r/WebScrapingInsider/comments/1vhrp89/browser_use_vs_playwright_in_2026_when_should_you/
- tier: secondary（未讀全文，僅搜尋摘要，轉述；內含 Browser Use 團隊自述）
- argument: 本題最強「分層」證詞：workflow 穩定/重複/性能敏感→Playwright 贏；開放式/站點常變→agent 贏；Browser Use 自己已把底層從 Playwright 換成直连 CDP 換取控制權；生產形態=agent 發現→凍結成腳本→壞了再叫 agent。

## Reddit r/AI_Agents: Stop Using Playwright and Puppeteer for automation
- URL: https://reddit.com/r/AI_Agents/comments/1nkkbas/stop_using_playwright_and_puppeteer_for_automation
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持「確定性執行器當默認」：LLM 觀察一次學出確定性計劃，之後執行不過 LLM（成本 $200/月→$2）——與 OpenCLI「crystallize repeated actions into CLI commands」同一哲學；留言同時保留反調：QA/測試場景仍留 Playwright。

## Reddit r/mcp: Microsoft recommends CLI over MCP for Playwright
- URL: https://reddit.com/r/mcp/comments/1spvkrz/microsoft_recommends_cli_over_mcp_for_playwright
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 直接支持 OpenCLI 式「CLI 層先於 MCP」：連微軟官方都推薦 playwright 用 CLI 而非 MCP，因 MCP 每步回流完整 accessibility tree（~114K tokens/task vs ~5K）；互動式 UI 自動化仍是 Playwright MCP 的主場。

## arXiv: Wuying-Browser-Agent（阿里雲，long-horizon browser agents）
- URL: https://arxiv.org/pdf/2608.17319v1
- tier: primary（已全文擷取）
- argument: 支持「默認層要提供確定性執行原語、收緊 per-step LLM 決策」：論文的核心貢獻就是 structured browser harness（validated action interface＋decision-oriented context）；且長任務（>50 步）最強模型成功率 <1/7——per-step 全 LLM 迴路在長程任務上不可靠，支持把可確定化的步驟下沉。

## arXiv: WebChallenger（架構勝過模型規模）
- URL: https://arxiv.org/html/2606.10423v1
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持混合分層：把「選擇性注意力/持久記憶/程序熟練度」做進架構（deterministic PageMem＋一次前向記憶＋compound actions 把多步合成單動作）即可用 32B 開源模型接近前沿——佐證「能確定性化的層就該下沉，LLM 只做決策」。

## arXiv: WebForge（benchmark trilemma）
- URL: https://arxiv.org/pdf/2604.10988v1
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 支持對默認層的真實環境假設：真站點 benchmark 半年內近半任務失效（content drift）——任何依賴站點結構的 adapter/selector 層都要預設會漂移、要有修復機制（呼應 OpenCLI autofix）。

## Agent Skills 官方規格（agentskills.io——OpenCLI 的接入介面）
- URL: https://agentskills.io
- tier: primary（已全文擷取）
- argument: 支持「介面層才是默認決策」：官方規格定調 skill=SKILL.md 資料夾＋progressive disclosure，跨產品复用——OpenCLI 靠這層把命令暴露給 agent，Playwright 靠 MCP；本題「誰當默認」其實是「默認走 skill/CLI 介面層還是 MCP 介面層」的介面決策，底下引擎可換。

## browser-use 官方文件（The Big Picture——架構直連 CDP）
- URL: https://docs.browser-use.com/library/browser-use/the-big-picture
- tier: secondary（未讀全文，僅搜尋摘要，轉述）
- argument: 反駁「Playwright 當 agent 層底座」：agent 層頭號專案官方宣告其瀏覽器層直接說 CDP（cdp-use），不經 Playwright/Selenium——為爭取控制權自拆 Playwright 抽象層；與 Reddit AMA 中 Browser Use 團隊自述互相印證。

## searched-and-absent: arXiv 學術界對「CLI-first 瀏覽器代理層」本身
- URL:
- tier: searched-and-absent
- argument: 查詢詞＝"arxiv browser agent LLM web automation benchmark mind2web webarena"；搜了＝arXiv（經 web 搜尋管道）；結果＝論文集內無一篇以 OpenCLI/CLI-first 代理層為研究對象——學術驗證全部落在 LLM-agent 層（harness/benchmark），CLI 層作為系統工程尚無文獻背書，此決策只能靠工程證據。
