---
name: feedback-delegate-impl-to-opus-subagent
description: 派工七件事：>50KB 逐条判断类先压缩输入、只读的浏览器走查派 visual-qa、收产出逐文件核（补丁 diff 回它的树 + 测试用 per-file JSON reporter；git apply --3way 会静默吞 hunk 且退码 0）、跨仓派工别用 isolation:worktree、两 agent 各做契约一侧必须跨仓喂真实字节、改线上配置的点验主会话自己用 chrome 做（visual-qa 不认转述授权）、批次先 plan 再派实作、主会话只检查（2026-09-13）——选 model 口径在 model-dispatch §2；多路并行查 bug / 修 bug 的实操教训：额度会打满、并发上限 20、文件归属硬边界、每路配独立审查、按组提交、子代理会往仓内写代理记忆、macOS 无 timeout；生成 prompt 的 7 条 rubric 已实体化进 write-a-prompt skill「质量线」节，按它逐条过别临场发挥
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1a98655-f407-4a08-98df-2abae18cf430
  modified: 2026-11-02T07:52:59.573Z
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

**④ 跨仓派工别用 `isolation: worktree`（2026-09-11）**：Agent 工具的 worktree 隔离**只会建在当前主工作目录那个仓**，而且隔离闸会拒绝 agent 对任何别的仓做 git 操作（连只读 `git log` 都拒）。T252 同时派 soliloquy + eval-arena 两个仓，eval-arena 那个 agent 分到的是 soliloquy 的 worktree，`apps/admin` 根本不存在，零改动交回、白烧 228s/106k token。第二个仓的做法：**自己先 `git worktree add -b <branch> /private/tmp/<repo>-<task> main`、装好 node_modules（`pnpm install --frozen-lockfile --offline`）、把绝对路径和分支名写进 prompt、不带 isolation 派**。未提交的 PRD 在 worktree 里没有，让 agent 用主 checkout 的绝对路径只读。**补（2026-10-22）：「当前主工作目录」指派工那一刻 Bash 的 cwd，不是会话起始目录**——前一条 Bash 为只读查 onlychat 做了 `cd`，紧接着派 perf-lab 的 agent，隔离 worktree 就建在 onlychat 里，agent 零改动交回。单仓派工前先 `cd` 回目标仓（或用 `git -C` 查别的仓、别 `cd`）。

**⑤ 两个 agent 各做契约一侧时，验收必须喂真实字节（2026-09-11）**：T252 产品侧 + 后台侧各按同一份 PRD 附录 A 写、各写各的严格解析器和测试固定装置、各自全绿，但把产品真实回执喂进后台解析器，三条主路径全部判废（null 字段、revision 0）——功能从迁移跑完那刻起自锁死，任何一侧的测试都测不出来。派工书里要写死：**交付前用 `tsx` 跨仓 import 两侧模块、把一侧的真实产出喂另一侧的解析器跑一遍，输出附报告**；集成会话再自己跑一次。bug-hunter 这次就是靠这一招抓到 3 条 P0。

**⑥ 改线上配置的浏览器点验，主会话自己做（2026-09-11）**：visual-qa 子 agent 不认转述的授权，哪怕逐字引用 owner 原话也不点「确认」这类改生产的按钮，派两次都停在弹层前、白跑约 20 分钟。第②条「浏览器走查派 visual-qa」只适用于只读走查和截图；**owner 在主对话里直接授权了会改线上的点验，就由主会话自己用 claude-in-chrome 做**，同时用接口挂监视器盯线上状态、准备好接口兜底回退。

**⑦ 施工批次的标准节奏：plan 模式出计划 → 派实作 → 主会话只检查（2026-09-13 owner 原话「plan模式 让子agent做 你来检查」）**：EnterPlanMode 里先派 Explore 侦察落点与在途改动、再派 Plan agent 写逐文件规格与可机械判定的验收，遇到会撞既有拍板的（那次是「8 篇冻结」）用 AskUserQuestion 一题一问带推荐，ExitPlanMode 批了才派实作。实作用 `isolation: worktree`（单仓好用：自动建在 `.claude/worktrees/agent-<id>`，`pnpm install --frozen-lockfile --offline` 就能跑闸），各在自己分支提交不 push；主会话收货时**自己在它的 worktree 里重跑显式测试 + tsc + grep 构建产物**，再 `merge --ff-only` 第一支、`cherry-pick` 第二支保线性，用完回收 worktree 和分支（mv 进废纸篓，不用 `remove --force`，细则见 [[feedback_cleanup_worktrees_when_done]]）。发布走 Bash `run_in_background` + Monitor 盯阶段，失败先读日志找因（那次先是短 sha 被当非法参数、再是 docker 构建 30 分钟硬超时被网络吃掉），别盲目重试。

