#!/usr/bin/env bash
# Claude Code 状态栏：模型 │ 目录 │ git 分支 │ 上下文占用 │ 花费 │ 本次时长
# Claude Code 每次刷新会把会话信息(JSON)喂给 stdin，stdout 第一行渲染为状态栏

input=$(cat)
JQ=/usr/bin/jq

IFS=$'\t' read -r model model_id cwd transcript cost dur_ms < <(
  printf '%s' "$input" | "$JQ" -r '[
    .model.display_name // "?",
    .model.id // "",
    .workspace.current_dir // .cwd // "",
    .transcript_path // "",
    ((.cost.total_cost_usd // 0) | tostring),
    ((.cost.total_duration_ms // 0) | tostring)
  ] | @tsv'
)

C_MODEL=$'\033[1;35m'; C_DIR=$'\033[1;36m'; C_GIT=$'\033[1;33m'
C_OK=$'\033[1;32m';    C_WARN=$'\033[1;33m'; C_BAD=$'\033[1;31m'
C_DIM=$'\033[0;37m';   R=$'\033[0m'
SEP="${C_DIM} │ ${R}"

dir=$cwd
[[ "$dir" == "$HOME"* ]] && dir="~${dir#"$HOME"}"

git_seg=""
branch=$(git -C "$cwd" branch --show-current 2>/dev/null)
if [[ -n "$branch" ]]; then
  dirty=""
  [[ -n $(git -C "$cwd" status --porcelain --untracked-files=no 2>/dev/null | head -c1) ]] && dirty="*"
  git_seg="${SEP}${C_GIT}🌿 ${branch}${dirty}${R}"
fi

# 上下文占用：从 transcript 里取最近一条带 usage 的消息算 token 总量
ctx_seg=""
if [[ -f "$transcript" ]]; then
  used=$(tail -n 200 "$transcript" 2>/dev/null | "$JQ" -r '
    try (select(.isSidechain != true) | .message.usage | select(.input_tokens != null)
         | (.input_tokens + (.cache_read_input_tokens // 0) + (.cache_creation_input_tokens // 0)))
  ' 2>/dev/null | tail -n 1)
  if [[ "$used" =~ ^[0-9]+$ ]]; then
    limit=200000
    [[ "$model_id" == *"[1m]"* || "$model" == *"1M"* ]] && limit=1000000
    pct=$(( used * 100 / limit ))
    tok="$used"
    (( used >= 1000 )) && tok=$(awk -v n="$used" 'BEGIN{printf "%.1fk", n/1000}')
    c=$C_OK; (( pct >= 60 )) && c=$C_WARN; (( pct >= 85 )) && c=$C_BAD
    ctx_seg="${SEP}${c}📊 CTX ${pct}% (${tok})${R}"
  fi
fi

cost_seg=""
if awk -v c="$cost" 'BEGIN{exit !(c > 0)}'; then
  cost_seg="${SEP}${C_DIM}$(awk -v c="$cost" 'BEGIN{printf "💰 $%.2f", c}')${R}"
fi

dur_ms=${dur_ms%%.*}
mins=$(( dur_ms / 60000 ))
if (( mins >= 60 )); then t="$((mins / 60))h$((mins % 60))m"; else t="${mins}m"; fi

printf '%s\n' "${C_MODEL}🤖 ${model}${R}${SEP}${C_DIR}📁 ${dir}${R}${git_seg}${ctx_seg}${cost_seg}${SEP}${C_DIM}⏱ ${t}${R}"
