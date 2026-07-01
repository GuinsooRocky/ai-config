---
name: onlychat-i18n
description: OnlyChat 项目专用 i18n 落地流水线——把"你自己写的、还硬编码英文的代码"一条龙接进 next-intl：扫硬编码 → 生成/复用 key → 接 t() → 出 HTML 清单 + 飞书可粘剪贴板 →（你粘飞书）→ 跑 pnpm i18n → 覆盖验证。只落英文，翻译归飞书。触发词："跑 onlychat i18n"、"这块/这个组件接 i18n"、"把硬编码接 t()"、"i18n 落地"、"生成 worldcard/xxx 的 i18n key"、给一个需求范围/文件集说"接 i18n"。仅处理你（zhanghao）写的代码，别人代码不碰。不用于：翻译录入（飞书的事）、非 onlychat 项目。
---

# OnlyChat i18n 落地

## 这个 skill 干什么

把 OnlyChat 里**你自己写的、文案还硬编码成英文**的代码，一条龙接进 next-intl 的 `t()`，并产出可直接粘进飞书多语言表的清单。**只负责英文落地 + 接线**；14 国翻译由飞书翻译流程做，本 skill 不碰。

**前提假设（不是本 skill 的动作）**：目标代码里文案已经写死成英文（开发时的习惯）。本 skill 从「扫这些硬编码」开始。

## 心智锚（最重要，先读）

**i18n 是扁平的字符串去重，不是逻辑/架构问题。** 一个 key 就是 `英文值 → 15 语言`。

- **同值 + 已全 15 语言翻译的现成 key → 机械复用，不准犹豫。** "Rating" 已有全翻译键就直接用它，结束。
- **做 i18n 时关掉"耦合洁癖"——key 不是模块。** 两处显示同一个词不是"耦合"，是正常且应该。`createoc_rating`、`bonus_btn_submitted` 带功能前缀也照样复用——"怕别的功能改文案"是个芝麻风险（极少发生、真发生也就一行 cosmetic fix），不准用它当借口去建重复键。
- **建了重复键 = 和"该复用没复用"同级的低级错**：重复键在飞书是两行各填各的 = 没翻译/会漂移/膨胀。代价远大于那个想象中的耦合。
- **唯一可以"同值不复用"的理由**：该值在某语言必须翻成不同的词（语法性别/格、chip 太窄要短译）。没有这个理由就必须复用。

这条锚贯穿下面的「复用规则」「四道闸」「决策点」。违反它就是这个 skill 存在的意义被打掉。

## 何时触发

- 用户给一个需求范围 / 一组文件 / 一个功能区，说"接 i18n / 把硬编码接 t() / i18n 落地"
- 用户说"跑 onlychat i18n"、"生成 xxx 的 i18n key"
- 用户飞书录完后说"跑 i18n"→ 进入 step 9（验证）

不触发：翻译录入、非 onlychat 项目、纯查某个 key 是否存在（直接 grep 即可）。

## 输入（开工前确认）

1. **范围 → 文件集**：需求范围落成一组路径/glob（如 `src/components/WorldCard/**`）。模糊就先问清或让用户给文件。
2. **key 前缀**：本批 key 的命名前缀（如 `worldcard_`）。
3. **（可选）PRD / Figma**：对照文案是否齐、措辞是否定稿。
4. **环境**：飞书 test 表 `zeHW5Z`（默认）/ 线上 `25kNVe`。

## 产出

- **代码**：硬编码 → `t()`，en.json 落英文
- **`~/Desktop/<feature>-i18n.html`**：① 本次新建（进飞书）② 本次复用（不进飞书），位置去重
- **剪贴板 → HTML `<table>`（key｜EN）**：飞书 Sheets 对纯文本 TSV **不拆格**（整块塞进一个单元格），只认富文本表格；故 `gitdiff`/`tsv` 默认用 osascript 把 HTML 表格写进 `«class HTML»` flavor，飞书/Google/Excel 单击选中格子 Cmd+V 即拆成网格。osascript 失败才回退纯 TSV。`--out` 仍落 TSV 文件。
- **验证报告**（跑完 pnpm i18n 后）：新建 N/N 存活 + 复用全在 + 翻译缺口 + git diff 概览

