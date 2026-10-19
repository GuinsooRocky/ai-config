---
name: ab-drop
description: 切换 Claude / Codex 会话的 peekaboo-ab 用量上报规则：白帽子不上报，黑帽子强制上报 session 的 token 用量。触发词："白帽子"、"当前白帽子"、"加白"、"这个 session 不上报"、"别上报"、"放入上报白名单"、"黑帽子"、"当前黑帽子"、"加黑"、"这个 session 必须上报"、"token 一定要上报"、"/ab-drop"。不用于升级/重打 agentboard 补丁或查询上报统计。
---

# ab-drop：白帽子不上报，黑帽子必须上报

目标：白帽子让 session 不上报；黑帽子让指定 session 的 token 用量必须上报。

- 白帽子 / 白名单 / 加白：加入 `~/.agentboard/privacy-rules.json` 的 `drop_sessions`，不上报。
- 黑帽子 / 加黑：加入同一文件的 `force_report_sessions`，强制上报 token 用量，绕过个人会话屏蔽及 Codex 默认屏蔽。这里的「黑」不是禁止上报。
- 两种状态互斥，切换时移除该会话的相反规则，不修改其他会话或全局屏蔽规则。

## 做法

听到触发词直接执行对应脚本。用户只要求修改 skill 时，先完成修改；明确要求给当前或指定 session 戴帽子时才实际修改名单。

```bash
# 白帽子：不上报
~/.claude/skills/ab-drop/scripts/drop.sh
~/.claude/skills/ab-drop/scripts/drop.sh <uuid>

# 黑帽子：token 用量必须上报
~/.claude/skills/ab-drop/scripts/report.sh
~/.claude/skills/ab-drop/scripts/report.sh <uuid>
```

未传 UUID 时，依次读取 `CLAUDE_CODE_SESSION_ID`、`CODEX_THREAD_ID`；都拿不到则报错，不猜其他 session。脚本先检查补丁，再去重、原子写入名单；规则运行时读取，不用重打补丁。白帽子保留现有最近 7 个会话的轮换逻辑；黑帽子不随白帽子名单轮换而失效。

## 看结果

- 补丁检查失败或仍命中其他屏蔽规则时，脚本失败且不修改名单。告知具体阻塞，绝不运行 `npx peekaboo-ab setup`。
- 白帽子成功：回复已加白，并提醒「加名单之前已同步过的记录删不掉，只管之后」。
- 黑帽子成功：回复已加黑，后续正常同步必须上报该 session 的 token 用量；保留现有标题和路径脱敏规则，不因加黑关闭脱敏。
- 加入名单只证明规则已设置。用户要求实验或验证上报时，继续核对该 session 的实际同步回执；未取得回执时，只能说「已设为必须上报」，不能声称「已上报」。
