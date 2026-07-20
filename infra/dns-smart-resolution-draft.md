# zentools.xyz — 国内直连阿里云 / 国外走 Cloudflare 加速（备案合规方案）

> 目标：**国内用户直连阿里云 ECS（备案合规），国外用户经 Cloudflare 边缘加速**，
> 同时 **DNS 权威始终留在阿里云（hichina），绝不把 NS 交给 Cloudflare**。

---

## 0. 为什么这么设计（合规要点）

- **ICP 备案要求**：备案域名在国内解析到的 IP 必须是中国内地服务器。
  当前 `zentools.xyz` / `www.zentools.xyz` 解析到 `39.96.10.135`（阿里云北京，AS37963），
  ip-api 已核实归属 `Aliyun Computing Co., LTD`，**符合要求**。
- **不能把 NS 切到 Cloudflare**：一旦 NS 交给 Cloudflare，全站解析都走 Cloudflare 海外节点，
  国内直连优势丧失，且备案解析 IP 变成海外 IP，存在合规风险。
- **正确做法 = 阿里云智能解析按线路分流**：
  - 默认 / 国内线路 → `39.96.10.135`（阿里云 ECS，直连）
  - 境外 / 国外线路 → Cloudflare 的接入目标（CNAME）
- **Cloudflare 侧用「不改 NS」的方式接入**：
  - 免费版 → **Cloudflare for SaaS（自定义主机名 / Custom Hostnames）**，需一个"提供方域名"完全托管在 Cloudflare。
  - Business/Enterprise → 直接用 **CNAME Setup（部分接入）**，无需提供方域名。

---

## 1. 架构一图

```
国内用户 ──DNS(阿里云 hichina, 国内线路)──▶ 39.96.10.135 (阿里云 ECS, nginx)
国外用户 ──DNS(阿里云 hichina, 境外线路)──▶ Cloudflare 边缘(提供方 zone 的 for-SaaS)──▶ 回源/Worker
                                                  │
                                  方案① CDN 回源 ECS(同内容, 推荐)
                                  方案② Route 到 Worker(zentools.taojianghu.workers.dev)
```

> 推荐 **方案①（Cloudflare 作为 CDN 回源 ECS）**：
> 海外拿到的是和国内完全一致的站点内容（由 deploy.yml 自动部署到 ECS），
> 不存在"Worker 内容与 ECS 不同步"的风险。方案② 仅在你想用它时才选。

---

## 2. Cloudflare 侧（你来做，需要 Cloudflare 账号）

> ⚠️ **前提（免费版绕不开）**：Cloudflare 免费版不支持"不改 NS 的部分接入"，
> 必须通过 **Cloudflare for SaaS（自定义主机名）** 实现；而它**需要一个已完全托管在 Cloudflare 的"提供方域名"(provider zone)**。
> 因为 `zentools.xyz` 的 NS 必须留在阿里云（备案），所以你**不能**把它整域交给 Cloudflare，
> 只能用另一个域名当提供方。

### 2.0 准备"提供方域名"（关键前置）
- 已注册提供方域名 **`zentools.qd.je`**（.je = Jersey ccTLD）。
  在 Cloudflare 用**标准方式（改 NS）完全托管**它 → 它成为提供方 zone。
- 此后所有加速都挂在 `www.zentools.xyz` 上，与提供方域名无关，用户无感知。
- ⚠️ 仅 `zentools.qd.je` 改 NS 到 Cloudflare；**`zentools.xyz` 的 NS 始终留在阿里云(hichina)，不可动**。

### 2.1 在提供方 zone 开启 Cloudflare for SaaS
1. Cloudflare 控制台 → 进入**提供方域名**的 zone。
2. 左侧 **SSL/TLS → Custom Hostnames（自定义主机名）** → 点击 **Enable（启用）**。
3. 按提示完成验证（通常会让你在**提供方域名**上加一条 TXT/CNAME，照做即可）。
4. 设置 **Fallback Origin / 回退源**，二选一：
   - 指向你的 Worker：`zentools.taojianghu.workers.dev`（方案②，海外内容与 Worker 一致）；
   - 或填 ECS 源站 `39.96.10.135`（方案① CDN 回源，需 ECS nginx 配好 HTTPS）。
   - **推荐填 Worker**（最简单，证书由 Cloudflare 自动管）。

### 2.2 添加自定义主机名 `www.zentools.xyz`
1. 同一 zone 的 **Custom Hostnames** 页 → **Add Custom Hostname（添加自定义主机名）**。
2. 主机名填 `www.zentools.xyz`。
3. 服务目标指向你刚设的回退源（Worker 或 ECS）。
4. Cloudflare 会**自动签发 `www.zentools.xyz` 的证书**，并给你一条
   **CNAME 目标**（形如 `www.zentools.xyz.cdn.cloudflare.net` 或 `xxxx.cloudflare.net`）。
   **记下这条 CNAME 目标 → 它就是 `CF_TARGET`，发给我。**

