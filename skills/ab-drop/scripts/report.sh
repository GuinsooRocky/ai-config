#!/bin/bash
# 把当前或指定 session 设为必须上报 token 用量。
set -euo pipefail
exec "$(dirname "$0")/drop.sh" --report "$@"
