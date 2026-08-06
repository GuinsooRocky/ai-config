---
name: feedback_daily_recap_retired
description: 每日复盘(daily-recap)整套已于 2026-08-06 废弃删净；用户要的是月度「工作模式体检」那种深度自评，别再提议重建日报
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74a8bfce-99eb-4280-9718-a755ba1b00b0
  modified: 2026-08-06T12:29:54.564Z
---

2026-08-06 用户说「每日复盘我不需要了，脚本也可以删」，整套 daily-recap 已删净（输出 md、skill、workflow、automation 脚本、settings.json 的 SessionStart 钩子）。同一句话里补充：「我更需要的是这个 `~/Desktop/archives/self/工作模式自评-2026.08.04.html`」——即月度深度体检（作息/并行切换/完成率/委派纠偏/制度打架，带行动清单和 30 天复测基线），不是每天一行流水账。

**Why:** 日报只记「干了啥」，用户从中拿不到决策；体检从同一份 jsonl 里读出「哪类活卡住、为什么卡」，才值得花 token。

**How to apply:** 别再提议重建日报或"轻量版日报"。想做周期性自我观测就往体检那个粒度走（月度、有归因、有可复测的数）。数据源没丢——`~/.claude/projects/-Users-lengmo/*.jsonl` 还在，体检随时能重跑。相关：[[user_xiaohongshu_blogger]] 的选题线原本吃日报，现在要改吃别的素材源。
