---
name: feedback_runtime_bug_dont_loop_static
description: 开关/对称操作类 bug 先并排 diff 两个分支的副作用找不对称；别一头扎进渲染层脑补，也别死磕静态分析绕圈
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 98ffaaa2-91c7-4346-b2f5-cf9a5af08607
---

两类错误叠在一起，都要改：

**A. 对称操作 bug → 先 diff 两个分支的副作用清单。** "开能用、关不行"（或反过来）这种，第一步就把两条分支的副作用并排比，找**不对称的那一项**——它基本就是根因。别因为症状描述成"列表不刷新"就一头扎进渲染/query key/订阅层脑补。

**B. 静态走到"每步看着都对却复现"→ 熔断，别再读码。** 这种 should-work-but-doesn't 八成是运行时（时序/持久化/状态回灌），纯读再读是原地打转：① 拿运行时真相（不能驱动浏览器就明说，别假装能跑）；② 向用户要 1 个判别事实；③ 按最可能判断直接改一版让用户验。

**Why:** 2026-06-25 世界卡 NSFW 开关"开着+18+ 刷新仍开，关掉后首页列表不更新/被顶回"。真因是 `useAge18Agree`：开分支 `onConfirm` 有 `await userPreferenceStore.update(...)` 落服务端，**关分支没有** → 服务端 preference 停在 true → 刷新被同步回灌覆盖本地。修法是关分支对称补上 `userPreferenceStore.update({nsfw:false,flyingNsfw:false})`。我**两段代码都读到了**（开有 update、关只有 setNsfw/setFlyingNsfw），却没并排 diff 出这个不对称，反而绕了 isLoad→header-lag→placeholderData→订阅时序→query key 一大圈全靠脑补，全程没碰浏览器，用户失去耐心自己修了，原话"你好慢"。

**How to apply:**
- 看到 enable/disable、open/close、add/remove、subscribe/unsubscribe 这类成对路径，第一动作是逐项对照副作用（本地 state / cookie / 服务端持久化 / 埋点 / 事件），缺哪项就是嫌疑。
- 持久化不对称是高频根因：一个方向写了后端、另一个只改本地 → 刷新/回灌时被覆盖。
- 第 2 次得出"该工作"就熔断，别开第 3 轮；回路要短，用户给新证据就收敛，别每轮重述全链路（用户也嫌啰嗦）。
- 关联 [[feedback_inline_over_background_workflow]]、[[feedback_task_execution_cadence]]。
