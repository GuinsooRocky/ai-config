---
name: feedback-gates-must-fail-on-purpose
description: 闸/检查/告警类改动必须实测「该红的时候真红」，正例绿不算验过
metadata:
  type: feedback
---

写或改任何闸、守卫、健康检查、告警判据，**验收必须包含失败分支的实跑**。
「跑一遍正例是绿的」证明不了它在该拦的时候会拦。

**Why**：2026-08-22 soliloquy 连着两次。①迁移撞号闸早就存在且对真仓是绿的，
但豁免是按 version 整组放行，往历史撞号组里再塞一个新文件照样绿——洞是靠补两条
「旧闸会放行」的用例才暴露的；而且 `migrate:check` 当时从没进过 CI，等于有检查没有闸
（**已接线**：`.github/workflows/ci.yml` 里有 `run: pnpm migrate:check`（按内容搜，别记行号），migrations 变更时触发）。
②备份新鲜度检查四个分支（新鲜 / 过期 / 无备份 / manifest 损坏）逐个实跑，owner 明确说
「四个失败分支都实测了这点尤其认可」。

**How to apply**：
- 每条判据配一个「本该被它拦住」的用例；改旧闸时，专门补上**旧闸会放行、新闸要红**的那几条。
- 闸写完先问一句：它接进 CI / timer 了吗？没接线的检查不是闸。
- 别为了让它绿去放宽断言（RPO/RTO、关 `--exit-on-error`、跳过必查表都算洗绿），
  差距如实报出来。参见 [[feedback-alarm-needs-a-reader]]。

## 反面验证脚本的卫生（2026-10-13）

临时改坏源码跑测试时，子进程（vitest）卡住被 Bash 超时打断，源码停在了改坏的状态、`.mutbak` 留在仓里，后来还是靠手动比对还原的。

**How to apply:** 每个用例单独起一次脚本；子进程设 `timeout`（或 `perl -e 'alarm N; exec …'`）；还原放进 `finally`，从仓外（scratchpad）的备份拷回而不是 move 仓内备份；跑完 `find src -name '*.mutbak'` 和源码哈希双重确认，再查有没有残留的测试进程。
