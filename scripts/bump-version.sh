#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
part="${1:-patch}"
exec python3 "$repo_root/scripts/profile_state.py" bump "$part"
