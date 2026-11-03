# Critique: judging the render

Detail for SKILL.md §13. Adapted from Leonxlnx/taste-skill v2.1.5 `references/critique.md` (MIT,
(c) 2026 Leonxlnx); screenshots come from the headless recipe below instead of the upstream inspector.

Ticking the pre-flight list means nothing banned was noticed. It says nothing about whether the page is
good. Judge the screenshots, never the code: you wrote the code, so you will read your intentions into
it. If a problem is visible in a screenshot, it is real, whatever the code says.

## 1. Taking the screenshots (headless only)

Rules: Playwright with `headless: true`, run the way the `webapp-testing` skill runs its scripts. Never
the Chrome extension, never `headless: false`, never a desktop or Tauri dev app (shoot the web build
only). Write the script and the images to a scratch folder, not into the project.

Serve what the visitor receives:
- A static page: serve its folder (`python3 -m http.server 4173`).
- A project with a build step: the production build and its preview (`vite build && vite preview
  --port 4173 --strictPort`, `next build && next start -p 4173`). Never ports 3000 or 3001; they may
  belong to a running dev server.
- Start and stop the server with `webapp-testing`'s `scripts/with_server.py`.

```js
// shoot.mjs <url> <outDir>
import { chromium } from 'playwright';
const [url, out] = process.argv.slice(2);
const views = [[1440, 900, 'desktop'], [768, 1024, 'tablet'], [390, 844, 'phone']];
const browser = await chromium.launch({ headless: true });
for (const [w, h, name] of views) {
  for (const reduced of name === 'desktop' ? [false, true] : [false]) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, reducedMotion: reduced ? 'reduce' : 'no-preference' });
    const tag = reduced ? `${name}-reduced` : name;
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1200);                       // let entrance motion settle
    await page.screenshot({ path: `${out}/${tag}-fold.png` });
    const total = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < total; y += Math.round(h / 3)) {   // scroll through so reveals fire
      await page.mouse.wheel(0, Math.round(h / 3));
      await page.waitForTimeout(200);
    }
    await page.waitForTimeout(800);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: `${out}/${tag}-full.png`, fullPage: true });
    console.log(tag, JSON.stringify(await page.evaluate(() => ({
      sidewaysOverflow: document.documentElement.scrollWidth > innerWidth + 1,
      h1Count: document.querySelectorAll('h1').length,
      longHeadlines: [...document.querySelectorAll('h1,h2,h3')].map((e) => {
        const cs = getComputedStyle(e);
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
        return { text: e.textContent.trim().slice(0, 40), lines: Math.round(e.offsetHeight / lh) };
      }).filter((x) => x.lines > 2),
      brokenImages: [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src),
    }))));
    await page.close();
  }
}
await browser.close();
```

The printed numbers only point where to look; the screenshot is the judge. Pinned scroll sections
can render oddly in a full-page shot: judge them in the fold shots taken while scrolling, or add fold
shots at the pinned positions. For a page with both colour schemes, repeat the desktop run with `colorScheme: 'dark'` in
`newPage`. If Playwright cannot run, say so in the report and do not claim any visual check.

## 2. How to look

Open `desktop-fold`, `desktop-full`, `tablet-full`, `phone-fold`, `phone-full`, then
`desktop-reduced-full`. Make each pass on its own.

1. **One second, then five.** Glance and look away. There should be exactly one answer: a word, an
   image, an object. Then give the first screen five seconds as a stranger: what is this, who is it
   for, what do I do next?
2. **Squint.** The page should reduce to two or three large masses with clear size differences.
3. **Cover the logo.** Could this first screen belong to a competitor? Does the idea reach the
   pricing, the FAQ and the footer, or does the page turn into stock blocks after the first screen?
4. **Edges.** Count the distinct left edges of text blocks. Two or three, reused on purpose.
5. **Space and frame.** Section gaps clearly larger than gaps inside a section? Any hole (empty by
   accident)? Equal left and right margins? A section with text in one half and the other half empty?
   A stretch of nothing taller than half a screen?
6. **Type.** Body-to-headline jump three times or more? More than five sizes? An orphan word? A
   paragraph wider than about 75 characters, or centred over more than three lines?
7. **Colour.** Name the proportions: ground, support, accent. An accent in ten places means nothing.
8. **Images.** Is every picture doing a job? Shared ratios and one treatment? Any grey box, stretched
   photo, fake screen of bars, random stock photo, broken image?
