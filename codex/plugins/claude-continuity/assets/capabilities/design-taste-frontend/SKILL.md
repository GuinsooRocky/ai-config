---
name: design-taste-frontend
description: 做落地页、作品集、官网改版这类要好看、不像模板的营销型页面：先盘产品独有事实定设计方向，再写文案、找图、出页面，最后 headless 截三个宽度自评改到位。触发词："做个落地页"、"landing page"、"官网改版"、"作品集页面"、"这页太像模板了"、"anti-slop"。不用于：dashboard / 后台 / 表格 / 多步骤产品界面、按 Figma 稿还原（归 onlychat-figma-revamp）、claude.ai 上发布的页面（归 artifact-design）。
---

# tasteskill: Anti-Slop Frontend Skill

## 何时使用

- 用户要做或改版落地页、作品集、产品官网、活动页，并且在意「好看、不像 AI 模板」。
- 用户说「这页太像模板了 / 太 AI 了」，要重做视觉方向。
- 不用于：dashboard、后台、数据表格、多步骤产品界面；有 Figma 稿要逐像素还原的；claude.ai 发布页（归 artifact-design）。

> Landing pages, portfolios, and redesigns. Not dashboards, not data tables, not multi-step product UI.
> Every rule below is **contextual**. None of it fires automatically. First read the brief, then pull only what fits.
> The order of work: read the brief and the subject (§0) → argument, idea, live thing (§1) → dials and foundation (§2-4) → words (§5) → build (§6-9) → look at screenshots and fix (§13) → pre-flight (§14) → report (§15).

---

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

Before touching code or tweaking dials, **infer what the user actually wants**. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

### 0.A Read these signals first
1. **Page kind** - landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** the user used - "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** - URLs they linked, screenshots they pasted, products they named, brands they're competing with.
4. **Audience** - B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** - logo, color, type, photography. For redesigns, these are starting material, not optional input (see §11).
6. **Quiet constraints** - accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These constraints OVERRIDE aesthetic preference.
7. **What imagery truly exists** - the project's own photographs or screenshots, a real interface that can be shown, an image tool you can call, or nothing. Do not plan around pictures you do not have.

### 0.B Inventory the subject (before any design)
In your notes, list **eight to twelve things that belong to this client and to no competitor**: its name and what the name means; its place (street, city, what that place looks like); the numbers in the brief (price, seats, minutes, the year); the constraint it lives with (one batch a month, invite only); its materials and colours; its rituals and hours; the printed or produced things of its world (a ticket, a label, the invoice the tool sends, the output the AI makes). This list is where the idea comes from (§1.B) and what you search for pictures with (§6.6). In blind tests the page that won each brief was built from an item on such a list; the pages that lost had a good composition with a category idea.

### 0.C Output a one-line "Design Read"
State in one line: **"Reading this as: \<page kind> for \<audience>, leaning toward \<design system or aesthetic family>; built around \<inventory item>."** The last clause is required: a read that names only a vibe ("Linear-style minimalist") is the category default, not a decision.

### 0.D If the brief is ambiguous, ask one question, do not guess
Ask exactly **one** clarifying question, and only when a missing fact blocks the work (no product name) or the read genuinely diverges. Otherwise decide, state your reading in one line, and proceed.

### 0.E Anti-Default Discipline
Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900. These are the LLM defaults. Reach past them deliberately based on the design read.

---

## 1. ARGUMENT, IDEA, LIVE THING

Detail and examples: [references/copy.md](references/copy.md) §1.

### 1.A Write the argument
Before any design, list the page as claims with their proof, one line per section (`It takes six weeks, and you can follow it. → the stages, photographed`). The claims decide which sections exist and in what order. **Delete any section that has no claim.** This is how you avoid the stock sequence of hero, logos, three features, testimonial, pricing, CTA.

### 1.B Find the idea
The design read is a way of composing; the idea is what makes the page belong to this subject and no other. Do not start building until this sentence is filled from the inventory (§0.B), not from the category:

