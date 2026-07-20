#!/usr/bin/env bash
# ============================================================
#  ZenTools 国外节点 - GCP 一键部署引导脚本
#  在一台全新的 Debian 12 / Ubuntu 22.04+ 实例上跑一次即可：
#    apt 安装 nginx + git + certbot
#    git clone 公网仓库到 /var/www/zentools
#    部署 nginx 配置 + 同步脚本 + systemd 定时任务
#    申请 Let's Encrypt 证书（需域名国外线路已指向本机）
#
#  用法（在实例上，需 root）：
#    export LETSENCRYPT_EMAIL=you@example.com   # 证书到期提醒用
#    bash setup-gcp.sh
# ============================================================
set -euo pipefail

REPO_URL="${ZENTOOLS_REPO:-https://github.com/LANGTAOSHA-prog/ZenTools.git}"
BRANCH="${ZENTOOLS_BRANCH:-main}"
WWW="/var/www/zentools"
LE_EMAIL="${LETSENCRYPT_EMAIL:-admin@zentools.xyz}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> [1/6] 更新 apt 并安装 nginx / git / certbot"
apt-get update -y
apt-get install -y nginx git certbot python3-certbot-nginx

echo "==> [2/6] 克隆仓库到 $WWW"
mkdir -p "$WWW"
if [ ! -d "$WWW/.git" ]; then
    git clone --branch "$BRANCH" --depth 1 "$REPO_URL" "$WWW"
else
    echo "    仓库已存在，跳过克隆（用 sync-site.sh 拉最新）"
fi

# 让 web 服务可读
chown -R www-data:www-data "$WWW" 2>/dev/null || true
chmod -R o+rX "$WWW"

echo "==> [3/6] 部署 nginx 配置"
cp "$SCRIPT_DIR/nginx-zentools.conf" /etc/nginx/sites-available/zentools
ln -sf /etc/nginx/sites-available/zentools /etc/nginx/sites-enabled/zentools
# 关掉默认站点，避免 server_name 冲突
rm -f /etc/nginx/sites-enabled/default
mkdir -p /var/www/letsencrypt
nginx -t
systemctl reload nginx

echo "==> [4/6] 部署同步脚本与 systemd 定时任务（每 10 分钟）"
cp "$SCRIPT_DIR/sync-site.sh" /usr/local/bin/sync-site.sh
chmod +x /usr/local/bin/sync-site.sh
cp "$SCRIPT_DIR/zentools-sync.service" /etc/systemd/system/
cp "$SCRIPT_DIR/zentools-sync.timer" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now zentools-sync.timer

echo "==> [5/6] 申请 Let's Encrypt 证书"
echo "    前提：DNS 国外线路(www + @)已指向本机外部 IP，且 80 端口已放开"
if certbot --nginx \
        -d zentools.xyz -d www.zentools.xyz \
        --non-interactive --agree-tos -m "$LE_EMAIL" \
        --redirect --uir; then
    echo "    证书申请成功，HTTPS 已启用"
    # 开启 certbot 自动续期（默认已装 timer，这里确认一次）
    systemctl enable --now certbot.timer 2>/dev/null || true
else
    echo "    [警告] 证书申请失败——请确认："
    echo "      1) GCP 防火墙已放通 80/443"
    echo "      2) 阿里云 DNS 国外线路已指向本机 IP 且生效（TTL 等待）"
    echo "      3) LETSENCRYPT_EMAIL 已设置"
    echo "    站点当前以 HTTP 提供；证书就绪后重跑："
    echo "      certbot --nginx -d zentools.xyz -d www.zentools.xyz --redirect"
fi

echo "==> [6/6] 完成"
echo "    站点目录 : $WWW"
echo "    同步间隔 : 10 分钟 (systemd timer)"
echo "    查看同步日志: tail -f /var/log/zentools-sync.log"
echo "    手动同步 : /usr/local/bin/sync-site.sh"