## 多路并行查修流水线教训

2026-10-02～06 eval-arena 全量查 bug（23 路猎手 + 22 路对抗核查）与全量修复（3 波 16 路 + 每路独立审查）的教训：

- **额度**：20 路 opus 猎手每路约 55–65 万 token，一波就打满 5 小时额度，两天内还撞过周额度。大规模并行前先按「每路 ≈60 万」估总量，并按波提交，断了不丢活。
- **并发上限 20**：超出的派不出去，报错里写「Do not retry」，等有空位再派。
- **子代理会卡死**：多路同时等「自己起的后台测试」会卡住一天不交卷（截图里 1d 0h）。工单里写明「每修完一条就更新报告」「别等慢测试，没结果的写明由主对话跑」。慢模块（如 test_phase2_formal_execution 11 分钟）由主对话跑。
- **子代理按自带规则往仓内 `.claude/agent-memory/` 写记忆**，并发时互相覆盖索引、大量重复。派工 prompt 必写「不写代理记忆」；事后合并去重，多余的 mv 到 ~/.Trash。
- **macOS 没有 `timeout`/`gtimeout`**：简报里写 `timeout 30` 会让所有路各自踩一遍。改写 `perl -e 'alarm 30; exec @ARGV' <cmd>`。
- **修复用独立 worktree**（基于 origin/main 新分支，`git branch --unset-upstream` 防误推），`.venv` 软链到主检出，前端用 `pnpm install --frozen-lockfile --offline`。同一工作树里多路并行靠**文件归属硬边界**，agent 禁止一切 git 写操作，主对话按组 `git add <路径>` 提交。
- **每路修完配一个 fresh-context 审查**（T5），审查要实跑测试、专攻放宽的闸和改了口径的地方。本次 16 路里 7 路被审查退回返工，退回的全是真问题（写 0 混淆未知、放宽判据漏进程判活、把未知显示成失败、运行时拒收旧配置等）。
- **共用产物目录会被别的路清掉**：2026-10-11 soliloquy 画布三路浏览器验证共用一个证据目录，后跑的一路把目录当「半成品」整个 mv 进废纸篓，连带另一路 35 张截图 + 结果 JSON（从 ~/.Trash 捞回）。派工写明「每路只写自己前缀的文件、禁止清空/移动共享目录」，或干脆每路一个子目录。
- **额度打满中途断掉的代理用 SendMessage 原地续**：它们保留各自上下文，续跑不用重读材料；续之前先看工作树有没有改了一半的文件，并把断点前的成果先提交成检查点。
- **「这路改哪、那路别碰」要在派工时就切好接缝**：同一大文件多路改之前先派一路做行为不变的 1:1 拆分（逐步比 DOM 证明不变）并留接缝函数，再并行；跨路接口约束（如拖动直写 `translate`、别的路动画只许用 `transform`）一出现就 SendMessage 转给还在干的路。
- **「生产是否走得到」决定定级**：对抗核查前先用 ssh 只读实查服务器（服务单元、配置键名、账本大小、日志错误码计数），比仓内文档可靠。本次 2 条 P0 因此降为潜伏。

**Why:** owner 原话「多路并行」「把所有都修了」，整套流程跑下来可用，但上述每一条都实际绊过。
**How to apply:** 下次 >10 路并行时照此配置简报、工单、提交节奏。相关：[[model-dispatch]]

