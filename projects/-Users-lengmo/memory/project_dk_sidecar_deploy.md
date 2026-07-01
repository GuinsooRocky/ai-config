---
name: project_dk_sidecar_deploy
description: DK macapp 后端(sidecar)部署铁律——别 in-place 换+重签，会破 launchd self-spawn
metadata: 
  node_type: memory
  type: project
  originSessionId: 0bfe1fc4-f4f0-4519-a099-41dd432c58f7
---

DK 的 macapp 后端跑法：launchd job `com.lengmo.chatccbot`（plist 在 ~/Library/LaunchAgents/，设了 DK_ROOT + WorkingDirectory=repo 根）→ 启 `dk_sidecar supervisor` → supervisor `subprocess.Popen` 自我 re-exec 出 hub(8787)+各渠道。

**铁律：改后端只能整体重建 `bash macapp/build_app.sh`（swift release + build_sidecar.sh + 一次性 deep 签名），绝不 in-place 换 sidecar/swift 二进制 + 零敲碎打 `codesign --force` 重签。**

**Why（2026-06-21 踩坑，把 bot 搞停 1+ 小时）：**
- in-place `cp` 新二进制进 `dist/DK.app` + 反复 `codesign --force` 重签，破坏 .app bundle 封印；
- 更狠的是：**重建的 PyInstaller sidecar 在 launchd 上下文下 `subprocess.Popen([sys.executable, mode])` 自我 spawn 子进程会被 amfi/Gatekeeper 拦** → 现象：`launchctl kickstart` 后 supervisor 进程在跑但 **0 子进程、8787 永不 bind、out/err.log 空**。
- 关键判据：**同一个 sidecar 二进制在 shell 里 `DK_ROOT=<repo> ./dk_sidecar supervisor` 直跑 spawn 子进程完全正常**（交互上下文）。所以是 launchd 安全上下文问题，不是二进制坏、不是 DK_ROOT 缺（plist 里有）、不是 quarantine（xattr 清了也没用）。
- 连 coherent 的 `build_app.sh` 整体签完，launchd 仍 spawn 不出子进程 → 疑似需「从访达双击 DK.app 交互启动一次重新注册」才解（**未确认**，待验）。

**How to apply：**
- 部署/验 /notify 等后端改动：优先**临时 hub 旁路**——`CHATCC_SUPERVISED=1 HUB_PORT=8788 hub/.venv/bin/python -m hub.app`（源码跑、不碰正牌 bot、curl 完即杀）。frozen 二进制旁验要带 `DK_ROOT`，否则 app_root() 走 __file__ 落到 _internal 找不到 config。
- **应急恢复 bot**：`DK_ROOT=<repo> PYTHONUNBUFFERED=1 dist/DK.app/Contents/Resources/dk_sidecar/dk_sidecar supervisor &`（bridge 直跑，能 spawn；但非 launchd 托管，重启/注销不自启）。
- 真要换正牌后端：`build_app.sh` 整体重建后，**让用户从访达双击 DK.app 一次**再看 launchd 能否拉起，别只 `launchctl kickstart`。

相关：[[feedback_dk_commit_push_freely]]（DK 项目 commit+push 自由）。出站通知/监听 tab 代码在 ralph/auto。
