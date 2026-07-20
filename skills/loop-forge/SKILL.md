---
name: loop-forge
description: 给一个项目和一组目标,生成并(交互确认后)执行一个 Ralph 风格自主 agent loop。自动探测验收命令(back-pressure)、按目标判形态(backlog 做完一批 / guardian 守不变量)、脚手架 `loop/` 任务文档+检查+决策箱+人工验证清单+执行器脚本,展示后问"跑吗"才起 `bash loop/loop.sh`。触发词:做个loop、生成loop、给这个项目上loop、loop起来、把这批需求自动跑完、loop-forge。Use when 用户想搭一个不打扰自己、把目标做完或守住某状态的自主回环。不用于:已成形 loop 的单纯执行(直接跑它的 loop.sh)、纯一次性任务、模糊到无法机械验收的目标。
---

# loop-forge

把"给项目手搓一套 Ralph loop 骨架"自动化:生成任务文档 + 机械验收 + 决策箱 + **自带的执行器脚本**。

核心信条:**loop = 目标文档 + 每条目标的机械验收(back-pressure)。没有验收的循环只会更快产 slop。**

执行器是本 skill **自己生成**的 `loop/loop.sh` / `loop/guard.sh`(纯 shell while,零插件依赖)。不预设任何第三方 loop 插件存在。

## 何时使用

触发场景:用户有**一组目标**(或一个要守住的状态)、**不想被反复打扰**、想让系统自己推进时。

- 触发词:`做个loop`、`生成loop`、`给这个项目上loop`、`loop起来`、`把这批需求自动跑完`、`守住别让X变红`、`loop-forge`。
- 负面边界(NEVER 在这些场景用):
  - 已成形 loop 只想执行 → 直接跑它的 `loop/loop.sh`,不必本 skill。
  - 纯一次性任务(改一个 bug、答一个问题)→ 直接做。
  - 目标模糊到无法机械验收("做得高级点")→ 先和用户翻成可判定验收点,翻不出就不上 loop。

## 工作流

### 0. 前置闸(不过就停,必须先满足)
- [ ] 是 git 仓 + **工作区干净**(`git status --porcelain` 为空)。脏 → 让用户先 commit/stash,**拒绝**继续(否则 loop 首轮会裹走未提交改动)。
- [ ] 目标**必须**可机械验证。模糊 → 先翻成可判定验收点(如"4 态有独立配色 + 空态有引导文案")。
- [ ] 是**绿地/可验证**的活。NEVER 往庞大已有库招呼自主 loop(Huntley 铁律)。

### 1. 探测验收命令(back-pressure)→ 用户确认
按 [references/detection.md](references/detection.md) 扫项目,列候选验收命令(`pytest`/`swift build`/`npm test`/`make`…),**必须**给用户确认或改,不要默默用。

**"这项目没测试"不等于没闸**——编译闸 / 产物存在性 / 必需接口存在性 / 结构不变量 / 冒烟脚本,任一能机械判 0/1 的都算(见 detection.md §一 bis)。真探不到 → 直接问"哪条命令一跑就算这件做完了"。

### 2. 判形态 —— 先判**该不该**做自主 loop(关键闸)
**必须先过这道判断**:若「改进/涨分的那一步是人的判断」,或「一件做完没,只能靠跑完整个循环才知道」→ **不要做自主 loop**(这是 evaluator-optimizer / 人在环里型,如对着 eval 分数调一个生码工具)。
- 改判为:把**验证半**(跑测/评分/diff)包成**一次性 pipeline 命令**,扳机留给人——人改一次、按一下看对比,再改。
- NEVER 让 agent 自动做那个判断步骤:它会刷分 / 过拟合 scorer,不是真变好。

否则,在两种自主形态里选:
- "把 X/Y/Z 做完、实现这批需求" → **backlog 型**
- "守住/盯着 X 别变红/别退化" → **guardian 型**

自动判 + 告诉用户结论,允许改。详见 [references/detection.md](references/detection.md)。

### 3. 脚手架(写进项目 `loop/` 目录,先读不盲覆盖)

**backlog 型骨架 = 6 份产物,一个都不能少:**

| 产物 | 干什么 |
|---|---|
| `loop/fix_plan.md` | 目标清单,每条带出处 + 验收断言 |
| `loop/check.sh` | back-pressure,跑验收,全绿退 0 |
| `loop/PROMPT.md` | 每轮喂给 claude 的指令(含 A/B 拍板分诊、人工验证降级、收尾审查、completion-promise) |
| `loop/decisions.md` | 决策箱三节:待拍 / 已拍 / 子 agent 代拍记录 |
| `loop/manual-verify.md` | 人工/真机/部署才能验的,攒在这,loop 不因它停 |
| `loop/loop.sh` | **执行器**:脏树闸 + 专用分支 + 喂 PROMPT + 判收工 + MAX 熔断 |

