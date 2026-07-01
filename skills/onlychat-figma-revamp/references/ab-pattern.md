# V2 + useGradualRollout AB 代码模板

以 `TagListV2` 为实战参照。

## 1. 注册 topic

`src/hooks/useGradualRollout.ts`：

```ts
export enum ROLLOUT_TOPIC {
  // 现有...
  home_ui_revamp = 'home_ui_revamp_ab',
  // ↑ 新增：<业务>_<动作>_ab；enum key 用 snake_case，value 是稳定字符串（上报/开关后端用）
}
```

## 2. 写 V2

与 V1 同目录：`src/components/Tag/TagListV2.tsx`。

**接口**：V1 所有 props + 可选 UI 控制位。例：

```tsx
type Props = {
  // 全部来自 V1
  tags: (CharacterTag | EventTag | string)[];
  selectSlug?: string | string[];
  onChange?: (slug: string) => void;
  emptyClassName?: string;
  className?: string;
  showBlockButton?: boolean;
  defaultExpanded?: boolean;
  hideLabel?: boolean;
  // V2 新增（仅 UI 控制，不改逻辑）
  hideImageSlug?: boolean;
};
```

**逻辑搬运**（从 V1 原样 copy，禁止修改）：

```tsx
const t = useTranslations();
const locale = useLocale();
const pathname = usePathname();
const blockStore = useBlockStore();
const { setHomeExpanded } = useHomeTagListStore();
const [expanded, setExpanded] = useState(defaultExpanded);

useAsyncBlockTags();  // ← 必须，否则屏蔽词列表不刷新

const blocked = blockStore.tag;

const tagsData = useMemo(
  () => tags
    .filter(t => !blocked.find(b => b === (typeof t === 'string' ? t : t.slug)))
    .map(/* ... */),
  [tags, selectSlug, t, blocked],
);

const handleToggle = () => {
  setExpanded(prev => {
    const next = !prev;
    if (next) TrackWithParams('cus.click_home_tag', { tag: 'expand' });
    if (pathname === '/' || pathname === `/${locale}`) {
      setHomeExpanded(next);  // ← 漏了会导致滚动错乱
    }
    return next;
  });
};

// Empty state 必须保留
if (tagsData.length === 0 ||
    (tagsData.length === 1 && tagsData[0].slug === DEFAULT_SORT)) {
  return <div className={twMerge('mb-4', emptyClassName)} />;
}
```

**i18n fallback**（用 `||` 不用 `??`）：

```tsx
const rawLabel = getTagLabel({ tag, t });
const label = rawLabel || (slug === 'image' ? t('image') : slug);
```

## 3. 消费端三元切换

`src/app/[locale]/(dashboard)/(home)/components/Content/DesktopFilter.tsx`：

```tsx
import TagList from '@/components/Tag/TagList';
import TagListV2 from '@/components/Tag/TagListV2';
import { ROLLOUT_TOPIC, useGradualRollout } from '@/hooks/useGradualRollout';

const isNewUI = useGradualRollout(ROLLOUT_TOPIC.home_ui_revamp, true);

return (
  // ...
  isNewUI ? (
    <TagListV2
      emptyClassName="mb-0"
      className={from === 'home' ? 'my-0' : 'mt-0'}
      tags={tags}
      selectSlug={slugList}
      onChange={changeSlug}
      showBlockButton={status === 'authenticated'}
      defaultExpanded={defaultTagListExpanded}
    />
  ) : (
    <TagList
      /* 同样的 props */
    />
  )
);
```

## 4. AB 分组曝光埋点

**放在容器组件**（例如 `HomeContent.tsx`），只报一次：

```tsx
const isNewUI = useGradualRollout(ROLLOUT_TOPIC.home_ui_revamp, true);

useEffect(() => {
  if (isNewUI === undefined) return;
  TrackWithParams('cus.home_abtest_ui_revamp', {
    category: isNewUI ? 'a' : 'b',
  });
}, [isNewUI]);
```

事件命名：`cus.<业务>_abtest_<topic_短名>`。

## 5. URL 调试

- `?__ab__=100` → 强制开（所有 topic）
- `?__ab__=0` → 强制关（所有 topic）
- **全局影响**：如果页面同时有 `home_card` 这种旧 topic，`?__ab__=100` 会一起把它切成变体 B，导致「我只改了 tag UI 但首页卡片也坏了」。诊断时优先清 URL 参数。

## 6. 回滚

V1 没动过，回滚只需：
1. 后端 rollout 配置下调到 0 / Growthbook feature off
2. 或 `useGradualRollout(ROLLOUT_TOPIC.xxx, false)` 默认关
3. 确认无影响后再考虑删 V2 文件（通常保留一两版，观察完再删）

## 不要做的事

- ❌ 在 V2 里加 AB 判断（职责混乱）
- ❌ 改 `.env` 当 AB 开关（要发版、无法灰度）
- ❌ 改 V1 文件（哪怕是「顺手」格式化）
- ❌ 把 V2 的 props 设计成 V1 的子集（下次再改会断）
