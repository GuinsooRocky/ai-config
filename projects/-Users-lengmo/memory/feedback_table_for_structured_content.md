---
name: feedback_table_for_structured_content
description: "结构化内容(N 项 × 属性,如\"留什么×为什么\")直接给表格,别埋进散文里让用户自己重新拆"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0ca73b83-b07b-48fe-9957-7e0aaf6a0f1e
---

呈现"几项各带一个属性/理由"这类结构化内容时,用户要的是**直接一张表格**(留什么 | 为什么),他一行行读就行;别把它写成一段散文再让他在脑子里重新拆成表。

**Why:** 散文里藏着的并列项,用户得自己重新切分对齐,费劲;表格一眼就能逐行扫。

**How to apply:** 内容只要是"N 个条目,每条一个理由/属性/对照",默认给表格,不写成流水句。口播项目(OUTLINE-三支柱-v2.html)里:把表格**直接以真 `<table>` 内联进稿子当可视内容**(不是塞 .note、不是给"deck 备注"),念的 `.mic` 只留一句引子(如"它有一份免压清单"),后面跟表;**绝不加"念/不念/deck slide"这类小标题小字标注**——用户嫌啰嗦。表本身别当口播逐字念(那是 PPT 腔),最多口头挑一行展开。关联 [[feedback_writing_taste_umbrella]]。
