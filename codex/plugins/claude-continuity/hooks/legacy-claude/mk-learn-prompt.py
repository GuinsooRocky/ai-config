#!/usr/bin/env python3
"""MK 学习模式 — UserPromptSubmit hook

仅当 ~/.mk/pending-learn-prompt.json 存在、< 30s、且 injected 文本出现在当前 prompt 时，
认领该 pending（rename 成 session 专属 pending-learn-prompt.{session_id}.json）并注入约定。
否则完全 passthrough（空 stdout），cc 行为 100% 不变。

stdin JSON: {"session_id", "prompt", "cwd"}
stdout: additionalContext 文本（cc 注入到 prompt）或空
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

PENDING_PATH = Path.home() / ".mk" / "pending-learn-prompt.json"
TTL_SEC = 30
LOG_PATH = Path.home() / ".mk" / "learn-prompt.log"


def _log(msg: str):
    try:
        with LOG_PATH.open("a") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def main():
    _log("=== mk-learn-prompt invoked ===")
    try:
        hook_input = json.load(sys.stdin)
    except Exception as e:
        _log(f"stdin parse failed: {e}")
        return

    session_id = hook_input.get("session_id")
    prompt_text = hook_input.get("prompt", "") or ""
    _log(f"session_id={session_id}, prompt_len={len(prompt_text)}, prompt_head={prompt_text[:80]!r}")
    if not session_id:
        _log("no session_id → skip")
        return

    if not PENDING_PATH.exists():
        _log("generic pending not exist → skip")
        return

    try:
        pending = json.loads(PENDING_PATH.read_text())
        scheduled_at = pending.get("scheduled_at", "")
        injected = pending.get("injected", "") or ""
        dt = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
        age = time.time() - dt.timestamp()
    except Exception as e:
        _log(f"pending parse failed: {e}")
        return
    _log(f"pending: age={age:.1f}s, injected_len={len(injected)}, injected_head={injected[:80]!r}")

    if age > TTL_SEC:
        _log(f"expired (age={age:.1f}>{TTL_SEC}s), unlink")
        try:
            PENDING_PATH.unlink()
        except Exception:
            pass
        return

    if injected and injected not in prompt_text:
        _log("injected NOT in prompt → not claiming (leave pending for real owner)")
        return

    session_pending = Path.home() / ".mk" / f"pending-learn-prompt.{session_id}.json"
    try:
        PENDING_PATH.rename(session_pending)
        _log(f"claimed → renamed to {session_pending.name}")
    except Exception as e:
        _log(f"rename failed: {e}")
        return

    # MK 刚注入过 + 用户提交了 prompt → 注入上报约定
    print(
        "<mk-learning-context>\n"
        "上面的 user message 由 MK 语音输入工具自动注入。MK 的 ASR 可能把词识别错，常见几类：\n"
        "  · 英文专有名词 → 中文音译（「飞哥妈」实为「Figma」、「逗客」实为「Docker」）\n"
        "  · 短英文词被识别错\n"
        "  · 中文词被英文化 / 中英混杂（「里main」实为「里面」这类音近、跨字符集误识）\n"
        "如检测到这类『明显音近误识、非用户本意』的错，在你响应的最最开头逐条加 tag：\n"
        '  <learn>里main→里面</learn>\n'
        "左边 = ASR 实际输出的错词，右边 = 用户本意。多对就多行（每对一个 tag）。\n"
        "只报音近误识；用户可能真想那么说的词、或你自己引用举例的词，都不要报。\n"
        "无识别错误则完全不输出此 tag。tag 之后再正常回答用户。\n"
        "</mk-learning-context>"
    )


if __name__ == "__main__":
    main()
