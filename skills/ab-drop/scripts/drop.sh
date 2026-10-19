#!/bin/bash
# 白帽子：drop.sh [uuid]；黑帽子：report.sh [uuid]。缺省取当前 Claude / Codex 会话。
set -euo pipefail

mode=drop
if [[ "${1:-}" == --report ]]; then
  mode=report
  shift
fi
[[ $# -le 1 ]] || { echo "用法：drop.sh [--report] [uuid]" >&2; exit 1; }
sid="${1:-${CLAUDE_CODE_SESSION_ID:-${CODEX_THREAD_ID:-}}}"
[[ "$sid" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || {
  echo "拿不到合法 session uuid: '$sid'" >&2
  exit 1
}

rules="$HOME/.agentboard/privacy-rules.json"
node "$HOME/.agentboard/privacy-patch.mjs" check
updated="$(jq -e --arg sid "$sid" --arg mode "$mode" '
  def valid_list:
    type == "array" and all(.[]; type == "string" and test("\\S"));
  def same_session:
    . == $sid or . == ("claude:" + $sid) or . == ("codex:" + $sid);
  def permanent: endswith(":") or . == "-";
  if (.drop_all_personal | type) != "boolean"
      or (.drop_sessions | valid_list | not)
      or (.force_report_sessions | valid_list | not) then
    error("上报规则缺失或损坏，未修改名单")
  else . end
  | .drop_sessions |= map(select(same_session | not))
  | .force_report_sessions |= map(select(same_session | not))
  | if $mode == "report" then
      if any(.drop_sessions[];
        . as $rule | $rule != "codex:" and
        (("claude:" + $sid | contains($rule)) or ("codex:" + $sid | contains($rule)))) then
        error("该 session 仍命中其他屏蔽规则，未修改名单")
      else .force_report_sessions += [$sid] end
    else
      .drop_sessions = (
        [.drop_sessions[] | select(permanent)] +
        (([.drop_sessions[] | select(permanent | not)] + [$sid]) | .[-7:])
      )
    end
' "$rules")"

tmp="$(mktemp "${rules}.tmp.XXXXXX")"
printf '%s\n' "$updated" > "$tmp"
mv "$tmp" "$rules"
if [[ "$mode" == report ]]; then
  printf '已加黑（token 用量必须上报）: %s\n' "$sid"
else
  printf '已加白（不上报）: %s\n' "$sid"
fi
