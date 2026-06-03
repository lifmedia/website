---
name: blog-writer
description: >-
  Research a keyword and write a top-tier LIF Media blog post on the existing
  HTML template, with full schema, sitemap entry, and IndexNow ping. Use when
  the user wants a new blog post, an SEO article, or content for a target keyword.
---

# Blog Writer — LIF Media

Produce a publish-ready blog post for `www.lifmedia.ca` that is genuinely useful,
anchored in a real LIF Media project, and technically clean for SEO. This skill
mirrors the manual process the team already follows — see `CLAUDE.md` and
`/blog/_template/index.html`.

## Inputs to gather first

Ask the user for whatever is missing:
- **Target keyword / topic** (e.g. "construction video production Moncton").
- **Anchor project**: which real client/shoot does this post tell the story of?
  (Posts must be story-first, not generic — check `/blog/` for the existing tone.)
- **Hero media**: image URL (Cloudinary) or a YouTube video ID, and author name.

## Process

### 1. Research the SERP (don't skip)
- `WebSearch` the target keyword. `WebFetch` the **top ~10 ranking pages**.
- **Discard** forums, Q&A threads, and thin/low-quality results — only learn from
  the strong pages (this is the hilo's rule).
- From what's left, extract the **common structure** (sections readers expect) and
  the **content gaps** (angles nobody covers well). Note the search intent.

### 2. Outline
- Build an outline that covers the expected structure **plus** the gap angles.
- Keep LIF Media's story-first voice: open on the real project, generalize from it.
- Plan 2–4 `<h2>` sections, an optional pull-quote, and a natural close into the CTA.

### 3. Draft on the template
- Copy `/blog/_template/index.html` → `/blog/<slug>/index.html`. Pick a short,
  keyword-rich `<slug>` consistent with existing posts (lowercase, hyphenated, geo).
- Replace **every** `<!-- TODO -->`. Keep all `../../` relative paths intact.
- Head tags: `<title>` (`… | LIF Media`), `meta description` 150–160 chars,
  geo `meta keywords`, canonical, OG (`og:locale` `en_CA`) and Twitter Card.
- Body: real, specific, no keyword stuffing. Use `loading="lazy"` images with alt text.

### 4. Schema (both blocks, valid JSON)
- `BlogPosting`: headline, description, image, `datePublished`/`dateModified`
  (today's date), author Person, publisher Organization (logo already in template),
  `mainEntityOfPage` with the post URL.
- `BreadcrumbList`: Home → Blog → this post.
- If a YouTube video is embedded, add a `VideoObject` block (see existing posts that
  embed Shorts, e.g. `/blog/un-more-than-a-game-soccer-nb-moncton/`).

### 5. Wire it into the site
- Add a `.blog-card` linking the new post in `/blog/index.html`.
- Fill the post's **Related** section with 2–3 hand-picked cards (`href="../other-slug/"`).
- Add the `<url>` entry to `sitemap.xml` (copy an existing blog entry's format:
  `lastmod` = today, `changefreq` monthly, `priority` 0.8).

### 6. Publish signal
- Run `scripts/publish-post.sh <slug> <YYYY-MM-DD>` to confirm the sitemap entry and
  ping IndexNow, **or** call `scripts/indexnow.sh https://www.lifmedia.ca/blog/<slug>/`.
- Note: IndexNow only works once the page is live on GitHub Pages, so run it after push.

## Guardrails (AEO "never do" list from the source thread)
- ❌ No keyword stuffing — write for the reader, place the keyword naturally.
- ❌ No generic AI filler — every claim ties back to a real LIF Media production.
- ❌ Don't invent clients, stats, or quotes. If you lack a real detail, ask the user.
- ❌ Don't link to `/blog/_template/` from the listing.

## Done means
A new `/blog/<slug>/index.html` with all TODOs resolved, two (or three) valid JSON-LD
blocks, a card in `/blog/index.html`, a `sitemap.xml` entry, and the IndexNow command
ready (or run, post-deploy). Verify locally via the port-8080 server in `.claude/launch.json`.
