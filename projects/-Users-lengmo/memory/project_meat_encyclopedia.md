---
name: project_meat_encyclopedia
description: 肉类介绍大全 RN/Expo app — 初心、v1 范围、技术栈实际偏差
metadata: 
  node_type: memory
  type: project
  originSessionId: 73ef4071-21db-48dd-9233-2c4ebb8826fe
---

肉类介绍大全 App，目录 `~/Desktop/my-code/meat-encyclopedia`（GuinsooRocky 个人项目，按 [[feedback_personal_repo_handling]] 处理）。2026-05-29 起。

**初心（产品北极星，不在代码里）**：解决买肉/点菜三件事 —— ①各种叫法（学名/普通名/俗称/餐厅菜单名）对不上是不是同一块；②不知道对应身体哪个部位；③知道部位也不知道口感、适合怎么做。核心数据闭环＝**名字（全部叫法）→ 部位 → 口感特色**，所以 `alias` 字段是头等公民（要喂满菜单名/俗称/英文），详情页布局按"又叫什么→哪个部位→口感→怎么做"排序。

**v1 范围决定**：只做 牛/猪/羊 3 类（共 23 条，数据在 `src/data/meats.json`，AI 生成+事实核查）；收藏功能不做；砍掉 nutritionHighlights 字段；部位"分割图"v1 是占位、可交互高亮留 v2。

**技术栈实际偏差（重要）**：`create-expo-app@latest` 实际给的是 **Expo SDK 56**（不是调研以为的 54），路由在 `src/app/`、别名 `@/*`→`src/*`、`typedRoutes`+`reactCompiler` 都开。导航＝根 Stack + `(tabs)` 组（经典 `Tabs` from 'expo-router'，非 unstable NativeTabs）。node 走 nvm v20.20.2，跑命令要 `export PATH=/Users/lengmo/.nvm/versions/node/v20.20.2/bin:$PATH`。项目根 `AGENTS.md` 要求写码前读 v56 版本文档。验证＝`npx expo export -p web` 打包 + `npx tsc --noEmit`。
