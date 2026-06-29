#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"

merged=$(git -C "$REPO" branch --merged HEAD 2>/dev/null | grep 'worktree-' | tr -d ' *' || true)

[ -z "$merged" ] && exit 0

worktree_info=$(git -C "$REPO" worktree list --porcelain 2>/dev/null)

for branch in $merged; do
  path=$(echo "$worktree_info" | awk -v b="refs/heads/$branch" '
    /^worktree / { p = substr($0, 10) }
    $0 == "branch " b { print p }
  ')

  if [ -n "$path" ] && [ "$path" != "$REPO" ]; then
    git -C "$REPO" worktree remove --force "$path" 2>/dev/null || true
  fi

  git -C "$REPO" branch -d "$branch" 2>/dev/null || true
done