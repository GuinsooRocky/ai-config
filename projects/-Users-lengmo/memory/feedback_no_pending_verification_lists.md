---
name: feedback-no-pending-verification-lists
description: 别给「待验清单」、别把改动标成未验证——用户一直在实时验，不说话就是验过了
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5cf71676-c2bb-4b3b-8f2d-f486571b280a
  modified: 2026-08-10T13:02:54.032Z
---

交付改动时不要输出「待验清单」，也不要用「这几条还没验，验完再决定下一步」当理由拖住后续工作。

**Why:** 用户原话「没验证的改动就是伪命题 因为 我一直在验证 我不说你可以默认我验证了」。他是边改边点的，
每轮都在真机/浏览器上过一遍；我列清单等于要求他重复汇报已经做过的事，还顺带把「等你验完」变成不动手的借口。
同一轮里他还说「一定要动 只有动了 做成真正的链路了 才能看出新问题」——链路不完整时的「谨慎分批」对他是负价值，
因为半成品暴露不出真问题。

**How to apply:** 改完直接说改了什么、为什么；要提醒就只提**具体现象**（「书还在飞那 210ms 里底边可能多一道暗边，
看到了跟我说」），不要罗列成表格式的验收清单。沉默 = 通过；他有问题会直接说。
需要他配合的只剩那种我拿不到的运行时事实（控制台读数之类），那时精确到一句话、一个数字，别扩成清单。

相关：[[feedback_just_do_no_stop_suggestions]]、[[feedback_task_execution_cadence]]、
[[feedback_runtime_bug_dont_loop_static]]
