# 脚手架模板 + 形态详解

所有产物写进目标项目的 `loop/` 目录。按探测结果(验收命令、目标清单)填充占位符 `<...>`。

## backlog 型(把一批目标做完)

### `loop/fix_plan.md`
```md
# fix_plan — <项目名> loop 任务清单
> loop 每轮挑「待办」最上面一个 [ ],只做这一件,跑 loop/check.sh,绿了打勾 [x] 退出。
> [ ] 待办 · [x] 完成 · [skip] 暂缓不计入循环。

## 待办
- [ ] <目标1>。验收:<验收命令/断言>。
- [ ] <目标2>。验收:<验收命令>。

## 提交边界
只在 loop/auto 分支 commit;只 add 本轮文件,绝不 git add -A。
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

### `loop/PROMPT.md`(喂给 /ralph-loop)
```md
读 loop/fix_plan.md。从「待办」从上到下一件件做,一次只做一件:
1. 只实现这一件,不顺手改别的。
2. 跑 bash loop/check.sh:绿 → 在 fix_plan 打勾 [x],只 git add 本轮文件提交(loop/auto 分支);红 → 修到绿,修不动就 git checkout 回滚、在该任务记「⚠ 卡住:原因」并停。
3. 待办全打勾 → 输出 <promise>ALL_DONE</promise>。
不碰 main、不动 .env 真实凭证、不确定就停。
```

### 执行(第 4 步用户点头后)
```
/ralph-loop "$(cat loop/PROMPT.md)" --completion-promise "ALL_DONE" --max-iterations <N>
```
`<N>` 取 任务数 × 3 左右(留出修红的轮次),保底熔断。

## guardian 型(守住不变量别变红)

### `loop/guard.sh`(现跑,不提交、不调 claude)
```bash
#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
INTERVAL="${1:-3}"
echo "🛡 守卫启动(间隔 ${INTERVAL}s,Ctrl-C 停)"
last=""
while :; do
  sig=$(find . -name '*.<ext>' -not -path '*/.venv/*' -not -path '*/.git/*' \
        -exec stat -f '%m %z %N' {} \; 2>/dev/null | sort | md5)
  if [ "$sig" != "$last" ]; then
    bash loop/check.sh || printf '\a👆 红了,按上面修\n'
    last="$sig"
  fi
  sleep "$INTERVAL"
done
```
guardian 不写 fix_plan、不 commit、不调 claude——它只观察 + 跑 check + 报警。引擎是 check,不是任务清单。

## 两种形态对照

| | backlog | guardian |
|---|---|---|
| 目的 | 把待办干到清空 | 守某不变量别变红 |
| 引擎 | fix_plan 任务 | check.sh |
| 执行 | 官方 /ralph-loop | bash loop/guard.sh(现跑) |
| 退出 | 清单空/卡住/max-iter | 你 Ctrl-C |
| 碰 git | 只 loop/auto 分支 | 不碰 |

## 安全铁律(两种都适用)
1. 脏工作区拒跑(SKILL.md 第 0 步)。
2. 只在 `loop/auto` 分支 commit;**绝不 `git add -A`**,只 add 本轮文件。
3. 不碰真实凭证;联网验收打 mock/测试端点。
4. 不确定就停,记 `⚠ 卡住` 喊人,别瞎猜。
5. backlog 必设 `--max-iterations` 熔断。

## 实战样板(照抄改)
`~/Desktop/my-code/dk/ralph/` —— 一套真实的 backlog(loop.sh/PROMPT.md/fix_plan.md/smoke_test.py)+ guardian(guard.sh)。smoke_test.py 演示了"结构不变量"式 back-pressure(渠道契约/endpoint 断言),不止跑命令。
