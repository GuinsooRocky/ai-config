---
name: feedback_no_dev_details_in_product
description: 产品界面不放「查看技术详情」这类开发信息；原始报错只进日志，界面只给人话和下一步
metadata:
  node_type: memory
  type: feedback
  originSessionId: 409de390-e3af-4d4d-bd6f-5d8b00f0d6f9
  modified: 2026-10-30T18:13:47.948Z
---

产品界面不放「查看技术详情」、原始报错、错误码这类东西，折叠起来也不行。用户要的是一句人话和下一步（比如「模型额度用完了，3:33 之后可以再试。」），原始错误只进日志。

**Why:** 2026-10-31 lich 全 App 收口时我把「查看技术详情」做成了共用部件，owner 截图顶回：「整个项目都不需要，那是开发需要的东西，不是用户需要的」。把英文报错收进折叠只是藏起来，不算处理。

**How to apply:** 写失败提示时，先想用户此刻能做什么，把它写进文案；认不出的错误给通用中文，不露原文。派工说明里不要把「技术详情」当成规范写进去。相关：[[feedback_no_jargon_plain_product_language]]
