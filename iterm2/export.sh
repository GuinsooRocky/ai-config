#!/usr/bin/env bash
# 把本机 iTerm2 配置导出到本目录：主偏好（XML、去掉机器态）+ 动态 profile + 脚本。只写文件，不 commit。
# 主偏好里去掉的：NoSync*（iTerm2 自己约定的本机状态）、窗口几何、更新检查时间、动态 profile 的缓存副本（真相在 DynamicProfiles/*.json）。
#
# 新机器还原（先 ⌘Q 退出 iTerm2）：
#   defaults import com.googlecode.iterm2 ~/.claude/iterm2/com.googlecode.iterm2.plist
#   mkdir -p ~/Library/Application\ Support/iTerm2
#   cp -R ~/.claude/iterm2/DynamicProfiles ~/.claude/iterm2/Scripts ~/Library/Application\ Support/iTerm2/
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="$HOME/Library/Application Support/iTerm2"

/usr/bin/python3 -I - "$HOME/Library/Preferences/com.googlecode.iterm2.plist" "$here/com.googlecode.iterm2.plist" <<'PY'
import plistlib, sys
src, dst = sys.argv[1:3]
with open(src, "rb") as f:
    prefs = plistlib.load(f)
drop_prefixes = ("NoSync", "NSWindow Frame ", "NSSplitView Subview Frames ", "NSToolbar Configuration ")
prefs = {k: v for k, v in prefs.items() if not k.startswith(drop_prefixes) and k != "SULastCheckTime"}
prefs["New Bookmarks"] = [p for p in prefs.get("New Bookmarks", []) if not p.get("Is Dynamic Profile")]
with open(dst, "wb") as f:
    plistlib.dump(prefs, f, fmt=plistlib.FMT_XML, sort_keys=True)
PY

rsync -a --delete "$src/DynamicProfiles/" "$here/DynamicProfiles/"
rsync -a --delete "$src/Scripts/" "$here/Scripts/"
echo "已导出到 $here"
