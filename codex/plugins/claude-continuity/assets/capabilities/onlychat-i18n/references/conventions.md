# OnlyChat i18n 细节约定

> SKILL.md 是流程主干；本文是接线/复用/飞书的具体写法与坑，按需查。

## next-intl 接线写法（项目实测）

### 1. 简单文案
```tsx
// 前：title="Basic Info"
// 后：
const t = useTranslations();
title={t('worldcard_basic_info')}
// en.json: "worldcard_basic_info": "Basic Info"
```

### 2. 带占位（`${}` → `{}`）
```tsx
// 前：placeholder={`Get your ${categoryLabel} a wonderful name`}
// 后：placeholder={t('worldcard_name_placeholder', { categoryLabel })}
// en.json: "worldcard_name_placeholder": "Get your {categoryLabel} a wonderful name"
```

### 3. 文内高亮 → t.rich（单 key，禁拆 prefix/suffix）
```tsx
// 前：<>Select an image(<span className="text-x">WebP/PNG; <5MB</span>) works best.</>
// 后：
helper={t.rich('worldcard_image_helper', {
  format: (chunks) => <span className="text-x">{chunks}</span>,
  imageRatioLabel,
})}
// en.json: "worldcard_image_helper": "Select an image(<format>WebP/PNG; <5MB</format>) ... {imageRatioLabel} works best."
```
项目现成范式：`createoc_uploadhint3` = `We supported <bold>...</bold> file.` + `t.rich('...', { bold: (v) => <span className="font-bold">{v}</span> })`。
注意：`<5MB` 里的 `<` 不会被当 tag（tag 名必须字母开头），安全。

### 4. 模块级常量数组（hook 不能在模块作用域调）
```tsx
// 前：const GENDER = [{ value:'MALE', label:'Male' }, ...]; 渲染 {label}
// 后：
const GENDER = [{ value:'MALE', labelKey:'worldcard_gender_male' }, ...];
// 渲染处（组件内有 t）：{t(labelKey)}
```

### 5. 整句带变量 = 一条完整 key（禁拼）
`Delete {name}?` 必须整条 key。**不能** `t('delete') + name + '?'`：
```
en:  Delete {displayName}?         "Delete" 在前
ja:  {displayName} を削除しますか？  "削除" 在句尾
```
拼接在非英语语序全错。

### 6. 非组件文件 / 顶层 const
`imageUploadConfig.ts`、`getNoteDisplayName.ts`、顶层 `const ERR = '...'` 这类没法用 hook：
- 把字符串解析挪进 React 调用点、把 `t` 传进去；或重构成函数接收 `t`
- 实在不好弄就**跳过 + 列为例外**让用户决定，别硬塞 hook 把构建弄崩

## 复用判定细节

- "现成可复用" = 目标英文与某个**非本前缀、且全 15 语言都有值**的 key **字符级完全相同**
- 优先**裸通用 key**（`cancel`/`save`/`name`/`clear`/`delete`/`done`/`back`/`draft`/`discard`/`description`/`image`/`gender`/`age`/`tags`/`introduction`/`got_it`/`add_tags`/`select_your_tags`/`create`/`manage`/`loading`/`coming_soon`/`untitled` …）
- pattern 复用：`{a}/{b} Chars`→`num_chars`（`t('num_chars',{current_num,max_num})`）；纯 "Chars"→`chars`；分类名→`world_section_<noteType>`
- **前缀/功能归属不是保留理由**：`createoc_rating`/`createoc_visibility`/`oc_create_view_guide`/`bonus_btn_submitted` 这种带功能前缀的，只要 en 值**字符级相同 + 全 15 语言** → **照样复用**。key 不是模块，两处显示同一个词不是"耦合"；"怕别的功能改文案"是芝麻风险（极少发生、真发生也就一行 cosmetic fix），不准用它当借口建重复键（见 SKILL.md 心智锚）
- **真正"同值也不复用"只有两种**：
  - **不是字符级相同**（"unknown" vs `oc_delete_name_unkown` 大小写不同、尾部空格差到会显形）→ 本就不算可复用
  - **该值在某语言必须翻成不同的词**（语法性别/格、chip 太窄要短译）→ 这才保留两个
- 别靠眼力：出飞书清单前 `reuse-audit` 机械兜一遍，值撞现成全语言键即命中、必复用

## 同值去重（同 en 值的 key 该不该合）

接线后多组件分头建 key，常出现**两个新 key 英文一模一样**（这次 worldcard 就有 `Always On` / `Unfinished` / `Create New World` 三对）。出飞书清单前用 `dups` 扫一遍。

