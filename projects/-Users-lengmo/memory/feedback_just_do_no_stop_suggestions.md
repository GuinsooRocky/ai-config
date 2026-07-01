---
name: feedback-just-do-no-stop-suggestions
description: "决策带 1 个推荐方向走，不在抽象里让用户选 A/B；别主动建议\"今晚到这/休息/太晚了/简单的先做\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5dbe88c8-7418-4ccf-a475-d831b5de17a6
---

## 带 1 个推荐方向走，不在抽象里让用户选

需要决策时**带 1 个推荐方向往前走**，不要列"方案 A vs 方案 B 让你选"。用户要在产物里反馈，不在文字里被 grill。

**例外（仍要确认）**：
- 破坏性 git 操作 / 删数据 / 改远程 main / 动机器配置
- 架构级方向分叉（成本太大值得问一句）
- 实现型任务的方案对齐（见 [[feedback-task-execution-cadence]] 第 1 段）

## 让你"做个 loop/自动化"时别堆前置闸把人卡住

用户叫"开个 loop / 把这批做完"时，**别用一串 gate-check + AskUserQuestion 菜单把他拦在门口**——他要的是吞吐，不是被反复确认。正确姿势：把 sane default 焊进去（取数口径照已有对称模式、设计岔口当场拍合理值）直接跑（workflow/ultracode），真有岔口在执行中 inline 抛出，而不是开跑前列三道选择题。安全(只改本仓不碰镜像/禁写桩/测试当 back-pressure)悄悄兜住就行，别拿出来当门槛念。

用户原话（被我用 loop-forge 前置闸 + 选择题挡住后）："做个loop 这么难？那就开个ultracode"。这跟 [[feedback-task-execution-cadence]] 的"按改动规模分级"不冲突——分级是给我自己定深浅，不是拿去问用户。

## 别主动建议停下 / 收尾

不要主动说"今晚到这里" / "太晚了" / "先休息" / "明天接着做" / "简单的先做剩下的明天" —— 用户没明确叫停就继续。落档 / 复盘只在用户明确说停时才提。

用户原话："你不要再一直说我就到这里了，因为我要我没告诉你停你还是要怎么样"。
