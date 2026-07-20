#!/usr/bin/env bash
# ============================================================
#  ZenTools 国外节点 - 一键启用「每 10 分钟自动同步」
#  在 GCP Debian 实例上以 root 运行一次：
#    sudo bash setup-sync-on-vm.sh
#  作用：
#    1) 确保 /var/www/zentools 是 git 仓库（同步脚本依赖 .git；
#       若你是复制文件上去的，本脚本会自动 git init 并对齐 origin/main）
#    2) 写入 /usr/local/bin/sync-site.sh
#    3) 写入 systemd unit + timer（每 10 分钟）
#    4) 启用 timer 并手动跑一次验证
# ============================================================
set -euo pipefail

REPO_DIR="/var/www/zentools"
REPO_URL="https://github.com/LANGTAOSHA-prog/ZenTools.git"
BRANCH="main"

echo "==> [1] 确保 $REPO_DIR 是 git 仓库（同步脚本依赖 .git）"
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "    未检测到 .git，将其初始化为 git 仓库并对齐 origin/$BRANCH"
    cd "$REPO_DIR"
    git init -q
    git remote add origin "$REPO_URL"
    git fetch origin "$BRANCH" -q
    git reset --hard "origin/$BRANCH" -q
    git clean -fd -q
    # nginx(www-data) 只需读权限；.git 必须保持 root 拥有，否则 sync 以 root 运行时会
    # 触发 git "dubious ownership" 报错。用 world-readable 让 www-data 能读取即可。
    chmod -R o+rX "$REPO_DIR"
    chown -R root:root "$REPO_DIR/.git" 2>/dev/null || true
    echo "    已完成 git 初始化"
else
    echo "    已是 git 仓库，跳过"
fi

echo "==> [2] 写入同步脚本 /usr/local/bin/sync-site.sh"
cat > /usr/local/bin/sync-site.sh <<'SYNC_EOF'
#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="/var/www/zentools"
BRANCH="main"
LOG_FILE="/var/log/zentools-sync.log"
ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "[$(ts)] SKIP: $REPO_DIR 不是 git 仓库" | tee -a "$LOG_FILE"
    exit 0
fi
cd "$REPO_DIR"
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
SYNC_EOF
chmod +x /usr/local/bin/sync-site.sh

echo "==> [3] 写入 systemd unit + timer"
cat > /etc/systemd/system/zentools-sync.service <<'SVC_EOF'
[Unit]
Description=ZenTools site sync from GitHub (GCP overseas node)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/sync-site.sh
SuccessExitStatus=0
SVC_EOF

cat > /etc/systemd/system/zentools-sync.timer <<'TMR_EOF'
[Unit]
Description=ZenTools site sync timer (every 10 minutes)

[Timer]
OnBootSec=60
OnUnitActiveSec=600
Persistent=true

[Install]
WantedBy=timers.target
TMR_EOF

echo "==> [4] 启用 timer"
systemctl daemon-reload
systemctl enable --now zentools-sync.timer

echo "==> [5] 手动跑一次验证"
/usr/local/bin/sync-site.sh
echo "---- 排程 ----"
systemctl list-timers zentools-sync
echo "---- 最近日志 ----"
tail -n 5 /var/log/zentools-sync.log 2>/dev/null || true
echo "完成。"
