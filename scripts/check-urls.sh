#!/usr/bin/env bash
# Extract http(s) URLs from each skill's SKILL.md and verify they respond.
# Skipped:
#   - templated URLs (containing { }): need real parameters
#   - URLs ending in '=': a <placeholder> parameter was cut off
#   - opendata.cwa.gov.tw/api/*: requires a CWA API key (401 without one)
# Fullwidth CJK punctuation (。,,、;:()) terminates a URL in zh-TW prose;
# halfwidth delimiters are stripped only at the end via sed.
set -u
fail=0
mapfile -t urls < <(grep -hoE "https?://[^ )\"\`<'。，、；：（）]+" -- */SKILL.md \
  | sed 's/[.,;。,]*$//' | sort -u)
for url in "${urls[@]}"; do
  case "$url" in
    *'{'*|*'}'*) echo "SKIP  $url (templated)"; continue ;;
    *=) echo "SKIP  $url (placeholder parameter)"; continue ;;
    *opendata.cwa.gov.tw/api/*) echo "SKIP  $url (needs CWA API key)"; continue ;;
  esac
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 \
    -A 'baodao-skill-url-check' "$url")
  case "$code" in
    2*|3*) echo "OK    $code $url" ;;
    *)     echo "FAIL  $code $url"; fail=1 ;;
  esac
done
exit "$fail"
