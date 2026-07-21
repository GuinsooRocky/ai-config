# 脚手架模板 + 形态详解

所有产物写进目标项目的 `loop/` 目录。按探测结果(验收命令、目标清单)填充占位符 `<...>`。

**执行器由本 skill 自己生成**(`loop/loop.sh` / `loop/guard.sh`,纯 shell、零插件依赖)。不依赖任何外部 loop 插件。

## backlog 型(把一批目标做完)

产物:`fix_plan.md` + `check.sh` + `PROMPT.md` + `decisions.md` + `manual-verify.md` + `loop.sh`

### `loop/fix_plan.md`
```md
# fix_plan — <项目名> loop 任务清单
> loop 每轮挑「待办」最上面一个 [ ],只做这一件,跑 loop/check.sh,绿了删掉该条并 commit。
> [ ] 待办 · [skip] 暂缓不计入循环 · [⚠] 卡住(附原因,留给人)。

## 待办
- [ ] <目标1>(出处:<需求文档> §<章节>)。验收:<验收命令/断言>。
- [ ] <目标2>(出处:<需求文档> §<章节>)。验收:<验收命令>。

## 提交边界
只在 <loop 分支> commit;只 add 本轮碰的文件,绝不 git add -A。
```

### `loop/check.sh`(back-pressure,全绿退 0)
```bash
#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
fail=0
# 按探测填:逐条验收,任一红就 fail=1
<验收命令1> || fail=1
<验收命令2> || fail=1
[ "$fail" = 0 ] && echo "✅ 全绿" || echo "❌ 有红"
exit $fail
```

### `loop/decisions.md`(决策箱 —— 让 loop 撞到拍板点也不停)
```md
# decisions — 拍板箱
> 三节:待拍(等人) / 已拍(人拍过的) / 子 agent 代拍记录(A 类可逆技术判断)。
> 每条统一格式:问题 / 选项 / 裁决 / 依据 / 反悔法(一行)。

## 待拍(B 类:只有人能拍,loop 一律 park 在这)
### <问题标题>(<日期>,出处:<出处>)
- 问题:<一句话>
- 选项:<A> / <B>
- 占位值:<loop 先用哪个继续做>(拍板后一行改回)
- 反悔法:<改哪一个常量/开关>

## 已拍
### <问题标题>(<日期>,人拍)
- 裁决:<结论>
- 依据:<为什么>
- 反悔法:<一行>

## 子 agent 代拍记录(A 类:可逆技术判断,人事后扫这区,不同意一行改回)
### <问题标题>(<日期>,裁决官代拍)
- 问题:<一句话>
- 选项:<A> / <B>
- 裁决:<选了哪个>
- 依据:<推理/证据>
- 反悔法:<一行怎么改回来>
```

### `loop/manual-verify.md`(人工验证清单 —— 让 loop 不因"没真验过"停下)
```md
# manual-verify — 跑完你手验清单
> loop 自己跑不了的验证(浏览器实测 / 真机 / 真实凭证 / 部署 / 真实数据)登记在此。
> loop 只要机械闸(check.sh)绿就算本轮达标,继续往下做,不因这些停。

## 待验
### <任务名>(<日期>)
- 怎么验:<步骤>
- 已过的机械闸:<check.sh 里跑绿了什么>
- 风险:<如果人工验证挂了会怎样>
```

