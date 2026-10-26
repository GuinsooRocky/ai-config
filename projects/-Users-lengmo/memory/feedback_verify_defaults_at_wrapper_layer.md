---
name: verify-defaults-at-wrapper-layer
description: 核工具默认值要核实际调用的最外层（包装工具常覆盖内层默认），最好直接在锁定的镜像/安装里 grep；按内层默认算出的提速建议会整个落空
metadata:
  node_type: memory
  type: feedback
  originSessionId: fe8a4abc-7bec-406f-8452-d998252d9633
  modified: 2026-10-26T07:59:02.790Z
---

报「默认值是多少、改了能省多少」之前，要在实际被调用的那一层核：A 包了 B 时，A 的 CLI 往往会重新定 B 的默认值。最稳的做法是直接在锁定版本的镜像或安装目录里 grep 选项定义，GitHub 上 B 的源码只能当线索。

**Why:** 2026-10-26 perf-lab 提速，我按 browsertime 自己的 `pageCompleteWaitTime` 默认 8000 算出「8 秒改 4 秒，整轮省 7 分钟」，owner 据此拍了「4s 就行」。真跑才发现 sitespeed.io 42.5.1 在 `lib/cli/options/browser.js` 里把默认改成了 5000，实际只省 1 秒/次，整轮约 2 分钟。owner 白拍了一次板，整轮也白跑。

**How to apply:** 提「改某参数能省多少」这类量化建议前，先在实际镜像里跑一遍 `grep -rn <option> lib/ node_modules/<inner>/`，内外两层的默认值都列出来，以外层为准。改完先拿一格真跑验证节省是否兑现，再报数。相关：[[not-ground-truth]]、[[perf-lab-report-technical-altitude]]。
