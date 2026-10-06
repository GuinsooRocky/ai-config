---
name: parallel-subagent-fix-pipeline
description: 多路并行查 bug / 修 bug 的实操教训：额度会打满、并发上限 20、文件归属硬边界、每路配独立审查、按组提交、子代理会往仓内写代理记忆、macOS 无 timeout
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7cb4f5d2-6323-4305-8176-2a7eacf24da5
  modified: 2026-10-06T02:49:16.927Z
---

2026-10-02～06 eval-arena 全量查 bug（23 路猎手 + 22 路对抗核查）与全量修复（3 波 16 路 + 每路独立审查）的教训：

- **额度**：20 路 opus 猎手每路约 55–65 万 token，一波就打满 5 小时额度，两天内还撞过周额度。大规模并行前先按「每路 ≈60 万」估总量，并按波提交，断了不丢活。
- **并发上限 20**：超出的派不出去，报错里写「Do not retry」，等有空位再派。
- **子代理会卡死**：多路同时等「自己起的后台测试」会卡住一天不交卷（截图里 1d 0h）。工单里写明「每修完一条就更新报告」「别等慢测试，没结果的写明由主对话跑」。慢模块（如 test_phase2_formal_execution 11 分钟）由主对话跑。
- **子代理按自带规则往仓内 `.claude/agent-memory/` 写记忆**，并发时互相覆盖索引、大量重复。派工 prompt 必写「不写代理记忆」；事后合并去重，多余的 mv 到 ~/.Trash。
- **macOS 没有 `timeout`/`gtimeout`**：简报里写 `timeout 30` 会让所有路各自踩一遍。改写 `perl -e 'alarm 30; exec @ARGV' <cmd>`。
- **修复用独立 worktree**（基于 origin/main 新分支，`git branch --unset-upstream` 防误推），`.venv` 软链到主检出，前端用 `pnpm install --frozen-lockfile --offline`。同一工作树里多路并行靠**文件归属硬边界**，agent 禁止一切 git 写操作，主对话按组 `git add <路径>` 提交。
- **每路修完配一个 fresh-context 审查**（T5），审查要实跑测试、专攻放宽的闸和改了口径的地方。本次 16 路里 7 路被审查退回返工，退回的全是真问题（写 0 混淆未知、放宽判据漏进程判活、把未知显示成失败、运行时拒收旧配置等）。
- **「生产是否走得到」决定定级**：对抗核查前先用 ssh 只读实查服务器（服务单元、配置键名、账本大小、日志错误码计数），比仓内文档可靠。本次 2 条 P0 因此降为潜伏。

**Why:** owner 原话「多路并行」「把所有都修了」，整套流程跑下来可用，但上述每一条都实际绊过。
**How to apply:** 下次 >10 路并行时照此配置简报、工单、提交节奏；全文记录在 `~/Desktop/loop_project/eval-arena-bugscan-20261002/fix/FIX_BRIEF.md` 与 `FIX_SUMMARY.md`。相关：[[model-dispatch]]、[[feedback_delegate_impl_to_opus_subagent]]
