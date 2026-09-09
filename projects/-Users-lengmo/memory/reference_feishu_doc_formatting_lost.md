---
name: reference-feishu-doc-formatting-lost
description: 读飞书 PRD 用 get_document 会丢删除线/颜色/高亮，判"这条是不是要求"必须改用 list_docx_blocks include_payload
metadata:
  type: reference
---

social-proxy 的 `get_document` 返回纯文本，**删除线、字色、背景高亮全部丢失**。而飞书 PRD 常拿格式承载语义（onlychat 付费图 PRD 自己在开头写了体例：删除线=废除、黄底=待讨论、红字=重点、橙字=可配文本）。纯文本里一条被划掉的废弃需求跟一条生效需求长得**一模一样**。

正确读法：
```
execute_tool(list_docx_blocks, {platform_doc_id, include_payload: true})
```
输出会大到落盘（付费图 PRD 1128 block = 1.2MB），**别读进上下文**，用 python 解析落盘文件：
每个 text run 在 `payload.<block_type_name>.elements[].text_run.text_element_style` 下带
`strikethrough` / `text_color` / `background_color`。

2026-08-31 栽过：拿 `get_document` 做了一份 PRD↔代码文案对照，把三条已被划掉的需求报成「代码缺口」，其中一条还反过来指控另一个会话删得不对——owner 截图指出「你是读不到中划线是吧」。

**判 PRD 某条是不是有效要求前，先跑一次删除线+高亮扫描。** 相关：[[feedback_comments_not_ground_truth]]、[[feedback_truncated_output_is_not_ground_truth]]