## 执行步骤 + 暂停点（一个 skill 内按序跑）

关键：**先出计划、审过、才动代码**。HTML 在接 `t()` 之前出（纸面审命名/复用，比接完 119 行再返工便宜）。

1. **接收范围** — 落成文件集 + 确认 key 前缀（模糊必须先问清）；**先拍 en.json 全量基线**（`baseline`，跑 i18n 前/接代码前），收尾差集靠它
2. **只取你的代码** — 逐行 `git blame`，只处理 zhanghao 写的；别人代码列出来、跳过（必须，别人 key 不进你的飞书清单）
3. **扫硬编码 → 决定 key** — 生成即查复用（见「复用规则」），不要事后再来一遍；把决策点（改文案/边界复用/疑似过度 i18n）一并标出
4. **落 plan HTML** — `key｜English｜新建or复用｜位置`，**此时代码还没改**，一次成型
   - ⏸ **暂停 1（必停，禁止跳过）** — 把 plan HTML 交用户审：命名/复用/新建对不对、决策点拍板。**确认后才动代码**
5. **接 `t()` + en.json 落英文** — 严格按确认的 plan 来（见「接线规则」）
6. **四道闸（全过才出飞书清单）** — ① grep 残留硬编码防漏字段 ② **`reuse-audit` 跨前缀复用必零残留**：值撞现成全语言键的一律复用（前缀/功能归属不是理由，见心智锚），命中即 repoint+删新建 key；跨作者别人 key 带 `--exclude` 过滤 ③ **`dups` 扫同前缀同值 key**：同 en 值=按概念重复，逐组合并（留通用名 → repoint → 删冗余）④ `tsc --noEmit` 必须 0 错
7. **出剪贴板** — **权威源（默认强制）：`gitdiff`（git diff en.json 的 +行）或 `tsv --baseline`（基线差集）**。**禁止前缀扫描**当清单源（漏 nav_/labelKey/map/动态拼接的间接 key，会被 pnpm i18n 冲掉）
   - ⏸ **暂停 2（必停，禁止跳过）** — 用户去飞书粘贴；**等用户回来说"粘好了"才继续**
8. **【用户说"跑"】`pnpm i18n` → 覆盖验证**（见「输出格式」）
9. **【用户】最终确认**

两个 ⏸ 是**硬暂停**，不准自己往下冲；其余「决策点」在 step 3 内随时小停。详细规则见 `references/conventions.md`；脚本见 `scripts/i18n_tool.py`（确定性执行，禁止临场手推逻辑）。

## 接线规则（硬规则，details 见 references）

- `${var}` JS 模板 → next-intl `{var}`，调 `t('k', { var })`
- **文内高亮**（一段文字中间夹彩色 span）→ **单 key + `t.rich`**，值用 `<tag>...</tag>`，调 `t.rich('k', { tag: (c) => <span className="...">{c}</span> })`。参考项目 `createoc_uploadhint3`。**禁止**拆成 prefix/suffix 多 key（其它语言语序会坏）
- **模块级常量数组**（不能用 hook）→ 存 `labelKey`，渲染处 `t(labelKey)`
- **整句带变量** = 一条完整 key。**不要**拿「词 key + 变量」拼（如 `t('delete') + name`），语序在日/德文会错
- **纯符号**（`>>` `·` `/` 等）→ **不接 i18n**，保持字面字符串（过度 i18n）
- **en.json 值不带双引号 `"`**（飞书 cell 对前导/内嵌双引号敏感）。要"高亮名字"用单引号 `'{name}'`
- 组件缺 `useTranslations` 就加 `import { useTranslations } from 'next-intl'; const t = useTranslations();`

## 复用规则（在 step3 生成 key 时当场查；机械执行，别判断"该不该"）