**guardian 型骨架 = 2 份:** `loop/check.sh` + `loop/guard.sh`(文件变就跑 check,绿心跳/红报警;不写 fix_plan、不 commit、不调 claude)。

模板见 [references/templates.md](references/templates.md),按探测结果填充占位符(分支名 / PROMPT 路径 / fix_plan 路径 / MAX 轮数都参数化)。

### 4. 展示 + 交互问"跑吗?"
展示生成物路径 + 将要跑的命令,**然后问用户跑不跑**。点头:
- backlog → `bash loop/loop.sh <N>`
- guardian → `bash loop/guard.sh`

摇头 → 留着不跑,告诉用户以后怎么自己跑。

## PROMPT 必须内建的四个机制(实战磨出来的,别省)

生成 `loop/PROMPT.md` 时**必须**把这四条写进去,否则 loop 会在半路停死或假装完成:

1. **拍板点 A/B 分诊,绝不空等**
   - A 类(可逆技术判断:顺序、拓扑、命名、要不要回填存量)→ 起**子 agent 当裁决官**(`model: opus`),要它出「裁决 + 依据 + 一行反悔法」,记进 `decisions.md`「子 agent 代拍记录」区,继续干。
   - B 类(花钱 / 签字 / 法务 / 不可逆的公开曝光 / 产品红线)→ **park 到 `decisions.md`「待拍」区 + 用占位值继续做能做的部分**。裁决官拿到 B 类必须回 `OWNER_RESERVED` 不给结论。
   - **判不准算 B**。两类都不许停在原地空等。
2. **人工验证降级** — 需要浏览器 / 真机 / 真实凭证 / 部署才能验的步骤:**机械闸绿就算本轮达标**,把 live 验证登记进 `manual-verify.md`,**不因"没真验过"停下或标卡住**。只有机械闸过不了才算卡。
3. **收尾独立审查** — 待办清空后**不许直接宣布完成**:先对整批 diff 起一个**没有执行者上下文**的子 agent 做 code review;它确认为真的 P0 **回填 fix_plan** 继续修,**零 P0 才 ALL_DONE**。
4. **决策箱** — `decisions.md` 三节(待拍 / 已拍 / 子 agent 代拍记录),每条格式统一:问题 / 选项 / 裁决 / 依据 / **一行反悔法**。反悔法是这箱子的命根子——没有它,代拍就是不可逆的。

## 输出格式(硬约束)

- **必须**先展示生成的 `loop/` 文件清单 + 路径,再展示那条要跑的命令,**最后**才问"跑吗"。
- backlog 的 `fix_plan.md` 每条待办**必须**带一条可机械判定的验收(命令或断言),没有验收的目标不许写进清单。
- `loop.sh` **必须**带 MAX 轮数熔断,不要省。
- 没拿到用户"跑"的确认前,**不要**擅自启动任何 loop。

## 示例输出

```
已生成 loop/(backlog 型):
  loop/fix_plan.md      3 条待办,每条验收 = swift build
  loop/check.sh         跑 swift build
  loop/PROMPT.md        含 A/B 拍板分诊 + 人工验证降级 + 收尾审查 + <promise>ALL_DONE</promise>
  loop/decisions.md     决策箱(待拍 / 已拍 / 子 agent 代拍记录)
  loop/manual-verify.md 人工验证清单(空)
  loop/loop.sh          执行器(分支 loop/auto,MAX 9,日志落 loop/logs/)

将要跑的命令:
  bash loop/loop.sh 9

跑吗?(点头我发起;摇头你以后自己粘上面这条)
```

## 安全铁律(实战提炼,违反会出事)
- 脏工作区**必须**拒跑(loop.sh 安全闸 0)。
- 只在专用 loop 分支 commit;**绝不** `git add -A`/`git add .`,只 `git add <本轮碰的文件>`。
- **不要**碰 `.env`/真实凭证;联网验收打 mock/测试端点。
- 需要真实凭证或会改动线上状态的命令(部署、迁移、发布)**一律不跑**——登记 `manual-verify.md` 给人。
- **不确定就停**:写进 fix_plan 记一行 `⚠ 卡住:原因`,NEVER 瞎猜往下推。
- backlog **必须**设 MAX 熔断,防失控空转。
- 日志落 `loop/logs/`,生成后确认已被 `.gitignore` 忽略(没忽略就在 `loop/logs/.gitignore` 放一行 `*`)。

## 交付后
- 提醒用户:新建/改动 skill 后**必须重启 session** 才装载。
- 自审:跑 `meta-check-skill loop-forge`(≥85 才算交付)。

> 装了第三方 loop 插件(如某些社区的 `/ralph-loop`)也可以拿它当执行器喂同一份 PROMPT,**但不是必须**,也不是默认路径——本 skill 生成的 `loop.sh` 已自带脏树闸、分支闸、双收工判据和熔断。
