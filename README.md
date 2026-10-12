# grilling-with-research

**Don't grill a plan on memory alone. Read first, then interrogate.**

![hero](assets/hero.png)

A [grilling](https://github.com/mattpocock/skills)-style interview skill for agents — with a **research gate** bolted on the front. Before the first question is asked, every open decision that outside evidence could touch gets a sub-agent dispatched to find sources. Only when each open question carries an *argued* citation — or an honest "searched, nothing found" — does the interrogation open.

Built for one failure mode: agents (and people) asking questions they could have answered by reading.

## Why

A plain grilling session is only as sharp as what the agent already knows. Ask about your architecture and it interrogates your vocabulary. Ask about a design space it hasn't read about and it asks *you* things it should have known — or worse, fabricates a citation to sound deep.

This skill closes that gap with three mechanics:

- **Research gate (consumption-based).** The gate opens when every listed open question has landed evidence — not when "enough sources" were collected. Count-thresholds breed decorative citations; consumption proves use.
- **Citation with argument.** A source lands with its URL, its tier (primary / secondary — secondary citations are labeled), and one line on *which open decision it bears on and how*. A citation without an argument has not landed.
- **Searched-and-absent is research output.** "Searched X, Y, Z across these sources, found nothing" is a fixed-format record — and a legitimate question-generator: the next round can shoot at exactly what wasn't searched.

Then the classic loop runs: frontier rounds, restate-before-advancing, propagate corrections, label proposals as revisable — with a live domain model written as you go (`CONTEXT.md` glossary + ADRs, offered only when a decision is hard to reverse, surprising, and a real trade-off).

## How it works

```
Step 0  Bootstrap    file-existence check, never memory — docs/agents/ layout
Step 1  Research     sub-agents → argued citations → research/<topic>.md
Step 2  Grill        frontier rounds; ≥1 question per round that couldn't
                     exist without a source. No contradiction, no question.
Step 3  Document     glossary + ADRs written the moment they crystallise
Finish  Shared understanding confirmed by the user. Nothing acts on it until then.
```

## Install

Drop this folder (or a symlink to it) into your agent's skills directory:

```bash
ln -s /path/to/grilling-with-research ~/.agents/skills/grilling-with-research
```

The skill is user-invoked (`disable-model-invocation: true`) — it never fires on its own, so it costs zero context until you call it:

```
/grilling-with-research
```

## The rules it refuses to break

| Rule | Failure it prevents |
|---|---|
| Citation without argument doesn't land | Decorative references |
| Secondary sources labeled 轉述/retold | Secondhand ideas passed off as first-hand |
| "Searched, nothing found" is a record | Fake consensus, fabricated tension |
| Restate each locked decision in one line | Misread approvals hardening into design |
| Unchallenged proposals stay *revisable* | Recommendations fossilizing into decisions |
| Glossary stays a glossary | `CONTEXT.md` rotting into a spec |

## Credit

The grilling loop, domain-modeling discipline, and skill-writing principles come from [Matt Pocock's skills](https://github.com/mattpocock/skills) (pinned at v1.2.2). The research gate — argued citations, consumption-based gate, searched-and-absent records — is the new organ.

## 外部使用者安裝須知（機器依賴三處＋第一步）

clone 後不改任何东西就跑的前提是這三處本機寫死點已被你接管：

1. **Roster 真相源** ＝本機 plugin `data/agents.json`（ADR-0001 寫死）——外部環境要換成你自己的 roster 來源。
2. **閘門查表** ＝本機模型映射（ADR-0003 寫死；本機無數據格是理論值）——按你的實際執行檔位重寫。
3. **AGENCY 錨點** ＝`scripts/check_rule_copy.py` 的 AGENCY 常數——外部使用者改這裡，或設 env `AGENCY_SKILL_DIR` 指向你本機的 overlay SKILL.md（預設值是本機默認值；ADR-0005／ADR-0007）。

安裝後第一步：跑 `python3 scripts/check_rule_copy.py`（骨架根目錄）——退出碼 0 ＝規則副本同步、可開工。ADR 檔案本體與字彙表住 overlay repo（ADR-0007：單一道真相源）。

## License

MIT
