---
name: project_onlychat_pnpm_i18n_py312
description: "onlychat `pnpm i18n` 本机必挂(pandas 撞 python3.13);用 3.12 venv 直跑 i18n.py 绕开"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8ed4c0fe-e3fc-4e9e-843a-9e2b055e7f43
---

onlychat 的 `pnpm i18n`(从飞书 pull 多语言、全量重建 `src/i18n/*.json`)在本机**直接跑必失败**:脚本 `python3 -m venv venv` 用的是默认 python3=**3.13**,而 `localization/requirements.txt` 钉死 `pandas==2.1.4`,在 3.13 上无预编译 wheel→现编译 C 扩展报 `2 errors / ninja build stopped`→`metadata-generation-failed`。

**绕法**(本机有 `/opt/homebrew/bin/python3.12`,pandas 2.1.4 有 3.12 wheel):
```bash
cd ~/Desktop/cmm/<worktree>/localization
rm -rf venv && /opt/homebrew/bin/python3.12 -m venv venv
./venv/bin/pip install -q -r requirements.txt
# 直接跑 i18n.py(别再走 pnpm i18n,它会用 3.13 重建 venv 再挂):
./venv/bin/python3 i18n.py ./.temp/localizely_all.csv ../src/i18n/ \
  Y0uMsICffhOewutAk1Xc0NLJnqd zeHW5Z \
  en,pt,ru,de,it,fr,pl,es,id,ja,ko,fil,hi,ar,zh-tw
```
feature 分支(非 release/develop)会用传入的 **test 表 `zeHW5Z`**;release/develop 分支脚本内部改读对应表(online=`25kNVe`)。

**两个关键认知**(踩过):
1. `csvtojson` 是 `data={}` 从 CSV **全量覆盖重写**——飞书没有的 key 会被从本地 json **删掉**。所以判断"译文缺没缺"必须**重新 pull 飞书**,别拿陈旧本地 json 下结论(本次本地判 114 缺译,pull 后真相只 31)。
2. 全量 pull 会改写全部 15 个 json(混入别功能的翻译刷新),**不该塞进 feature 分支**。验证完用备份还原回"仅含本次改动"的干净态,只留 surgical diff。

相关:[[project_onlychat]] [[feedback_worldcard_worktree]] [[project_worldbook_dev_oom]]
