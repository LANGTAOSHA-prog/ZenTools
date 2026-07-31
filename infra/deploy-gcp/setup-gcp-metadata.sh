#!/usr/bin/env bash
# ============================================================
#  把部署公钥写入 GCP VM 实例元数据（ssh-keys），并配置开机脚本。
#  这样即使 VM 重启 / 被重置，GCP 也会自动把公钥注入 authorized_keys，
#  不再依赖手动维护，GitHub Actions 的 GCP 步不会再 Permission denied。
#
#  前置：本机已装 gcloud 且已 `gcloud auth login` / 配置好项目。
#  用法：
#    export GCP_INSTANCE=<你的VM实例名>
#    export GCP_ZONE=<zone，如 us-central1-a>
#    bash setup-gcp-metadata.sh
# ============================================================
set -euo pipefail

INSTANCE="${GCP_INSTANCE:?请先设置环境变量 GCP_INSTANCE（VM 实例名）}"
ZONE="${GCP_ZONE:?请先设置环境变量 GCP_ZONE（如 us-central1-a）}"

# 注意：写入 GCP 实例 ssh-keys 元数据时，格式必须是 "用户名:密钥"，
# Guest Agent 才能知道把公钥注入到哪个用户的 ~/.ssh/authorized_keys。
# 漏掉 "taojiangtj:" 前缀会导致该行被跳过、重启后公钥仍未注入（部署继续 Permission denied）。
DEPLOY_PUBKEY="taojiangtj:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINtNXLsL3eo2G8/fEN2RcIhJWlk0h4OWl3PC9ASD/kJX zentools_gcp"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------- 1) 追加部署公钥到实例 ssh-keys 元数据（不覆盖现有 key） ----------
EXISTING="$(gcloud compute instances describe "$INSTANCE" --zone="$ZONE" \
  --format="value(metadata.ssh-keys)" 2>/dev/null || true)"

if ! printf '%s\n' "$EXISTING" | grep -qF "$DEPLOY_PUBKEY"; then
  if [ -n "$EXISTING" ]; then
    NEW_KEYS="$EXISTING"$'\n'"$DEPLOY_PUBKEY"
  else
    NEW_KEYS="$DEPLOY_PUBKEY"
  fi
  gcloud compute instances add-metadata "$INSTANCE" --zone="$ZONE" \
    --metadata "ssh-keys=$NEW_KEYS"
  echo "==> 已把部署公钥追加进实例 ssh-keys 元数据"
else
  echo "==> 部署公钥已存在于实例 ssh-keys 元数据，跳过"
fi

# ---------- 2) 配置开机脚本（从本仓库同目录读取 vm-startup.sh） ----------
gcloud compute instances add-metadata "$INSTANCE" --zone="$ZONE" \
  --metadata-from-file "startup-script=$SCRIPT_DIR/vm-startup.sh"
echo "==> 已配置 startup-script 元数据"

# ---------- 3) 立即重启让开机脚本生效（首次需要） ----------
read -r -p "是否现在重启 VM 让开机脚本立即生效？(y/N) " ANS
if [[ "$ANS" =~ ^[Yy]$ ]]; then
  gcloud compute instances reset "$INSTANCE" --zone="$ZONE"
  echo "==> 已发送重启指令，VM 启动后会自动跑开机脚本"
else
  echo "==> 未重启。开机脚本将在下次 VM 启动时首次执行。"
fi
