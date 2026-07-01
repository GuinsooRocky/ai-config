---
name: reference_rtk_smart_gateway
description: rtk 不再无脑全改写——2026-06-26 起装了智能网关，精度命令默认裸跑、只有大输出命令走 rtk；含路由规则/手动开关/文件位置
metadata: 
  node_type: memory
  type: reference
  originSessionId: b2f171fc-450d-468f-916a-c8d5892b07c7
---

2026-06-26 把 `settings.json` 里那行 `rtk hook claude` 的 Bash PreToolUse 钩子换成了智能网关 `~/.claude/hooks/rtk-smart.sh`（旧配置备份 `~/.claude/settings.json.bak-rtk-20260626`）。

**起因**：旧钩子无脑把每条 Bash 改写成 `rtk <cmd>`，rtk 的有损摘要静默吞内容——`grep` 返回 `N matches` + `[+12 more]`（真匹配行全没）、`cat`→`rtk read` 只留 ~24%、`ps` 砍 98%。那些 `...done`/`[+N more]` 就是摘要噪声被当输出回显。rtk 二进制本身没坏（正版 rtk-ai 0.42.4，`rtk gain` 累计省 100M token），坏的是"对所有命令默认有损"这件事，对要精确输出的 agentic 编码是对着干。

**网关路由**（默认 RAW 保真，只省真正大的）：
- 精度命令 `git/grep/cat/jq/awk/sed/find/diff` 及一切杂项 → **裸跑**（输出完整忠实）
- 大输出白名单 `*(npm/pnpm/yarn/bun/pip/brew/cargo) install|build|test`、`ps`、`docker logs`、`eslint`、`tsc`、`vitest/jest/playwright` → **rtk 摘要省 token**
- 手动开关（写命令尾部，是 shell 注释无副作用）：`<cmd> #rtk` 强制省 / `<cmd> #raw` 强制裸（#raw 优先级最高）
- 改"哪些自动省" = 改脚本里的 `SAVINGS` 正则

**How to apply**：现在精度命令默认就是裸跑，**不用再为拿地面真相加 `rtk proxy`/`--porcelain`/落盘**（那是旧钩子时代的绕路，见 [[feedback_rtk_pipeline_corruption]] [[feedback_git_porcelain_with_rtk]]，二者已被本网关缓解）。要省 token 就主动 `#rtk`。验证生效：跑条 grep 看是不是完整输出而非 `[+N more]`。排错：把钩子 command 换回 `rtk hook claude` 或删掉即整体停用。rtk 仍是第三方只读二进制见 [[reference_rtk_is_third_party]]。
