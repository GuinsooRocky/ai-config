---
name: reference-iterm2-advanced-settings-key-case
description: iTerm2 高级设置用 defaults write 改时键名要首字母大写（customTabBarFontSize → CustomTabBarFontSize），小写键会被静默忽略
metadata:
  node_type: memory
  type: reference
  originSessionId: bf0c0581-499c-42ef-b02a-4e9834bb714e
  modified: 2026-10-09T04:17:15.657Z
---

iTerm2（3.7.x）的 Advanced 设置，读 NSUserDefaults 时会对源码里的设置名做 `stringByCapitalizingFirstLetter`，所以 `defaults write com.googlecode.iterm2 <键>` 必须写**首字母大写**的键：`UseCustomTabBarFontSize`、`CustomTabBarFontSize`、`DefaultTabBarHeight`。`strings` 二进制里只看得到小写名，照抄就会写成无效键，而且不报错。

owner 竖排标签栏现行配置：行高 `DefaultTabBarHeight=60`，标签字号 `CustomTabBarFontSize=20`（10-09 从 24 调小）（`UseCustomTabBarFontSize=1`）。都只在 iTerm2 启动时读取，改完要 ⌘Q 重开。

**Why:** 2026-09-14 写成了小写键，字号一直没变大，到 10-09 反汇编 `load_useCustomTabBarFontSize` 才发现是键名大小写的问题。
**How to apply:** 改 iTerm2 隐藏设置前，先用 `otool -arch arm64 -tV -p '+[iTermAdvancedSettingsModel <名字>UserDefaultsKey]'` 看它有没有调用 capitalize；改完用 `defaults read` 确认写的是大写键。
