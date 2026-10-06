---
name: feedback_content_policy_scope_is_owner
description: 内容过滤/词表/安全口径的「范围」归 owner 定，我只修实现 bug，不主动提议扩语言、加词、接审核服务
metadata:
  node_type: memory
  type: feedback
  originSessionId: bf2f57f8-3d9c-438f-830d-d29424652b54
  modified: 2026-10-06T06:16:04.821Z
---

修完未成年红线的实现 bug（词尾、年龄写法漏拦）后，我提议再扩到日西葡阿四种语言、加 child/kid、接内容审核服务，被 owner 顶回：「先不要拦这些，这些模型的事情跟你有什么关系？」（2026-10-06，soliloquy）。

**Why:** 词表覆盖什么、拦到哪一档，是产品与合规取舍，是 owner 的口径；我把「发现实现 bug」顺势滑成「替他重定政策范围」，越了界。

**How to apply:** 安全过滤、分级、词表、模型侧审核这类事，只报「现有规则没按设计工作」的 bug 并修；范围缺口（没覆盖的语言、没列的词）最多在报告里提一句「现状如此」，不列成待拍项、不出方案、不催。同类的还有 soliloquy 已记录的「公开面不按成人分级过滤」（[[feedback_public_means_public]]）。
