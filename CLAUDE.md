# CLAUDE.md — LIF Media (lifmedia.ca)

Project memory for Claude Code sessions working on this repository.

## What this is

**LIF Media** is a cinematic video production company based in **Moncton, New
Brunswick**, serving Atlantic Canada and beyond. Founder / Creative Director:
**Jorge Melgar**. Officially bilingual (EN/FR); the team also works in Spanish.

- Phone: +1 (506) 688-7043 · Email: contact@lifmedia.ca
- Address: 21 Rue Foxtrot, Moncton, NB, E1C 1E6, Canada
- Domain: `www.lifmedia.ca`

## Stack & deployment

- **Static HTML, no framework, no build step.** Plain HTML5 + CSS3 + vanilla JS.
- Hosted on **GitHub Pages** (`CNAME` → `www.lifmedia.ca`). A push to the default
  branch **is** the deploy. There is nothing to compile.
- Each route is a folder with an `index.html` (e.g. `/cinematic-commercials/index.html`).
- Styles: `css/style.css` (design system), `css/blog.css`, `css/contact-form.css`.
- Scripts: `js/main.js` (header scroll, menu, reveal animations, FAB), `js/contact-form.js`.
- Local preview: server config in `.claude/launch.json` (Node, port 8080).

## Brand voice

Story-first, sober, cinematic. Lead with a real client/project, not generic claims.
Avoid hype and keyword stuffing. Every blog post anchors in an actual production.

## SEO conventions (already in place — keep consistent)

- `sitemap.xml` is **hand-maintained**. Every new public page must be added there.
- `robots.txt` allows all crawlers incl. an explicit AI-crawler allowlist; references
  the sitemap. `llms.txt` holds LLM-facing company info.
- Every page carries: canonical, Open Graph (`og:locale` = `en_CA`), Twitter Card,
  and **JSON-LD schema** appropriate to the page type.
- Geo-targeted keywords: Moncton + NB cities (Dieppe, Riverview, Fredericton, Saint
  John) + Atlantic Canada.
- Analytics: GA4 `G-R4RGQTNSQS`, Google Ads `AW-17933483390` (click-to-call conversion).
- Instant indexing: `scripts/indexnow.sh` pings IndexNow (Bing/Yandex/etc., which also
  feeds ChatGPT/Copilot/Perplexity). Key file: `ed5c56354de7ef6e58fd079806770323.txt`.

## Blog publishing workflow (do ALL steps)

Posts live at `/blog/<slug>/index.html`. To create one:

1. **Copy** `/blog/_template/index.html` to `/blog/<slug>/index.html` and replace every
   `<!-- TODO -->` marker. Internal paths use `../../`.
2. Fill the **two JSON-LD blocks**: `BlogPosting` + `BreadcrumbList`. Add a `VideoObject`
   block if the post embeds a YouTube video.
3. Set `<title>`, `meta description` (150–160 chars), geo `meta keywords`, canonical, OG/Twitter.
4. Add a card linking the post in `/blog/index.html` and pick 2–3 related posts in the post.
5. Add the post's `<url>` to `sitemap.xml` (same format as existing entries).
6. Ping IndexNow: `scripts/publish-post.sh <slug> <YYYY-MM-DD>` (adds to sitemap + pings),
   or `scripts/indexnow.sh https://www.lifmedia.ca/blog/<slug>/` directly.

## Skills available in this repo (`.claude/skills/`)

- **blog-writer** — research a keyword, draft a top-tier post on the `_template`, wire up
  schema, sitemap and IndexNow.
- **seo-competitor-gap** — pull competitor sitemaps (Aspen Films, Uproar, Atlas Films) +
  ours, run gap analysis, write a 6-month content roadmap to `seo/`.
- **digital-pr** — find link/PR opportunities and data angles for the NB/video niche.

## Out of scope (future)

A centralized SEO dashboard (DataforSEO, GSC, Apify, ScreamingFrog MCP) requires external
API keys / MCP servers configured outside this repo. Not set up here yet.
