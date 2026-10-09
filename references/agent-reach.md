# Agent-Reach 登入態管道命令卡（按需載入）

觸發：Research 需要登入態管道（Twitter/X、Reddit、小紅書等），或宿主原生搜尋與 Jina 抓取都失敗時的升級層。

前提：本機已裝 Agent-Reach 本體（`which agent-reach`）。未裝 → 本卡不適用，照 SKILL.md 降級序走，缺席照 searched-and-absent 落盤。

## 管道路由

| 研究管道 | 命令 | 登入態 |
|---|---|---|
| Twitter/X | `twitter search "QUERY" -c`／`twitter tweet URL` | 小號 Cookie（`agent-reach configure twitter-cookies`） |
| B站 | `bili search --type video -n 10 "QUERY" --yaml`／`bili hot --yaml` | 免登錄 |
| Reddit | `agent-reach doctor --json` 查當前後端；桌面 OpenCLI 路線為主 | 登入態必須 |
| HN | 無專用 channel——照舊 HN Algolia（`https://hn.algolia.com/api/v1/search?query=`） | 免 |
| GitHub | 照舊 `gh` CLI | — |
| Web | 照舊 Jina Reader（`curl https://r.jina.ai/URL`） | 免 |

先體檢再使用：`agent-reach doctor --json`（JSON 欄位：`status`／`active_backend`；`warn`=已裝未配置、`off`=沒後端）。doctor 有誤報前科（issue #685/#732）——報 ok 的渠道首次仍實跑一條命令驗證，自報數不入帳。

## 憑據紀律

- Cookie 渠道一律專用小號；絕不在聊天明文貼 Cookie，用 `agent-reach configure twitter-cookies --stdin` 或 `--from-browser --platform twitter`。
- 落盤 `~/.agent-reach/`（0600）——引用研究時引用管道輸出，不引用憑據。

## 降級與缺席

CLI 失敗（反爬、封號、上遊停更）→ 一次升一層照 SKILL.md 階梯；仍失敗 → searched-and-absent 固定三行落盤（查詢詞／搜了哪裡／結果），管道覆蓋以 absent 記錄成立。

## 驗證記錄

- 2026-10-10：`bili search --type video` 實測返回真實結果（run workspace `.scratch/agent-reach/`）。`twitter` CLI 已裝、Cookie 未配置——配置後首次使用需再驗。
- 安裝釘定：uv tool install --from `archive/94f06c1.zip`（Agent-Reach v1.5.0）。
