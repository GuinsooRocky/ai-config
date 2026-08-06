---
name: feedback-ledger-close-on-done
description: 销账即回勾——报告完成的同一轮回勾台账/清记忆假待办/销人工闸；08-04 体检抓出账本单向高估欠债的病灶
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c0153ed3-e365-4634-a887-50ea9efcfe66
  modified: 2026-08-06T12:53:39.149Z
---

2026-08-04 工作模式体检进仓核对 21 项，抓出 4 条「活干完了、账没关」：T164 修完 BACKLOG 没回勾、creator_id 07-11 洗完记忆还写「等放行」、T36 拍的是不做记忆记成「23 天没动」、多语言仓内全落自查还写「未落地」。四条方向一致——台账**单向高估欠债**：做完的忘回勾、判不做的仍挂账、执行完的还写「等放行」。后果是用户自我核账偏悲观，且每次「我怎么这么多没做完」的感受都在为并行更多项目提供假理由。

**Why:** 回勾没有「下一个 commit」的推进感，一被打断就沉底；没人负责关账，账就永远停在写完代码那一刻。

**How to apply:**
- 我报告「已合 main / 已上线 / 已修完」的同一轮，主动回勾对应台账：BACKLOG checkbox、memory 假待办、`~/Desktop/archives/self/人工闸.md`。改不动的（工作仓不明说不提交）就明确提醒用户回勾
- 反向也算：拍板「不做」的要记成已关闭，别继续挂着当欠账
- 发现「只有用户本人能做」的活（真机验收/真钱/外部授权/部署占位符/人工标注）→ 追加进人工闸清单，别散落在对话或各仓
- 配套机制：rhythm-guard hook（`~/.claude/hooks/rhythm-guard.sh`）每周首次开工报清单未销数、凌晨 3 点后熔断提醒——收到注入就原样转达

相关：[[project-fable-legislation]]、[[feedback-memory-experiment-vs-adopted]]、[[feedback-comments-not-ground-truth]]
