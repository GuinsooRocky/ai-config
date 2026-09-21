---
name: feedback_ui_visibility_screenshot_not_coords
description: 验 UI 元素可见/被切用截图当裁判，别信自算的 getBoundingClientRect 坐标
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f0356a0c-d347-4b63-8fa9-9cc66c3ef436
  modified: 2026-09-03T12:16:18.157Z
---

判「某元素是否完整可见/被切掉」时，用**截图**看，别拿 `getBoundingClientRect()` 自己算坐标下结论。

**Why**：09-03 验 pricing swiper 修复（末档 Imperial 定位），我用 `imp.right - container.left > containerWidth` 算出「Imperial 被切、fix 没生效」，据此对 owner 报了"没生效"——被当场顶「放屁，都部署好了肯定有」。一截图，Imperial 完整露着，fix 明明生效。我量的 `.swiper` 容器宽（1814）跟实际可见裁剪区对不上（overflow/sidebar 偏移/父级布局），坐标算法给了假阴性。

**How to apply**：
- 可见性/被切/落位这类**视觉判定**，第一手证据是 `computer` 截图，不是坐标运算。
- 坐标只用来定位点击目标；一旦要下「露没露全」的结论，先截图。
- 同族教训 [[feedback_not_ground_truth]]（按内容特征校验、别信中间量）、modal 死类「拿页面真实编译 CSS 当裁判」。
- 部署已确认（build hash 对得上）时，别用自己的测量去推翻「已部署」，先截图核。
