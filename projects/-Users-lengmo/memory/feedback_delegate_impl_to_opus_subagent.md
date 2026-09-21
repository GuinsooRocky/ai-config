---
name: feedback-delegate-impl-to-opus-subagent
description: 派工七件事：>50KB 逐条判断类先压缩输入、只读的浏览器走查派 visual-qa、收产出逐文件核（补丁 diff 回它的树 + 测试用 per-file JSON reporter；git apply --3way 会静默吞 hunk 且退码 0）、跨仓派工别用 isolation:worktree、两 agent 各做契约一侧必须跨仓喂真实字节、改线上配置的点验主会话自己用 chrome 做（visual-qa 不认转述授权）、批次先 plan 再派实作、主会话只检查（2026-09-13）——选 model 口径在 model-dispatch §2
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1a98655-f407-4a08-98df-2abae18cf430
  modified: 2026-09-21T09:00:00.000Z
---

> 选型口径（显式写 `model` 别靠继承、档位 ≥ 任务所需、拿不准往上取、2026-08-06 主会话默认换 Fable 后仍显式 `opus`）以及「独立派工放同一条消息并行发」已全量落 `~/.claude/model-dispatch.md` §2/§7，本文件只留那边没有的三条。

**Why:** 2026-07-10 onlychat create component test 战役连续三次纠偏（派 sonnet 扫路由被改 opus、主对话亲写测试被打断「用子agent opus 写就行」、串行写 4 个测试文件被问「不可以开3个子agent一起吗」）催生了制度化；之后又长出三条 model-dispatch 覆盖不到的执行面裁决，记在这里。

**How to apply:**

**① 派工前先压缩输入（2026-07-27）**：派 agent 标注一份 182KB 的清单（133 条），我图省事直接把整个文件丢给它，一趟烧 174k token，用户当场质疑「写文件花 174.4k？」。**贵不在写，在读**——长文档进了 context，agent 每多说一句都要把它重带一遍，40 个工具调用 = 那笔底子被重复计 40 次。判据：
- 逐条分类/标注/核账类 → **先用命令抽结构**（标题行、编号、关键字段）几 KB 丢过去，**只对判不准的那几条再读全文**
- 需要全文的场合（写代码、改逻辑、审 diff）照旧给全，别为省 token 让它盲改
- 粗判据：**输入 > 50KB 且任务是「逐条判断」= 该压缩了**
- 同日实测对照：审查那批 25 个 agent 是值的（挖出 82 条真缺陷、两条 P0 赶在迁移固化前修掉）；**贵得没道理的恰恰是「读长文档做标注」这种活**

**② 浏览器走查/点验也算执行（2026-07-16 边界扩大）**：主 agent 亲自跑浏览器截图走查（HTML 交付验收）被叫停——「这件事要拿子agent来做啊 主agent 只用来做 决策 思考 调度」。执行类不止写码/扫描：**浏览器走查、点验、跑验证一律派子 agent（走查归 visual-qa），主对话只列 checklist + 收报告裁决**。

**③ 收产出必须逐文件核（2026-07-11 create-test 战役 + 2026-08-07 补丁吞 hunk，合并自 feedback_verify_subagent_patch_against_worktree）**：
- 测试产出：主对话勾选清单前用 per-file JSON reporter 逐文件核用例数，别只看总绿；agent 别 mv 自己的产出文件（第八波 mv 丢过文件）。
- worktree 补丁：`git apply --3way` **会静默丢掉整个 hunk**——只要我在同一文件邻近行也改过（哪怕是注释）。它打印 `Falling back to direct application...` 就走了，退码 0。2026-08-07 soliloquy 搬聊天页，agent 修的一条登记指向就这么没了，子 agent 报告写「已修」、补丁也「应用成功」，两边都没撒谎，东西就是没进来。收完逐文件比回去：
  ```bash
  WT=<agent worktree>
  for f in $(git -C "$WT" diff --cached -M --name-only); do
    [ -f "$f" ] && [ -f "$WT/$f" ] && { diff -q "$f" "$WT/$f" >/dev/null || echo "≠ $f"; }
  done
  ```
- 连带：闸别在主目录跑。主目录常混着别的会话的未提交改动，会掩盖真红（同一提交混合树全绿、干净树红）。落主线前在 `git worktree add --detach <sha>` 的干净树上跑一遍。相关 [[feedback_not_ground_truth]]。

**④ 跨仓派工别用 `isolation: worktree`（2026-09-11）**：Agent 工具的 worktree 隔离**只会建在当前主工作目录那个仓**，而且隔离闸会拒绝 agent 对任何别的仓做 git 操作（连只读 `git log` 都拒）。T252 同时派 soliloquy + eval-arena 两个仓，eval-arena 那个 agent 分到的是 soliloquy 的 worktree，`apps/admin` 根本不存在，零改动交回、白烧 228s/106k token。第二个仓的做法：**自己先 `git worktree add -b <branch> /private/tmp/<repo>-<task> main`、装好 node_modules（`pnpm install --frozen-lockfile --offline`）、把绝对路径和分支名写进 prompt、不带 isolation 派**。未提交的 PRD 在 worktree 里没有，让 agent 用主 checkout 的绝对路径只读。

**⑤ 两个 agent 各做契约一侧时，验收必须喂真实字节（2026-09-11）**：T252 产品侧 + 后台侧各按同一份 PRD 附录 A 写、各写各的严格解析器和测试固定装置、各自全绿，但把产品真实回执喂进后台解析器，三条主路径全部判废（null 字段、revision 0）——功能从迁移跑完那刻起自锁死，任何一侧的测试都测不出来。派工书里要写死：**交付前用 `tsx` 跨仓 import 两侧模块、把一侧的真实产出喂另一侧的解析器跑一遍，输出附报告**；集成会话再自己跑一次。bug-hunter 这次就是靠这一招抓到 3 条 P0。

**⑥ 改线上配置的浏览器点验，主会话自己做（2026-09-11）**：visual-qa 子 agent 不认转述的授权，哪怕逐字引用 owner 原话也不点「确认」这类改生产的按钮，派两次都停在弹层前、白跑约 20 分钟。第②条「浏览器走查派 visual-qa」只适用于只读走查和截图；**owner 在主对话里直接授权了会改线上的点验，就由主会话自己用 claude-in-chrome 做**，同时用接口挂监视器盯线上状态、准备好接口兜底回退。

**⑦ 施工批次的标准节奏：plan 模式出计划 → 派实作 → 主会话只检查（2026-09-13 owner 原话「plan模式 让子agent做 你来检查」）**：EnterPlanMode 里先派 Explore 侦察落点与在途改动、再派 Plan agent 写逐文件规格与可机械判定的验收，遇到会撞既有拍板的（那次是「8 篇冻结」）用 AskUserQuestion 一题一问带推荐，ExitPlanMode 批了才派实作。实作用 `isolation: worktree`（单仓好用：自动建在 `.claude/worktrees/agent-<id>`，`pnpm install --frozen-lockfile --offline` 就能跑闸），各在自己分支提交不 push；主会话收货时**自己在它的 worktree 里重跑显式测试 + tsc + grep 构建产物**，再 `merge --ff-only` 第一支、`cherry-pick` 第二支保线性，用完 `git worktree remove --force` + `branch -D`。发布走 Bash `run_in_background` + Monitor 盯阶段，失败先读日志找因（那次先是短 sha 被当非法参数、再是 docker 构建 30 分钟硬超时被网络吃掉），别盲目重试。
