---
name: soliloquy-supabase-quota
description: 2026-10-31 soliloquy 超 Supabase 免费流量连带 lich 停服，owner 定不搬家，整库备份改约 15 天一次（T299 执行包交 Codex）；T298 自托管搬家后置
metadata:
  node_type: memory
  type: project
  originSessionId: 37783444-4309-40e1-89b5-ac1ea884d8d9
  modified: 2026-10-30T17:08:27.158Z
---

owner 说「soliloquy 把 lich 的流量用了、不想花钱」时指这件事。超额九成来自每天 4 次的整库备份，10-31 owner 选了不搬家：备份改每月 1、16 号，接受最坏丢约 16 天数据，不开新机器，不买 Supabase。

**Why:** 9 个月活、数据库 278 MB，为一个备份任务搬整个后端不成比例；`vpn-tokyo` 只有 1 GB 内存，当临时也不行。

**How to apply:** 10-31 已部署到生产机，进度只认 soliloquy 仓 BACKLOG 的 T299、T298（后置）；剩执行包第 8 步（11-01 首次备份、11-10 恢复、11-17 读用量）。Healthchecks 账号是 `agent@soliloquy.live`，用邮件登录链接进，浏览器默认没登录。要重提搬家时先读方案 §9（支付会关死、图片重签、触发器、7 把找不到的密钥），别从头查。相关：[[project_soliloquy]]
