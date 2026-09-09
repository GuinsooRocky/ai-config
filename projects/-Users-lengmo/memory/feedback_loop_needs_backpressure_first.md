---
name: feedback_loop_needs_backpressure_first
description: 上自主 loop 前必须先有可机械判定的 back-pressure;但 back-pressure 要配任务——纯改造 loop 的 done=改了即可,别默认塞测试/eval;骨架怎么搭归 loop-forge skill
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 06862612-799e-47ff-be06-7b1d5074ae41
---

想让个人项目"用上 loop"(自主回环)前,判据(2026-06-17 跟用户拆透):

**核心判据:上 loop 前必须先有 back-pressure(可机械判定的检查),否则 loop 只会更快产 slop。**
Ralph(Geoffrey Huntley)/老皮 Loop 05/07 的铁律:完成与否由独立检查说了算,不是 agent 自己说。
Huntley 还有一条——Ralph 只适合**绿地项目**,不碰庞大已有库(这也印证了用户"cmm 公司项目上 loop 太危险"的直觉)。

> **怎么搭已归 `loop-forge` skill,别在这里找做法**:两种形态判定(backlog 型「把 X/Y/Z 做完」vs guardian 型「守住别变红」)、验收命令探测、干净工作区闸(`git status --porcelain` 非空拒跑)、**绝不 `git add -A`** 的 scoped commit、`loop/` 脚手架与自带执行器脚本,全在 `~/.claude/skills/loop-forge/`(SKILL.md `:27`/`:29`/`:109` + `references/templates.md`)。老骨架 `~/Desktop/my-code/dk/ralph/` 仍在(smoke_test.py / guard.sh / loop.sh / PROMPT.md / fix_plan.md,另有 PRINCIPLES.md、close-batch.sh),当参考实现看。本文件只留 skill 没接管的两条裁决。

**裁决一——back-pressure 要配任务,别默认上测试/eval:** 先切清"改(edit) vs 验(verify)"。用户说"做个 loop 改造 X"——"改造"常=只改代码,**做完一条 = 那处改了(看文件即可)**,别擅自把跑测试/跑 eval/生码/质量"变好没"塞进 loop 当刹车(那多半是用户以后自己的事;塞了既复杂又撞"自动判=刷分"死结)。纯改造 loop 的 check = grep 改动落没落,不跑任何东西。

**裁决二——"生成一个 loop"= 交付产物,不是我代劳:** 给 loop 骨架(fix_plan/check/PROMPT)+ 驱动 prompt,别跳过 loop 自己手动把活干了、别搭一堆没要的验证基建。报进度只报"清单第几条改了",**绝不报工具内部测试条数**(如"212 测试绿"——跟用户任务无关的内部数字,纯噪音)。

相关:[[feedback_just_do_no_stop_suggestions]] §2——**闸 ≠ 摆给用户的菜单**:back-pressure 该自己焊进去悄悄兜住,别做成开跑前的 gate-check + 选择题(用户原话"做个loop 这么难?那就开个ultracode"就是被这么挡住的)。另 [[project_codegen_workflow]]。
