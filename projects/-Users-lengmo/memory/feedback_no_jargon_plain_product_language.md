---
name: feedback_no_jargon_plain_product_language
description: "别用黑话/术语渲染问题；用户已知且接受的前置条件当\"写说明书\"处理，别说成墙/天花板"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1101eeb0-f88c-4cd6-935b-b4cbed2ba064
---

用户讨厌黑话/术语堆砌，也讨厌把"用户都知道、都接受的前置条件"渲染成砸不穿的「墙/天花板」。

**Why:** 从产品负责人视角，这些（要付费 Claude 并登录、Mac 别休眠、每个渠道要建 bot）只是正常的上手事实，不是限制更不是障碍 —— 该做的只是把它们写清楚。

**How to apply:** 大白话讲产品。避免 Persona / RCE / footgun / fail-closed / heartbeat / oracle / moonshot / GREEN / 天花板 / 墙 / **北极星(North Star，说"最重要的那个目标/主线方向"就行)** 这类词。用户明确说过"北极星"这词讨厌到不想在电脑里出现（2026-07-04）。遇到任何前置条件，动作是"写进设置说明 + 向导里替用户挡步骤"，不是当成 blocker 反复掂量。相关 [[feedback_just_do_no_stop_suggestions]]。

**2026-07-11 两次加重案例（同一晚连撞）**："外部触发/召回口/常驻基建/依赖链" 让用户直接说"这是什么我都看不懂"；"HTML 线框" 让用户炸毛"你上网查这几个字能查出来东西吗"。修正后有效的说法："她不会主动来找你，微信没打开也会弹消息，我们连这个能力都没有"、"线框=页面草图，之前的计划是等你画草图我们照着做"。**解释产品问题的正确姿势：先给用户亲历的场景（他看到什么/对比他熟的产品），再给结论；名词能不出现就不出现。**
