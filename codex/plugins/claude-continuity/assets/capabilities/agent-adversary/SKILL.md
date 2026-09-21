---
name: agent-adversary
description: "Migrated Claude agent role. Use as step 2 of the bug-hunter → adversary → judge review flow. Takes bug-hunter's numbered bug report and tries to prove each one wrong. Produces a per-bug rebuttal (confirmed real / false positive / partially wrong) with evidence. Invoke after bug-hunter completes, or when the user says \"跑对抗 Agent\", \"challenge these bugs\", or \"对抗评审\".\n\n<example>\nContext: bug-hunter just produced a 32-bug report, user wants it challenged.\nuser: \"对抗 Agent 上场，把刚才那份报告挑战一遍\"\nassistant: \"我用 adversary 对每条 bug 做反驳/确认，产出对抗评审报告给裁判。\"\n<commentary>\nSecond of three agents. Needs the numbered bug-hunter report as input.\n</commentary>\n</example> Use when the user names adversary, requests this specialist, or invokes a workflow that requires it."
---

# adversary Agent

Read `references/role.md` completely and preserve its role, scope, evidence requirements and output contract.

When the user requests agent, delegated, parallel, panel or adversarial work, give the role to an independent Codex sub-agent if the current runtime permits it. Otherwise perform the role locally and state that it was not an independent agent. Do not hard-code a Claude model name; respect current concurrency and safety rules.
