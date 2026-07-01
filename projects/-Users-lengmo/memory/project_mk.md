---
name: mk
description: macOS 语音输入个人项目（替代 superwhisper），fork ambient-voice 改名 MK，给 cc 终端用
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
---

**MK** = 用户的个人 macOS 语音输入 app，主要用途是给 Claude Code 终端做语音输入（手打太累，每天对话量大）。仓库根 `.claude/CLAUDE.md` 有完整的路径 / bundle / 签名 / launchd label / 触发键等元数据，需要时 ls / cat 即可。

## 引擎方向（2026-05-22 大改，方案"甲-1"）

- 可切引擎：`polish.engine` = `sa` | `sensevoice` | `groq` | `tencent`，**默认 / 回落 = SA**；菜单栏有「识别引擎」选择器（✓ 标当前，点切，`StatusBarController.selectEngine`）
- **tencent（2026-06-09 加）**：腾讯云「一句话识别」`SentenceRecognition`，TC3-HMAC-SHA256 签名，`Sources/TencentEngine.swift` 镜像 GroqEngine 形状；config 填 `tencent_secret_id`/`tencent_secret_key`（手动加，同 groq）；5000 次/月免费，push-to-talk「说一句=一次调用」正配。质量好（SA「GS脚本」→腾讯「JS脚本」）；用户倾向云端准确率胜过本地
- **选定方向 = SenseVoice**：native sherpa-onnx（**非 Python**），int8 模型在 `~/.mk/models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17/`，**松手后整段转**（不是流式）
- SA 仍全程录音落 WAV + 引擎失败时回落
- 集成件：`client/CSherpaOnnx/`(C 模块) + `client/Vendor/sherpa-onnx/`(dylib+头, 进 git) + `Sources/SenseVoiceEngine.swift` + `Sources/SherpaOnnx.swift` + Package.swift 链 + Makefile 打包 dylib 进 .app
- **只有 `make run` / `make install` 新二进制才生效**（老二进制不认 engine 字段）

## 痛点边界（实测载弹）

- **通用错（大人物→大任务 / HTML / 标点）**：换引擎修通用错有效
- **私有专名 OOV 物理墙**：Vercel / khazix / worktree / session 等私有专名**在任何现成模型都不稳**——这是物理墙，不是调参问题
- **双真词同音词物理墙（2026-06-02 实测确认）**：流失/流式、买点/埋点、Scala/skill 这类「两个都是真词的同音词」——字典/拼音层**结构性无解**，只能在两个错向之间二选一挪错落点（实测：加 `流失→流式` 后「录音流失→流式」✅ 但「人才流失→人才流式」❌）。唯一根治 = Step 5 上下文 LLM 判别。**用户 2026-06-02 明确拒绝上 LLM（"我不想加大模型"）**，故此类只能认频率赌注（保留 `流失→流式`，赌 streaming 频率 >> churn）。别再劝用户上 ollama/qwen Step 5。需要时只加短语级 `protected-terms.txt`（护 人才流失/客户流失 等 churn 搭配，不碰 streaming 语境）。
- **旧纠错字典与 SenseVoice 错音不命中**：旧字典按 SA 错音学的，对 SenseVoice 新错音失效，需要重新 learn
- **微调是唯一钉自造词的路但重**（用户暂不做）
- **延迟硬指标 = ≤120ms**（来自 SA 边说边出的体感）；长句超标的话后续可上"甲-2 = SenseVoice + silero VAD 分段流式"

## 注入架构（2026-06-09 大改，深度研究后定案）

**核心原则（铁律）：目标 app 永远只收到「最终文本」一次；实时体验全部发生在 MK 自己的浮窗 HUD 里。**

