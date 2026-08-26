---
name: project_onlychat_env_pitfalls
description: onlychat 本地环境四坑索引（i18n 挂/静态图裂/共用组件双轴/tRPC 403）——细节全在 World-Path，此处只留症状→章节
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-26T07:15:35.274Z
  originSessionId: 93994ccd-a234-4de3-b00b-c54580b8bd7d
---

onlychat 本地环境高频坑索引，**细节全在 `~/Desktop/cmm/onlychat-World-Path/` 对应章节，此处只认症状**：

| 症状 | 一句话结论 | 细节 |
|---|---|---|
| `pnpm i18n` 必挂 | python3.13 撞 pandas==2.1.4，用 3.12 venv 直跑 i18n.py；`csvtojson` 全量覆盖会删飞书没有的 key，判译文缺口先 pull | 04-本地启动指南.md §七 |
| 本地 dev `/static/` 图裂 | `next/image` 的 customLoader 转 img.cocdn.co 够不着 localhost；本地静态图用 inline `backgroundImage` | 04 §十四 |
| 改共用组件外溢 | 两条正交轴都要点一遍：PC/mobile（z-index/布局）+ dark/light（用 token 或 `dark:`，别写死 hex） | 04 §十五 |
| dev 全站 tRPC 403/UNAVAILABLE | 第一嫌疑 dev 进程继承 `http_proxy=127.0.0.1:7897`（Clash 污染 grpc-js）；proxy-clean shell 重起 | 03-环境变量说明.md 末节 |
