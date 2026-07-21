# dev-watchdog 生命周期判定

watchdog 脚本：`~/.local/bin/dev-watchdog.sh`（token-free，守一个 worktree 的 `pnpm dev`，phys_footprint ≥ 6G 或端口无监听/HTTP 僵死时自动重启）。设计原理与踩坑教训见 memory: `project_worldbook_dev_oom`。重启/清理/自停的具体行为见下文 [§2026-06-01 强化](#2026-06-01-强化5-点已落地脚本)。

## 判定（第 3 步用）

**核心：以 3000 监听进程的 cwd 为准**，不以 watchdog 进程参数为准。两者会分叉 —— 用户手动 `kill -9 <dev pid>` 再自己 `pnpm dev` 起新 dev 时，watchdog 还活着，但 3000 跑的已经是别的 worktree 了（watchdog 通过 `lsof` 看端口监听者，不认它启过哪个 dev pid）。判定必须看真实在跑的 cwd，不是 watchdog 怎么登记的。

**检测要稳，四条坑（dogfood 实测踩到）**：
- ① 别用宽松的 `pgrep -f dev-watchdog.sh` —— 会匹配到 terminal-notifier 通知弹窗里带的 "dev-watchdog.sh" 文字，**假阳性**。必须卡 `bash .*dev-watchdog.sh` 这种真进程形态。
- ② 状态文件 `/tmp/onlychat-dev-3000.json` 的 pid 可能是**过期死 pid**，必须 `ps -p` 验活才算数；光有文件不代表在跑。
- ③ watchdog 进程参数 ≠ 3000 实际 cwd 时，**信 cwd**（动态），不信进程参数（启动时快照）。
- ④ **macOS 上 `pgrep -af` 只输出 PID 不带 command**（Linux 才是 PID+cmd），必须用 `pgrep -lf` —— 否则 awk 过滤永远拿不到 command 来匹配，靠运气。

```bash
# (1) 3000 真实跑的 worktree —— 唯一可信源
PORT_PID=$(lsof -ti tcp:3000 -sTCP:LISTEN 2>/dev/null | head -1)
PORT_CWD=$(lsof -a -p "$PORT_PID" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')

# (2) 真 watchdog 进程参数（仅 advisory：告诉你 dev 挂时会重启回哪个）
# 注意 macOS 用 -lf 不是 -af
WPID=$(pgrep -lf "dev-watchdog.sh" | awk '/ bash .*dev-watchdog\.sh /{print $1; exit}')
WD_WORKTREE=$(ps -o command= -p "$WPID" 2>/dev/null | awk '{print $NF}')
```

判定看 `PORT_CWD`（不是 `WD_WORKTREE`）：

| 情况 | 面板显示 | 动作 |
|---|---|---|
| `PORT_PID` 空（3000 没人监听） | `● 已自动启动（首次开工自起）` | 直接起，不问。报昵称=开工信号。唯一例外：用户明说"先别起 / 只看不跑 / 收工"就不起 |
| `PORT_CWD == 本 worktree` | `● 已运行（本 session 跳过）` | 不动它 |
| `PORT_CWD != 本 worktree` | `⚠ 3000 实际跑 <PORT_CWD>，不是本项目`（一行，止于此） | **啥都不动**。不问切换、不杀别人。用户自己手动切 |

**额外 advisory line**（不影响判定，仅多给一条信息）：当 `WD_WORKTREE` 非空且 `WD_WORKTREE != PORT_CWD` 时（watchdog 被绕过），加一行：
```
（watchdog 参数=<WD_WORKTREE>，跟 3000 实际不符；下次 dev 挂掉会被 watchdog 重启回 <WD_WORKTREE>）
```
让用户知道"现在跑啥" + "下次挂了会跑回啥"，两个真相都摊开。

## 命令

起（或切到本 worktree，脚本自带单实例自替换）：
```bash
nohup ~/.local/bin/dev-watchdog.sh <worktree绝对路径> > /tmp/dev-watchdog.log 2>&1 & disown
```

刷新 dev（改了路由让 Next 重扫，不双实例）：`pkill -USR1 -f dev-watchdog.sh`

停（彻底，收工）：
```bash
pkill -9 -f dev-watchdog.sh   # 强杀守护：pkill 默认 TERM 会卡在 sleep 90 里最多等 90s 才响应（实测），-9 决断
{ lsof -ti tcp:3000 -sTCP:LISTEN; lsof -ti tcp:3001 -sTCP:LISTEN; } | xargs kill -9 2>/dev/null
# ⚠ 必须卡 -sTCP:LISTEN —— 裸 lsof -ti tcp:3000 会把正在预览的 Chrome 客户端连接一起 kill（实测 pid 命中浏览器）
# 顺序不能反：先停守护再杀 dev，否则会被回拉
```

状态文件 `/tmp/onlychat-dev-3000.json` 里有 watchdog 自报的 pid/footprint/worktree，可读来填面板。

## 2026-06-01 强化（5 点，已落地脚本）

旧版只"按 socket 杀 + 内存超限即重启"，制造了孤儿高 CPU + 误杀预览 + 重启风暴烤热机器。本次改（细节起因见对抗审查结论，根因诊断见 memory: `project_worldbook_dev_oom`）：

1. **kill_tree 按血缘连根杀**：重启先 `pgrep -P` 后序杀整棵 `pnpm→next→worker` 树（`start()` 抓 `DEV_PID=$!`），不再漏留不持 socket 的 `next-router-worker` 孤儿空转烧 CPU（曾实测一个孤儿父进程已死、烧 138% CPU）。
2. **kill_port 卡 `-sTCP:LISTEN`**：不再误杀正在预览的 Chrome 客户端连接（裸 lsof 会把浏览器到 :3000 的 ESTABLISHED 连接也 kill）。
3. **HTTP_FAILS 复位放进 `start()`**：所有重启路径都从干净探活计数起，不把上轮慢编译的失败数带进新 dev → 不跨重启误判僵死。
4. **内存重启加冷却**：`RESTART_COOLDOWN=120` + `MEM_PANIC_MB≈8.6G` 熔断 —— 刚过 6G 的温和超标给新 dev 编译稳定窗、不让重编译尖峰首尾相接；失控暴涨才无视冷却即时重启。
5. **自适应轮询 + idle 判据换信号**：footprint ≥80% 阈值（≈4.9G）时下轮 `sleep` 缩到 15s 压 overshoot；idle 自停从"有没有 iTerm 进程"（iTerm 用户 iTermServer 常驻 → 永不触发的坏逻辑）改成"3000/3001 上有没有浏览器 ESTABLISHED 连接 + 跑满 10h"**双条件才停**。

> 内存根因（world-book dev ~7min 涨到 6G 的泄漏）是源码问题，watchdog 治不了，只能干净地管理（无孤儿/不误杀/压 overshoot）。崩溃→检测→重编译仍有固有空窗（最多 1 个 POLL 检测延迟 + 重编译耗时）。

### 改脚本后如何激活（受控 relaunch）

改 `dev-watchdog.sh` **不影响正在跑的 watchdog**（已加载进内存），必须 relaunch 才生效。安全流程（实测多次）：
```bash
# 1. 强杀旧守护（-9，免 TERM 卡 sleep）
WD=$(pgrep -lf dev-watchdog.sh | awk '/bash .*dev-watchdog\.sh/{print $1;exit}'); kill -9 "$WD"
# 2. 从 3000 监听者爬到 dev 树根，按血缘清整树（别用裸 lsof，避开 Chrome）：
#    lis=$(lsof -ti tcp:3000 -sTCP:LISTEN|head -1)；沿 ps -o ppid= 向上爬到顶层 node；递归 kill -9 它及后代
# 3. 起新 watchdog（见上"起"命令）
# 4. 等就绪（curl 内部重试，别用 sleep 等编译）：
#    curl -s -o /dev/null -w '%{http_code}' --retry 50 --retry-delay 2 --retry-connrefused --max-time 150 http://127.0.0.1:3000/
```

## phase 2（v1 不实现，先记着）

**自动停**：每个 onlychat session 起来时登记自己（写 `/tmp/onlychat-sessions/<session-id>` 存 claude pid）；watchdog 每轮检查"还有没有活着的登记进程"，归零就自杀 + 杀 dev。这样"最后一个 session 关掉就自动收工"，不用手动停、也不用 hook。

> 更新（2026-06-01）：已先用更轻的信号实现了一版 idle 自停（见上 §强化 #5：3000/3001 无浏览器 ESTABLISHED 连接 ≥1h + 跑满 10h → 收工），不依赖 session 登记表。本 phase 2 的 session 登记方案是更精确的替代思路，按需再做；在那之前手动停仍可喊"收工"。
