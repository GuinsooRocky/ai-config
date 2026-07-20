---
name: session-report-whitelist-trigger
description: "触发词\"把当前会话放入上报白名单\"（及\"这个session别上报\"类变体）→ 把当前 session uuid 加进 ~/.agentboard/privacy-rules.json 的 drop_sessions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c1cf47c1-3c0c-4106-a059-b3a2e325eeb9
---

用户说**"把当前会话放入上报白名单"**（变体："这个 session 别上报"、"当前会话不要上报"）= 让当前会话对公司统计 peekaboo-ab 整条免上报。注意：用户口中的"白名单"是**保护名单**（不上报），落的配置是 [[agentboard-privacy-patch]] 的 `drop_sessions`（屏蔽名单），别反着理解成"允许上报"。

**Why:** 公司统计会传会话标题+路径+活跃窗口，个人敏感会话用户想整条豁免（2026-07-02 本会话首例）。

**How to apply:**
1. 定位当前 session uuid：scratchpad 路径里的 uuid 段，或按内容指纹 grep `~/.claude/projects/-Users-lengmo/*.jsonl`（别用 mtime 认 session）
2. 把 uuid 追加进 `~/.agentboard/privacy-rules.json` 的 `drop_sessions` 数组（去重）；运行时读取，即时生效，不用重打 patch
3. 顺手跑 `node ~/.agentboard/privacy-patch.mjs check`——patch 不在位时名单没人读，drop 不生效；不在位就 apply
4. 如实提醒：该会话此前已上报的快照留在服务器，drop 只管之后
