# Motion skeletons (React + GSAP / Motion)

Canonical code for the scroll patterns named in SKILL.md §7. Copy the skeleton, then fill it with the project's content. Every skeleton keeps a reduced-motion path; do not remove it.

## A. Sticky-Stack - Canonical Skeleton

```tsx
"use client";
import { useRef, useEffect, useId, type ReactNode } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();
  const instanceId = useId().replace(/:/g, "");
  const cardClass = `stack-card-${instanceId}`;
  const innerClass = `stack-card-inner-${instanceId}`;

  useEffect(() => {
    if (reduce || !ref.current || cards.length <= 1) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(`.${cardClass}`);
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        });
        const inner = card.querySelector(`.${innerClass}`);
        if (!inner) return;
        gsap.to(inner, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
            invalidateOnRefresh: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce, cards.length, cardClass, innerClass]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          style={{ zIndex: i + 1 }}
          className={`${cardClass} relative min-h-[100dvh] flex items-center justify-center`}
        >
          <div className={`${innerClass} w-full flex items-center justify-center will-change-transform`}>
            {card}
          </div>
        </div>
      ))}
    </div>
  );
}
```

Critical points: `start: "top top"`, `pin: true`, every card except the last is pinned, the scale/opacity transform is driven by the NEXT card's scroll trigger (so previous card shrinks as next one arrives). Never combine CSS `position: sticky` with `pin: true` on the same element: the native sticky engine and ScrollTrigger's `position: fixed` fight at the hand-off (judder, snapping, coordinate drift). The pinned element must also not be the element being transformed - pin the outer card and animate an inner wrapper, or the scale tween throws off the pin measurements. Scope the card class per instance (`useId`) so two stacks on one page do not cross-select; stack with ascending `zIndex`. Under `prefers-reduced-motion` the component renders a plain list: no pin, no transforms, all content reachable.

## B. Horizontal-Pan - Canonical Skeleton

```tsx
"use client";
import { useRef, useEffect, type ReactNode } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: ReactNode }) {
  const wrap = useRef<HTMLElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const getDistance = () =>
        Math.max(0, track.current!.scrollWidth - wrap.current!.clientWidth);
      gsap.to(track.current, {
        x: () => -getDistance(),
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${getDistance()}`,               // scroll distance = track width minus viewport, recomputed on refresh
          pin: true,
          scrub: 1,
          anticipatePin: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section
      ref={wrap}
      role="region"
      aria-label="Horizontal content track"
      tabIndex={reduce ? 0 : undefined}
      className={`relative w-full ${reduce ? "overflow-x-auto scroll-smooth" : "overflow-hidden"}`}
    >
      <div
        ref={track}
        className={`flex h-[100dvh] w-max items-center ${reduce ? "snap-x snap-mandatory" : ""}`}
      >
        {children}
      </div>
    </section>
  );
}
```

Critical points: `start: "top top"`, `pin: true`, `end: "+=${getDistance()}"` (scroll length = horizontal travel needed), `scrub: 1`. The wrapper is pinned, the inner track slides horizontally as the user scrolls vertically. `x` and `end` must be function-based and paired with `invalidateOnRefresh: true`; a `distance` captured once never recomputes - after a resize it overshoots into blank space (or pans to nothing when the track fits). Keep `w-max` on the track and make each panel non-shrinking (`shrink-0` or an explicit width): without it, overflow compression collapses `scrollWidth` and the section pins without panning. Under `prefers-reduced-motion` keep every panel reachable: swap the wrapper to `overflow-x-auto` with snap points instead of leaving `overflow-hidden`.

## C. Scroll-Reveal Stagger - Canonical Skeleton (lighter alternative)

For simple "items appear as they enter viewport" (no pinning), prefer Motion's `whileInView` over GSAP - lighter, no ScrollTrigger needed:

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

Use this for: feature lists, testimonial grids, logo walls, anything that just needs "enter on scroll." Save GSAP for actual pin/scrub work.

## D. Forbidden Animation Patterns

* **`window.addEventListener("scroll", ...)`** is banned. It runs on every scroll frame, jank-prone, no batching. Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Custom scroll progress calculations using `window.scrollY`** in React state. Same reason. Re-renders on every frame.
* **`requestAnimationFrame` loops that touch React state.** Use motion values (`useMotionValue` + `useTransform`) instead.
* **Layout Transitions:** Use Motion's `layout` and `layoutId` props for visible state changes (re-ordering lists, expanding modals, shared elements between routes). Do not wrap static content in `layout` props "for safety" - it costs measurement work.
* **Staggered Orchestration:** Use `staggerChildren` (Motion) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for reveal moments where sequence matters. For `staggerChildren`, parent (`variants`) and children MUST share the same Client Component tree.
