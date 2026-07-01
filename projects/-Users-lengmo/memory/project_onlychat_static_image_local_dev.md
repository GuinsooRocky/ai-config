---
name: project_onlychat_static_image_local_dev
description: onlychat 本地 dev 下 next/image 渲染 /static/ public 图会裂；用 inline backgroundImage
metadata: 
  node_type: memory
  type: project
  originSessionId: 136a0310-5f43-45e6-9c66-e34bcac19a40
---

onlychat 的 `next.config.js` 用 `loader: 'custom'`（`src/utils/customLoader.ts`）。它把**非 http 的本地路径**（`/static/images/x.png`）转成远程优化代理：
`${imageUrl}/_image/optimize/${siteUrl}${src}`，其中 `imageUrl=https://img.cocdn.co`（非 beta）、`siteUrl=window.location.origin`。

**后果**：本地 dev（localhost:3000）下，`next/image` 渲染 `/static/` public 图 → 让 img.cocdn.co 去抓 `http://localhost:3000/static/...` → 够不着你本机 → **裂图**。`WorldDefault.tsx`（hukangbao 客态组件）就是这样，本地也裂。

**判断**：
- `cdn.crushon.ai` 等**绝对 http 图**本地正常（优化器够得着公网）。
- 本地裂的只有 `/static/` 这类本地相对路径图。
- `NEXT_PUBLIC_FE_ENV=beta` 时 loader 对 `/` 开头直接返回 src（本地能显示），但 beta 会让 imageUrl 切内网、首页其它图崩——别为这个开 beta。

**要本地也显示的静态图，照项目主流写法走 CSS 背景，别用 next/image**：
- 首选 inline `style={{ backgroundImage: \`url(/static/images/x.png)\` }}`（见 `DetailModal.tsx:274`、`MemoryModal`、`MemoryList`）——直连静态文件、不经优化代理。
- light/dark 用两层 `dark:hidden` / `hidden dark:block` 切，不必测 JS 主题。
- `bg-[url(...)]` Tailwind 写法（`NoComment.tsx`/`UserBox.tsx`）也行，但**经 twMerge 包装会把 arbitrary url 类名搞坏 → webpack 当模块解析 → globals.css 编译炸**；要用就直接写进 className 字面量、别过 twMerge。

实战：世界卡 note 类型默认图（`NoteTypeDefaultImage.tsx`）就是踩完 CDN→next/image→bg-[url] 三坑后落到 inline backgroundImage。相关 [[project_onlychat_shared_component_env_split]]。