9. **Sameness.** One word for each section's layout. The same word twice in a row, or three times on
   the page, is the template showing.
10. **Phone.** Its own composition, or the desktop squeezed? Is the first screen still one clear thing?
11. **Fullness.** Is each desktop screen a composed poster, or a narrow column of small text with dead
    ground either side? A page that could pass for an unfinished wireframe is underbuilt.
12. **Substance.** Does every section the brief asked for deliver its information completely, at a
    readable size? Is the primary action a real button on the first screen?
13. **Collisions.** Anything on top of a headline, a statement or a button? Anything off the edge of
    the phone? A blank band where a reveal did not fire? Content missing in the reduced-motion shot?
14. **The competitor and the live thing.** Put the nearest competitor's name in the idea sentence:
    does it still work? Name the one live thing. If either is weak, that is problem one.

## 3. The score

Four criteria, 1-10 each, weighted **design 40%, usability 30%, creativity 20%, content 10%**.

- **Design:** 9-10 every screen holds as a poster; 8 confident, one or two soft spots; 7 clean, little
  tension; 6 tidy but anonymous, reads as a kit; 5 or less weak hierarchy, default type, mismatched
  images.
- **Usability:** 9-10 you know what it is and what to do without scrolling, flawless on a phone; 8
  minor friction; 7 one real problem; 6 or less you have to hunt, or something breaks.
- **Creativity:** 9-10 a concept specific to this subject; 8 a clear idea with one memorable move; 7 a
  tasteful known approach; 6 or less the category default.
- **Content:** 9-10 every line could only be about this subject; 7-8 concrete, some generic lines; 6 or
  less slogans, filler, stock.

`overall = 0.4·design + 0.3·usability + 0.2·creativity + 0.1·content`. Real award-level sites land
around 7.5-8.0. If your first score for your own work is 9, score it again as a juror who did not
build it.

## 4. Caps (override the arithmetic)

- A headline of three or more lines at any width, sideways overflow on the phone, a broken image, or
  any tell from SKILL.md §10 visible in a screenshot: overall ≤ **6.5**.
- The page could belong to anyone (pass 3): creativity ≤ **6**. The idea passes for the nearest
  competitor (pass 14): creativity ≤ **7**. No live thing: creativity ≤ **7.5**.
- No real picture and no careful drawing of the subject anywhere: design ≤ **6.5**.
- `MOTION_INTENSITY` above 4 but the page barely moves, or one identical fade on every block:
  design ≤ **7**.
- Any placeholder (grey box, lorem, "Image here", a random stock photo): content ≤ **5**.
- Two or more desktop screens mostly empty, or running text small and grey: design ≤ **6.5**.
- A section the brief asked for that is missing or reduced to a few words: content ≤ **6**.
- No real button for the primary action on the first screen: usability ≤ **7**.
- No clear title on the first screen saying what this is: usability ≤ **6**.
- Unequal page margins, a section huddled on one side, or a blank stretch taller than half a screen:
  design ≤ **6.5**.
- A section of running text with no heading: usability ≤ **7**.
- Anything covering a headline at any scroll position: usability ≤ **6**.
- A blank band where a reveal did not fire, content clipped off-screen, or content missing under
  reduced motion: usability ≤ **5**.

## 5. Writing the critique

Write it down, in exactly this shape, so rounds can be compared:

```
ROUND n
Seen in one second: …
Idea (one sentence): …
Live thing: …
Layout words by section: hero=… / …=… / …
Scores: design _ · usability _ · creativity _ · content _ → overall _._
Caps applied: …
Top three problems (most visible first), each with the screenshot it shows in and the fix:
1. …
2. …
3. …
```

Name problems the way a designer would to a colleague: "the supporting paragraph starts 40px left of
the headline's edge", "the testimonial section is the third split layout in a row". "Could be more
polished" is not a finding.

## 6. What to fix first

Later items cannot rescue earlier ones: 1. the idea (if pass 3 fails, change the hero concept, not the
details); 2. hierarchy (one dominant element per screen); 3. composition (edges, spacing, layout
variety, holes); 4. typography; 5. imagery; 6. colour; 7. detail (states, focus, mobile); 8. motion.
When removing something leaves a gap, do not refill it with an ornament: close the gap, enlarge what
remains, or let a picture or a colour field take the space.

## 7. When to stop

At most three rounds: critique, fix the top three, shoot again, critique. Stop early when a round finds
no problem a stranger would notice. If round three still scores under 7.5, say so plainly in the
report with the remaining problems listed; do not round up.