### `loop/PROMPT.md`(喂给 loop.sh,每轮全新 context)
```md
读 loop/fix_plan.md。从「待办」从上到下挑第一个 [ ] 任务,一次只做这一件:

1. 先读该任务出处的原文(fix_plan 每条都标了出处),对齐意图再动手;遵守项目 CLAUDE.md 的约定。
2. 只实现这一件,不顺手改别的。修 bug 只修报告点名的那条路径,不推广到别的场景。

3. **碰到拍板点,先 A/B 分诊,两类都绝不停在原地空等:**
   - **A 类·可逆技术判断**(有可推理的最优解、错了一行能回滚、不涉钱/不涉签字/不涉产品红线):
     例=执行顺序、并发拓扑、存量数据回不回填、命名与结构取舍。
     → **起一个子 agent 当裁决官**(`Agent` 工具,`model: opus`),喂它:问题 + 各选项 + 本项目约束(红线 / 既有 decisions)。
     要它产出 **裁决 + 依据 + 一行反悔法**。结果记进 `loop/decisions.md`「子 agent 代拍记录」区,然后按裁决继续干。
   - **B 类·人保留域**(花钱 / 签字 / 法务 / 不可逆的公开曝光 / 产品定位与红线取舍):
     **裁决官也不许碰**。追加到 `loop/decisions.md`「待拍」区 + **用占位值继续做能做的部分**。
     裁决官若拿到 B 类问题,必须回 `OWNER_RESERVED` 不给结论,loop 收到就 park。
   - **判不准 A 还是 B → 当 B 处理**(park,不代拍)。这条让 loop 在可逆包络内真自主,但不越人的保留域。

4. **人工/实时验证降级**:任务验收里凡是需要「浏览器实测 / 真机 / 真实凭证 / 部署 / 真实数据」这类你跑不了的步骤
   —— **把代码 + 机械可判的闸(check.sh / mock / 注入式 smoke)做到绿就算本轮达标**,
   把那条 live 验证追加到 `loop/manual-verify.md`(人会在别的 session 做),
   **不要因为「没真验过」就停下或标卡住**。只有机械闸都过不了才算卡。

5. 跑 `bash loop/check.sh` + 该任务自带的验收断言:
   - 全绿 → 从 fix_plan 删掉该条、只 `git add` 本轮碰的文件、在 <loop 分支> commit。
   - 有红 → 修到绿;修不动就 `git checkout -- .` 回滚、在该任务行下记「⚠ 卡住:原因」并结束本轮。

6. 待办清空(只剩 [skip]/[⚠])→ **进入收尾审查,别直接 ALL_DONE**:
   a. **独立 code review**:对本分支自上次人工验收点以来的**整批 diff**,起一个**没有执行者上下文**的子 agent 做审查
      (它只读 diff + 需求出处,不知道你干活时怎么想的)。
   b. 它确认为真的 **P0 回填 fix_plan「待办」**当新 `[ ]`(附出处 + 断言),结束本轮让 loop 继续修,直到某轮**零 P0**。
   c. 零 P0 → 才输出 <promise>ALL_DONE</promise>,结束语点明「loop/manual-verify.md 里的人工验证还没做,没过别合主干」。

铁律:不碰主干分支 / 不 push / 绝不 git add -A / 不动 .env 与真实凭证 /
不跑需要真实凭证或会改动线上状态的命令(属人工,登记 loop/manual-verify.md)/
不确定就停下记「⚠ 卡住」,别瞎猜往下推。
```

### `loop/loop.sh`(执行器 —— 本 skill 生成,纯 shell 无插件)
```bash
#!/usr/bin/env bash
# <项目名> loop —— 在专用分支上反复唤起 claude,直到 fix_plan 清空。
# 用法:  bash loop/loop.sh [MAX轮数]      (Ctrl-C 随时停)
# 机理:  每轮 = 全新 context 喂同一个 PROMPT.md;状态全在磁盘(fix_plan + git),不靠上下文记忆。
# ⚠ 会消耗 Claude 额度并自动 commit(仅专用分支)。先在干净工作区跑。
set -u
cd "$(dirname "$0")/.." || exit 1

BR=${BR:-<loop 分支,如 loop/auto>}
PROMPT=${PROMPT:-loop/PROMPT.md}
PLAN=${PLAN:-loop/fix_plan.md}
MAX=${1:-<N>}                       # 轮数上限,防失控
LOGDIR=loop/logs
mkdir -p "$LOGDIR"

# 安全闸 0:工作区必须干净,否则首轮 git add 会裹走未提交的手改
if [ -n "$(git status --porcelain)" ]; then
  echo "⛔ 工作区不干净。先 commit 或 stash 再跑。"
  git status --short
  exit 1
fi

# 安全闸 1:只在专用分支跑,绝不碰主干
git rev-parse --verify "$BR" >/dev/null 2>&1 || git branch "$BR"
git switch "$BR" || { echo "切不到分支 $BR,停"; exit 1; }

ITER=0
while [ "$ITER" -lt "$MAX" ]; do
  ITER=$((ITER+1))
  LOG="$LOGDIR/$(date '+%Y%m%d-%H%M%S')-iter$ITER.log"
  echo "===== loop iteration $ITER / $MAX ($(date '+%H:%M:%S')) → $LOG ====="

  cat "$PROMPT" | claude -p --dangerously-skip-permissions 2>&1 | tee "$LOG"

  # 收工判据 1:agent 宣告 completion-promise
  if grep -q 'ALL_DONE' "$LOG"; then
    echo "✅ agent 输出 ALL_DONE,收工(共 $ITER 轮)"
    exit 0
  fi
  # 收工判据 2:fix_plan 无 [ ] 待办([skip]/[⚠] 不算)
  if ! grep -q '^- \[ \]' "$PLAN"; then
    echo "✅ fix_plan 无待办,收工(共 $ITER 轮)"
    grep -q '^- \[⚠\]' "$PLAN" && echo "⚠ 有被标卡住的任务,搜 '⚠ 卡住' 看原因。"
    echo "ℹ 记得看 loop/manual-verify.md(人工验证)和 loop/decisions.md「待拍」。"
    exit 0
  fi
  sleep 2
done
echo "⏹ 到轮数上限 $MAX,停(防失控)。还有待办就再跑一次。"
```

