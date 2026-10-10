---
name: project_manju_test_lingjing
description: 漫剧测试项目：用《灵境行者》跑通 SeeDream 5.0 Pro + Seedance 2.5 竖屏漫剧流程，只做测试不发布；可复用资料在 AI课/时空之门
metadata:
  node_type: memory
  type: project
  originSessionId: 33ca3792-8c86-4e5e-ab35-4884839c950a
  modified: 2026-10-10T07:06:20.205Z
---

2026-10-10 起 owner 在做一个 AI 漫剧测试：拿网文《灵境行者》（/Users/lengmo/Downloads/灵境行者.txt）第一集试流程。图模型 SeeDream 5.0 Pro，视频模型 Seedance 2.5（时长 4–30s 任意整数秒可选，不是只有 4/6/8 档；实际每镜 4–8s），竖屏 9:16，画风句锁死「二维手绘国漫风格，赛璐珞上色带厚涂质感，清晰的黑色描边，光影对比强烈」。

**Owner 拍板（2026-10-10）：灵境行者只当测试材料，不发布。** 原因：改编权在腾讯，换皮（改名+抽象剧情）照样构成实质性相似侵权（宁波中院 2025 短剧案按「情节顺序与原著前 46 章一致」判侵权）。流程跑通后换原创本子或买小众网文授权。

**Why:** 别再往发布/起号方向推，也别再提「换皮 skill」；市面上只有改编工具（Scriptify = npm ai-scriptify、novel-to-script），没有合法的去原作痕迹工具。

**How to apply:**
- 流程：角色三视图 → 场景图 → 每镜首帧（9:16，2K，挂人物正面+场景两张参考）→ Seedance 图生视频（挂首帧，6s，480p 试错）→ 后期统一 TTS 配音 + 字幕 + BGM。Seedance 阶段只要环境音/音效 + 「无对白」，台词后期配（音色会漂、口型 P0）。
- prompt 一律对话内贴，每轮 2 条（见 [[feedback_copy_content_delivery]]）。
- 可复用资料：`~/Desktop/cmm/AI课/时空之门/`（真实漫剧交付项目的剧本格式 + 7 张制作表，建《灵境行者》制作表照它抄）；`AI课/AI漫剧（6月25号更新）/AIGC漫剧教程…/aigc视频教程/…人物微表情…/微表情提示词.txt`（8 条固定镜头微表情句式）；`AI课/AI漫剧教程（6月14号更新）/配音/`（音色 wav 库）；`AI课/AI视频生成52个系统性问题全清单.html`（owner 自己的工作流问题清单）。
- `~/Desktop/cmm/crushon-ai-perf-lab` 是性能测试仓，与漫剧无关。
