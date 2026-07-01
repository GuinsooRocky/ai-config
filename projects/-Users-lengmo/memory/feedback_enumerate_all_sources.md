---
name: feedback_enumerate_all_sources
description: 用户给一批来源(URL/目录/文件)时，先列全清单逐个核，绝不静默丢；报告要给覆盖率 X/N
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d282902-a6aa-47b0-a5d2-ca193123dd4c
---

用户一次性给多个来源（一串 URL、几个本地目录、几个文件）时：**先把全部 N 个显式列成清单，逐个处理，最后报"X/N 已纳入 + 哪些没纳入及原因"**。绝不静默丢掉其中几个。

**Why**：2026-05-30 做 pageforge v0.0.6 调研，用户给了 15 个 URL + 2 个本地目录(`cc-memory/claude架构学习`、`PRD/技术总结`)。我把清单转录进 workflow 时只配了 12 个 URL（漏 1 微信 + 2 B站），且**整两个本地目录一篇没读**就说"调研完了"。用户连着追问"你都拿了哪八篇""还有其他的你怎么没抓""你研究那两个目录了吗"才暴露。属于"凭状态说完成、没按内容核覆盖"的同类病（见 [[feedback_verify_capture_not_status]]）。

**How to apply**：
- 收到来源清单 → 立刻枚举编号（含本地目录！目录要 ls 出信号文件，别只数 URL）。
- 转录进 workflow/脚本后，回头比对"配置的条数 == 用户给的条数"。
- 交付时明说覆盖率，无关/跳过的项要写明理由，不假装全覆盖。
- 本地目录和网页 URL 一样是"来源"，别只盯着能抓的链接。
