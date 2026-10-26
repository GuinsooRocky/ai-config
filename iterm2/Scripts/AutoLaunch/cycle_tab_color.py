#!/usr/bin/env python3
"""Cycle background colors for new iTerm2 tabs (Cmd+T / "+").

- Cmd+N (new window): untouched, keeps Default profile color.
- Split panes (Cmd+D / Cmd+Shift+D): untouched.
- Profiles whose name starts with "claude": untouched
  (claude-2/3/2h/3h scripts set their own pane colors).

Color pool, in cycle order:
  黑   #000000
  紫   #2a1a2a
  绿   #1a2e1a
  深蓝 #0a1432
"""
import os

import iterm2

COLORS = [
    (0, 0, 0),      # 黑
    (70, 30, 85),   # 紫
    (25, 70, 35),   # 绿
    (20, 45, 100),  # 深蓝
    (90, 50, 20),   # 棕橙
]

COUNTER_FILE = os.path.expanduser("~/.cache/iterm2-tab-cycle.idx")


def _read_counter() -> int:
    try:
        with open(COUNTER_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def _write_counter(n: int) -> None:
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
    with open(COUNTER_FILE, "w") as f:
        f.write(str(n))


async def _apply_cycle_color(app, session_id: str) -> None:
    session = app.get_session_by_id(session_id)
    if session is None:
        return

    profile = await session.async_get_profile()
    name = profile.name or ""
    if name.startswith("claude"):
        return

    tab = session.tab
    if tab is None:
        return
    window = tab.window
    if window is None:
        return

    if len(tab.sessions) > 1:
        return  # split pane, not a fresh tab
    if len(window.tabs) <= 1:
        return  # Cmd+N new window — leave the default alone

    n = _read_counter()
    r, g, b = COLORS[n % len(COLORS)]
    color = iterm2.Color(r, g, b)
    change = iterm2.LocalWriteOnlyProfile()
    # 现代 profile 启用 "Use Separate Colors for Light/Dark Mode" 时，渲染读 _dark/_light，
    # 老字段 background_color 被忽略 —— 三个一起写，所有情况都覆盖。
    change.set_background_color(color)
    change.set_background_color_dark(color)
    change.set_background_color_light(color)
    await session.async_set_profile_properties(change)
    _write_counter((n + 1) % len(COLORS))


async def main(connection):
    app = await iterm2.async_get_app(connection)
    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            try:
                await _apply_cycle_color(app, session_id)
            except Exception:
                # one bad session must not kill the daemon
                pass


iterm2.run_forever(main)
