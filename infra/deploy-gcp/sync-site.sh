#!/usr/bin/env bash
# ============================================================
#  ZenTools 站点同步脚本（GCP 国外节点）
#  从 GitHub 公开仓库拉取最新 main，使本机与 origin/main 完全一致。
#  由 systemd timer（zentools-sync.timer）每 10 分钟调用一次。
# ============================================================
set -euo pipefail

REPO_DIR="/var/www/zentools"
BRANCH="main"
LOG_FILE="/var/log/zentools-sync.log"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

if [ ! -d "$REPO_DIR/.git" ]; then
    echo "[$(ts)] SKIP: $REPO_DIR 不是 git 仓库（请先跑 setup-gcp.sh 克隆）" | tee -a "$LOG_FILE"
    exit 0
fi

cd "$REPO_DIR"

# 本地若有意外改动，强制对齐到远端（静态站，无需保留本地改动）
git fetch --all --prune --quiet
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "origin/$BRANCH")

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "[$(ts)] already up-to-date ($LOCAL)" >> "$LOG_FILE"
    exit 0
fi

git reset --hard "origin/$BRANCH" --quiet
git clean -fd --quiet
echo "[$(ts)] synced $LOCAL -> $REMOTE" | tee -a "$LOG_FILE"
