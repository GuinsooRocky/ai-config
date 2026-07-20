---
name: feedback-delegate-impl-to-opus-subagent
description: 跨项目派工偏好：实作/扫描/调研类子 agent 一律显式 model=opus，别沿用主会话模型；主对话别亲写代码
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1a98655-f407-4a08-98df-2abae18cf430
---

2026-07-10 onlychat create component test 战役中用户连续三次纠偏：① 我派 sonnet 扫 edit 路由被打断改 opus；② 我主对话亲写测试文件被打断，"用子agent opus 写就行"；③ 我派单个 agent 串行写 4 个测试文件，被问"不可以开3个子agent一起吗"——互不踩文件的独立产出就该并行扇出，共享写点（如清单勾选）收回主对话消冲突。

**Why:** 用户对该战役的期望是主对话做编排/裁决，写码和扫描下放子 agent，且模型直接上 opus（不按 model-dispatch 默认的 sonnet 主力档）。主对话亲写烧主上下文，与[[project-fable-legislation]]的"指挥官不下场"一致，但模型档位偏好比制度文件写的更激进。

**How to apply:** 测试/实作/扫描/调研类派工默认 `model: opus`，**显式写进 Agent 调用，别省略靠继承**（主会话常是 sonnet，继承=降档）；主对话只做范式设计、清单维护、验收跑命令。

**2026-07-10 升制度：** 偏好已非 onlychat 专属——当日另一会话派"竞品定价页与免费额度调研"又沿用主模型，被叫停换 opus，一天数起。已写进 model-dispatch.md §2（显式指定为默认、调研/实作/扫描归 opus 档、拿不准往上取）。

**2026-07-16 边界扩大：** 主 agent 亲自跑浏览器截图走查（HTML 交付验收）也被叫停——"这件事要拿子agent来做啊 主agent 只用来做 决策 思考 调度"。执行类不止写码/扫描：**浏览器走查、点验、跑验证一律派子 agent（走查归 visual-qa），主对话只列 checklist + 收报告裁决**。
