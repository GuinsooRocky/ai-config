---
name: project_onlychat_static_image_local_dev
description: onlychat 本地 dev 下 next/image 渲染 /static/ public 图会裂；用 inline backgroundImage
metadata: 
  node_type: memory
  type: project
  originSessionId: 136a0310-5f43-45e6-9c66-e34bcac19a40
---

onlychat 本地 dev 下 `next/image` 渲染 `/static/` public 图必裂（customLoader 转 img.cocdn.co 够不着 localhost）；要本地显示的静态图用 inline `backgroundImage`，别用 next/image、别过 twMerge 的 bg-[url]。

**判断方法与三坑实录已迁入** `~/Desktop/cmm/onlychat-World-Path/04-本地启动指南.md` §十四（2026-07-06）。