> On this page, **[something that belongs to the subject]** becomes **[the device the composition calls for]**.

Places to look: its **output** (put the real output on the page as material), its **object or shape** (enlarge it, crop it, make it the frame), its **name** (can the letters hold a picture, stack into a wall?), its **place**, its **ritual** (a sequence the page can perform as it scrolls), its **artefact** (ticket, menu, label, receipt, manual), its **opposite** (which other category owns the feeling this one lacks?).

**The competitor test:** put the nearest real competitor in the sentence. If it still works, the idea belongs to the category: a loaf of bread is every bakery; the seven doors of the street this one is named after are only this one. "Clean and modern" is not an idea.

### 1.C One live thing
Give the page one thing the visitor can do, or that differs per visit, made from the idea: set the loan and read the real monthly figure; type your name and see it in the foundry's letters; choose a size and see it against the room. In blind tests every winning page had one and jurors named it first. Rules: real content, works with a thumb on a phone, a plain fallback without script, never blocks reading, one thing (not a playground). It is built as part of the page, not added as motion at the end.

---

## 2. THE THREE DIALS (Core Configuration)

After the design read, set three dials. Every layout, motion, and density decision below is gated by these.

* **`DESIGN_VARIANCE: 8`** - 1 = Perfect Symmetry, 10 = Artsy Chaos
* **`MOTION_INTENSITY: 6`** - 1 = Static, 10 = Cinematic / Physics
* **`VISUAL_DENSITY: 4`** - 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4` unless the design read overrides it. Overrides happen conversationally. Use these exact variable names; never invent aliases like `LAYOUT_VARIANCE`. Level definitions: §9.

| Signal / use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site" (default) | 7-9 | 6-8 | 3-5 |
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match existing | +1 | match existing |
| Redesign - overhaul | +2 | +2 | match existing |

---

## 3. FOUNDATION: REAL DESIGN SYSTEM OR AESTHETIC

Do not invent CSS for things that have an official package. Do not pretend an aesthetic trend is an official system. Install commands, canonical sources, the aesthetic-family table and the honest Liquid Glass approximation: [references/design-systems.md](references/design-systems.md).

| Brief reads as… | Reach for |
|---|---|
| Microsoft / enterprise SaaS | `@fluentui/react-components` or `@fluentui/web-components` |
| Google-ish, Material-flavored | `@material/web` + Material 3 tokens |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` |
| Shopify app surfaces | Polaris web components / Polaris React |
| Atlassian / Jira-style | `@atlaskit/*` + `@atlaskit/tokens` |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` |
| Public-sector UK / US | `govuk-frontend` / `uswds` |
| Fast local-business / agency MVP | Bootstrap 5.3 |
| Modern accessible React foundation | `@radix-ui/themes` |
| SaaS where you own the components | shadcn/ui, never shipped in default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind utilities (the project's version) |

**Honesty rule:** if the brief reads as one of the systems above, install and use the **official** package; do not recreate its CSS by hand or override 90% of its tokens. **One system per project.** Aesthetic families (glass, bento, brutalism, editorial, kinetic type, Liquid Glass) have no official package: build them natively and label approximations honestly.

---

## 4. STACK & CONVENTIONS

### 4.A Stack: keep the project's
* **Existing project:** use its framework, styling method (Tailwind v3 or v4, CSS modules, styled-components, plain CSS), component library and animation library. Check `package.json` before adding anything. **No framework or styling-library migration.**
* **Greenfield, no stack named:** a single page → plain HTML + CSS + a small script; an app-shaped site → the user's usual ecosystem (React with Vite, or Next.js). Tailwind v4 if utility CSS is wanted (use `@tailwindcss/postcss` or the Vite plugin, not `tailwindcss` in `postcss.config.js`).
* **Only in Next.js:** Server Components by default; providers and anything using Motion, scroll listeners or pointer physics live in isolated `'use client'` leaves; fonts via `next/font`.
* **Animation:** Motion (`import { motion } from "motion/react"`) in React projects; CSS, Web Animations or GSAP elsewhere.
* **Fonts:** self-host with `@font-face` + `font-display: swap`, or the framework's font loader. No render-blocking Google Fonts `<link>` in production.

### 4.B State (React)
Local `useState` / `useReducer` for isolated UI; global state only to avoid deep prop-drilling (Zustand, Jotai, context). **Never** track continuous values (mouse position, scroll progress, pointer physics) in `useState`; use `useMotionValue` / `useTransform` / `useScroll`.

### 4.C Icons
* **Allowed libraries (priority order):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`. `lucide-react` only on request or when the project already depends on it.
* **Never hand-roll icon paths.** One family per project; standardize `strokeWidth` globally (e.g. `1.5`).

