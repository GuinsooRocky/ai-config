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
- 一个 loop 可以有**多条**验收(编译 + 测试 + 结构断言),`check.sh` 里全绿才算过。
- 探到候选后**务必列给用户确认**(用户已选"自动探测+确认"模式),别默默用。

## 一 bis、没有测试的项目照样能有硬闸

**back-pressure ≠ 只能跑测试。** "这项目没测试"不是不上 loop 的理由——退化到下面任一种,只要**能机械判定 0/1**,就是合法的闸。按成本从低到高:

| 闸的种类 | 怎么做 | 例子 |
|---|---|---|
| **编译闸 / 类型闸** | 编译器或类型检查器退 0 | `tsc --noEmit`、`cargo build`、`go build ./...`、`python -m py_compile` |
| **产物存在性** | 断言构建/生成的东西真出来了 | build 后 `[ -f dist/app.js ]`、生成器跑完 `[ -s out/schema.json ]` |
| **必需接口存在性** | 断言约定的函数/路由/导出/命令没漏 | grep/AST 断言每个渠道都注册了 handler、每个必需 endpoint 都在路由表里 |
| **结构不变量** | 断言"每个 X 都必须满足 Y"的横向契约 | 每个模块都走同一个 core 契约、每个页面都有对应 i18n key、配置项都有默认值 |
| **一致性闸** | 两处该同步的东西必须对得上 | schema 与类型定义一致、清单文件与磁盘文件一一对应 |
| **冒烟脚本** | 一个 `smoke.sh`/`smoke.py`,跑一遍最小主链路,断言不抛 | 起服务 → 打一个 mock 请求 → 断言返回结构 |

写法:任一种都塞进 `loop/check.sh`,任一红就 `exit 1`。**结构不变量类的闸往往比测试更值**——它挡的是"某个渠道漏改了"这种 loop 最容易犯的错。

真没有任何可机械判定的闸(改进那步全靠人眼看)→ 别上自主 loop,见下面第三节第 0 道。

## 二、有些验收命令验不了的(诚实标注)

编译/类型只证明"编得过",证明不了运行时行为(UI 起得来、定时器真在跑)。这类:
- 把它从 loop 自动验收里**挪出来**,登记进 `loop/manual-verify.md`(人事后手验)。
  **关键**:loop 不因"这条没真验过"就停下或标卡住——机械闸绿即本轮达标,live 验证攒着给人。
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
