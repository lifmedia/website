# DESIGN.md — Cinematic Editorial Design System

A portable, framework-free design system distilled from **LIF Media** (lifmedia.ca).
Plain HTML5 + CSS3 + vanilla JS, no build step. Drop the tokens and components into
any static site to get the same sober, cinematic, story-first feel.

> **Aesthetic in one line:** earthy olive/sage palette + a serif-display headline
> against clean Inter body copy, generous whitespace, subtle film-grain overlay, and
> slow scroll-reveal motion. Restrained, premium, editorial — never hype.

---

## 1. Design tokens

All design decisions live in CSS custom properties on `:root`. Copy this block
verbatim, then rename the brand colors if you're rebranding.

```css
:root {
  /* ── Brand palette ── */
  --deep-olive:  #42682E;  /* primary — buttons, links, accents */
  --muted-sage:  #758E63;  /* secondary green */
  --soft-moss:   #D3E2C0;  /* light green — arrows, hover text on dark */
  --terracotta:  #C67155;  /* warm accent — labels, FAB, focus rings */

  /* ── Neutrals ── */
  --obsidian:    #1A1A1A;  /* primary text */
  --white:       #FFFFFF;
  --off-white:   #F5F3EF;  /* page background */
  --warm-cream:  #EDE8E0;  /* alt section background */

  /* ── Type ── */
  --font-body:   'Inter', -apple-system, sans-serif;
  --font-accent: 'DM Serif Display', Georgia, serif;

  /* ── Layout ── */
  --max-w:       1200px;
  --section-pad: 120px 24px;

  /* ── Motion ── */
  --ease:     cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out: cubic-bezier(0.0, 0, 0.2, 1);

  /* ── Radii ── */
  --radius-sm:   8px;
  --radius-md:   12px;
  --radius-lg:   16px;
  --radius-xl:   20px;
  --radius-pill: 9999px;
}
```

### Color usage rules
- **Background** is `--off-white`, never pure white. Alternate sections with `--warm-cream`.
- **Body text** is `--obsidian` (`#1A1A1A`), never `#000`.
- **Primary action / link** = `--deep-olive`. Hover lightens to `#527a38`.
- **Accent** (eyebrow labels, FAB, focus outlines) = `--terracotta`. Use sparingly — it's the one warm pop in an otherwise green/neutral field.
- **Dark sections / footer / mobile menu** use near-black `#0a0a0a` (slightly off true black), with white text at reduced opacity (`rgba(255,255,255,0.6)` for body, `0.35` for labels).

---

## 2. Typography

Two families, loaded from Google Fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

| Role | Family | Notes |
|------|--------|-------|
| Display / headlines | `DM Serif Display` (`--font-accent`) | Used for `h1`/`h2` and big editorial moments. Italic variant for emphasis. |
| Body, UI, labels | `Inter` (`--font-body`) | Weights 300–700. 300 for large hero sub-copy, 600 for labels/buttons. |

### Type scale (fluid, `clamp()`)
Headlines scale with the viewport. Reference sizes pulled from production pages:

```css
/* Hero headline */            font-size: clamp(2.8rem, 7vw, 6rem);   line-height: 1.0; letter-spacing: -0.02em;
/* Section heading (h2) */     font-size: clamp(2rem, 4vw, 3.2rem);   line-height: 1.1;
/* Sub-heading (h3) */         font-size: clamp(1.5rem, 2.5vw, 2rem);
/* Hero sub / lead copy */     font-size: clamp(1rem, 1.5vw, 1.15rem); font-weight: 300; line-height: 1.75;
/* Body */                     font-size: 1rem; line-height: 1.7;
```

**Conventions**
- Display headlines: `font-family: var(--font-accent)`, tight `letter-spacing: -0.02em`, `line-height` ~1.0–1.15.
- Use `<em>` inside headlines for an italic serif accent word (same color, `font-style: italic`).
- On photos/video, add `text-shadow: 0 4px 40px rgba(0,0,0,0.6)` so text stays legible.

### Eyebrow label (`.lif-label`)
The signature small-caps tag with a leading rule. Sits above most section headings.

```css
.lif-label {
  font-family: var(--font-body);
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--terracotta);
  display: flex; align-items: center; gap: 10px;
}
.lif-label::before {
  content: ''; display: inline-block; width: 28px; height: 1px;
  background: var(--terracotta); flex-shrink: 0;
}
```

---

## 3. Global base styles

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--font-body);
  background: var(--off-white);
  color: var(--obsidian);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
