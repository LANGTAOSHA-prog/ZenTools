#!/usr/bin/env bash
# patch-block-git.sh — 封堵 GCP 节点 webroot 下 .git 及敏感文件的公网访问
# 在 GCP 实例上以 root 运行:  sudo bash patch-block-git.sh
# 背景: setup-gcp.sh 把整仓 git clone 到 /var/www/zentools, 若 nginx 不屏蔽 /.git,
#       海外访客可 GET /.git/config 并用 git-dumper 拖走全部源码。
set -euo pipefail

FILES=(/etc/nginx/sites-available/zentools /etc/nginx/sites-enabled/zentools-ssl.conf)

patched=0
for f in "${FILES[@]}"; do
  [ -f "$f" ] || { echo "跳过(不存在): $f"; continue; }
  grep -q 'location ~ /\.git' "$f" && { echo "已含 deny, 跳过: $f"; continue; }
  python3 - "$f" <<'PY'
import pathlib, sys
f = sys.argv[1]
rules = r'''    location ~ /\.git      { deny all; }
    location ~* \.(env|ini|sql|bak|key|pem)$ { deny all; }
'''
t = pathlib.Path(f).read_text()
i = t.rfind("}")
t = t[:i] + "\n" + rules + "\n" + t[i:]
pathlib.Path(f).write_text(t)
print("已修补:", f)
PY
  patched=1
done

if [ "$patched" -eq 0 ]; then
  echo "⚠️ 未发现可修补的 nginx 配置文件。请先确认配置文件真实路径:"
  echo "   grep -rl 'root /var/www/zentools' /etc/nginx/ 2>/dev/null"
  exit 1
fi

nginx -t && systemctl reload nginx
echo "✅ .git 及其它敏感文件已封锁, 复测应返回 403/404"
