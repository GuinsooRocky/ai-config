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

