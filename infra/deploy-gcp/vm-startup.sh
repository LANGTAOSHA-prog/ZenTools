#!/usr/bin/env bash
# ============================================================
#  ZenTools GCP VM 开机脚本（startup-script）
#  解决痛点：部署公钥（zentools_gcp）此前手动写进 authorized_keys，
#            一旦 VM 重启 / 被重置就会被清掉，导致 GitHub Actions 的
#            GCP 步 Permission denied 反复复发。
#  本脚本在每次 VM 启动时运行，确保：
#    1) 部署公钥常驻 taojiangtj 的 ~/.ssh/authorized_keys（幂等去重）
#    2) 兜底：若 /var/www/zentools 因 VM 被重建而消失，自动恢复 目录/克隆仓库/nginx
#    3) 始终关闭旧 zentools-sync.timer（部署已改 rsync 推，timer 会把新文件 revert 回 git HEAD）
#  配置方式（二选一）：
#    a) gcloud compute instances add-metadata <VM> --metadata-from-file startup-script=vm-startup.sh
#    b) GCP 控制台 VM「自定义元数据」加键 startup-script、值贴本脚本全文
# ============================================================
set -uo pipefail

DEPLOY_PUBKEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINtNXLsL3eo2G8/fEN2RcIhJWlk0h4OWl3PC9ASD/kJX zentools_gcp"
DEPLOY_USER="taojiangtj"
WWW="/var/www/zentools"

# ---------- 1) 部署公钥常驻 ----------
USER_HOME="$(getent passwd "$DEPLOY_USER" 2>/dev/null | cut -d: -f6)"
[ -z "$USER_HOME" ] && USER_HOME="/home/$DEPLOY_USER"
AUTH="$USER_HOME/.ssh/authorized_keys"
mkdir -p "$USER_HOME/.ssh"
chmod 700 "$USER_HOME/.ssh"
if ! grep -qF "$DEPLOY_PUBKEY" "$AUTH" 2>/dev/null; then
  echo "$DEPLOY_PUBKEY" >> "$AUTH"
fi
chmod 600 "$AUTH"
chown -R "$DEPLOY_USER":"$DEPLOY_USER" "$USER_HOME/.ssh" 2>/dev/null || true

# ---------- 2) 兜底重建（目录缺失 = VM 被重建过） ----------
if [ ! -d "$WWW" ]; then
  echo "==> [startup] $WWW 缺失，重建基础环境"
  apt-get update -y
  apt-get install -y nginx git certbot python3-certbot-nginx
  mkdir -p "$WWW"
  git clone --branch main --depth 1 https://github.com/LANGTAOSHA-prog/ZenTools.git "$WWW"
  chown -R www-data:www-data "$WWW" 2>/dev/null || true
  chmod -R o+rX "$WWW"
  if [ -f "$WWW/infra/deploy-gcp/nginx-zentools.conf" ]; then
    cp "$WWW/infra/deploy-gcp/nginx-zentools.conf" /etc/nginx/sites-available/zentools
    ln -sf /etc/nginx/sites-available/zentools /etc/nginx/sites-enabled/zentools
    rm -f /etc/nginx/sites-enabled/default
    mkdir -p /var/www/letsencrypt
    nginx -t && systemctl reload nginx
  fi
  # 证书需 DNS 已指向本机且 80 放通，重建后请手动：
  #   certbot --nginx -d zentools.xyz -d www.zentools.xyz --redirect
fi

# ---------- 3) 双保险：关闭旧 timer ----------
systemctl disable --now zentools-sync.timer 2>/dev/null || true

echo "==> [startup] ZenTools GCP 开机脚本完成"
