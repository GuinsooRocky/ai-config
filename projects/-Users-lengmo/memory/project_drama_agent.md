---
name: project-drama-agent
description: drama-agent 项目定位、两条线分家、单一真相交接单位置
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d89aa0b-9452-43e0-9f98-c451e8e90301
---

drama-agent：把短故事/多轮对话编译成 AI 视频工具（目标 Seedance 2.0，走 WaveSpeed）prompt 制作包的纯前端 SPA（React18+TS+Vite+antd6+ajv），五步流水线 + schemas 校验 + dialects 方言。

## ⚠ 2026-07-17 两条线已分家（认路径别认仓名）

- **`~/Desktop/my-code/drama-agent`** = **晚上线**，独占 GitHub `GuinsooRocky/drama-agent`。**要做 SEO + 收费的是这条。**
- `~/Desktop/cmm/drama-agent` = 白天线，**已断 origin 纯离线**，不碰。

理由（owner 原话）：cmm 那边是工作时候的事，晚上这条要赚钱、不想让白天知道。两边共用历史但从此各走各的。

## 单一真相 = 项目内交接单

**`my-code/drama-agent/docs/2026-07-17-付费墙与SEO-交接.md`** —— 开工先读它。四份调研全文在 `docs/research/`。

里面有：owner 已拍板清单 / 价格实测（NOWPayments 下限 ≈$10，$0.8/$6.6 都收不了，07-18 重定）/ 付费墙全链路代码现状（已码完未提交）/ 上线硬前置顺序 / SEO「抄 soliloquy 自己」的完整方案 / 证据卫生教训 / 假警报存档。

**已拍板（别再问）**：市场=**英文** · 蒙层=**全蒙一字不给** · 收款走 soliloquy 那套 NOWPayments · **SEO 要做**（他否的是内容农场不是 SEO）· 提现/费率/模型选型=owner 的域别管。

## 老坑（仍有效）

- **仓库政策**：个人仓，可直推 main、commit 自行判断（[[feedback_personal_repo_handling]]）
- `App.tsx` 的 ENV_KEY **必须 DEV 门控**，否则 Vite 把 .env.local 的 key 内联进 dist（验收抓过 P0）
- OpenRouter key 在 git 历史里泄露过，owner 拍板不轮换（"带就带了"）
- 2026-07-16 mixboard 三件套已入库（commit 4a06d7a）：retry.ts / worker 代理藏 key / evals（`npm run eval`）/ .claude 规则

## 本项目的血泪（[[feedback_dont_declare_infeasible]] 的案发现场）

07-17 一天判错六次「不能做」，全是转述子 agent 未核的结论去推翻 owner 已拍的板。**子 agent 的否定结论必须自己核。**
