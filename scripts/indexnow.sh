#!/bin/bash
#
# Ping IndexNow to instantly notify Bing, Yandex, Naver, Seznam, and Yep
# of new or updated URLs on lifmedia.ca.
#
# ChatGPT search, Copilot, and Perplexity all draw heavily from Bing's index,
# so this is also the fastest path to AI-search visibility for new content.
#
# Usage:
#   ./scripts/indexnow.sh                      # ping every URL in sitemap.xml
#   ./scripts/indexnow.sh URL [URL ...]        # ping specific URLs
#
# Requires: curl, sed, grep (all standard on macOS/Linux)
#
# Run from the repo root after publishing new content.

set -e

HOST="www.lifmedia.ca"
KEY="ed5c56354de7ef6e58fd079806770323"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
SITEMAP="https://${HOST}/sitemap.xml"

# Collect URLs — from arguments if provided, otherwise from sitemap.xml
if [ "$#" -gt 0 ]; then
  URLS=("$@")
else
  echo "→ Reading URLs from ${SITEMAP}"
  # Pull <loc> entries out of sitemap.xml
  mapfile -t URLS < <(curl -s "${SITEMAP}" | grep -oE '<loc>[^<]+</loc>' | sed 's/<loc>//;s/<\/loc>//')
fi

if [ "${#URLS[@]}" -eq 0 ]; then
  echo "✗ No URLs to submit." >&2
  exit 1
fi

# Build JSON payload (urlList as an array of strings)
URL_JSON=$(printf '"%s",' "${URLS[@]}")
URL_JSON="[${URL_JSON%,}]"

PAYLOAD=$(cat <<EOF
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "${KEY_LOCATION}",
  "urlList": ${URL_JSON}
}
EOF
)

echo "→ Submitting ${#URLS[@]} URL(s) to IndexNow..."
for url in "${URLS[@]}"; do
  echo "   • ${url}"
done

RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://api.indexnow.org/IndexNow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${PAYLOAD}")

case "${RESPONSE}" in
  200) echo "✓ IndexNow accepted the submission (HTTP 200)." ;;
  202) echo "✓ IndexNow received the submission (HTTP 202 — processed)." ;;
  400) echo "✗ Bad request (HTTP 400). Check payload format." >&2; exit 1 ;;
  403) echo "✗ Key not valid (HTTP 403). Check ${KEY_LOCATION} is publicly accessible and contains exactly: ${KEY}" >&2; exit 1 ;;
  422) echo "✗ URLs don't belong to host (HTTP 422)." >&2; exit 1 ;;
  429) echo "✗ Rate limited (HTTP 429). Try again later." >&2; exit 1 ;;
  *)   echo "? IndexNow returned HTTP ${RESPONSE}." ;;
esac
