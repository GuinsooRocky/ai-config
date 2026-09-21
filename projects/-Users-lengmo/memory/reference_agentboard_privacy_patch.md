---
name: agentboard-privacy-patch
description: "公司用量统计 peekaboo-ab(agentboard) 本机已升 2.4.6 + 打 v6 脱敏 patch（2026-09-10 实测：全量 529 条里 401 条个人会话被拦，实发 0 条个人）— 非工作会话 title/path/label 上报为 \"personal\"，privacy-rules.json 可整条屏蔽；2.4.6 起必须 config.json 关 autoUpdate 否则自升级会静默冲掉 patch；永远别跑 npx setup（自带未脱敏全量 backfill）"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c1cf47c1-3c0c-4106-a059-b3a2e325eeb9
  modified: 2026-09-11T06:43:34.411Z
---

公司用量统计工具 peekaboo-ab（`~/.agentboard/`，Stop hook + launchd `cc.agentboard.sync` 每 60s sync）扫全部 `~/.claude/projects/` + `~/.codex/sessions` 上报到 `https://peekaboo-ab.work`。

**上报字段（2.4.6 逐字段核过）**：用量数字（token 各类计数/时长/消息数/工具调用分布/增删行数/文件数）+ `title`（Claude 自动生成的会话标题）+ `project_path`（完整 cwd）+ `project_label` + `model`。**不传对话内容、不传代码、不读 .env/zshrc/keychain**；只读 `~/.claude/projects`、`~/.codex/sessions`、Cursor db 三处，`process.env` 只用 `AGENTBOARD_DISABLE_SELF_UPDATE` 和 `APPDATA`。payload 里的 `token` 字段 = agentboard 登录凭证（本来就该发），跟 API key 无关。

## 当前状态（2026-09-10 迁移完成）

- cli 2.4.6 + `privacy-patch.mjs` **v6**；`node ~/.agentboard/privacy-patch.mjs check` → `PATCHED(v6)`
- `config.json` 带 `"autoUpdate": false`；plist 改走 `sync-runner.sh`（运行时解析 node，不再钉死 nvm 绝对路径）
- 备份：`cli.mjs.orig-2026-09-10` = 干净 2.4.6（重打前先 `cp` 它回 cli.mjs）；`*.bak-pre246-*` = 迁移前的整套旧现场

## ⚠️ 2.4.6 带来的三个新事实

- **自升级**：每次 sync 先去 npm 拉最新 cli.mjs 覆盖自己 → 会静默冲掉 patch。靠 `config.json` 的 `"autoUpdate": false` 挡住（`maybeSelfUpdate` 第 2 行就 return）。**出现 `~/.agentboard/cli.mjs.bak` = 发生过自升级，立刻查 check**。注意重跑 setup 会整份重写 config.json（`JSON.stringify` 直接盖，不是合并），这个 flag 会没
- **Claude 改走批量**：`syncClaude` 不再调 `postCheckin`，改成攒 50 条批量 `postBackfillRaw` → 由 patch 的 `__abPrivacyFilter` 拦。codex/cursor 仍走 `postCheckin` → 由 `__abPrivacyShouldDrop` 拦。三条路都管住了
- **`upload-count-patch.mjs` 已作废**：它修的是 `postCheckin` 返回值，而 Claude 路径已经不走那儿了；别再打（锚点也对不上）。改由 patch v6 自己在 `logs/sync.log` 打 `[privacy] dropped <sid> (list|personal)` 行（**顶层 `~/.agentboard/sync.log` 永远 0 字节**，看它会误判成 daemon 没跑）
- **`uploaded N` 是过滤前的条数**，别当真实上传数。读法：**真实发出 = uploaded − 同一次 run 里的 `[privacy] dropped` 行数**（实测 claude `uploaded 529` + 224 条 dropped = 实发 305）

## 机制

- **脱敏**：`project_path` 在 `~/Desktop/{cmm,my-code,archives,cc-memory}` 下 = 工作会话原样上报；其余会话 title/project_path/project_label → `"personal"`；**用量数字一律不动**——token 计不计数只取决于 drop 与否，跟脱敏无关
- **cwd 升级**：原版认「首条 cwd、之后不覆盖」，从 home 开局的会话即便中途 cd 进工作目录也被钉死成 personal。patch 改成「一旦出现工作 cwd 就升级过去、不降级」→ 不用逐个加名单。Codex 侧更严：只有工具调用明确把 workdir 设在工作目录才升级，仅引用路径不算
- **整条屏蔽 / 强制上报**：`~/.agentboard/privacy-rules.json` **运行时读取，改名单不用重打**。优先级 `drop_sessions`（显式屏蔽，最高，支持前缀如 `"codex:"`）> `force_report_sessions` > `drop_all_personal: true`（当前 true）
- **patch 脚本**：`node ~/.agentboard/privacy-patch.mjs apply|check`。幂等、5 个锚点各校验必须恰好 1 次、对不上就整个拒绝应用（不盲打，exit 1）、备份 `cli.mjs.orig-<日期>`、原子写入。**上游改代码就会打不上，需要人工更新锚点**——2.4.6 就是这么栽的（`postBackfillRaw` 多了 `final` 参数）

## ⚠️ 升级流程：绝不跑 `npx peekaboo-ab setup`

setup 自带 `backfillAll`，用**刚装的未打补丁的代码**扫全部会话上传。2026-09-10 实测：不打补丁跑全量 = 发出 529 条，其中 **401 条个人会话**（soliloquy / eval-arena / home 会话 / memory 目录，标题全是真的）。打了补丁 = 305 条，个人会话 0。

正确路线（daemon 先停）：

1. `launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/cc.agentboard.sync.plist`
2. 备份现场 → `npm pack peekaboo-ab@latest` 解出 `package/dist/cli.mjs`
3. **先在沙箱试打**：`HOME=<沙箱> node <沙箱>/.agentboard/privacy-patch.mjs apply`，锚点对不上就人工改锚点，别动真环境
4. 拷进 `~/.agentboard/cli.mjs` → `privacy-patch.mjs apply` → `check`
5. `config.json` 补 `"autoUpdate": false`
6. `launchctl bootstrap gui/$(id -u) <plist>` → 看 **`logs/sync.log`** 有 `[privacy] dropped` 行才算通

**已上报的删不掉**（服务器只有 checkin/backfill 两个上行接口），drop 只管之后。

## 触发词：「把当前会话放入上报白名单」（及"这个 session 别上报"类变体）

= 让当前会话对 peekaboo-ab 整条免上报。⚠ 用户口中的"白名单"是**保护名单**（不上报），落的配置是 `drop_sessions`（屏蔽名单），别反着理解成"允许上报"。

1. 定位当前 session uuid：scratchpad 路径里的 uuid 段，或按内容指纹 grep `~/.claude/projects/-Users-lengmo/*.jsonl`（[[feedback_session_id_by_content_not_mtime]]，别用 mtime）
2. uuid 追加进 `~/.agentboard/privacy-rules.json` 的 `drop_sessions`（去重）；运行时读取即时生效，不用重打 patch
3. 顺手 `node ~/.agentboard/privacy-patch.mjs check`——patch 不在位时名单没人读；不在位就 apply
4. 如实提醒：该会话此前已上报的快照留在服务器，drop 只管之后
5. ⚠ 时机：会话一进 cmm 等工作目录就升级成工作会话，下一轮 sync（≤60s）就带真标题+当日累计用量上报。**要免报必须在进工作目录之前加名单**（09-11 实例：5d9b9391 从 home 开局，15:24:52 进 cmm/onlychat，15:30 才加名单，中间 7 轮同步全部实发）
