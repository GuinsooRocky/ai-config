---
name: mk
description: macOS 语音输入个人项目（替代 superwhisper），fork ambient-voice 改名 MK，给 cc 终端用
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
---

**MK** = 个人 macOS 语音输入 app（fork ambient-voice），主用途给 Claude Code 终端语音输入。仓库 `~/Desktop/my-code/mk`，**根 `.claude/CLAUDE.md` 是 ground truth**（路径/bundle/签名/launchd/触发键）；技术细节看 `docs/`（architecture / realtime-asr-decision / correction-roadmap 等）。

**留在全局的用户裁决**（docs 不承载的偏好层）：
- 引擎方向=sherpa-onnx SenseVoice native（非 Python，松手整段转）；用户倾向云端准确率胜过本地
- **拒绝上 LLM 做同音词判别**（2026-06-02 "我不想加大模型"）——双真词同音词只能挪错落点，别再劝 ollama/qwen Step 5；需要时只加短语级 protected-terms
- 延迟硬指标 ≤120ms；微调是钉自造词唯一的路但用户暂不做
- **文档偏好**：不留累积式 recap/changelog，只维护当前态 doc（覆盖更新）
- 分支：开发在 lengmo_* 分支、做完并 main；日常签出 main。改码要 `make install`+重启才生效