2026-10-11 soliloquy 全仓捉虫（28 路猎手 + 27 路对抗 + 3 路整理，约 3500 万 token）补充：
- **撞额度时 20 路同断，恢复后用 SendMessage 原地续跑全部成功**：报告文件就是检查点，续跑消息要写明「先看报告文件有没有内容、续写不重写、临时 Postgres 是否还在」。中断前已写完报告的路（dbmig2）续跑只花 2 万 token 收尾。
- **分区生成的排除正则别用裸单词**：`generated` 误排了 `generatedAssetLifecycle.ts`、`trafficPolicy.generated.ts`；先 `grep -i` 核一遍被排掉的源码文件再派。
- **数据库层分法可复用**：基线 pg_dump 按行段切 3 路（函数前半 / 后半 / 表·策略）+ 基线之后的迁移按时间切 2 路，每路都要「报之前先 grep 更晚迁移有没有重定义」；对抗核查强制本机 `initdb` 临时库实跑，7 条 P1 里有 4 条靠实跑定级（含 1 条推翻、3 条降级）。
- **对抗核查的裁定分布可当校准**：150 条里 CONFIRMED 68%、PARTIAL 24%、REFUTED 3%，猎手标 P1 的 26 条里 7 条降级——猎手的 P1 别直接给 owner。
- **接缝路要给「本仓无消费方」出口**：seamA 83 条路由里 45 条消费方在别的仓（eval-arena 后台），只能核服务端一侧，覆盖率要分开报。
- **整理员别串行**：一路整理 27 个分区的摘要会拖 1 小时以上，按 10 / 10 / 7 分三路各写各的文件再合并；给整理员的简报要求「只读报告不读源码、两份报告矛盾时才核一行」。
- **裁判自己留三类判断**：两份报告结论相反（设计 vs 缺陷）、两份对抗报告修法分歧、文档与记忆口径冲突——这三类整理员会标出来留给主对话，FINAL 里单列「裁判裁决」节。

2026-10-12 soliloquy 27 路并行修复补充：
- **文件归属路单 + 槽位时间戳**可行：每路一节「归你的文件」白名单 + 迁移时间戳槽位，27 路同树零冲突；共享文件（i18n JSON）给带锁的追加脚本、共享 docs 最后统一提交、`migrationReleasePlan.ts` / 退役目录由最后一路统一登记。
- **审查者的「临时还原 → 红 → 恢复 → 绿」必须写进简报**：27 路里 10 路被退回，全是审查者实跑抓出的（恒真断言、放宽闸、修一半、规格写宽）；返工后让同一审查者复审最省（上下文在）。
- **卡死识别**：agent 的 transcript mtime 停了几小时且没有子进程 = 死在 API 侧没通知；`TaskStop` 再 `SendMessage` 即可续，别重派。
- **owner 批准件别代签**：machine-release-override.json 这类带 decisionRef / approvedAt 的文件是 owner 批准记录，重绑哈希等 owner 一句话，先列待拍。
- **跨路请求要有归宿**：每路报告「跨路请求」节 + 主对话随手转给归属路（已交卷的路用 SendMessage 续派最便宜），结尾再扫一遍 DIGEST / 审查报告的「部分」条目把尾巴收掉。

## 生成 prompt 的质量标准

> **7 条 rubric 已实体化进 `~/.claude/skills/write-a-prompt/SKILL.md`「质量线（7 条，每次逐条过，别临场发挥）」节**——角色+硬规则（违反即失败）/ 焊入真实上下文（实时收，不凭记忆脑补）/ 输出契约 / 内建优先级 P0P1P2 / 可逆护栏 surgical / 参数留 `____` 填空位 / 做深不做大（专家四问：内行多做的一步、一手材料、具体方法工具、外部裁判）；「意图四要素（目标 / 谁跑它 / 成功长啥样 / 绝不做什么）缺一先反问」也在该 skill 的 Step 1。**生成 prompt 一律照那份走，别在这里找口径。**

**Why:** 用户经常让我「生成一个 prompt」（回头贴给别的 session 跑），痛点是质量不稳、取决于我当时手上有多少他的上下文。他自己判断这是「习惯」问题不是「工具」问题——所以答案是固定标准，不是更聪明的临场发挥。

**How to apply:** 触发词没命中、skill 没 fire 的场合（用户在别的任务里顺口要一段 prompt），手动把那 7 条过一遍即可。关联 [[feedback_no_jargon_plain_product_language]] [[feedback_skill_design_pattern]]
