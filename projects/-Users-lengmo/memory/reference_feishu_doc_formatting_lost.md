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

**判 PRD 某条是不是有效要求前，先跑一次删除线+高亮扫描。** 相关：[[feedback_not_ground_truth]]

---

**2026-09-18 补三条（推荐模型批量管理 PRD 反讲时踩的）**

1. **色号别硬记，从文档自己的图例行反查。** PRD 开头那段「红字=重点/黄底=待讨论」的体例说明，每一行**本身就带着对应样式**，拿它当色号字典最可靠。那次实测：`text_color 1`=红 `2`=橙 `5`=蓝，`background_color 3`=黄底 `4`=绿标黄。文档还可能用图例里没定义的颜色（那次有 7 处紫字），照报别归类。

2. **「图例定义了但正文 0 次使用」本身就是结论。** 那份 PRD 黄底（=待讨论）用了 0 次 → 说明 PM 认为已无待议项，反讲挑出来的每一条都是她眼里「已写清楚」的。这句话要写进交付物，不然对方以为你在走流程。

3. **飞书自动编号两个接口都不返回**，get_document 和 list_docx_blocks 都只给标题文字。要 §X.X 就自己按 heading level 数（`block_types:[3,4,5,6,7]` = heading1~5，**参数收数字不收字符串**），数完**必须**拿正文里的交叉引用验证（那次靠 PRD 正文一句「只算 4.1 里计入的 OC」确认推算正确）。没有交叉引用可验就标明是推算的。
