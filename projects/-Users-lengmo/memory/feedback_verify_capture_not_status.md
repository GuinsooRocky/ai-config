---
name: feedback-verify-capture-not-status
description: "批量抓取/归档后，要校验真实正文，不能凭状态码就说\"全量完成\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bbd9da7b-902c-465f-bd8a-8eb8f9f1c576
---

批量下载 / 归档 / 抓取后，**不要凭 HTTP 200 或工具的 "ok" 状态就声称完成**——
要抽样或全量校验抓回来的是真内容，不是登录墙 / 空壳 / 占位页。

**Why**：给用户蒸馏 10 本小册时，`archive` 工具全报 "ok"，我就说"全量正文已归档"，
实际大量付费章抓回的是登录墙。用户连续追问才暴露，反复打脸。

**How to apply**：抓取类任务收尾前跑一个检测脚本——按内容特征（正文长度、登录墙关键词）
逐文件判定，给出"真正文 / 墙 / 偏薄"计数，再下结论。宁可说"556/622"也不说"全量"。
相关：[[project-kaka-perspective-skill]]
