---
name: agentboard-privacy-patch
description: "公司用量统计 peekaboo-ab(agentboard) 已打 v3 脱敏 patch — 非 cmm 会话 title/path/label 上报为 \"personal\"；v3 新增：中途 cd 进 cmm 的会话自动升级为工作会话上报 + force_report_sessions 手动兜底；privacy-rules.json 可整条屏蔽指定 session；更新后需重打"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c1cf47c1-3c0c-4106-a059-b3a2e325eeb9
---

公司用量统计工具 peekaboo-ab（`~/.agentboard/`，Stop hook + launchd `cc.agentboard.sync` 每 60s sync）扫全部 `~/.claude/projects/` + `~/.codex/sessions` 上报到 `https://peekaboo-ab.work/api/checkin`。**不传对话内容**，但传会话标题(title)、完整 cwd(project_path)、project_label、token/时长/活跃窗口。

2026-07-03 已打 **v3 patch**（v2 基础上加两条，沙箱 9/9 + 真实 transcript 端到端验证）：

- **patch 脚本**：`node ~/.agentboard/privacy-patch.mjs apply|check`（幂等，锚点校验，备份 `cli.mjs.orig-*`，原子写入；检测到旧版会提示先恢复备份再打）。**v2→v3 升级须先 `cp ~/.agentboard/cli.mjs.orig-<真原版日期> cli.mjs` 恢复原版再 apply**（真原版=最早那份 orig，2026-07-02）
- **脱敏**：project_path 在 `~/Desktop/cmm` 下 = 工作会话原样上报；其余会话 title/project_path/project_label → `"personal"`；**用量数字（token/时长/消息数）一律不动——token 计不计数只取决于 drop 与否，跟脱敏无关**
- **⭐v3 cwd 升级**：peekaboo 原本 `project_path` 认「首条 cwd、之后不覆盖」（parseTranscripts line ~4279），从 home 开局的会话即便中途 cd 进 cmm 也被钉死成 personal 被 drop。v3 改成「一旦出现 cmm cwd 就升级过去、不降级」（自包含内联 `__abIsCmm`，不依赖注入块作用域）→ home 启→cd 进 cmm 的会话自动按 cmm 真实路径上报，**不用逐个加名单**
- **整条屏蔽 / 强制上报**：`~/.agentboard/privacy-rules.json` 运行时读取，改名单不用重打。优先级：`drop_sessions:[uuid]`（显式屏蔽，最高）> `force_report_sessions:[uuid]`（⭐v3 新增，覆盖 drop_all_personal 的手动兜底）> `drop_all_personal:true`（所有非 cmm 会话全不上报，当前 true）。**cwd 升级已覆盖「cd 进 cmm」主场景，force_report 只作「从不进 cmm 但仍想上报」的边缘兜底**
- **更新会覆盖**：`npx peekaboo-ab setup` 或自升级会重写 cli.mjs → patch 丢失，重跑 apply（顺序：先 privacy-patch.mjs apply 再 upload-count-patch.mjs apply）；用 check 可随时验证
- **⚠️ setup 的 backfill 防不住**：重跑 setup 时 backfill 由 npx 官方包（未打 patch）执行，会把全量历史（含真实 title/path）重传一遍。**别随便重跑 setup**；2026-05 首次 setup 的历史数据本来就已在服务器上，patch 只管之后的增量；服务器上已有记录无法删除（只有 checkin/backfill 两个上行接口）
- **2026-07-03 追加 upload-count-patch(v1)**：`node ~/.agentboard/upload-count-patch.mjs apply|check`。修的是本地 sync.log 的计数 bug——原代码里 `postCheckin()` 命中隐私屏蔽会提前 return（真实网络请求确实没发），但调用方 `syncClaude/syncCodex/syncCursor` 不看返回值、无条件 `uploadedSessions += 1`，导致日志把"屏蔽掉的"也算成"上传了"，容易被误读成"非 cmm 会话还是上报了"。修完后 postCheckin 返回 "ok"/"dropped"/"no-config"，日志区分 `uploaded X, dropped(privacy) Y`。**这只是本地日志措辞修正，不是隐私漏洞修复**——实测当时日志显示 `uploaded 0, dropped(privacy) 2`，证明非 cmm 会话本来就没被真实上传，drop_all_personal 参数([[agentboard-privacy-patch]] 里那个"true=非cmm会话全不上报"的开关)一直在正确生效
