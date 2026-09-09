---
name: feedback_no_jargon_plain_product_language
description: "大白话讲产品 + owner 禁用词表（臂/客户端/北极星/Persona/RCE 等）；前置条件当写说明书别渲染成墙"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1101eeb0-f88c-4cd6-935b-b4cbed2ba064
  modified: 2026-08-26T07:13:32.320Z
---

用户讨厌黑话/术语堆砌，也讨厌把"用户都知道、都接受的前置条件"渲染成砸不穿的「墙/天花板」。

**Why:** 从产品负责人视角，这些（要付费 Claude 并登录、Mac 别休眠、每个渠道要建 bot）只是正常的上手事实，不是限制更不是障碍——该做的只是把它们写清楚。

**禁用词表（对话/文档/看板文案/代码注释/测试用例名一律适用）：**

| 禁用 | 该说什么 |
|---|---|
| 臂（对照臂/实验臂/两臂/A 臂 B 臂） | 产品语言点名各组是什么：世界卡=「整页跳转（老）」/「浮层动画（新）」，搜索=「老路由」/「新动效」；泛指就说「两组」「对照组/实验组」 |
| 客户端 | 「你打开的页面」/「浏览器页面」/「桌面 app」；服务器侧说「后台」 |
| 北极星 / North Star | 「最重要的那个目标 / 主线方向」（用户明说讨厌到不想在电脑里出现，2026-07-04） |
| Persona / RCE / footgun / fail-closed / heartbeat / oracle / moonshot / GREEN / 天花板 / 墙 | 各自的大白话 |

**复发警示（这两个词都被纠正过十几次，靠记得没用，要机械检查）：**
- 「臂」：2026-08 两天被纠十几次（原话「我这两天说了 10 遍」）。已把 onlychat 全仓（src+docs，32 文件 202 处）机械换成「组」。**2026-09-01 复核实况：docs 侧存量 0，src 侧还剩 10 处**，全在测试注释与 `describe`/`it` 用例名里（`botMessageHeader.test.tsx`、`useAsyncVoiceGuideAbFlow.test.tsx`、`GroupChatPage.test.tsx`、`RecommendSettingModal.test.tsx`）——测试用例名同样在禁用范围内，这几处是待清的存量，不是豁免。凡碰 worldcard 转场 / search 转场这类 A/B 埋点任务（那些文件的旧上下文会把这个字带出来），发消息/写注释/写用例名之前先自己搜一遍「臂」。
- 「客户端」：2026-08-18 soliloquy 迁移监工连续触雷（原话「我的天 我已经不想听到这个名字了」）。转述别的 session 原话也要当场翻译，不许原样带出。

**解释产品问题的正确姿势**（2026-07-11 同晚连撞两次："外部触发/召回口/常驻基建/依赖链"被说"这是什么我都看不懂"；"HTML 线框"让用户炸毛）：先给用户亲历的场景（他看到什么/对比他熟的产品），再给结论；名词能不出现就不出现。有效示范："她不会主动来找你，微信没打开也会弹消息，我们连这个能力都没有"、"线框=页面草图，之前的计划是等你画草图我们照着做"。

**How to apply:** 大白话讲产品；输出前扫一遍禁用词表（尤其聊 AB/实验/看板数据的回合扫「臂」，聊架构分层的回合扫「客户端」）。遇到前置条件，动作是"写进设置说明 + 向导里替用户挡步骤"，不是当成 blocker 反复掂量。边界见 [[feedback_writing_taste_umbrella]]（大白话 ≠ 注水奶味）。相关 [[feedback_just_do_no_stop_suggestions]]。