img { max-width: 100%; display: block; }
a { text-decoration: none; color: inherit; }
```

### Film-grain overlay (signature texture)
A fixed, full-viewport SVG noise layer above everything (`z-index: 10000`,
`pointer-events: none`). It's what makes flat sections feel filmic.

```css
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 10000;
  opacity: 0.4;
}
```

---

## 4. Layout & spacing

- **Content width:** wrap sections in a centered container at `max-width: var(--max-w)` (1200px), `margin: 0 auto`, side padding 24px.
- **Section rhythm:** vertical padding via `--section-pad` (`120px 24px` desktop), which automatically tightens on small screens (see responsive tokens below).
- **Grids:** use CSS Grid for multi-column layouts. The footer is the canonical example: `grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 48px`.

### Responsive breakpoints
Three breakpoints, mobile-first overrides:

```css
@media (max-width: 900px) { /* nav collapses to overlay menu; logo shrinks */ }
@media (max-width: 700px) { :root { --section-pad: 72px 16px; } }
@media (max-width: 480px) { :root { --section-pad: 64px 16px; } /* single-col footer */ }
```

The 900px breakpoint is the desktop↔mobile line: above it the inline nav shows,
below it the hamburger + full-screen overlay menu takes over.

---

## 5. Components

### 5.1 Buttons (`.lif-btn`)
Pill-shaped, uppercase, letter-spaced. One base class + a variant. Optional animated
arrow that grows on hover.

```css
.lif-btn {
  display: inline-flex; align-items: center; gap: 14px;
  padding: 16px 32px; font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.12em; text-transform: uppercase;
  transition: background 0.3s, transform 0.2s;
  border: none; cursor: pointer; border-radius: var(--radius-pill);
}
.lif-btn--primary       { background: var(--deep-olive); color: var(--white); }
.lif-btn--primary:hover { background: #527a38; transform: translateX(4px); }
.lif-btn--dark          { background: var(--obsidian); color: var(--white); }
.lif-btn--dark:hover    { background: var(--deep-olive); transform: translateY(-2px); }
.lif-btn--outline       { background: transparent; color: var(--obsidian); border: 1px solid rgba(26,26,26,0.25); }
.lif-btn--outline:hover { border-color: var(--deep-olive); color: var(--deep-olive); transform: translateX(4px); }
.lif-btn--outline-light { background: transparent; color: var(--white); border: 1px solid rgba(255,255,255,0.25); }
.lif-btn--white         { background: var(--white); color: var(--obsidian); }
.lif-btn:focus-visible  { outline: 2px solid var(--deep-olive); outline-offset: 3px; }
```

Variants by context: `--primary` (olive on light), `--dark` (black, becomes olive on
hover), `--outline` (light bg), `--outline-light` / `--white` (dark/photo bg).

Optional arrow element inside the button:
```html
<a class="lif-btn lif-btn--primary">Get in touch <span class="lif-btn__arrow"></span></a>
```
```css
.lif-btn__arrow { width: 20px; height: 1px; background: var(--soft-moss); position: relative; transition: width 0.3s; }
.lif-btn__arrow::after { content: ''; position: absolute; right: 0; top: -3px; width: 7px; height: 7px;
  border-top: 1px solid var(--soft-moss); border-right: 1px solid var(--soft-moss); transform: rotate(45deg); }
.lif-btn:hover .lif-btn__arrow { width: 32px; }
```

### 5.2 Hero (full-bleed video/photo)
Bottom-left aligned content over a darkened media background.

```css
.lif-hero {
  min-height: 100vh; min-height: 100svh;
  display: flex; flex-direction: column; justify-content: flex-end;
  position: relative; padding: 0 24px 80px; overflow: hidden; background: #000;
}
.lif-hero__overlay  { position: absolute; inset: 0; z-index: 2; background: rgba(0,0,0,0.5); }
.lif-hero__content  { position: relative; z-index: 5; max-width: var(--max-w); margin: 0 auto; width: 100%; }
.lif-hero__headline { font-family: var(--font-accent); font-size: clamp(2.8rem, 7vw, 6rem);
  line-height: 1.0; letter-spacing: -0.02em; color: var(--white); text-shadow: 0 4px 40px rgba(0,0,0,0.6); }
.lif-hero__sub      { font-size: clamp(1rem, 1.5vw, 1.15rem); font-weight: 300;
  color: rgba(255,255,255,0.8); max-width: 520px; line-height: 1.75; }
```
For a video bg, cover-fit it absolutely behind a `0.5` black overlay.

### 5.3 Header (`#lif-hdr`)
Fixed, transparent over the hero, then turns into a frosted-glass white bar after
50px of scroll (toggled by JS adding `.hdr-scrolled`). Logo swaps white→dark variant.

```css
#lif-hdr {
  position: fixed; top: 0; left: 0; right: 0; z-index: 10002;
  padding: 20px 40px; display: flex; align-items: center; justify-content: space-between;
  background: transparent;
  transition: background 0.45s var(--ease), padding 0.35s var(--ease), box-shadow 0.45s var(--ease);
}
#lif-hdr.hdr-scrolled {
  padding: 12px 40px;
  background: rgba(255,255,255,0.94);
  backdrop-filter: blur(28px) saturate(1.6);
  -webkit-backdrop-filter: blur(28px) saturate(1.6);
  box-shadow: 0 1px 0 rgba(0,0,0,0.05);
}
```
Nav links: 11px, `font-weight: 600`, `text-transform: uppercase`, `letter-spacing: 0.14em`.
Dropdowns are white rounded cards (`border-radius: 14px`, soft shadow) that fade/slide in on hover.

### 5.4 Mobile overlay menu (`#lif-mob`)
Full-screen black panel. Big serif links (`clamp(42px, 7vw, 80px)`), an info column on
the right with contact + socials. Opened/closed via JS; locks body scroll while open.

### 5.5 Footer (`.lif-footer`)
Near-black (`#0a0a0a`), white text at low opacity, 4-column grid collapsing to 2 then 1.
Brand column uses the serif display face for the name; nav columns use 11px uppercase
labels over 14px links.

### 5.6 Floating action button (`.lif-fab`)
Round terracotta tap-to-call button, fixed bottom-right, injected by JS. Hidden until
the user scrolls past the hero, then scales in.

```css
.lif-fab {
  display: flex; position: fixed; bottom: 24px; right: 20px; z-index: 10001;
  width: 56px; height: 56px; border-radius: 50%;
  background: var(--terracotta); color: var(--white);
  align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(198,113,85,0.4), 0 2px 8px rgba(0,0,0,0.2);
  transition: transform 0.3s var(--ease), opacity 0.3s var(--ease);
  opacity: 0; transform: scale(0.8); pointer-events: none;
}
.lif-fab.visible { opacity: 1 !important; transform: scale(1) !important; pointer-events: auto; }
```

---

## 6. Motion

Motion is slow, soft, and one-directional (fade + rise). Never bouncy.

### Scroll-reveal
Elements get `.lif-reveal` and animate in when they enter the viewport (via
`IntersectionObserver`, threshold ~0.12). Stagger with `-d1`…`-d4` delay classes.

```css
.lif-reveal {
  opacity: 0; transform: translateY(28px);
  transition: opacity 0.8s cubic-bezier(0.22,1,0.36,1), transform 0.8s cubic-bezier(0.22,1,0.36,1);
}
.lif-reveal.is-visible { opacity: 1; transform: translateY(0); }
.lif-reveal-d1 { transition-delay: 0.15s; }
.lif-reveal-d2 { transition-delay: 0.3s; }
.lif-reveal-d3 { transition-delay: 0.45s; }
.lif-reveal-d4 { transition-delay: 0.6s; }
```

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.lif-reveal').forEach((el) => observer.observe(el));
```

**Hover motion:** small `translateX(4px)` / `translateY(-2px)` nudges on buttons and
links — subtle, ~0.2–0.3s.

---

## 7. Accessibility & quality conventions

- Every interactive element has a visible `:focus-visible` ring (`2px` solid, brand
  color or terracotta, `outline-offset: 3px`).
- Color choices avoid pure black/white for softer contrast, but keep text legible
  (dark text on `--off-white`; white text on `#0a0a0a` / darkened media).
- Use `min-height: 100svh`/`100dvh` alongside `100vh` for mobile-correct full-height
  sections.
- Respect reduced-motion: gate the reveal/transition CSS behind
  `@media (prefers-reduced-motion: no-preference)` when porting (the source site
  relies on JS-added classes; add this guard for the new site).

---

## 8. How to reuse on another site

1. Copy the `:root` token block (Section 1) into your global stylesheet. Rename the
   brand colors and fonts to rebrand while keeping structure.
2. Add the two Google Fonts (or swap for your own display + sans pairing).
3. Bring over the base reset, `body::before` grain, and the components you need
   (`.lif-btn`, `.lif-label`, header, footer, `.lif-fab`, `.lif-reveal`).
4. Copy the small vanilla-JS block (Section 6 + header scroll toggle + menu open/close).
   No framework or build step required — it's all static.
5. Keep the **rules of thumb**: off-white (not white) backgrounds, one warm accent,
   serif display + Inter body, generous spacing, slow fade-up motion, a whisper of grain.

---

*Source of truth: `css/style.css`, `js/main.js`, and page-level `<style>` blocks in
the LIF Media repository. This document is a portable extraction — when the source
changes, regenerate.*
