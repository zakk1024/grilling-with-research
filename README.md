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

## License

MIT
