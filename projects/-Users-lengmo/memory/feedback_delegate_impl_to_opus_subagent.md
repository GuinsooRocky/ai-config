---
name: feedback-delegate-impl-to-opus-subagent
description: 派工三条独有增量：>50KB 逐条判断类先压缩输入、浏览器走查/点验也算执行要派 visual-qa、子 agent 测试产出用 per-file JSON reporter 验收（选 model 的口径在 model-dispatch §2）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1a98655-f407-4a08-98df-2abae18cf430
  modified: 2026-08-06T12:54:16.380Z
---

> 选型口径（显式写 `model` 别靠继承、档位 ≥ 任务所需、拿不准往上取、2026-08-06 主会话默认换 Fable 后仍显式 `opus`）以及「独立派工放同一条消息并行发」已全量落 `~/.claude/model-dispatch.md` §2/§7，本文件只留那边没有的三条。

**Why:** 2026-07-10 onlychat create component test 战役连续三次纠偏（派 sonnet 扫路由被改 opus、主对话亲写测试被打断「用子agent opus 写就行」、串行写 4 个测试文件被问「不可以开3个子agent一起吗」）催生了制度化；之后又长出三条 model-dispatch 覆盖不到的执行面裁决，记在这里。

**How to apply:**

**① 派工前先压缩输入（2026-07-27）**：派 agent 标注一份 182KB 的清单（133 条），我图省事直接把整个文件丢给它，一趟烧 174k token，用户当场质疑「写文件花 174.4k？」。**贵不在写，在读**——长文档进了 context，agent 每多说一句都要把它重带一遍，40 个工具调用 = 那笔底子被重复计 40 次。判据：
- 逐条分类/标注/核账类 → **先用命令抽结构**（标题行、编号、关键字段）几 KB 丢过去，**只对判不准的那几条再读全文**
- 需要全文的场合（写代码、改逻辑、审 diff）照旧给全，别为省 token 让它盲改
- 粗判据：**输入 > 50KB 且任务是「逐条判断」= 该压缩了**
- 同日实测对照：审查那批 25 个 agent 是值的（挖出 82 条真缺陷、两条 P0 赶在迁移固化前修掉）；**贵得没道理的恰恰是「读长文档做标注」这种活**

**② 浏览器走查/点验也算执行（2026-07-16 边界扩大）**：主 agent 亲自跑浏览器截图走查（HTML 交付验收）被叫停——「这件事要拿子agent来做啊 主agent 只用来做 决策 思考 调度」。执行类不止写码/扫描：**浏览器走查、点验、跑验证一律派子 agent（走查归 visual-qa），主对话只列 checklist + 收报告裁决**。

**③ 验收子 agent 的测试产出（2026-07-11 create-test 战役）**：主对话勾选清单前用 per-file JSON reporter 逐文件核用例数，别只看总绿；并且 agent 别 mv 自己的产出文件（第八波 mv 丢过文件）。
