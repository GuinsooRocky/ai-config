# 验收命令探测 + 形态判定

## 一、探测 back-pressure 命令(按项目信号)

扫项目根 + 一级子目录,命中哪条就把对应命令列为候选。**优先选最便宜可靠的"闸"(编译/类型检查),有测试再叠加。**

| 项目信号(文件/字段) | 验收命令候选 | 备注 |
|---|---|---|
| `package.json` 有 `scripts.test` | `npm test` / `pnpm test` / `yarn test` | 看 lockfile 定包管理器 |
| `package.json` 有 `scripts.build` | `npm run build` | 构建即闸 |
| `tsconfig.json` | `npx tsc --noEmit` | 最快的类型闸 |
| `pyproject.toml`/`setup.py` + pytest | `pytest -q` | |
| 任意 `.py`(无测试框架) | `python -m py_compile <files>` | 语法闸,最低成本兜底 |
| `Cargo.toml` | `cargo build` →(有测试)`cargo test` | 类型系统强,build 即强闸 |
| `Package.swift` | `swift build` | |
| `go.mod` | `go build ./...` →(有测试)`go test ./...` | |
| `Makefile` 有 `test`/`check` target | `make test` / `make check` | |
| 都没命中 | **直接问用户**:"哪条命令一跑就能判断这件做完了?" | 不许瞎编 |

补充规则:
- **结构不变量**也是 back-pressure(不只跑命令):像 dk 那样"每个渠道都得走 core 契约""必需 endpoint 在不在"——这类用脚本断言。样板见 `~/Desktop/my-code/dk/ralph/smoke_test.py`。
- 一个 loop 可以有**多条**验收(编译 + 测试 + 结构断言),`check.sh` 里全绿才算过。
- 探到候选后**务必列给用户确认**(用户已选"自动探测+确认"模式),别默默用。

## 二、有些验收命令验不了的(诚实标注)

编译/类型只证明"编得过",证明不了运行时行为(UI 起得来、定时器真在跑)。这类:
- 把它从 loop 自动验收里**挪出来**,列成"跑完你手验"清单;
- 或加更强的可自动判信号(mock + 断言被调用 ≥N 次),但要先搭测试,多一步——让用户选。

## 三、形态判定

### 第 0 道:该不该做自主 loop(先判这个)
若命中任一,**不要做自主 loop**,降级成"一次性 pipeline + 人扳机":
- 真正涨分/改进的那一步是**人的判断**(品味、设计、策略),且用户想自己留着;
- 一件"做完没"**只能靠跑完整个循环才知道**(改了才知有没有用),没有独立的逐件验收;
- 典型:对着一套 eval 分数调一个生成器/prompt(evaluator-optimizer,optimizer 是人)。

**产出**(而非 while loop):把"验证半"(清空→重生/重跑→评分→diff 上一轮)包成**一条 pipeline 命令**,如 `bash loop/run-round.sh`。人改一次 → 跑一次 → 看对比表 → 再改。
**雷**:NEVER 让 agent 自动做那个判断步骤去刷分——它会过拟合 scorer(对着固定测试集刷分),不是真变好;真要全自动得先有 holdout 集防作弊,另起谨慎实验。

### 否则:两种自主形态
| 信号 | 形态 | 引擎 | 退出 |
|---|---|---|---|
| "把 X/Y/Z 做完""实现这批需求""跑完这些 todo" | **backlog** | 啃 `fix_plan.md` 任务 | 清单清空 / 卡住 / max-iterations |
| "守住""盯着""别让 X 变红/退化""持续验证" | **guardian** | 文件变就跑 check | 你 Ctrl-C(常驻) |

判不准 → 问用户一句:"改进的那步是你自己判断(→pipeline),还是机器能逐件验着做完(→backlog),还是守着别坏(→guardian)?"

形态可叠:一边 guardian 守,一边 backlog 推,互不冲突。
