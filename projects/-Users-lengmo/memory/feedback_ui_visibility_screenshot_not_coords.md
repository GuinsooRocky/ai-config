---
name: feedback_ui_visibility_screenshot_not_coords
description: 验 UI 元素可见/被切用截图当裁判，量尺寸用 offsetWidth/getComputedStyle 且等动画落定；getBoundingClientRect 只用于定位点击目标和判断是否在视口内
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f0356a0c-d347-4b63-8fa9-9cc66c3ef436
  modified: 2026-11-02T06:13:10.517Z
---

判「某元素是否完整可见/被切掉」时，用**截图**看，别拿 `getBoundingClientRect()` 自己算坐标下结论。量尺寸用 `offsetWidth` / `getComputedStyle()`，量之前先确认动画落定。浏览器走查里「弹窗/浮层看起来不对」的**第一嫌疑是量早了**，不是代码错了。

**Why**：09-03 验 pricing swiper 修复（末档 Imperial 定位），我用 `imp.right - container.left > containerWidth` 算出「Imperial 被切、fix 没生效」，据此对 owner 报了"没生效"——被当场顶「放屁，都部署好了肯定有」。一截图，Imperial 完整露着，fix 明明生效。我量的 `.swiper` 容器宽（1814）跟实际可见裁剪区对不上（overflow/sidebar 偏移/父级布局），坐标算法给了假阴性。

09-22 onlychat 推荐模型走查又栽三次：点开弹窗立刻截图只看到蒙层变暗，报成 bug，`read_page` 一看 DOM 全在；同一弹窗量 `getBoundingClientRect` 得宽 380、行高 51、头像 30，以为尺寸全错；等 1.2s 再量数值没变，因为 `zoom-appear-act` 类根本没被移除。真因：rc-dialog 的 zoom 入场动画用 CSS transform scale，`getBoundingClientRect()` 返回 transform 之后的视觉矩形，动画中间帧的数值全部等比缩水（当时全体 ×0.63：380/600、51/80、30/48，比例一致就是识别信号）。浏览器窗口在自动化控制下没有焦点时，Chrome 会节流动画，`appear-act` 可能长时间不摘。

**How to apply**：
- 可见性/被切/落位这类**视觉判定**，第一手证据是 `computer` 截图，不是坐标运算。
- `getBoundingClientRect` 只用于定位点击目标和判断是否在视口内；一旦要下「露没露全 / 被切」的结论，先截图。
- 量盒模型一律用 `offsetWidth` / `offsetHeight` + `getComputedStyle()`（padding / gap / 颜色），这些不受 transform 影响。
- 量之前先断言动画已落定：`el.className.includes('appear-act') === false`；没落定就别下结论。发现所有数值等比偏小，先查 transform，别急着改代码。
- 截图同理：点击后至少等一拍再截；「截图里没有」不等于「DOM 里没有」，先 `read_page` / JS 查 DOM 再判。
- 同族教训 [[feedback_not_ground_truth]]（按内容特征校验、别信中间量）、modal 死类「拿页面真实编译 CSS 当裁判」。
- 部署已确认（build hash 对得上）时，别用自己的测量去推翻「已部署」，先截图核。


补充：09-03 pricing 修复据错误坐标报「没生效」被顶，一截图 Imperial 明明全露
