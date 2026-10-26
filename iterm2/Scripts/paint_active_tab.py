#!/usr/bin/env python3
"""One-shot sanity check: paint the currently-active session PURPLE.

Run from iTerm: Scripts menu → paint_active_tab.py.
If the active tab does NOT turn purple, the issue is profile/permission,
not the cycle daemon.
"""
import iterm2


async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window
    if window is None:
        print("no current window")
        return
    tab = window.current_tab
    if tab is None:
        print("no current tab")
        return
    session = tab.current_session
    if session is None:
        print("no current session")
        return

    profile = await session.async_get_profile()
    print(f"session profile name = {profile.name!r}")
    print(f"current bg color    = {profile.background_color}")

    change = iterm2.LocalWriteOnlyProfile()
    change.set_background_color(iterm2.Color(80, 30, 80))  # bright purple, hard to miss
    await session.async_set_profile_properties(change)
    print("painted PURPLE (80,30,80)")


iterm2.run_until_complete(main)