对每条要接的英文，照「心智锚」机械走：
1. **en 值与某「全 15 语言都有值」的现成 key 字符级完全相同 → 必复用，不建新。** 前缀/功能归属（`createoc_rating`、`bonus_btn_submitted`、`oc_create_*` 等）**都不是保留理由**——key 不是模块。
2. **多个现成候选时选最裸通用的**（`male` 优于 `gender_radio_male` 优于 `octag_male`；`all`/`cancel`/`save`/`private`…）。
3. **pattern 复用**：`{a}/{b} Chars` → `num_chars`；纯 "Chars" → `chars`；分类名 → `world_section_<type>`。
4. **唯一保留两个的理由**：该值在某语言必须翻成不同的词（语法性别/格、chip 太窄要短译）。没有这理由就必须复用。
5. **无任何现成全语言键** → 新建唯一 key（不撞 en.json 已有）。

> 这一步不靠眼力——**step6 的 `reuse-audit` 会机械兜一遍**，命中即必复用。眼力漏了脚本也会拦。

## 改文案分支（单独规则）

改某处文案 ≠ 改旧 key 的值（旧 key 可能别处共用，直接改会无声改掉别处 = 耦合）。正确：
1. **新建唯一 key**（不撞已有），旧 key **不动**
2. 列进 HTML
3. 告诉用户旧 key **能不能删**：
   - 旧 key **只此一处**用 → 可删
   - 或**所有用到旧 key 的地方都改成新文案** → 可删
   - 否则（别处还用旧文案）→ **保留**，不删

## 决策点（必须停下来问用户，不自作主张）

1. **改文案 / 删字段**（如 `Delete {name}?` → `Delete`）= UX/PRD 决定 → 问
2. **疑似过度 i18n**（纯符号）→ 标出确认
3. **同值合并留谁**（`dups` 扫出的同 en 值组）→ 留哪个 key 名，列给用户拍板；跨作者别人 key 不碰
4. **`reuse-audit` 命中但你判断该值将来要分化**（语法性别/格、chip 长度）→ 说明理由保留；否则一律复用

⚠️ 「能不能复用」**不是决策点**——同值+全翻译 = 机械复用（见心智锚），别再"列给用户定要不要复用"。只有 #4 那种罕见"将来要分化"才停。

## 防空转铁律

- **「该进飞书的 key」唯一权威源 = `git diff en.json`（+/-）或 en.json 基线差集；前缀 / 字面 `t()` 扫描只是辅助参考，绝不作为飞书清单来源**。间接调的 key 字面扫描全看不见——`t(labelKey)`、`titleKey`/`descKey`、map 表 `t(MAP[x])`、动态拼 `t(\`nav_${name}\`)`——漏掉会在 `pnpm i18n` 从飞书全量覆盖时被冲掉、线上露 key。git diff / 基线差集跨前缀跨调用方式一个不漏（本次翻车就是用了前缀扫描漏 36 个间接 key）
- **能复用没复用 = 和建重复键同级的错。出飞书清单前 `reuse-audit` 必须零残留**。值撞现成全语言键的一律复用——**前缀/功能归属/"怕跨功能耦合"都不是建重复键的借口**（key 不是模块，同值就是同概念该共用，见心智锚）。`inventory` 也能看复用机会但只是"辅助参考"，正是这次翻车点：能力在、没当硬闸照做。唯一例外：值在某语言要分化（语法/长度）
- **同值 = 重复，出飞书清单前必须 `dups` 去重**。gitdiff/基线只抓"哪些是**新增**"，抓不到"两个新 key 英文一样"——同 en 值的 key 在飞书是**两行各填各的**，想保证永远一致就**必须合**（按概念建 key，不按"显示在哪个组件"建）。例外：跨作者别人的 key 不碰、英文恰好相同但预判将来要分歧（语法格/长度）才保留两个
- 复用在"生成 key"当场查，**不事后再来一遍**（否则建了又删、HTML 反复重生成）
- HTML / TSV **末尾一次性生成**，中途别反复刷
- **共享 worktree** 的 `git status` 会把**多个 session 的改动混在一起**显示。看到意料外的删除/新建/重构，**先 `git blame` 或问用户「是不是另一个 session 做的」**，别当成自己/自己 agent 干的去回滚

## 输出格式（硬约束）

