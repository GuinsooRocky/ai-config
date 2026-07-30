---
name: feedback-dont-import-other-project-conventions
description: 在 A 项目干活别把 B 项目的惯例/模版/人名当依据搬过来，文档没写的就是没写
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1a040bc-9e74-4958-986c-8c8581840387
  modified: 2026-07-27T08:57:11.821Z
---

在某个项目做事时，只认这个项目自己文档里写的东西。别人项目的消息模版、发版惯例、负责人姓名，即使文档放在同一个目录下，也不是当前项目的事实。

**Why**: 07-27 crushon-admin 上线，文档只写到「把验证过的 `release-<7sha>` 告诉负责发布的人」——没有消息模版、没点名是谁。我把 onlychat 那份的模版和「林珉（husky）」搬过来当依据摆给 owner，被顶回：「关你什么事情 你不是管 crushon-admin 吗」。

**How to apply**: 当前项目文档没写的，直接说「文档没写」，别用邻近项目的惯例填空再标注「这是推断」——摆出来本身就已经是噪音。跨项目的东西只在 owner 明确问「别的项目怎么做的」时才提。参见 [[feedback_comments_not_ground_truth]]、[[feedback_project_intel_stays_in_project_docs]]。
