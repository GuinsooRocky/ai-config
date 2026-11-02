---
name: brew-ca-certificates-hook-broken
description: 本机 brew ca-certificates 的 post-install 钩子静默失败，证书 bundle 需手动重建（影响 yt-dlp/certifi 系工具的 SSL）；本机 Clash（127.0.0.1:7897）没开时 GitHub push/fetch/ls-remote 直连会 Connection reset / 超时，soliloquy 发版脚本的 ssh 也靠这个 SOCKS 口，brew upgrade 同样要它
metadata: 
  node_type: memory
  type: project
  originSessionId: 9513f580-1b7b-453b-9235-c4e9274897a5
  modified: 2026-11-02T07:52:51.234Z
---

2026-06-11 实锤：`brew postinstall ca-certificates` 在本机始终失败且不报原因（沙箱内外都失败），导致 `/opt/homebrew/etc/ca-certificates/cert.pem` 缺失 → brew certifi 的 cacert.pem 是指向它的断链 → 依赖 brew certifi 的工具（yt-dlp 等）启动即崩 `FileNotFoundError ... load_verify_locations`。

**Why:** video skill 的字幕/转写线依赖 yt-dlp；这类 SSL 报错表象在工具、根因在证书链，重装工具本身（`brew reinstall yt-dlp`）无效。

**How to apply:** 再遇到 brew 系 Python 工具报 CA bundle FileNotFoundError，直接手动重建（已验证有效）：
```bash
mkdir -p /opt/homebrew/etc/ca-certificates
security find-certificate -a -p /System/Library/Keychains/SystemRootCertificates.keychain > /tmp/_c1.pem
security find-certificate -a -p /Library/Keychains/System.keychain > /tmp/_c2.pem
cat /tmp/_c1.pem /tmp/_c2.pem > /opt/homebrew/etc/ca-certificates/cert.pem && chmod 644 同文件
```
注意：brew 升级 ca-certificates 后钩子可能失败，该文件可能再次丢失，照方抓药即可。另：B 站裸请求 412 属风控（与 SSL 无关）；勿轻易 `brew upgrade yt-dlp`——可能级联升级 python formula，有打断 sf-reader-all venv 的风险，升级前先确认 sf-reader 的 python 来源。

**2026-10-08 批量升级教训**：本机不开代理（ClashX 7897）时 `brew upgrade` 必败——清华镜像只管瓶子，每个包仍要去 ghcr.io 取 manifest，直连约一半 SSL 超时，任一失败整批中止（无 env 可跳过，bottle.rb `github_packages_manifest_resource` 写死）。逐个升也不行：被依赖多的包要连带取一串 manifest。**半截升级会坏依赖**：abseil 先升了、protobuf 没跟上 → protoc dyld 找不到 `libabsl_*.2407` → 把新 keg 挪废纸篓 + `brew link abseil` 回退。下次升级：先开代理、`brew pin pnpm ruby tea`（大版本会破用法），升完核对 cert.pem，缺了就重建；sf-reader venv 走 opt 路径，升级后一般不断，断了再 `pipx reinstall-all`。

**2026-10-08 走代理升级成功**：`https_proxy=http://127.0.0.1:7897 no_proxy=mirrors.tuna.tsinghua.edu.cn` + pin pnpm/ruby/tea → 108 个一次过、约 10 分钟；这次 ca-certificates postinstall **自己成功了**（cert.pem 已更新），sf-reader venv 没断（venv 走 opt 路径）。副作用：certifi 拉进 python@3.14，`/opt/homebrew/bin/python3` 变 3.14（versioned 3.13 不再提供无版本号链接），hook 全是标准库、实测无影响。

## GitHub 要开 Clash（7897）

2026-10-12 实锤：`lsof -iTCP:7897` 无监听时，`git push/fetch origin`（github.com）连续 `Recv failure: Connection reset by peer`，`curl https://github.com` 15 秒超时 000；不是仓库或凭证问题。

**Why:** 日本住宅网到 GitHub 的直连会被中途切（soliloquy `docs/ops/2026-09-13-Web发版链路抖动与SOCKS绕行.md` 记过同源现象）；`~/.ssh/config` 里 soliloquy 生产机 `167.179.78.237` 也挂了 `ProxyCommand nc -X 5 -x 127.0.0.1:7897`，Clash 不开 `pnpm release:web` 第一步 ssh 就死。

**How to apply:** 推送/发版前先 `lsof -nP -iTCP:7897 -sTCP:LISTEN`；没监听 → 让 owner 开 Clash，别自己改网络设置、别无限重试。开着仍卡住（10-13 实测 7897 在监听、`git fetch` 直连照样挂 >120s——git 不会自动走 Clash）→ 命令前加 `git -c http.proxy=http://127.0.0.1:7897 …`，ai-config 这类 https remote 立刻通；再不行才查别的。brew 升级同样要它，见本文件上文。
