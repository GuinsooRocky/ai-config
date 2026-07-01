# 📱 LAN 测试（手机扫码连本地 dev）

用户说"开 LAN / 测 h5 / 生码扫码 / 手机看本地"时执行。

## 步骤

1. 项目 `package.json` 的 `dev` 脚本加 `-H 0.0.0.0`（next dev 默认只绑 localhost）
2. `pkill -USR1 -f dev-watchdog.sh` 干净重启 dev
3. `ipconfig getifaddr en0` 拿 LAN IP（公司/VPN 网段可能不通，备选下面 tunnel）
4. `qrencode -t ANSIUTF8 "http://<LAN-IP>:3000"` 终端直接打 ASCII 二维码（brew qrencode 已装；**不要**导 PNG 开 Preview）
5. 手机同 wifi 扫码

## 登录 / OAuth 场景额外补丁

补 `.env.local` 改 `NEXTAUTH_URL`（host 不是 localhost 会挂）。

## 子网不通备选

`cloudflared tunnel --url http://localhost:3000` 出公网临时 URL，对码再生一次即可。
