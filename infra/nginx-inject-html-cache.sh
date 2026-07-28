#!/usr/bin/env bash
# ============================================================
#  源站 nginx 就地注入 HTML 缓存头（保留 certbot 已注入的 SSL 配置）
#  用法: bash nginx-inject-html-cache.sh <nginx-conf-path>
#  由 GitHub Actions 部署步调用：
#    - 仅在 location / 缺失 expires 时注入 1h 缓存头
#    - 绝不整文件覆盖（避免丢失 certbot 的 SSL 配置）
#    - 先做 nginx -t 校验，失败则回退到备份，不破坏现有服务
# ============================================================
set -uo pipefail

NG="${1:-/etc/nginx/sites-available/zentools}"

if [ ! -f "$NG" ]; then
    echo "INFO nginx 配置 $NG 不存在，跳过"
    exit 0
fi

if grep -q 'expires 1h' "$NG"; then
    echo "INFO $NG 已注入缓存头，跳过"
    exit 0
fi

cp "$NG" /tmp/nginx.inject.bak

python3 - "$NG" <<'PY'
import sys, io
p = sys.argv[1]
s = io.open(p, encoding='utf-8', newline='').read()
marker = 'location / {'
if marker in s:
    s = s.replace(marker, marker + '\n        expires 1h;\n        add_header Cache-Control "public";', 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
PY

if nginx -t >/dev/null 2>&1; then
    if systemctl reload nginx >/dev/null 2>&1; then
        echo "OK nginx reloaded: $NG (HTML 缓存头已生效)"
    else
        echo "WARN nginx reload 失败（可能无权限），请手动 reload 或配置免密 sudo"
    fi
else
    cp /tmp/nginx.inject.bak "$NG"
    echo "WARN nginx -t 失败，已回退: $NG"
fi
