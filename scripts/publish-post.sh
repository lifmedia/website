#!/bin/bash
#
# Add a new blog post to sitemap.xml and ping IndexNow.
#
# Closes the publishing checklist: inserts a well-formed <url> entry for the post
# (same format as existing blog entries) just before </urlset>, then calls
# indexnow.sh so Bing/Yandex/etc. (and downstream ChatGPT/Copilot/Perplexity)
# pick it up.
#
# Usage:
#   ./scripts/publish-post.sh <slug> [YYYY-MM-DD]
#
# Examples:
#   ./scripts/publish-post.sh construction-video-production-moncton
#   ./scripts/publish-post.sh construction-video-production-moncton 2026-06-02
#
# Notes:
#   - IndexNow only works once the page is live on GitHub Pages, so run this
#     AFTER pushing. The sitemap edit, however, is local and should be committed.
#   - Run from the repo root. Requires: curl, sed, grep (used by indexnow.sh).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SITEMAP_FILE="${ROOT_DIR}/sitemap.xml"
HOST="www.lifmedia.ca"

SLUG="$1"
DATE="${2:-$(date +%F)}"

if [ -z "${SLUG}" ]; then
  echo "✗ Usage: ./scripts/publish-post.sh <slug> [YYYY-MM-DD]" >&2
  exit 1
fi

# Strip any leading/trailing slashes from the slug.
SLUG="${SLUG#/}"; SLUG="${SLUG%/}"
URL="https://${HOST}/blog/${SLUG}/"

if [ ! -f "${SITEMAP_FILE}" ]; then
  echo "✗ sitemap.xml not found at ${SITEMAP_FILE}" >&2
  exit 1
fi

# Insert the <url> block before </urlset>, unless the URL is already present.
if grep -qF "<loc>${URL}</loc>" "${SITEMAP_FILE}"; then
  echo "→ ${URL} already in sitemap.xml — skipping insert."
else
  ENTRY="  <url>\n    <loc>${URL}</loc>\n    <lastmod>${DATE}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n"
  # Insert before the closing tag (portable across GNU/BSD sed via a temp file).
  TMP="$(mktemp)"
  sed "s#</urlset>#${ENTRY}</urlset>#" "${SITEMAP_FILE}" > "${TMP}"
  mv "${TMP}" "${SITEMAP_FILE}"
  echo "✓ Added ${URL} to sitemap.xml (lastmod ${DATE})."
fi

# Ping IndexNow for just this URL.
echo "→ Pinging IndexNow for ${URL}"
"${SCRIPT_DIR}/indexnow.sh" "${URL}"
