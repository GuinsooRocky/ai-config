---
name: reference_rtk_smart_gateway
description: RTK 当前口径——第三方只读二进制（想改只能提 upstream）、现存污染形态（吃参数报假「未知选项」/碎片注入/管道截断/包 vitest 挂死）+ zsh grep 邻坑；网关路由细节见 ~/.claude/RTK.md
metadata:
  node_type: memory
  type: reference
  originSessionId: b2f171fc-450d-468f-916a-c8d5892b07c7
  modified: 2026-08-26T07:15:24.520Z
---

# RTK 当前口径

> 网关路由（白名单、`#rtk`/`#raw` 开关、钩子路径）见 `~/.claude/RTK.md`——它经 CLAUDE.md 的 `@RTK.md` 每会话必载，本条不复述，只记 RTK.md 里没有的三块。

**身份**：RTK = 第三方开源工具 `github.com/rtk-ai/rtk`，**不是 lengmo 的仓**。本机只有预编译二进制 `~/.local/bin/rtk`（arm64，curl install.sh 装的，非 brew），无源码——想改它只能提 upstream（已提 CCR 缓存 issue [#2485](https://github.com/rtk-ai/rtk/issues/2485)）或 fork 自维护，不能本地 edit。管道改写 bug = 上游 #1560（P1），已有多个 open PR，**别再提重复 PR**。已有能力：`rtk learn`、`rtk proxy`（逃生口）；`rtk cache` 不存在。

## 现存污染形态（走 `#rtk` 或命中白名单时仍会发生）

1. **吃参数报假「未知选项」（2026-08-25）**：`npx vitest list --filesOnly --changed` 报 `CACError: Unknown option --filesOnly`，日志头 `[RTK:PASSTHROUGH] vitest parser: All parsing tiers failed`——网关解析失败把参数丢了，`#raw` 立刻正常。**危害在于它长得像「工具不支持」**：子 agent 据此跳过干跑熔断、被 859 文件全量炸到。凡 build/test 类命令报「未知选项/参数非法」，先 `#raw` 复验再下结论，别改命令迁就。
2. **碎片注入（2026-07-02，未根治）**：长输出尾部被注入 `count /<invoke>` 等长得像工具调用语法的碎片，混进上下文诱发连锁 malformed 调用 + 自我强化。铁律：**长输出/机器判断用的输出一律落盘 + Read 回读，不信管道里看到的**；「查无 X」结论必须绝对路径复核一次才算数。
3. **管道语境不识别（上游 #1560）**：`curl ... | python3` 被改写后下游拿到截断 JSON，报错形态（JSON 解析失败）会误导去怀疑数据源而不是 rtk。输出要被下游程序解析时三选一：`rtk proxy`、绝对路径（hook 只匹配裸命令名）、先落盘再解析。完整输出在 `~/Library/Application Support/rtk/tee/*.log`。

4. **包 vitest 会挂死不返回（2026-09-09）**：命中白名单的 `npx vitest run <files>` 被改写成 `rtk vitest ... --reporter=json`，进程**永远不退**、输出文件恒 0 字节，只能靠 `ps` 看 ELAPSED 判死。同一批文件 `#raw` 直跑 **472ms**。本机当场捞出两个前次留下的僵尸：一个跑了 **20 小时**、一个 **2 天**，全是 `--reporter=json` 形态。**跑测试一律 `#raw`**；发现「测试跑很久没输出」先 `ps -o etime` 查是不是这个，别当测试慢等下去。

**邻坑（非 rtk，同类误判，2026-08-25）**：zsh 下 `grep --include=*.ts` 会因 glob 展开整条中止（`no matches found`），grep 根本没跑，空输出被读成「符号不存在」报过假结论。`--include` 的值必须加引号；**空结果先确认命令真的执行过**。

**验证网关生效**：跑条 grep 看是完整输出还是 `[+N more]`。
