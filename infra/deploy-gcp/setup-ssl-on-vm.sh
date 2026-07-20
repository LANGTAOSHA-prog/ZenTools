#!/usr/bin/env bash
# ============================================================
#  ZenTools 国外节点 - 一键申请 Let's Encrypt 证书 + 启用 HTTPS
#  在 GCP Debian 实例上运行（需 Aliyun AccessKey 凭证）：
#    export ALIBABACLOUD_ACCESS_KEY_ID=xxxx
#    export ALIBABACLOUD_ACCESS_KEY_SECRET=xxxx
#    sudo -E bash setup-ssl-on-vm.sh
#  作用：
#    1) 装 certbot + certbot-dns-aliyun（venv /opt/certbot）
#    2) 写 /etc/letsencrypt/aliyun.ini（用上面环境变量）
#    3) DNS-01 申请 zentools.xyz + www.zentools.xyz 证书
#       （与解析路由无关，智能 DNS 分流也不影响）
#    4) 单独写 443 server 块（不改动你现有的 80 配置）
#    5) nginx -t 校验并重载
#    6) 配置证书自动续期 timer
#  注：证书已存在则跳过申请；nginx 已有 443 监听则跳过写 443 块。
# ============================================================
set -euo pipefail

AK="${ALIBABACLOUD_ACCESS_KEY_ID:-}"
SK="${ALIBABACLOUD_ACCESS_KEY_SECRET:-}"
DOMAIN="zentools.xyz"
EMAIL="${LETSENCRYPT_EMAIL:-admin@zentools.xyz}"
VENV="/opt/certbot"

if [ -z "$AK" ] || [ -z "$SK" ]; then
    echo "✗ 缺少 Aliyun 凭证，请先："
    echo "  export ALIBABACLOUD_ACCESS_KEY_ID=xxxx"
    echo "  export ALIBABACLOUD_ACCESS_KEY_SECRET=xxxx"
    echo "  然后 sudo -E bash $0"
    exit 1
fi

echo "==> [1] 安装 certbot + certbot-dns-aliyun (venv $VENV)"
apt-get update -y
apt-get install -y python3-venv
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip certbot certbot-dns-aliyun

echo "==> [2] 写入凭证文件 /etc/letsencrypt/aliyun.ini"
mkdir -p /etc/letsencrypt
# 注意：certbot-dns-aliyun 2.x 要求顶层键（无段名）且带 certbot_ 前缀，
# 用 [certbot_dns_aliyun] 段或 dns_aliyun_access_key（无前缀）都会报 Missing properties。
cat > /etc/letsencrypt/aliyun.ini <<INI_EOF
certbot_dns_aliyun_access_key = $AK
certbot_dns_aliyun_access_key_secret = $SK
INI_EOF
chmod 600 /etc/letsencrypt/aliyun.ini

echo "==> [3] DNS-01 申请证书"
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "    证书已存在，跳过申请（如需重签可先删 /etc/letsencrypt/live/$DOMAIN）"
else
    "$VENV/bin/certbot" certonly \
        --authenticator dns-aliyun --dns-aliyun-credentials /etc/letsencrypt/aliyun.ini \
        -d "$DOMAIN" -d "www.$DOMAIN" \
        --non-interactive --agree-tos -m "$EMAIL" \
        --cert-name "$DOMAIN" || {
        echo "✗ 证书申请失败：检查 Aliyun AccessKey 与 RAM 权限（需 alidns:*）"
        exit 1
    }
fi

echo "==> [4] 写入 443 server 块 /etc/nginx/sites-enabled/zentools-ssl.conf"
if grep -rq "listen 443" /etc/nginx/sites-enabled/ 2>/dev/null; then
    echo "    检测到已有 443 监听配置，跳过写入（请确认你自己的配置已引用证书）"
else
    cat > /etc/nginx/sites-enabled/zentools-ssl.conf <<NGINX_EOF
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name $DOMAIN www.$DOMAIN;

    root /var/www/zentools;
    index index.html;

    ssl_certificate     /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_session_cache   shared:SSL:10m;

    # 安全：禁止访问 Git/VCS 元数据与敏感文件（防源码泄露）
    location ~ /\.git      { deny all; }
    location ~* \.(env|ini|sql|bak|key|pem)$ { deny all; }

    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript application/xml image/svg+xml application/ld+json;

    location ~* \.(?:css|js|png|jpg|jpeg|gif|svg|ico|webp|woff2?|ttf|eot|json)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }
    location / { try_files $uri $uri/ $uri.html /index.html; }
}
NGINX_EOF
fi

echo "==> [5] 校验并重载 nginx"
nginx -t
systemctl reload nginx

echo "==> [6] 配置证书自动续期"
cat > /etc/systemd/system/certbot-renew.service <<'R_EOF'
[Unit]
Description=Certbot renewal (venv)

[Service]
Type=oneshot
ExecStart=/opt/certbot/bin/certbot renew --quiet
R_EOF
cat > /etc/systemd/system/certbot-renew.timer <<'RT_EOF'
[Unit]
Description=Certbot renewal timer (twice daily)

[Timer]
OnCalendar=*-*-* 00,12:00:00
Persistent=true

[Install]
WantedBy=timers.target
RT_EOF
systemctl daemon-reload
systemctl enable --now certbot-renew.timer

echo "==> 完成。验证："
echo "  curl -I https://$DOMAIN/faq.html"
echo "  echo | openssl s_client -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates -issuer"
