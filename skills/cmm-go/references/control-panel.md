# 控制面板 — 格式 + 漂移检测

面板是 cmm-go 的正脸。目的：把"我拿到了啥"摊开（准，用户能纠）+"可拉哪些缓存"做成菜单（快，按需拉）。出完面板就停，等用户点菜。

## 格式

```
📍 onlychat · <昵称>
────────────────────────────────
worktree   <目录名>                          ✓
分支       <git branch --show-current 实时>
需求       <表里的一句话>
上次干到   <git log -5 --oneline 顶一两条>
watchdog   <见 watchdog.md 判定（基于 3000 实际 cwd，不是 watchdog 进程参数）：
            ● 已运行(本session跳过) / ● 已自动启动(首次开工自起) / ⚠ 3000 实际跑 <X>>
<可选>     （watchdog 参数=<Y>，跟 3000 实际不符；dev 挂会重启回 <Y>）
群         <见下 §群同步指示灯；条目无 `群:` 则整行不出>
<可选>     ⚠ 这个 worktree 现在在 <live branch>，
           上次见到的是 <last-seen branch>——换活了吗？

可拉缓存
  PRD     <有指针:●指针 / 无:○现搜飞书>
  Figma   <●/○>
  后端文档 <●/○>
  ─ 低档，干到那步再拉 ─
  埋点 / i18n / 接口     ○按需
  📱 LAN 测试           ○按需  （见 lan-test.md）
  坑      <memory 条目名，逗号分隔>
```

没匹配到 worktree 时，把 `worktree/分支/需求/上次` 那块换成 worktree 选择列表：
```
没匹配到「<用户说的>」。现有 worktree，选一个：
  [1] onlychat-world-book      lengmo_..._world_book_ui
  [2] onlychat-next15          lengmo_..._next15_turbopack
  [3] onlychat                 develop
  ...
```

## 群同步指示灯（只读，不替用户起同步）

**为什么有这一格**：social-proxy 的群消息是「同步进 DB 才读得到」，`get_history` 不会现去飞书拉。
一个群掉出同步队列时，「没同步」和「群里真没人说」**返回的都是空** —— 会让人一起推断错。
2026-08-27 就栽过一次：付费图那个群没进队列，当天消息读不到，差点当成「群里没人回」。
（同类立法见 memory: `feedback_alarm_needs_a_reader` —— 别装哑铃。）

**怎么判**：条目有 `群:` 时，跑一次
`execute_tool(name="list_sync_tasks", args={"platform":"feishu","status":"queued","limit":20})`
（queued 才是 cron 每分钟真在轮询的；paused 的是历史群，不会更新）。
拿 `thread_name` 跟条目的群名比：

| 情况 | 面板显示 |
|---|---|
| 命中 queued | `群         ● <群名> · 同步中（<updated_at>）` |
| 没命中 | `群         ⚠ <群名> · 不在同步队列 —— 现在拉到的可能不是最新，起吗？` |
| 命中但 `history_done: false` | `群         ◐ <群名> · 历史回填中（已 <progress_synced> 条），老消息可能还没到` |

**边界**：
- 只报状态，**不自动 `start_sync_task`** —— 起同步是写动作，等用户点头（面板的规矩是出完就停）
- 用户说「起吧 / 同步」→ `start_sync_task({task_id})`，起完说一句「cron 每分钟 tick，等一轮再读」
- 这一格失败（MCP 没连 / 超时）→ 整行降级成 `群  ○ 状态未知`，**不要卡住面板**
- 私聊（`chat_type: dm`）同理，用同一格

## 漂移检测（分支变了就报警，不默默给过期信息）

状态文件 `~/Desktop/cc-memory/onlychat/.last-seen.json`，结构：
```json
{ "/Users/lengmo/Desktop/cmm/onlychat-world-book": {"branch": "lengmo_...", "ts": "2026-05-26 22:00"} }
```

流程：
1. 读现在的分支 `live = git -C <wt> branch --show-current`
2. 从 .last-seen.json 取这个 worktree 的 `seen`
3. `seen` 存在且 `seen != live` → 面板加一行 ⚠ 漂移告警（"上次见 seen，现在 live，换活了吗"）
4. 无论是否漂移，把 `<wt> → {live, now}` 写回 .last-seen.json（用 jq 或直接重写 JSON）
5. `seen` 不存在（第一次见）→ 不告警，只记录

注意：漂移告警只是**提示**，不替用户决定。用户确认换活了，就把 features.md 里这条的"需求一句话"等更新（问用户要不要更）。

