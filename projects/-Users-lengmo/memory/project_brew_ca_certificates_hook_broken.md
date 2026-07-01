---
name: brew-ca-certificates-hook-broken
description: 本机 brew ca-certificates 的 post-install 钩子静默失败，证书 bundle 需手动重建（影响 yt-dlp/certifi 系工具的 SSL）
metadata: 
  node_type: memory
  type: project
  originSessionId: 9513f580-1b7b-453b-9235-c4e9274897a5
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
注意：brew 升级 ca-certificates 后钩子还会失败，该文件可能再次丢失，照方抓药即可。另：本机 yt-dlp 仍是 2025.4.30 旧版，B 站裸请求 412 属风控（与 SSL 无关）；勿轻易 `brew upgrade yt-dlp`——可能级联升级 python formula，有打断 sf-reader-all venv 的风险，升级前先确认 sf-reader 的 python 来源。
