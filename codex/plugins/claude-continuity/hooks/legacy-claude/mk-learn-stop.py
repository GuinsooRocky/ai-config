#!/usr/bin/env python3
"""MK 学习模式 — Stop hook

仅当 ~/.mk/pending-learn-prompt.{session_id}.json 存在时（本 session 由 MK 注入并认领），
扫最后一条 assistant 响应里的 <learn>X→Y</learn> tag，调 mk --learn 落字典。

stdin JSON: {"session_id", "stop_reason", "transcript_path"}
stdout: 不输出（仅有 side effect 调 mk --learn）
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

MK_DIR = Path.home() / ".mk"
MK_BINARY = str(Path.home() / "Applications" / "MK.app" / "Contents" / "MacOS" / "MK")
LEARN_TAG_RE = re.compile(r"<learn>\s*([^<]+?)\s*</learn>")
# 支持 → 箭头、ASCII -> 、冒号
PAIR_SEP_RE = re.compile(r"\s*(?:→|->|:)\s*")
LOG_PATH = MK_DIR / "learn-stop.log"


def _log(msg: str):
    try:
        with LOG_PATH.open("a") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def _clear_pending(path: Path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    except Exception:
        pass


def main():
    _log("=== mk-learn-stop invoked ===")
    try:
        hook_input = json.load(sys.stdin)
        session_id = hook_input.get("session_id")
        _log(f"session_id={session_id}, stop_reason={hook_input.get('stop_reason')}")
    except Exception as e:
        _log(f"stdin parse failed: {e}")
        return

    if not session_id:
        _log("no session_id → skip")
        return

    session_pending = MK_DIR / f"pending-learn-prompt.{session_id}.json"
    if not session_pending.exists():
        _log(f"no session pending {session_pending.name} → skip")
        return
    _log(f"session pending exists: {session_pending.name}")

    # 止血补丁(2026-05-31)：只学确实出现在 ASR 注入文本里的错词。
    # 背景：原逻辑把整条 prompt 交给 LLM 找 ASR 误识，但 prompt 含手打补字，
    # LLM 分不清，手打错字/模型脑补会被误当 ASR 错例落字典。
    # 拿被认领 pending 里的 injected(=ASR 注入原文)做硬校验兜底。
    # 详见 ~/Desktop/MK-纠错学习bug-handoff.md。根治后可由新逻辑替换。
    try:
        _pending = json.loads(session_pending.read_text())
        injected_norm = (_pending.get("injected", "") or "").replace(" ", "")
    except Exception as e:
        _log(f"injected read failed: {e}")
        injected_norm = ""

    transcript_path = hook_input.get("transcript_path")
    if not transcript_path or not Path(transcript_path).exists():
        _log(f"transcript_path missing: {transcript_path!r}")
        _clear_pending(session_pending)
        return
    _log(f"transcript_path: {transcript_path}")

    last_text = _extract_last_assistant_text(transcript_path)
    if not last_text:
        _log("last_text empty")
        _clear_pending(session_pending)
        return
    _log(f"last_text len={len(last_text)}, head={last_text[:200]!r}")

    matches = LEARN_TAG_RE.findall(last_text)
    _log(f"tag matches: {matches}")
    learned = 0
    for tag in matches:
        for line in tag.splitlines():
            parts = PAIR_SEP_RE.split(line.strip(), maxsplit=1)
            _log(f"  tag={tag!r} line={line!r} split={parts}")
            if len(parts) != 2:
                continue
            wrong, correct = parts[0].strip(), parts[1].strip()
            if not wrong or not correct or wrong == correct:
                _log(f"  skip wrong={wrong!r} correct={correct!r}")
                continue
            # 止血校验：错词必须真在 ASR 注入文本里，否则疑似手打/脑补 → 拒学
            if injected_norm and wrong.replace(" ", "") not in injected_norm:
                _log(f"  skip(止血): wrong={wrong!r} 不在注入 ASR 文本里(疑手打/脑补)，拒学")
                continue
            try:
                result = subprocess.run(
                    [MK_BINARY, "--learn", wrong, correct],
                    capture_output=True, timeout=10, text=True,
                )
                _log(f"  mk --learn rc={result.returncode} stdout={result.stdout!r} stderr={result.stderr!r}")
                learned += 1
            except Exception as e:
                _log(f"  subprocess failed: {e}")

    _log(f"=== done, learned={learned} ===")
    _clear_pending(session_pending)


def _extract_last_assistant_text(transcript_path: str) -> str | None:
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("type") != "assistant":
            continue
        content = msg.get("message", {}).get("content", [])
        text_parts = []
        if isinstance(content, str):
            text_parts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
        text = "".join(text_parts)
        if text:
            return text
    return None


if __name__ == "__main__":
    main()
