---
name: reference_onlychat_cdn_batch_upload
description: onlychat 批量种图/拿 CDN fileURL 的浏览器 console 技法（querySignedUploadUrlV2 签名直传）
metadata: 
  node_type: memory
  type: reference
  originSessionId: 56e3808e-b62e-4541-938c-66ab21db5118
---

把一批本地图片刷进 onlychat CDN 拿回 fileURL 的技法（原 `~/Desktop/note-defaults/` 工具包，2026-06-17 删，能力存这）。用于世界卡笔记默认配图等"种图"场景。

**鉴权**：必须借浏览器已登录态，所以在 onlychat 页面 DevTools Console 跑，不能终端跑（这也是它不该做成 skill/agent 的原因——auth 绕不开 console，封装省不掉手动）。

**Console snippet**（选文件 → 逐个签名直传 → 输出 `文件名\tfileURL` 并复制剪贴板）：
```js
(async () => {
  const SIGN = '/api/trpc/character.querySignedUploadUrlV2?input=%7B%22json%22%3A%7B%7D%7D';
  const inp = Object.assign(document.createElement('input'), { type: 'file', multiple: true, accept: 'image/png' });
  inp.onchange = async () => {
    const files = [...inp.files].sort((a, b) => a.name.localeCompare(b.name));
    const out = [];
    for (const f of files) {
      try {
        const j = await (await fetch(SIGN, { headers: { accept: '*/*' } })).json();
        const u = j.result.data.json;                  // { uploadURL, fileURL }
        const r = await fetch(u.uploadURL, { method: 'PUT', body: f, headers: { 'Content-Type': f.type || 'image/png' } });
        out.push(f.name.replace(/\.[a-z]+$/i, '') + '\t' + (r.ok ? u.fileURL : 'PUT_FAIL_' + r.status));
      } catch (e) { out.push(f.name + '\tERR_' + e.message); }
      console.log(out[out.length - 1]);
    }
    const txt = out.join('\n'); console.log('=== COPY THESE LINES BACK ===\n' + txt);
    try { await navigator.clipboard.writeText(txt); } catch (e) {}
  };
  inp.click();
})();
```

**关键点**：签名接口 `character.querySignedUploadUrlV2` 返回 `{uploadURL, fileURL}`，PUT 直传到 `uploadURL`，`fileURL` 是最终 CDN 地址。非交互环境想跑就从 DevTools 把该请求 Copy as cURL（含 cookie）改造，别外发。世界卡笔记默认图按 6 类 × dark/light 命名（characters/events/items/locations/organizations/rules）。相关：[[project_onlychat]]、[[feedback_worldcard_worktree]]。