### 4.D Emoji Policy
Discouraged by default in code, markup and visible text; use icon-library glyphs. Allow emoji only when the user explicitly asks for a playful / chat-style vibe, and then sparingly.

### 4.E Responsiveness & Layout Mechanics
* Standard breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`); contain layouts (`max-w-7xl mx-auto` or equivalent).
* **Viewport stability:** never `h-screen` for full-height heroes; use `min-h-[100dvh]` / `min-height: 100dvh`.
* **Grid over flex-math:** never `w-[calc(33%-1rem)]`; use CSS Grid.

### 4.F Dependency Verification (mandatory)
Before importing ANY third-party library, check `package.json`. If missing, output the install command first. Never assume a library exists.

---

## 5. WRITE THE WORDS FIRST

Write the whole page as a copy deck (plain text) before markup. Detail: [references/copy.md](references/copy.md).

* **Every headline fits in two lines or fewer at every width.** Cut words first, then widen the measure, set the size last. About **32 Latin characters** survives everywhere at a confident size (gallery hero median: 5 words). For Chinese / Japanese / Korean, about **16 characters** (full-width, `k ≈ 1.0`). Do the arithmetic in copy.md §2 before committing to a sentence.
* **One supporting sentence** directly under the headline, saying plainly what the thing is and for whom (≤ 20-22 words). One primary action, named for what it does, as a real button on the first screen.
* **The first screen answers the visitor's first question in large type.** Event: what, when, where. Product: what it is and what it costs or does. Person: who and what they do.
* **Write the full content.** Every section the brief asks for delivers its information completely: the whole menu with prices, each plan with what it includes, every speaker with a talk. Thin sections are the commonest reason a clean page loses to a busier one.
* **Sample details are expected** where the brief leaves gaps (dish names, plan names, project titles), so the design is seen at full density. List every one in the report for the client to confirm.
* **Proof is never invented.** No customers, quotes from named people, logos, user counts, ratings, press or business statistics the brief does not supply. Without real proof, show the thing itself, state how it works, use facts from the brief. If a testimonial or logo section is explicitly requested, use plainly fictional sample content (no real companies, no real people) and flag it in the report.
* **Copy self-audit (before shipping):** re-read every visible string. Rewrite anything grammatically broken, with unclear referents, cute-but-wrong wordplay, mock-poetic micro-meta, or genre verbs (unlock, elevate, seamless, supercharge). A plain functional sentence beats AI-cute copy. One copy register per page.
* **Quotes:** max 3 lines of body; attribution is name + role (+ company), never name only; typographic quotes or none.

---

## 6. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

LLMs default to clichés. Override these defaults proactively. Each rule has a context-aware override path.

### 6.1 Typography
* **Scale contrast:** two or three sizes do the visible work: one very large, one small. Headline at least 3x body; on studied top sites the largest type has a median of 8.4vw against 5.0vw on weak ones. Five sizes per page is the ceiling. Display: tracking -0.02 to -0.05em, leading 0.85-1.05 (Latin only). Text: 16-20px, leading 1.45-1.6, 45-75 characters per line, running text in full ink.
* **CJK text:** no negative tracking, display leading ≥ 1.2, body leading 1.6-1.8, break at phrase boundaries (copy.md §2).
* **Sans font choice:** `Inter` is discouraged as default (pick Geist, Outfit, Cabinet Grotesk, Satoshi, or a brand-appropriate face); Inter is fine for a neutral / Linear-style or public-sector brief.
* **Serif discipline:** serif is not the default for "creative / premium". Use it only when the brand names one, or the family is genuinely editorial / luxury / publication / heritage and you can say why this serif fits this brand. `Fraunces` and `Instrument Serif` are banned as defaults; rotate justified serifs across projects (PP Editorial New, GT Sectra Display, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Editorial Old, Saol Display, Domaine Display, Canela, Schnyder, Tobias, ITC Galliard). Emphasis inside a headline uses italic or bold of the **same** family, never an injected second family.
* **Italic descender clearance:** italic display words with `y g j p q` need `leading-[1.1]` minimum plus `pb-1` reserve.

### 6.2 Color Calibration
* Max 1 accent color, saturation < 80% by default. One ground, one ink, one accent; the accent sits on the action and perhaps one other thing. **Color consistency lock:** the accent is identical on every section.
* **The Lila rule:** no default AI purple / blue glow. Neutral bases with one high-contrast accent. If the brand is purple, embrace it with intent.
* **Take colour from the subject** when it has unmistakable colours of its own (its material, its street, its landscape); keep the proportions, change the colours.
* **Premium-consumer palette ban:** for cookware / wellness / artisan / luxury / DTC briefs, the default reach of warm cream (`#f5f1ea`, `#fbf8f1`, `#efeae0`…) + brass / clay / oxblood / ochre (`#b08947`, `#b6553a`, `#9a2436`…) + espresso text (`#1a1714`…) is banned unless the brand names it or can justify it. Rotate families instead: cold luxury, forest, black and tan, cobalt + cream, terracotta + slate, olive + brick, monochrome + one saturated pop.
* One palette per project; do not drift between warm and cool greys.