### 2.3（可选）让境外 `@` 也走 Cloudflare
根域名不能用 CNAME。若想境外 `@` 也加速，在 Custom Hostnames 里再加一个 `zentools.xyz` 即可，
Cloudflare 同样会给它发 CNAME 目标。不填则 `@` 始终直连阿里云（最省事）。

### 2.4 备选 A：直接上 Business 套餐做「CNAME Setup（部分接入）」
不想买第二个域名时：把 Cloudflare 套餐升到 **Business**，
在 `zentools.xyz` 的 zone 里直接用 **CNAME Setup（部分接入）**，Cloudflare 会直接给你 `www` 的 CNAME 目标，
无需提供方域名。代价：Business 按月付费（$）。

### 2.5 备选 B（更贴合国内用户）：阿里云 DCDN / CDN 海外加速
如果你只是要"国外也快"，**不一定非要 Cloudflare**：
- 阿里云 **全站加速 DCDN** 或 **CDN（开启海外节点）** 支持**纯 CNAME 接入**，不改 NS、备案友好、
  与阿里云 ECS 同生态、海外有节点。
- 做法：阿里云 CDN/DCDN 控制台添加域名 `www.zentools.xyz`、源站 `39.96.10.135`、开启海外加速，
  阿里云会给你一条 CNAME 目标 → 同样用 `setup_aliyun_dns_smart.py` 加进境外线路。
- 好处：不用第二个域名、不用 Cloudflare、备案与国内直连完全不受影响。

---

## 3. 阿里云侧（DNS 权威，做线路分流）

当前 zone（已核实）：
| RR | 类型 | 线路 | 值 | 状态 |
|----|------|------|----|------|
| www | A | default | 39.96.10.135 | 启用 |
| @   | A | default | 39.96.10.135 | 启用 |
| www | CNAME | default | langtaosha-prog.github.io | **禁用**(残留, 可删) |

要做的：
1. **删除** 那条禁用的 GitHub Pages CNAME 残留（`www` CNAME `langtaosha-prog.github.io`）。
2. **保留** `@` / `www` 的 `default` A → `39.96.10.135`（国内直连不变）。
3. **新增** `www` / `境外` / CNAME → `CF_TARGET`（Cloudflare 接入目标）。

> 用脚本 `setup_aliyun_dns_smart.py`（纯标准库，凭证走环境变量）：
```bash
# 预览（无需凭证，只需 CF_TARGET）
export CF_TARGET=www.zentools.xyz.cdn.cloudflare.net
python setup_aliyun_dns_smart.py

# 真实写入（需阿里云 AccessKey）
export ALIBABACLOUD_ACCESS_KEY_ID=xxxx
export ALIBABACLOUD_ACCESS_KEY_SECRET=xxxx
export CF_TARGET=www.zentools.xyz.cdn.cloudflare.net
# export CF_APEX_IP=104.16.x.x,172.67.x.x   # 可选：境外 @ 也走 Cloudflare
python setup_aliyun_dns_smart.py --apply
```
也可在阿里云控制台 **云解析 DNS → zentools.xyz → 添加记录**：
- 主机记录 `www`，类型 `CNAME`，线路类型 **境外 / 海外**，值 `CF_TARGET`，TTL 600。

---

## 4. 验证

```bash
# 国内视角（应仍解析到 39.96.10.135）
nslookup zentools.xyz
nslookup www.zentools.xyz

# 海外视角（用公共 DNS 模拟，应解析到 Cloudflare）
nslookup www.zentools.xyz 1.1.1.1
# 或 curl 经 Cloudflare：
curl -sS -o /dev/null -w "%{http_code} %{time_total}s\n" https://www.zentools.xyz/
```

---

## 5. 回滚

若海外异常，把 `www / 境外` 那条 CNAME 记录删除即可，国内立即恢复全直连。
（DNS 缓存最长按 TTL=600s 生效。）

---

## 6. 注意事项
- **备案**：国内线路始终直连阿里云（合规）。海外线路走 Cloudflare 是国内站点的
  常见加速做法，风险低；如所在管局有特别要求，可仅保留国内直连、不启海外线路。
- **证书**：方案① 用 Cloudflare 灵活 SSL 最简单；方案② 由 Cloudflare 自动签。
- **内容一致性**：方案①（回源 ECS）内容自动与国内一致；方案②（Worker）需自行保证同步。
- **`.monkeycode/` 等内部目录**：已由 deploy.yml 的 EXCLUDE 排除，不会上公网，与本次 DNS 改动无关。