- **为什么**：MK 往任意 app 注入（用 `CGEvent` ⌘V + backspace），对目标文本 buffer 零控制权。想做「实时显示→替换」只能合成 backspace 删字——**在终端（cc/iTerm/Ghostty/Warp/VS Code）必死**：PTY 字节流不是文本框、erase char `^?`/`^H` 歧义、TUI 自绘不认合成键、合成事件≠真实按键。实测：往 cc 注入临时版 + backspace 替换 = 本地版没删掉 + 云版追加 = **重复**。
- **微信/飞书是反例不是榜样**：它们 Electron/CEF，在自家 WebView DOM buffer 内改，从不外注入。
- **marked text（NSTextInputClient）这条路对 MK 关着**：发送端 API 只存在于「系统注册输入法（InputMethodKit）」或特权听写服务；MK 是辅助功能 app，拿不到。要走得注册成输入法（UX 重，跟中文输入法冲突，已记为「暂不做的更重备选」）。
- **行业共识**（superwhisper / VoiceInk[开源铁证,只有 ⌘V paste] / Aqua / Wispr Flow 终端模式）= HUD 浮窗显示实时 + 目标只 paste 一次最终版。
- **实现**：`Sources/TranscriptionHUD.swift`（NSPanel 浮窗，目标窗口顶部居中、AX 取 frame、磨玻璃黑底灰边圆角、随文字撑高）。`VoiceModule` 两条路径（live/非live）已合并：热键按下 show HUD → live 段只 `hud.update()` 不进 app → 松手 setProcessing → 引擎整段产出 → `pipeline.process` 单次回填 + `hud.showFinal` 停留淡出。`handleLiveSegment` 不再 `TextInjector.pasteText`。
- **状态流规格**（用户定，2026-06-09）：按下即显监听态(距窗顶~60px,clamp可见区)；说话中浮窗实时；松手 finalizing 不立即消失；final 回填成功后停留 600ms 淡出；**paste 失败/目标丢失→不消失，给重粘/复制/取消 交互 fallback（🔴 待做）**。视觉：宽 clamp(360,窗宽×0.25,640)、高 min64/max240 留尾、bg rgba(18,18,18,0.72)、边 rgba(255,255,255,0.16)、圆角16。
- 分支：`lengmo_*` MK 仓（GuinsooRocky/mk，单人，无 PR review）。

## 文档偏好（2026-05-22 用户明确改）

MK **不要**产品演进 / changelog / 逐次 session recap 那套（之前的 `docs/sessions/` 累积式 recap 规则作废）。**只维护一份"最新当前态"的 doc**（覆盖更新，不堆历史）。

用户原话："mk 的产品演进什么的都不必要，就留最新的 doc 就行"。

## 已知坑 + dev 验证（2026-05-30 实测）

- **streaming 注入已整个删除（2026-06-09）**：`StreamingInjector.swift` 删（→废纸篓）、菜单「流式注入」toggle 删、`streaming_enabled` config 删。原因见下「注入架构」。
- **长句根因 = SenseVoice 整段无 VAD**：NAR 离线模型整段塞 >10s 音频会延迟暴涨 + 中段塌只剩头尾。已接 silero VAD 切段（`SenseVoiceEngine.transcribeSegmented`，>10s 才切）。silero 模型 `~/.mk/models/silero_vad.onnx`（~640KB），`download-model.sh` 会下。
- **不用麦克风验证文本管线**：`DYLD_LIBRARY_PATH=client/Vendor/sherpa-onnx/lib <bin> --test-pipeline "原始文本"` 打印 RAW→DICT→NUMBER→FILLER→PUNCT 各层。dev 裸二进制在 `client/.build/arm64-apple-macosx/debug/MK`（rpath 解析不到 dylib，必须带 DYLD_LIBRARY_PATH）。
- **改了代码要 `make install` + 重启 MK 才生效**（老进程认旧二进制）；签名用 keychain 里的 `MK Development` 证书，重启不丢 TCC 授权。

## How to apply

- 用户提到"MK"、"语音输入"、"麦克风工具"在 mk 仓库工作时，遵循该项目的约定（仓库根 `.claude/CLAUDE.md` 是 ground truth）
- 引擎切换决策按上面的"方向 + 痛点边界"判断，不要重提"换其他引擎"除非用户明示
