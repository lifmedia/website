---
name: seo-competitor-gap
description: >-
  Pull competitor sitemaps (Aspen Films, Uproar, Atlas Films) plus lifmedia.ca,
  infer the target keyword of each URL, run a content gap analysis, and write a
  6-month content roadmap. Use for competitor SEO research, gap analysis, or a
  monthly competitor tracker.
---

# SEO Competitor Gap — LIF Media

Reproduce the "steal your competitor's SEO strategy" + "automated competitor
tracker" tactics from the source thread, scoped to what runs from this repo using
`WebFetch` / `WebSearch` (no paid tools).

## Targets

| Site | Sitemap |
|------|---------|
| LIF Media (us) | `https://www.lifmedia.ca/sitemap.xml` |
| Aspen Films | discover (see below) |
| Uproar | discover (see below) |
| Atlas Films | discover (see below) |

> Competitor domains are not yet pinned. First run: ask the user to confirm each
> competitor's exact domain, or find it via `WebSearch` (e.g. "Aspen Films video
> production"). Once confirmed, record the domains at the top of the generated
> `seo/competitor-gap-analysis.md` so future runs reuse them.

## Process

### 1. Locate each sitemap
For every competitor, `WebFetch` in order until one resolves:
`/sitemap.xml` → `/sitemap_index.xml` → the `Sitemap:` line in `/robots.txt`.
Follow sitemap-index files down to the child sitemaps. Collect all `<loc>` URLs.

### 2. Infer keyword / intent per URL
For each URL (ours and theirs), infer the **target keyword and search intent** from
the slug and, where useful, by `WebFetch`-ing the page `<title>`/`<h1>`. Bucket each
URL into a theme: service, industry vertical, location page, blog/story, about, etc.

### 3. Gap analysis
Build two lists:
- **Gaps to capture** — themes/keywords competitors cover that LIF Media does **not**
  (or covers thinly). Prioritize by: relevance to LIF Media's real services ×
  apparent demand × how thin the competitor's coverage is (room to do it better).
- **Moats to defend** — themes where LIF Media leads (e.g. notable clients: UN, TSN,
  Wildcats; same-day delivery; bilingual NB production). Keep these fresh.

### 4. Write the outputs
- `seo/competitor-gap-analysis.md` — pinned competitor domains, the per-site URL/keyword
  inventory, and the gap + moat tables.
- `seo/roadmap.md` — a **6-month content roadmap**: month-by-month list of pages /
  industry pages / blog posts to create, each with target keyword, intent, the gap it
  fills, and which existing LIF Media service/portfolio piece it can anchor on. Blog
  items should be feedable straight into the `blog-writer` skill.

### 5. Monthly tracker mode (the thread's tactic 2)
This skill is the engine; scheduling lives in **Claude Desktop**, not the repo. Give the
user this prompt to paste into a Claude Desktop scheduled task (start of each month):

> "Run the seo-competitor-gap process: re-pull the live sitemaps of Aspen Films, Uproar,
> Atlas Films, and lifmedia.ca. Diff against last month's inventory in
> `seo/competitor-gap-analysis.md`. Tell me which pages/blogs the competitors published
> since last month, infer their target keywords, and append any new gaps to `seo/roadmap.md`."

On each tracker run, **diff** against the previously saved inventory and report only the
*new* competitor URLs, then update the roadmap.

## Done means
`seo/competitor-gap-analysis.md` and `seo/roadmap.md` exist, are non-empty, list all four
sites' inventories, and the roadmap has concrete, prioritized, keyword-tagged items.