- **判定**：i18n 按**概念**分 key，不按"显示在哪个组件"。同一个东西（同一状态 / 同一动作 / 同一标题）= 一个 key，不管它出现在卡片、设置项、还是筛选 chip
- **为什么必须合**：同值两 key 在飞书是**两行**，翻译各填各的——可能填一样、可能填不一样、可能漏一行。想让两处永远显示一致，**只有合成一个 key 能保证**
- **合并机制**：留通用名那个 → 把另一处 call site `t()` repoint 过去 → 删冗余 key。**删法 = 删飞书那一行 + `pnpm i18n`（覆盖式自动从 15 个 json 清掉）**，不要手删 15 个 json
- **保留两个的唯一理由**：你预判某语言里这两处译文要分歧（语法格、或 chip 太窄要短译）。短状态词（Always On / Unfinished）几乎不会，一律合
- **跨作者不碰**：`dups` 也会扫出别人 key 的同值对（如 `worldcard_under_review_got_it` vs `worldcard_chat_unavailable_got_it`）。别人的不合、不动，带 `--exclude` 过滤

## 别人代码的剔除（git blame 作者过滤）

- 只处理 `zhanghao@peekaboogames.com` 写的行（gitea/work 身份）
- 同一文件可能混作者：逐行 blame，别人写的 key（如 fuxiaojie/justxuemin 的 chat_unavailable/switch/under_review/block 系列）**跳过、列出来**，不接、不进你的飞书清单
- 历史经验里别人的 worldcard key（剔除清单可作 `--exclude` 起点）：
  `worldcard_block_*` `worldcard_chat_unavailable_*` `worldcard_switch_*` `worldcard_under_review_*` `worldcard_note_not_usable_label` `worldcard_note_view_sensitive_content` `worldcard_delete_failed/title/undone_desc` `worldcard_metric_notes` `worldcard_submit`

## 飞书 / pnpm i18n

- 表：`Y0uMsICffhOewutAk1Xc0NLJnqd`，sheet `zeHW5Z`（web 测试）/ `25kNVe`（预发&线上）。A 列 key、B 列 en、后面是各语言
- `pnpm i18n` 凭证硬编码在 `localization/i18n.py`（无需配 env）；submodule 空就先 `git submodule update --init localization`
- `pnpm i18n` = 从飞书**全量重写** 15 个 json。**覆盖式**：飞书没有的 key 会被删。所以**用户飞书录完再跑**
- 跑完验证：snapshot 的新建 key 应 100% 存活（没存活=飞书漏录，列出来让补）；其它语言空=翻译列没填（预期，等翻译）
- 值里**别放双引号**（飞书 cell 前导 `"` 会被当 CSV quote 截断/串行）；TSV 粘贴：`key\tEN`，无换行值才安全（多行值会串行）

## i18n JSON 文件格式（脚本/合并必须匹配，否则炸 diff）

`src/i18n/*.json` 的硬约束：

- `.prettierignore` 含 `*.json` → **prettier 不格式化 i18n**（`prettier --write` 是 no-op，`--check` 还会误报 "All matched files use Prettier code style"）
- 实际格式 = **4-space 缩进 + 非 ASCII 一律 `\uXXXX` 转义（lowercase）**
- 任何脚本 / codegen / 合并产出 i18n **必须匹配这两点**。`JSON.stringify(obj, null, 2)`（默认 2-space + 原始 UTF-8）会让每行都 diff
- 实测：rebase 用脚本合并，非英文文件每个炸出 ~8000 行纯格式噪音；改 4-space + `\uXXXX` 后塌缩到 ~200 行真增量
- 输出转义实现：`JSON.stringify(obj, null, 4)` 后遍历 `charCodeAt(i) > 127` 的字符替成 `'\\u' + n.toString(16).padStart(4, '0')`。**别用带字面 unicode 的正则**（Write 工具会把 `中` 写成真字符）

## rebase i18n 冲突 → 三方合并

`src/i18n/*.json` rebase 冲突时不要手解，用 git stage 三方 merge：

- 取 `:1:<path>` (base) / `:2:<path>` (ours) / `:3:<path>` (theirs)
- 按 key 用 `undefined` 表缺失，做 3-way：`o === t → o` / `o === b → t` / `t === b → o` / 否则真冲突
- **必须用 `undefined` 表缺失**才能尊重"一侧删除"——否则会把对方删掉的 key **复活**
- 键序保留 ours，再追加 theirs-only
- `worldcard_*` key 冲突取 WIP 分支（你的）；其余取主干
- 写回时仍按上一节格式（4-space + `\uXXXX`），否则一样炸 diff

## HTML 清单格式

- 两段：**① 本次新建（进飞书，N 个）② 本次复用（不进飞书，已全语言）**
- 位置列**去重**：同文件只标行号 `L123`，跨文件才标 `relpath:line`（section 头已有文件名，别重复整路径）
- 顶部统计：新建数 / 复用数 / 缺 en（应为 0）

## 这次（2026-05）落 worldcard 的实绩（可作校准基线）

PRD 3.1/3.4/4.1/8，zhanghao 代码：硬编码全接 t()，**新建 119 + 复用 33**（24 通用词 + num_chars/chars/world_section + 几个 error/something_wrong 等既有依赖），tsc 0 错，飞书覆盖后 119/119 存活。