### 执行(第 4 步用户点头后)
```
bash loop/loop.sh <N>
```
`<N>` 取 任务数 × 3 左右(留出修红 + 收尾审查回填的轮次),保底熔断。日志逐轮落 `loop/logs/`
(生成后确认项目 `.gitignore` 已忽略日志;没忽略就在 `loop/logs/.gitignore` 放一行 `*`)。

> 装了第三方 loop 插件(如 `/ralph-loop`)也可以拿它当执行器喂同一份 PROMPT,但**不是必须**——
> 本 skill 生成的 `loop.sh` 已经自带脏树闸、分支闸、双收工判据和轮数熔断。

## guardian 型(守住不变量别变红)

产物:`check.sh` + `guard.sh`(不写 fix_plan、不 commit、不调 claude)

### `loop/guard.sh`
```bash
#!/usr/bin/env bash
# 守卫:源文件一变就重跑 check。绿=安静心跳,红=响铃报警。不提交、不调 claude、不烧额度。
# 用法:  bash loop/guard.sh [轮询间隔秒]      (Ctrl-C 停)
set -u
cd "$(dirname "$0")/.." || exit 1

INTERVAL="${1:-3}"
echo "🛡 守卫启动(间隔 ${INTERVAL}s,Ctrl-C 停)"

# 源文件指纹(排除依赖目录 / .git / loop 自身),变了才重跑
fingerprint() {
  find . -name '*.<源文件后缀>' \
    -not -path '*/<依赖目录>/*' -not -path '*/.git/*' -not -path './loop/*' \
    -exec stat -f '%m %z %N' {} \; 2>/dev/null | sort | md5
}

last=""; first=1
while :; do
  sig="$(fingerprint)"
  if [ "$sig" != "$last" ]; then
    [ "$first" = 1 ] || echo "── $(date '+%H:%M:%S') 检测到改动,重跑 ──"
    first=0
    bash loop/check.sh || { printf '\a'; echo "👆 红了,按上面提示修;修好这里自动转绿。"; }
    last="$sig"
  fi
  sleep "$INTERVAL"
done
```
guardian 的引擎是 check,不是任务清单——它只观察 + 跑 check + 报警。

## 两种形态对照

| | backlog | guardian |
|---|---|---|
| 目的 | 把待办干到清空 | 守某不变量别变红 |
| 引擎 | fix_plan 任务 | check.sh |
| 执行 | `bash loop/loop.sh <N>` | `bash loop/guard.sh` |
| 退出 | 清单空 / ALL_DONE / max 熔断 | 你 Ctrl-C |
| 碰 git | 只在专用分支 commit | 不碰 |
| 决策箱 | decisions.md + manual-verify.md | 不需要 |

## 安全铁律(两种都适用)
1. 脏工作区拒跑(loop.sh 安全闸 0)。
2. 只在专用 loop 分支 commit;**绝不 `git add -A`**,只 add 本轮文件。
3. 不碰真实凭证;联网验收打 mock/测试端点。
4. 撞拍板点不空等:A 类代拍记 decisions,B 类 park + 占位值继续。
5. 人工才能验的不算卡:机械闸绿即达标,live 验证登记 manual-verify。
6. 待办清空 ≠ 完成:先过独立 code review,零 P0 才 ALL_DONE。
7. backlog 必设 MAX 熔断,防失控空转。
