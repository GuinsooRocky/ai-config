---
name: feedback-gates-must-fail-on-purpose
description: 闸/检查/告警类改动必须实测「该红的时候真红」，正例绿不算验过；上自主 loop 前必须先有可机械判定的 back-pressure，但 back-pressure 要配任务——纯改造 loop 的 done=改了即可，别默认塞测试/eval；骨架怎么搭归 loop-forge skill
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7ea49df9-4ecd-41a9-999f-cd80a8377ddd
  modified: 2026-11-02T07:52:57.015Z
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

## 上 loop 先补 back-pressure

想让个人项目"用上 loop"(自主回环)前,判据(2026-06-17 跟用户拆透):

**核心判据:上 loop 前必须先有 back-pressure(可机械判定的检查),否则 loop 只会更快产 slop。**
Ralph(Geoffrey Huntley)/老皮 Loop 05/07 的铁律:完成与否由独立检查说了算,不是 agent 自己说。
Huntley 还有一条——Ralph 只适合**绿地项目**,不碰庞大已有库(这也印证了用户"cmm 公司项目上 loop 太危险"的直觉)。

> **怎么搭已归 `loop-forge` skill,别在这里找做法**:两种形态判定(backlog 型「把 X/Y/Z 做完」vs guardian 型「守住别变红」)、验收命令探测、干净工作区闸(`git status --porcelain` 非空拒跑)、**绝不 `git add -A`** 的 scoped commit、`loop/` 脚手架与自带执行器脚本,全在 `~/.claude/skills/loop-forge/`(SKILL.md `:27`/`:29`/`:109` + `references/templates.md`)。老骨架 `~/Desktop/my-code/dk/ralph/` 仍在(smoke_test.py / guard.sh / loop.sh / PROMPT.md / fix_plan.md,另有 PRINCIPLES.md、close-batch.sh),当参考实现看。本文件只留 skill 没接管的两条裁决。

**裁决一——back-pressure 要配任务,别默认上测试/eval:** 先切清"改(edit) vs 验(verify)"。用户说"做个 loop 改造 X"——"改造"常=只改代码,**做完一条 = 那处改了(看文件即可)**,别擅自把跑测试/跑 eval/生码/质量"变好没"塞进 loop 当刹车(那多半是用户以后自己的事;塞了既复杂又撞"自动判=刷分"死结)。纯改造 loop 的 check = grep 改动落没落,不跑任何东西。

**裁决二——"生成一个 loop"= 交付产物,不是我代劳:** 给 loop 骨架(fix_plan/check/PROMPT)+ 驱动 prompt,别跳过 loop 自己手动把活干了、别搭一堆没要的验证基建。报进度只报"清单第几条改了",**绝不报工具内部测试条数**(如"212 测试绿"——跟用户任务无关的内部数字,纯噪音)。

相关:[[feedback_owner_decision_interaction]] §2——**闸 ≠ 摆给用户的菜单**:back-pressure 该自己焊进去悄悄兜住,别做成开跑前的 gate-check + 选择题(用户原话"做个loop 这么难?那就开个ultracode"就是被这么挡住的)。另 [[project_codegen_workflow]]。
