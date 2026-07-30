---
name: feedback_rtk_pipeline_corruption
description: rtk hook 会改写管道里的首个命令，过滤后的残缺流喂给下游解析器导致 JSON 报错；机器消费的输出必须绕过 rtk
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ceab74e4-7fa6-4edd-b8ed-19dcc9fa01a3
  modified: 2026-07-30T06:47:32.107Z
---

**⚠ 2026-06-26 更新**：已装智能网关 [[reference_rtk_smart_gateway]]——精度命令(含 curl/grep/cat/管道首命令)默认裸跑不再过 rtk，本条描述的污染大部分已被缓解。下面是旧钩子（无脑全改写）时代的踩坑记录，仅当走 `#rtk` 强制或命中 savings 白名单时仍适用。

**⚠⚠ 2026-07-02 反例：智能网关"已缓解"太乐观，同日两个 session 各中一次**：① `ps aux | grep claude` 走 rtk（ps 在 savings 白名单）被摘要成**零结果**——查无进程的假阴性，差点误判并发 session 已死；`/bin/ps` 绝对路径立刻全出来。② 另一 session 的长输出（grep/Read 尾部）被注入 `count /<invoke>`、`next` 等碎片——**这些碎片长得像工具调用语法，混进上下文后诱发该 session 连锁 malformed 工具调用 + 自我强化**（坏样例污染 next-token 分布），最终连"虚报完成"都与此同根。教训升级：**长输出/机器判断用的输出，一律落盘 + Read 回读，不信管道里看到的**；"查无 X"结论必须绝对路径复核一次才算数。

rtk PreToolUse hook（`rtk hook claude`）改写命令时**不识别管道语境**：`curl ... | python3 -c "json.load(...)"` 被改写成 `rtk curl ... | python3 ...`。rtk 对 curl stdout 做 token 截断/加注（完整输出 tee 到 `~/Library/Application Support/rtk/tee/*.log`），下游 python3 拿到的是残缺 JSON → `Invalid control character` / `Unterminated string`。实测 2026-06-12：GitHub API 5197 字节合法 JSON，tee 日志完整，管道下游收到的是截断版。

上游状态：管道改写 bug = issue #1560（P1-critical），已有多个 open PR 无人 review，**别再提重复 PR**。（原文另记的 `rtk ls` locale 误报已由上游 v0.39.0 修掉，2026-07-30 清理。）

**Why:** rtk 的过滤是给模型眼睛省 token 设计的，不是给机器消费设计的；混进数据管道就是数据损坏，而且报错形态（JSON 解析失败）会误导去怀疑数据源（GitHub API / curl）而不是 rtk。

**How to apply:** 输出要被下游程序解析（pipe 给 python/jq/wc、`$(...)` 捕获）时，三选一绕过 rtk：① `rtk proxy <cmd>` 跑原始命令；② 用绝对路径（`/usr/bin/curl`、`/bin/ls`）——hook 只匹配裸命令名；③ 先 `curl -o /tmp/x.json` 落盘再解析文件。怀疑 rtk 截断时去 tee 目录找完整输出。同根问题已并入 [[reference_rtk_smart_gateway]]。
