---
name: project-drama-agent
description: drama-agent 项目定位、两条线分家、单一真相交接单位置
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d89aa0b-9452-43e0-9f98-c451e8e90301
  modified: 2026-07-30T06:40:42.525Z
---

drama-agent：把短故事/多轮对话编译成 AI 视频工具（目标 Seedance 2.0，走 WaveSpeed）prompt 制作包的纯前端 SPA（React18+TS+Vite+antd6+ajv），五步流水线 + schemas 校验 + dialects 方言。

## ⚠ 2026-07-17 两条线已分家（认路径别认仓名）

- **`~/Desktop/my-code/drama-agent`** = **晚上线**。**要做 SEO + 收费的是这条。** 在 `main`（07-22）。
- `~/Desktop/cmm/drama-agent` = 白天线，不碰。在 `lengmo_20260720_feat_prompt-chain`（07-24 已推）。

理由（owner 原话）：cmm 那边是工作时候的事，晚上这条要赚钱、不想让白天知道。两边共用历史但从此各走各的。

⚠ **2026-07-27 核实：「cmm 那份已断 origin 纯离线」的旧口径已作废。** 两份 remote 同指
`GuinsooRocky/drama-agent`，只是各在各的分支上。两条线从 `cc8ebc7` 分叉，**合并会有 11 个文件冲突**——
真要并线得当成一次正经 merge 排期，别当"同步一下"。

## 单一真相 = 项目内交接单

**`my-code/drama-agent/docs/2026-07-17-付费墙与SEO-交接.md`** —— 开工先读它。四份调研全文在 `docs/research/`。

里面有：owner 已拍板清单 / 价格实测（NOWPayments 下限 ≈$10，$0.8/$6.6 都收不了，07-18 重定）/ 付费墙全链路代码现状 / 上线硬前置顺序 / SEO「抄 soliloquy 自己」的完整方案 / 证据卫生教训 / 假警报存档。

## 付费墙进度（2026-07-22 更新，`docs/2026-07-17-付费墙与SEO-交接.md` 仍是单一真相）

**代码已全部提交进 `main`**：价格定 `PRICE_USD=12` / 20 次 + 匿名额度码 + D1；tsc 净、eval 199 全过。

**但一行都没部署。** 线上 workers.dev 还是 07-16 的老壳：
- `wrangler.jsonc` 三个占位符没填（`PUBLIC_ORIGIN` / KV id / D1 id）
- 三把 secret 全空

**两个未解缺口（开工前先看）**：
1. 市场已拍板英文，但**输出语言仍写死中文**（`dialects/seedance.md:121`，即 Seedance 措辞手册）+ UI 也还是中文。
2. **付费链路从没在真浏览器点过**——只有 tsc 和 eval 的绿，没有一次端到端人工验证。

**已拍板（别再问）**：市场=**英文** · 蒙层=**全蒙一字不给** · 收款走 soliloquy 那套 NOWPayments · **SEO 要做**（他否的是内容农场不是 SEO）· 提现/费率/模型选型=owner 的域别管。

## 术语约定（07-21）

- **对 owner 说话别用「方言」这个词** —— 他理解成"非普通话"，07-21 因此误拍板把 `dialects/seedance.md` 整层移除（子 agent 已执行完才发现误会，又整体倒带恢复，白烧两轮 opus）。一律叫 **「Seedance 措辞手册」**。[[feedback_no_jargon_plain_product_language]] 的案发现场之二。

## 老坑（仍有效）

- **仓库政策**：个人仓，可直推 main、commit 自行判断（[[feedback_commit_policy]]）
- `App.tsx` 的 ENV_KEY **必须 DEV 门控**，否则 Vite 把 .env.local 的 key 内联进 dist（验收抓过 P0）
- OpenRouter key 在 git 历史里泄露过，owner 拍板不轮换（"带就带了"）
- 2026-07-16 mixboard 三件套已入库（commit 4a06d7a）：retry.ts / worker 代理藏 key / evals（`npm run eval`）/ .claude 规则

## 本项目的血泪（[[feedback_dont_declare_infeasible]] 的案发现场）

07-17 一天判错六次「不能做」，全是转述子 agent 未核的结论去推翻 owner 已拍的板。**子 agent 的否定结论必须自己核。**
