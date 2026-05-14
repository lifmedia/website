# Google Ads Landing Page — `/video-production-new-brunswick/`

A standalone, conversion-focused landing page for Google Ads paid-search traffic.
**Not** a normal site page: no global nav, no exit paths, one job — turn an ad click
into a lead (form submit or tap-to-call).

It is **noindexed** and deliberately **kept out of `sitemap.xml`** — it should only
ever be reached via a paid ad. Do not link to it from the main site and do not add
it to the sitemap.

Everything is in a single self-contained `index.html` (inline `<style>` + inline
`<script>`). It reuses the shared `../css/style.css` (design tokens, FAB) and
`../js/main.js` (injects the tap-to-call floating button).

---

## How leads + conversion tracking work

1. Visitor submits one of the two `.lp-form` instances (hero + final CTA).
2. The inline script validates, then sends the lead via **EmailJS** to
   `contact@lifmedia.ca`.
3. On success it redirects to **`/thank-you/`**.
4. `/thank-you/` is what fires the conversions on page load — GA4 `generate_lead`
   **and** the Google Ads conversion `AW-17933483390/SqJmCLPNipccEP76rOdC`.

The conversion is tied to the **thank-you page load**, never to the button click —
so it fires exactly once and only on a genuinely successful submit. There is a
commented-out optional inline-fire spot in the `.then()` callback if you ever want
belt-and-suspenders, but you normally should not need it.

The tap-to-call links and the floating call button fire the click-to-call
conversion `AW-17933483390/qHYXCJLw-JYcEP76rOdC` via `gtag_report_conversion()`.

---

## Where to wire / change tracking

- **GA4 + Google Ads IDs:** in `index.html` `<head>`, inside the
  `<!-- TRACKING CONFIG -->` block (`G-R4RGQTNSQS`, `AW-17933483390`).
- **EmailJS IDs + thank-you URL + lead source label:** in the `CONFIG` object at
  the top of the inline `<script>` at the bottom of `index.html`.

---

## Swapping the hero video / poster

In the `<section class="lp-hero">` block, the `<video>` tag has:
- `poster="…showreelforwebsite_kxfbgl.jpg"` — the still shown before/while the video loads.
- `<source src="…showreelforwebsite_kxfbgl.mp4">` — the looping showreel.

Both are Cloudinary URLs. Swap them for any other Cloudinary video — keep
`f_auto,q_auto` in the path so Cloudinary auto-optimizes format and quality.
Keep `preload="metadata"` + a valid `poster` so the page paints instantly.

---

## Cloning for a new city (e.g. Moncton, Fredericton, Saint John)

1. Copy this whole folder to `/video-production-<city>/`.
2. In `index.html`, update everything marked `data-swap="…"` plus the head tags.
   The full checklist is in the `CITY VARIANT SWAP POINTS` comment block at the top
   of `<body>`:
   - `<title>`, meta description, and canonical URL (in `<head>`)
   - Hero `<h1>` headline — `data-swap="headline"`
   - Hero subheadline — `data-swap="subheadline"`
   - Hero trust line — `data-swap="trustline"`
   - FAQ geographic-coverage answer — `data-swap="geo-faq"`
   - Footer location line — `data-swap="footer-location"`
3. Update `CONFIG.LEAD_SOURCE` in the inline script so leads are attributed to the
   right page.
4. Do **not** add the new page to `sitemap.xml`. Keep the `noindex` meta tag.
5. Deploy = `git push` (GitHub Pages, no build step).

---

## Open items to confirm before spending ad budget

- Final hero headline + subheadline copy (current text is a working draft).
- That the "What do you need?" `<select>` options match how LIF wants inbound
  categorized.
- That `AW-17933483390/SqJmCLPNipccEP76rOdC` (fired by `/thank-you/`) is the
  conversion action you want Google Ads to optimize toward.
