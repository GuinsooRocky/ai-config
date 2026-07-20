---
name: feedback_git_contains_misses_cherrypick
description: 判断「某改动在不在某分支上」禁用 git branch --contains（cherry-pick 换 hash 查不出），按内容查
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f2f56a2d-9fa8-4b35-961a-fc457b37287c
---

判断「某个改动有没有落到另一条分支」，**不能用 `git branch -r --contains <hash>`**——cherry-pick 会生成新 commit 对象、新 hash，`--contains` 只认对象身份，同内容照样报「不在」。

按内容查：
```bash
git log --oneline --format='%h %ci %an %s' origin/<branch> --grep="<commit message 关键词>"
git log --oneline origin/<branch> -5 -- <改动的文件路径>
diff <(git show A -- f | grep -E '^[+-][^+-]') <(git show B -- f | grep -E '^[+-][^+-]')
```

**Why**：2026-07-17 开 onlychat banner 7/17 期，用 `--contains` 判定叶昶的 HtmlRichText fix「只在 release-v6.27.0、没进 develop」，据此向 owner 报「banner 包会夹带别人未发布的改动」的假警报，差点卡住发布。owner 说「yechang 说 cp 到 develop 了，他这没检查出来啊」——按内容重查坐实：develop 上 `da98b3c35e` 14:28 在前，release 上 `e89b0a073e` 14:30 在后，标准 cherry-pick 顺序。**是我的检查方法有缺陷，不是人说错。**

**How to apply**：cherry-pick 密集的仓（onlychat 三条 release 线每周互相 cp）里，任何「这 commit 在不在 X 分支」的判断一律按内容验。人给的口头事实（「我已经发上线了」「已经 cp 过了」）跟工具结论打架时，先怀疑工具用法——尤其在拿它当理由去阻拦 owner 的时候。同源原则见 [[feedback_verify_capture_not_status]]（按内容特征校验、别凭状态码下结论）、[[feedback_dont_declare_infeasible]]（别急着替 owner 判死刑）。