- **HTML** 必须两段：① 本次新建（进飞书，统计 N 个）② 本次复用（不进飞书，全语言）。位置列同文件只标 `L行号`，跨文件才标完整路径（section 头已有文件名，禁止重复整路径）。
- **TSV** 必须 `key\tEN` 两列、无表头；含换行的值必须先标出（多行会在飞书串行）。
- **验证报告**必须含三块：新建 N/N 存活、复用全在、翻译缺口（ja/de 填了几个）+ `git diff` 概览。

## 示例输出（权威源 gitdiff + 覆盖验证）

gitdiff（step7 出剪贴板的权威源，跨前缀/间接 key 一个不漏）：
```
== git diff en.json（权威增删源）==
  + 新增进飞书: 155
  - 从飞书删（确认无他处用再删）: 0
  ✅ 155 行新增已进剪贴板（key\tEN）
```
覆盖验证（pnpm i18n 后）：
```
✅ 存活（飞书已收录）: 155/155
ja 翻译已填: 0/155（空=待翻译）
git diff: src/i18n/en.json: +207 -47 ...
```

## 本 skill 不做（用户的事）

- 粘飞书、翻译录入、最终验收
- `pnpm i18n` 默认等用户说"跑"才跑（它从飞书全量覆盖，要用户飞书录完）

## pnpm i18n 机制（验证时要懂）

`pnpm i18n` = `localization/i18n.py` 调飞书 API 把表 `zeHW5Z` 导出 → **全量重生成** `src/i18n/*.json`（15 语言）。
- 是**覆盖**：飞书有的 key 才留；手填 en.json 但飞书没有的 → **被冲掉**。所以必须**用户飞书录完再跑**
- `localization` 是 submodule，空的话先 `git submodule update --init localization`
- 跑完：en 持久；其它语言只有飞书对应列填了翻译才有值，否则空白（露空/key）

## 脚本（确定性执行，见 scripts/i18n_tool.py）

```
# step1 接代码前：拍 en.json 全量基线（收尾差集靠它）
python3 scripts/i18n_tool.py baseline --out /tmp/i18n-before.txt
# step3 决定 key 时：查复用
python3 scripts/i18n_tool.py reuse --strings-file /tmp/strings.txt        # 英文列表 → 15/15 现成可复用 key
# step4 出 plan HTML（接代码前，给暂停 1 审）
python3 scripts/i18n_tool.py plan  --plan-file /tmp/plan.tsv --out ~/Desktop/<feat>-i18n.html
#   plan.tsv 每行: status<TAB>key<TAB>English<TAB>location   （status = new 或 reuse:<现成key>）
# step6 第二道闸：跨前缀复用审计（值撞现成全语言键的=必复用，命中非零退出）；跨作者带 --exclude
python3 scripts/i18n_tool.py reuse-audit --prefix worldcard_ [--exclude /tmp/others.txt]
# step6 第三道闸：扫同前缀同值 key（同 en 值=按概念重复，逐组合并；跨作者带 --exclude 过滤）
python3 scripts/i18n_tool.py dups --prefix worldcard_ [--exclude /tmp/others.txt]
# step7 出剪贴板【权威源·默认强制·二选一】（都跨前缀/labelKey/map/动态拼接，一个不漏）：
python3 scripts/i18n_tool.py gitdiff [--exclude /tmp/others.txt]          # ★默认：git diff en.json 的 +行 → 剪贴板（en.json 未提交时用，最简）
python3 scripts/i18n_tool.py tsv --baseline /tmp/i18n-before.txt          # 或：基线差集（en.json 已部分提交时用）
# step8 覆盖验证（pnpm i18n 之后）
python3 scripts/i18n_tool.py verify --before /tmp/i18n-before.txt         # 存活 N/N + 翻译缺口 + git diff
# 【仅辅助·绝不当飞书清单源】前缀扫描会漏间接 key（labelKey/map/动态）：
python3 scripts/i18n_tool.py inventory --prefix worldcard_               # 只看复用机会/缺 en，参考用
```
默认在 onlychat worktree（cwd）跑，读 `src/i18n/*.json`。`--exclude` 传别人 key 清单（每行一个）。
**飞书增删清单只认 `gitdiff` / `tsv --baseline`；`inventory`/`--prefix` 仅辅助，永不作为清单来源。**
