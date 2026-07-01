---
name: feedback_loop_needs_backpressure_first
description: 给个人项目上自主 loop 前先补 back-pressure;两种 loop 引擎分清(测试型 guard vs 需求型 Ralph)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 06862612-799e-47ff-be06-7b1d5074ae41
---

想让个人项目"用上 loop"(自主回环)前,判据与做法(2026-06-17 跟用户拆透):

**核心判据:上 loop 前必须先有 back-pressure(可机械判定的检查),否则 loop 只会更快产 slop。**
Ralph(Geoffrey Huntley)/老皮 Loop 05/07 的铁律:完成与否由独立检查说了算,不是 agent 自己说。
Huntley 还有一条——Ralph 只适合**绿地项目**,不碰庞大已有库(这也印证了用户"cmm 公司项目上 loop 太危险"的直觉)。

**两种 loop 引擎要分清(用户最初困惑点):**
- **测试型 / 守卫**:引擎 = 跑测试。目的=别让一致性变红。源文件一变就重跑检查,绿心跳/红报警。不需 backlog、不需干净树、不 commit、现在就能跑。
- **需求型 / Ralph**:引擎 = 任务清单(fix_plan.md)。目的=把待办干到清空。`while: cat PROMPT.md | claude -p` 每轮全新 context,挑一件→改→过测试→只提交本轮文件→退出;状态全在磁盘(fix_plan + git commit),不靠上下文记忆。

**Ralph 前置条件(血泪):** 必须干净已提交基线 + scoped commit(逐个 `git add <file>`,**绝不 `git add -A`**——会把未提交手改全裹进一个驴唇不对马嘴的提交,违背用户"不明说不提交")。loop.sh 开头要 `git status --porcelain` 非空就拒跑。

**back-pressure 要配任务,别默认上测试/eval:** 先切清"改(edit) vs 验(verify)"。用户说"做个 loop 改造 X"——"改造"常=只改代码,**做完一条 = 那处改了(看文件即可)**,别擅自把跑测试/跑 eval/生码/质量"变好没"塞进 loop 当刹车(那多半是用户以后自己的事;塞了既复杂又撞"自动判=刷分"死结)。纯改造 loop 的 check = grep 改动落没落,不跑任何东西。

**"生成一个 loop"= 交付产物,不是我代劳:** 给 loop 骨架(fix_plan/check/PROMPT)+ 驱动 prompt,别跳过 loop 自己手动把活干了、别搭一堆没要的验证基建。报进度只报"清单第几条改了",**绝不报工具内部测试条数**(如"212 测试绿"——跟用户任务无关的内部数字,纯噪音)。

**已落地资产:** `~/Desktop/my-code/dk/ralph/`(smoke_test.py 4 条链路不变量 + guard.sh 守卫型现跑 + loop.sh/PROMPT.md/fix_plan.md Ralph 型 parked 给 v2)。下个个人项目想上 loop 直接复用这套判据+骨架。相关:[[project_codegen_workflow]]