### 6.3 Layout Discipline and the Frame (failing any of these is shipping broken work)
* **Anti-center bias:** centered hero / H1 avoided when `DESIGN_VARIANCE > 4` (split, left content / right asset, scroll-pinned). Centered is fine for manifesto / launch briefs.
* **Hero fits the initial viewport:** headline ≤ 2 lines, subtext ≤ 20 words, CTA visible without scroll; hero top padding ≤ `pt-24` at desktop. Plan font size and image size together.
* **Hero stack: max 4 text elements** (zero or one eyebrow-or-brand-strip, headline, subtext, CTAs). No tagline under CTAs, trust micro-strip, pricing teaser, feature bullets or avatar row in the hero; those get their own sections below.
* **Navigation:** one line at desktop, height ≤ 80px (64-72 default); wordmark, three to five plain links, one action.
* **The frame:** one pair of **equal outer margins** at every width. When a section's text sits in one half, the other half holds its picture, second column, list or figure, never nothing. **No blank stretch taller than about half a screen.** Section gaps (120-240px desktop) are clearly larger than any gap inside a section. Every section the visitor came for opens with a heading that names it; the first screen carries the title in the page's one `h1`.
* **Fullness:** each desktop screen reads as a poster with one dominant thing and its content. One deliberate rest per page at most.
* **Section variety:** each layout family appears at most once (8 sections → ≥ 4 families). Max 2 consecutive image+text zigzag splits.
* **Bento:** rhythm, not repetition; exactly as many cells as content items; at least 2-3 cells with real visual variation (a real image, a brand-appropriate gradient (not AI-purple), a pattern, a tinted field), not white-on-white text cards.
* **Eyebrow restraint (the #1 violated rule):** max 1 small uppercase tracked label per 3 sections (hero counts). Default: drop it; the headline is enough.
* **Split-header ban:** no "big headline left + small explainer floating right" section header unless the right column carries a real visual or interactive element.
* **Mobile collapse is explicit per section:** declare the `< 768px` layout in the same component; the phone is a composition of its own.

### 6.4 Materiality, Shadows, Cards, Shape
* Cards only when elevation communicates real hierarchy; otherwise group with `border-t`, `divide-y`, or negative space. Tinted shadows only, never pure black on light grounds. For `VISUAL_DENSITY > 7`, generic card containers are banned.
* **Shape consistency lock:** one corner-radius system (all sharp, all soft 12-16px, or pill for interactive), or a documented mixed rule followed everywhere.

### 6.5 Interactive States, Forms, Accessibility
* **Full cycles:** skeleton loaders matching the final shape, composed empty states that say how to populate, inline errors (toasts only for transient), tactile `:active` (`scale-[0.98]` or 1px push).
* **Button contrast** WCAG AA (4.5:1 body, 3:1 large); ghost buttons over photos get a scrim or stroke. **CTA labels never wrap** at desktop (1-3 words). **One label per intent** ("Get in touch" + "Let's talk" on one page = fail).
* **Forms:** label above input, helper text, error below, never placeholder-as-label; inputs, placeholders, focus rings and errors all pass AA.
* **Keyboard and names:** every control, the live thing included, works from the keyboard in reading order and has an accessible name (visible label, or `aria-label` for icon-only).
* **A control explains itself** by its form, label and place; if it needs a sentence on how to operate it, redesign it. A field's real limits (password rules, file type and size) stay visible beside it, tied with `aria-describedby`.

### 6.6 Imagery
Landing pages and portfolios are visual products. Detail, search endpoints and credits: [references/imagery.md](references/imagery.md).
1. **Priority:** the project's own images → generated with an image tool, if one exists → real pictures of the subject's world from open collections (downloaded, licence CC0 / PD / CC BY / BY-SA, credited) → **drawn in code from the subject itself** (its objects, its interface, its map), with care and detail → type and colour alone, on purpose.
2. **Never** a random placeholder-photo service, a grey box, "image here", or a photograph of something else standing in for the subject. A found picture never poses as the client's own product, room, person or team.
3. **Showing software:** a real fragment of the interface built in HTML at true size, with believable sample data that adds up, cropped to the point. No `<div>`-bar fake dashboards, no laptop frames.
4. **Logos and social proof:** a logo wall shows only real customers the brief names. Never real company names or marks the brief did not supply. No real proof → leave the section out, or (if explicitly requested) plainly fictional samples flagged in the report.
5. One dominant image beats six small ones; shared crop ratios, one treatment, one radius; nothing lies on top of a headline.

### 6.7 Content Density
* Each section carries one claim, its proof and its **full** content. Cut filler words, never the information the visitor came for.
* **No data dumps for secondary material:** a 30-row award list or giant pricing matrix on a marketing page becomes top highlights + "View full list", a marquee, or its own page.
* **Long lists need a different component, not a longer list:** > 5 items → grouped 2-column split, card per item, tabs / accordion, scroll-snap pills, carousel or marquee. A 10-row spec table with a hairline under every row is the worst default; use grouped chunks, a card per spec with the value large, or featured specs + a disclosure for the rest.

### 6.8 Page Theme Lock
The page has ONE theme; sections do not invert (no warm-paper section between dark ones). One deliberate "theme switch on scroll" is allowed when the brief calls for it. Tints within the same family are fine. With a theming design system, set the theme once at the root.

---

## 7. MOTION

Tools, not defaults; **none fire automatically**. Code skeletons and forbidden patterns: [references/motion-skeletons.md](references/motion-skeletons.md).

* **Motion must be motivated:** each animation answers "what does this communicate?" (hierarchy, storytelling, feedback, state change). "It looked cool" is not an answer.
* **Motion claimed, motion shown:** if `MOTION_INTENSITY > 4`, the page actually moves: hero entrance, staggered section entrances (heading, then text, then picture, 60-90ms apart), feedback on every control. If you cannot ship working motion, drop the dial to 3 and ship a clean static page. Content never stays hidden if a script fails.
* **Glassmorphism / Liquid Glass:** premium consumer, Apple-adjacent, media-overlay only. Inner border + inner highlight, solid fallback under `prefers-reduced-transparency`.
* **Magnetic micro-physics:** `MOTION_INTENSITY > 5` and premium / playful briefs only, via motion values outside the render cycle.
* **Perpetual micro-interactions** (pulse, typewriter, float, shimmer): only where the section benefits (live status, feeds). Spring physics, no linear easing.
* **Marquee: max one per page.**
* **Sticky-stack and horizontal-pan:** use the canonical skeletons (`start: "top top"`, `pin: true`, scrub, instance-scoped selectors, reduced-motion fallback that keeps every panel reachable).
* **Forbidden:** `window.addEventListener("scroll")`, `window.scrollY` progress in React state, `requestAnimationFrame` loops touching React state, `transition: all`.
* **Library choice:** Motion for UI / state change; GSAP + ScrollTrigger for scrolltelling and pins; Three.js for canvas. Never mix GSAP / Three.js with Motion in the same component tree.

---

## 8. PERFORMANCE, ACCESSIBILITY, DARK MODE

* **Hardware acceleration:** animate only `transform` and `opacity`; `will-change` sparingly.
* **Reduced motion (mandatory):** everything above `MOTION_INTENSITY > 3` honours `prefers-reduced-motion`; loops, parallax, scroll-hijack and magnetic physics collapse to static, with all content still visible.
* **Dark mode:** dual-mode by default for consumer-facing pages unless the brief or brand insists on one. One token strategy (`dark:` variant or CSS variables). The brief decides colours; this skill enforces contrast (AA body, AAA target for hero copy), hierarchy parity, brand fidelity, and no pure `#000000` / `#ffffff`. Respect `prefers-color-scheme`. Look at both modes before finishing.
* **Core Web Vitals targets:** LCP < 2.5s (hero image preloaded / priority), INP < 200ms, CLS < 0.1 (reserve space for images, fonts, embeds). Report only numbers you measured.
* **DOM cost:** grain / noise only on fixed `pointer-events-none` pseudo-elements; lazy-load anything below the fold (Motion and Three.js are not small).
* **Z-index restraint:** z-index only for systemic layers (nav, modal, overlay, grain), documented as a scale.

---

## 9. DIAL DEFINITIONS (Technical Reference)

* **DESIGN_VARIANCE** - 1-3 predictable (symmetric grid, equal paddings, centered); 4-7 offset (overlaps, varied aspect ratios, left-aligned headers); 8-10 asymmetric (masonry, `2fr 1fr 1fr` grids, large deliberate empty zones that something closes on the far side). **Mobile override:** levels 4-10 collapse to a strict single column below `768px`.
* **MOTION_INTENSITY** - 1-3 static (hover / active only); 4-7 fluid CSS (`transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1)`, cascaded load-ins; name the properties, never `transition: all`); 8-10 choreography (scroll-triggered reveals, parallax, scroll-driven animation via CSS `animation-timeline` or ScrollTrigger).
* **VISUAL_DENSITY** - 1-3 art gallery (section gaps `py-32` to `py-48`); 4-7 daily app (`py-16` to `py-24`); 8-10 cockpit (tight paddings, no card boxes, 1px lines separate data, `font-variant-numeric: tabular-nums` for all numbers).

---

## 10. AI TELLS (Forbidden Patterns)

Avoid unless the brief explicitly asks. The full registry with alternatives: [references/tells.md](references/tells.md).

* **Visual:** neon / outer glows, pure black, oversaturated accents, gradient headline text, custom cursors, three equal feature cards, icons in tinted squares, `<div>`-bar fake screenshots.
* **Content:** invented proof or statistics; "John Doe" / "Acme" / "Nexus" names; filler verbs (elevate, seamless, unleash, next-gen); performative labels ("Quietly trusted by", "Field notes", "On our desks"); micro-meta sentences under headings; "Step 1 / Phase 02" labels.
* **Furniture:** version labels in the hero (`V0.6`, `BETA`) unless it is a launch; section-number eyebrows (`00 / INDEX`, `001 · Capabilities`); `01 / 4` pagination on tiles; decorative status dots; locale / time / weather strips; scroll cues; decoration text strips (`BRAND. MOTION. SPATIAL.`); pills or labels overlaid on images; decorative photo credits; version footers; middle-dot chains.
* **Dashes:** on English pages, at most one or two em dashes per page and none in headlines, eyebrows, buttons, nav, captions or quote attribution (use a full stop, comma or colon). In Chinese copy 「——」 is standard punctuation; use it sparingly. Ranges may use a hyphen or an en dash.

---

## 11. REDESIGN PROTOCOL

Misclassifying the mode is the single biggest source of bad redesign output.

1. **Detect the mode.** Greenfield (no site, or full overhaul approved) / **Preserve** (modernise without breaking the brand) / **Overhaul** (new visual language, content and IA preserved). If ambiguous, ask once: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*
2. **Record the before.** Shoot the current page with the §13 recipe into a `before` folder (all three widths) and read the code: framework, styling method, components, and what must survive (routes, forms, data, behaviour, brand assets).
3. **Audit before touching:** brand tokens; information architecture and conversion paths; content blocks doing work vs filler; patterns to preserve (signature interactions, copy voice); patterns to retire (tells, broken layouts, dead links, stock imagery); the dial reading of the existing site (your starting point, not the baseline); SEO baseline (ranking pages, meta, structured data, OG cards). **SEO migration is the #1 redesign risk.**
4. **A review stops here.** Critique the before screenshots with [references/critique.md](references/critique.md) and name the three changes that would move the page most.
5. **Preservation rules:** keep the stack (no framework or styling migration), IA, slugs, anchor IDs, nav labels, copy voice, accessibility wins, analytics events. A brand that is already purple stays purple.
6. **Levers, in order (stop when the brief is satisfied):** typography → spacing, rhythm and the frame (equal margins, a heading per section, an `h1`) → colour → states (hover, focus, loading, empty, error) → motion → hero and key-section recomposition → full block replacement only when unsalvageable. IA, content and SEO sound → targeted evolution (levers 1-4); structural visual debt → full redesign with strict content preservation; brand changing → greenfield.
7. **Never change silently:** URL structure, primary nav labels, form field names or order, logo / wordmark, legal / consent / cookie copy.
8. **Prove it.** Shoot again into an `after` folder, compare before and after at every width, click through every link, form and menu that worked before, and report the comparison.

---

## 12. OUT OF SCOPE

This skill is NOT for: dashboards / dense product UI / admin panels (use Fluent, Carbon, Atlassian or Polaris from §3); data tables (TanStack Table, AG Grid); multi-step forms / wizards; code editors (Monaco / CodeMirror); native mobile (Apple HIG / Material); realtime collab UIs. If the brief is one of these, **say so explicitly**, point to the right tool, and apply this skill only to the marketing / about / landing surfaces.

---

## 13. LOOK: SCREENSHOT CRITIQUE LOOP (required before the report)

Ticking boxes is not looking. After the build, look at what you made:

1. **Shoot headless only.** Use the `webapp-testing` skill's way of running Playwright (`headless: true`) with the script in [references/critique.md](references/critique.md) §1: 1440, 768 and 390 wide, a first-screen shot and a full-page shot after scrolling through, plus a desktop shot with reduced motion. Serve the production build or the static folder on a free port (never 3000 / 3001). **Never** the Chrome extension, `headless: false`, or a desktop / Tauri dev app. Keep the script and images in a scratch folder, not the project.
2. **Read every screenshot** (Read tool), not only the first screen.
3. **Critique in writing** with critique.md: the fourteen passes, the weighted score, the caps, the `ROUND n` block.
4. **Fix the top three problems**, shoot again, look again. **At most three rounds.** Stop early when a round finds nothing a stranger would notice. If round three still scores under 7.5, say so in the report with what still falls short.
5. If Playwright cannot run here, say so in the report and claim no visual check.

---

## 14. FINAL PRE-FLIGHT CHECK

Run this before reporting. If a box cannot be honestly ticked, the page is not done.

**Thinking**
- [ ] Inventory written (§0.B); Design Read names an inventory item (§0.C); dials reasoned, not silently baseline.
- [ ] Argument lists one claim per section; the idea sentence passes the competitor test; one live thing built with a no-script fallback.
- [ ] Design system chosen (§3) or aesthetic labeled honestly; one system; the project's stack kept; redesign mode detected and before recorded (§11).

**Words and content**
- [ ] Every headline ≤ 2 lines at 1440 / 768 / 390; first screen says what this is in an `h1`; one real primary button.
- [ ] Full content in every section the brief asked for; sample details listed for the report.
- [ ] No invented proof: no real company logos or names the brief did not supply, no invented statistics, ratings or quotes.
- [ ] Copy self-audit done; dash rule (§10) respected; quotes ≤ 3 lines with clean attribution.

**Layout and frame**
- [ ] Equal outer margins; no half-empty section; no blank stretch over half a screen; a heading on every section.
- [ ] Hero fits the viewport (≤ 20-word subtext, `pt-24` cap, ≤ 4 text elements, no trust strip inside); nav one line, ≤ 80px.
- [ ] Section layout families vary (no 3rd consecutive zigzag split); bento cell count = content count; eyebrows ≤ ceil(sections / 3); no split headers.
- [ ] Theme lock, color consistency lock, shape consistency lock; serif and premium-palette discipline.

**Imagery**
- [ ] No AI tells from §10 visible in the screenshots.
- [ ] Pictures follow §6.6 priority; no random placeholder photos, grey boxes or `<div>`-bar fake screens; found pictures downloaded, licensed and credited; drawings depict the subject's own things.

**Interaction, motion, accessibility**
- [ ] Button and form contrast AA; no wrapping CTA labels; one label per intent; keyboard reachable with accessible names; loading / empty / error states.
- [ ] Every animation motivated; motion claimed = motion shown; reduced-motion fallback keeps all content; no `window` scroll listeners, no `transition: all`; `useEffect` animations clean up; one marquee max; skeleton rules for pins.
- [ ] Dark / light handled per §8; `min-h-[100dvh]` not `h-screen`; mobile collapse explicit; icons from one allowed library.

**Evidence**
- [ ] The §13 loop ran: screenshots read at all three widths after the last change, the last `ROUND` block written.

---

## 15. REPORT

Tell the user, briefly, and claim no check you did not run:
- The Design Read, the dials, the idea sentence and the live thing.
- The last critique round's scores, caps applied, and what still falls short.
- Every sample detail and every fictional sample section to replace before launch.
- Every found picture (file, title, creator, licence, source page) and where its credit sits; which drawings stand in for photography.
- Which checks ran (screenshot rounds and widths, Lighthouse if measured) and which could not run.

---

## Reference files

| File | Read it when |
|---|---|
| [references/copy.md](references/copy.md) | Writing the argument and the copy deck (§1.A, §5); the two-line headline arithmetic, Latin and CJK. |
| [references/imagery.md](references/imagery.md) | Choosing, finding, crediting, drawing and placing pictures (§6.6). |
| [references/critique.md](references/critique.md) | The screenshot recipe and how to score and fix (§13, redesign review). |
| [references/tells.md](references/tells.md) | The full registry of AI tells and what replaces each (§10). |
| [references/motion-skeletons.md](references/motion-skeletons.md) | Building sticky-stack, horizontal-pan or scroll-reveal; forbidden animation patterns (§7). |
| [references/design-systems.md](references/design-systems.md) | Installing a design system, canonical docs, aesthetic families, Liquid Glass approximation (§3). |
| [references/vocabulary.md](references/vocabulary.md) | Naming a hero, nav, grid, card, scroll or gallery pattern. |

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
