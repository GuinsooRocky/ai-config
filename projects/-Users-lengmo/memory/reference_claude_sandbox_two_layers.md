---
name: reference_claude_sandbox_two_layers
description: claude 的 settings.sandbox 只包 Bash 子进程，claude 自己的 Read/Grep 读得穿；要配 permissions.deny 做第二层
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2f80354d-2a49-4554-9e73-b712e1b4a74a
  modified: 2026-07-30T08:45:54.593Z
---

`settings.json` 里 `sandbox.filesystem.denyRead` **只约束 Bash 起的子进程**（macOS Seatbelt，
claude 2.1.220 内置 `@anthropic-ai/sandbox-runtime`）。**claude 自己的进程不在沙箱里**，所以它自己的
`Read` / `Grep` / `Glob` / `WebFetch` 完全不受 `denyRead` 约束。

2026-07-30 实测（denyRead 一个目录，同一文件两种读法）：

```
Read 工具       → OK:TOPSECRET-BANANA-42      ← 读穿了
bash python3 读  → BLOCKED PermissionError     ← OS 挡住
```

要闭环得两层：`sandbox.*`（管子进程，含"写个 .py 再跑它"）+ `permissions.deny`（管 claude 自己的工具）。
两层各有各的洞，缺一层就漏。

`permissions` 的路径写法跟 `sandbox` 段不同：**`//` 开头=绝对路径，不吃 `~` 展开**；`sandbox` 段可以用 `~`。
已验证生效的形式：`Read(//Users/x/.ssh/**)`、`Read(//**/.env)`、`Grep(//Users/x/.ssh/**)`。

**规则名/路径写错，claude 静默忽略** —— 配置看起来滴水不漏、实际一点没生效。所以这类配置
必须跑探针验，不能靠读配置确认。参考实现：`~/Desktop/my-code/dk/scripts/sandbox-probe.sh`
（5 探针 + 一个必须 OK 的控制组，防"全挡"其实是把正常活也掐死了）。

姿态问题：`permissions.deny` 只能 deny-list（deny 优先级压过 allow，没法"全禁再开小口"）。
要 allow-list 真边界，得把整个 claude 进程用 srt 从外面包住 —— 详见 [[project_dk_sidecar_deploy]]
相关的 dk/SANDBOX.md。

## 限权的三条实测坑（同日，比上面更容易踩）

1. **`--allowedTools` 不限权**，它只是"免提示放行清单"。实测 `--allowedTools
   "Read,Glob,Grep,WebFetch"` 跑 `echo` 照样成功、`permission_denials` 为空。
   真要摘工具只能 `--disallowedTools`（或 `permissions.deny`）。
   → 凡是靠"从 allowedTools 里剥掉 Bash"实现的限权，全是假的。
2. **按名字 deny 是打地鼠**：`--disallowedTools Bash` 之后 claude 改用 `Monitor` 工具跑了同一条命令
   （原话 "no Bash tool exposed, so I ran it via the Monitor tool, which executes commands in the
   same shell environment"）。要按能力列全：Bash/BashOutput/KillShell/Monitor（跑命令）、
   Task/Agent（子 agent 自带 Bash）、Write/Edit/MultiEdit/NotebookEdit（改文件）。
   名单会随版本长出新成员 → **验行为别核名单**。
3. **两个配置会把审批整条旁路掉**：`sandbox.autoAllowBashIfSandboxed: true` 和
   `--permission-mode acceptEdits`。任一打开，`--permission-prompt-tool` 压根不被调用、
   命令直接执行。要审批就得 `autoAllowBash=false` + `permission-mode default`。

审批链路契约（二进制原文）：工具返回 `{behavior:'allow', updatedInput?}` 或
`{behavior:'deny', message}`；传入 payload 是 `{tool_name, input, tool_use_id}`（snake_case）。
`permissions.ask` 是把工具路由到审批工具的开关。PreToolUse hook 的
`permissionDecision` 支持 allow/deny/ask，另有未文档化的 `defer`（**只在 print 模式可用**）。
参考实现：`~/Desktop/my-code/dk/APPROVALS.md` + `scripts/approval-e2e.sh`。
