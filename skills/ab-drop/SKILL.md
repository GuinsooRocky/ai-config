---
name: ab-drop
description: 把当前 Claude 会话加进公司用量统计 peekaboo-ab 的保护名单（不上报）。触发词："白帽子"、"当前白帽子"、"加白"、"这个 session 不上报"、"别上报"、"放入上报白名单"、"/ab-drop"。不用于：升级/重打 agentboard 补丁（照 memory reference_agentboard_privacy_patch 手顺走）、查上报统计。
---

# ab-drop：当前会话不上报

用户说的「白名单/加白」= **不上报**的保护名单，落在 `~/.agentboard/privacy-rules.json` 的 `drop_sessions`。别理解反。

## 做法

**听到触发词直接跑脚本、回一句结果，别查、别解释原理、别问。**

```bash
~/.claude/skills/ab-drop/scripts/drop.sh          # 当前会话（读 $CLAUDE_CODE_SESSION_ID）
~/.claude/skills/ab-drop/scripts/drop.sh <uuid>   # 指定别的会话
```

脚本去重追加、原子写入，最后跑 patch check。名单运行时读取，不用重打补丁。

## 看结果

- 输出 `PATCHED(v6)` 之类 = 生效；check 报没打上 → 名单没人读，告诉用户并照 memory `reference_agentboard_privacy_patch` 的升级流程处理，**绝不跑 `npx peekaboo-ab setup`**
- 回用户一句：已加入 + 如实提醒「加名单之前已同步过的记录删不掉，只管之后」
- 会话一进 `~/Desktop/{cmm,my-code,archives,cc-memory}` 就按工作会话、≤60s 带真标题上报——所以越早加越好
