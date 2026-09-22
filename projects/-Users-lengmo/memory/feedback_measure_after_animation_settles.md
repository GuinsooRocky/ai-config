---
name: feedback-measure-after-animation-settles
description: 走查量尺寸前必须等动画落定，且用 offsetWidth 而非 getBoundingClientRect（transform 会骗人）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6305a791-88b1-44a9-abe7-aa28345e5a75
  modified: 2026-09-22T08:47:07.379Z
---

浏览器走查里「弹窗/浮层看起来不对」的**第一嫌疑是量早了**，不是代码错了。2026-09-22 onlychat 推荐模型走查一轮栽三次：

1. 点开弹窗立刻截图 → 只看到蒙层变暗、弹窗"没出来" → 报成 bug；`read_page` 一看 DOM 全在
2. 同一弹窗量 `getBoundingClientRect` → 宽 380、行高 51、头像 30 → 以为尺寸全错
3. 等了 1.2s 再量 → 数值没变，**因为 `zoom-appear-act` 类根本没被移除**

真因：rc-dialog 的 zoom 入场动画用 **CSS transform scale**，而 `getBoundingClientRect()` **返回的是 transform 之后的视觉矩形**。动画中间帧量到的所有数值会**等比缩水**（当时全体 ×0.63：380/600、51/80、30/48、13/20、8/12 比例一致——这个"比例一致"就是识别信号）。而且浏览器窗口在自动化控制下没有焦点时，Chrome 会节流动画，`appear-act` 可能长时间不摘。

**How to apply:**
- 量盒模型一律用 `offsetWidth` / `offsetHeight` + `getComputedStyle()`（padding / gap / 颜色），**这些不受 transform 影响**；`getBoundingClientRect` 只用于判「在不在视口内 / 有没有被切」
- 量之前先断言动画已落定：`el.className.includes('appear-act') === false`；没落定就别下结论
- 发现"所有数值等比偏小"→ 先查 transform，别急着改代码
- 截图同理：点击后至少等一拍再截；"截图里没有"不等于"DOM 里没有"，先 `read_page` / JS 查 DOM 再判

关联 [[feedback_ui_visibility_screenshot_not_coords]]（那条说「判露没露全用截图、别信自算坐标」）——两条合起来才完整：**可见性看截图，尺寸看 offsetWidth，两者都要等动画停**。
