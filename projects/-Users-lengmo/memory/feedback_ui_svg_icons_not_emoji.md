---
name: feedback_ui_svg_icons_not_emoji
description: UI 图标一律线性 SVG，绝不用 emoji 当导航/按钮/chrome 图标——用户强烈反感（觉得丑、跟 SVG 风格不搭）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e6fd5496-d103-4fb2-a638-c2c193f6e01c
---

UI 的图标（导航栏、按钮、快捷区、任何界面 chrome）**一律用线性 SVG 图标**（stroke=currentColor，跟项目现有图标同风格），**绝不用 emoji**（🏠💬🔔💳👤◐🌐⭐⚙ 这类）。

**Why**：2026-07-08 soliloquy 全局导航我盲写时图省事用了 emoji 当 5 个导航图标，用户炸了——"不觉得这几个标签好丑吗？太他妈丑了，丑爆了……结果你又放上来了"。emoji 图标在深色专业 UI 里跟周围的线性 SVG 完全不搭、显廉价业余。

**How to apply**：
- 新写任何带图标的 UI，默认线性 SVG（feather 风：24 viewBox、stroke 1.9、round cap、currentColor），别偷懒塞 emoji。
- 项目里已有 SVG 图标就复用/仿其风格；没有就画 path（home/chat/bell/card/user/moon/sun/globe/star/gear/heart 这些都是标准线条图标）。
- 例外：内容区里语义化的符号（如 ♥ 点赞、★ 收藏）可接受；但导航/工具栏/logo 这类 chrome 一律 SVG。
- 用户对 emoji 复现敏感（"又放上来了"）——改过一次就别再犯。

相关：[[feedback_writing_taste_umbrella]]（文字/视觉都过品味关）。
