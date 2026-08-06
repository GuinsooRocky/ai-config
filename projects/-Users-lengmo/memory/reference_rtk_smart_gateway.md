---
name: reference_rtk_smart_gateway
description: rtk 不再无脑全改写——2026-06-26 起装了智能网关，精度命令默认裸跑、只有大输出命令走 rtk；含路由规则/手动开关/文件位置
metadata: 
  node_type: memory
  type: reference
  originSessionId: b2f171fc-450d-468f-916a-c8d5892b07c7
  modified: 2026-07-30T06:46:48.983Z
---

2026-06-26 把 `settings.json` 里那行 `rtk hook claude` 的 Bash PreToolUse 钩子换成了智能网关 `~/.claude/hooks/rtk-smart.sh`（旧配置备份 `~/.claude/settings.json.bak-rtk-20260626`）。

**起因**：旧钩子无脑把每条 Bash 改写成 `rtk <cmd>`，rtk 的有损摘要静默吞内容——`grep` 返回 `N matches` + `[+12 more]`（真匹配行全没）、`cat`→`rtk read` 只留 ~24%、`ps` 砍 98%。那些 `...done`/`[+N more]` 就是摘要噪声被当输出回显。rtk 二进制本身没坏（正版 rtk-ai 0.42.4，`rtk gain` 累计省 100M token），坏的是"对所有命令默认有损"这件事，对要精确输出的 agentic 编码是对着干。

**网关路由**（默认 RAW 保真，只省真正大的）：
- 精度命令 `git/grep/cat/jq/awk/sed/find/diff` 及一切杂项 → **裸跑**（输出完整忠实）
- 大输出白名单 `*(npm/pnpm/yarn/bun/pip/brew/cargo) install|build|test`、`docker logs`、`eslint`、`tsc`、`vitest/jest/playwright` → **rtk 摘要省 token**（`ps` 2026-08-03 移出：存活判断走摘要有实测假阴性 2-3 vs 8，见 [[feedback_rtk_pipeline_corruption]]）
- 手动开关（写命令尾部，是 shell 注释无副作用）：`<cmd> #rtk` 强制省 / `<cmd> #raw` 强制裸（#raw 优先级最高）
- 改"哪些自动省" = 改脚本里的 `SAVINGS` 正则

**旧钩子时代的绕路（现已不需要，仅 `#rtk` 强制时还适用）**：以前 `git status`/`git diff --stat` 过 rtk 会**漏列文件**——实测 `--stat` 只显示 34 个，`git add -A` 时冒出没列出的 `worldCard.router.ts` 和 proto 子模块，差点把没察觉的改动一起提交。那时的对策是 `git -c core.pager=cat status --porcelain=v1` 或 `rtk proxy git <cmd>` 拿全量。（原 `feedback_git_porcelain_with_rtk` 已并入本条，2026-07-30。）

**How to apply**：现在精度命令默认就是裸跑，**不用再为拿地面真相加 `rtk proxy`/`--porcelain`/落盘**（见 [[feedback_rtk_pipeline_corruption]]，已被本网关缓解——但那条里 07-02 的反例仍然成立，别当它完全无害）。要省 token 就主动 `#rtk`。验证生效：跑条 grep 看是不是完整输出而非 `[+N more]`。排错：把钩子 command 换回 `rtk hook claude` 或删掉即整体停用。rtk 仍是第三方只读二进制见 [[reference_rtk_is_third_party]]。
