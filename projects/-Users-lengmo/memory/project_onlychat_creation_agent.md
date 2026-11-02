---
name: project_onlychat_creation_agent
description: onlychat 创建 Agent MVP 开发现场：worktree、分支、后端归属、PRD 口径变化；接手前现读 PRD 和群，别信本条的进度
metadata:
  node_type: memory
  type: project
  originSessionId: 7f807ba3-20be-4aa6-b2a9-f8783f54877b
  modified: 2026-11-02T11:12:41.847Z
---

11-02 开工。worktree=`~/Desktop/cmm/onlychat-creation-agent`，分支 `lengmo_20261102_feat_creation-agent`（基于 origin/develop 2d92adb8be）。PRD=飞书 wiki XOxjwi4BwiMuNzkAawnc4LjKnxh，群=「创建大群---创建Agent」（thread 13）。工时拆分在排期表（app_token CptYbz2h1aEb3Ns84NOciCADn6c，表 tblmocj0YKG0pOAj，按需求标题含「创建agent」过滤）；看排期表只看需求描述和工时两列（owner 11-02 明说）。代码规格在仓内 `docs/architecture/character-system/creation-agent.md`。owner 的节奏：子 agent 实作，主会话检查，文档必须与 PRD 一致；11-02 晚 owner 要求不局限 5 天范围，按 PRD 给出 PC 完整流程（不要求做完，要尽量完整）。

- **11-02 群结论（刘心仪 17:26，覆盖 PRD）**：一期只做 PC，MVP 跟 6.39.0 上线，开发预计 11-17 结束；11/6–11/9 出 showcase demo；前端共 18.8 人日，本期张昊 5 人日独立做主流程 demo，下期 Wei 加入两人收尾；**对话内容本期不存储，每次进入都是全新对话**。待定：对话模型、流式是否保留（延泽工时超 2 天，可能砍）、测试节奏。
- **后端**：李延泽管 Agent 主线，任长宏管生图和计费（10-30 群里定的），下期加张佳晨；11-02 时接口未出，技术方案 11-03 晚出。
- **PRD 口径变过**：存储规则 10-29 版是服务端存、一账号多草稿；11-02 版改成新建角色存本地、一浏览器一草稿、已发布角色存服务端，标题仍「待定」，又被上面的群结论覆盖。桌面 10.30 反讲 HTML 的存储一节已过期，多方案任务名以现版 PRD 的 Options 为准。读 PRD 前重新拉，别用旧缓存。
- **祝悦 10-21**：先做 web PC，调好再扩 web mobile 和 app。
- **demo 分支 `origin/demo/oc-creation-agent`**（Agent 部分主要是 Wei 写的，git log 25 次提交）：基于 09-20，混着短剧代码，不合并。能抄的是表单写入和拖动调宽。它是整条一次性返回、共用 Jelly token、没有扣费记录，README 写明了这些限制。

**How to apply:** 接手先看 worktree 的 `git log`，再读 PRD 和群里最新消息。Figma 只能走 MCP（127.0.0.1:3845），连不上要 owner 开 Figma 桌面端。相关：[[project_onlychat]]、[[feedback_work_hour_breakdown_format]]、[[feedback_task_execution_cadence]]
