#!/usr/bin/env bash
# Extract http(s) URLs from each skill's SKILL.md and verify they respond.
# Skipped:
#   - templated URLs (containing { } or < >): need real parameters
#   - URLs ending in '=': a <placeholder> parameter was cut off
#   - opendata.cwa.gov.tw/api/*: requires a CWA API key (401 without one)
#   - the YouBike feeds below: covered by deep JSON validation instead
# Fullwidth CJK punctuation (。,,、;:()) terminates a URL in zh-TW prose;
# halfwidth delimiters are stripped only at the end via sed.
set -u
fail=0

# Deep validation: HTTP 200 is not enough for the YouBike feeds - a dying
# endpoint can return 200 with an error page or empty JSON. Parse the body
# as JSON and enforce a minimum station count per feed (thresholds are
# ~85% of the 2026-09-10 counts; station numbers only drift slowly).
declare -A FEEDS=(
  ["https://apis.youbike.com.tw/json/station-yb2.json"]=9000
  ["https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"]=1500
  ["https://data.ntpc.gov.tw/api/datasets/010E5B15-3823-4B20-B401-B1CF000550C5/json?page=0&size=5000"]=1400
  ["https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=9468c0d0-e1ed-4ecc-a86f-ab5a9fd590ff"]=1600
  ["https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json&limit=2000"]=600
)
for url in "${!FEEDS[@]}"; do
  min=${FEEDS[$url]}
  body=$(curl -s -L --max-time 60 -A 'baodao-skill-url-check' "$url")
  count=$(printf '%s' "$body" | jq -r 'if type=="array" then length else 0 end' 2>/dev/null || echo 0)
  if [[ "$count" =~ ^[0-9]+$ ]] && [ "$count" -ge "$min" ]; then
    echo "OK    $url ($count stations >= $min)"
  else
    echo "FAIL  $url (parsed ${count:-0} stations, expected >= $min)"
    fail=1
  fi
done

mapfile -t urls < <(grep -hoE "https?://[^ )\"\`'。，、；：（）]+" -- */SKILL.md \
  | sed 's/[.,;。,]*$//' | sort -u)
for url in "${urls[@]}"; do
  case "$url" in
    *'{'*|*'}'*|*'<'*|*'>'*) echo "SKIP  $url (templated)"; continue ;;
    *=) echo "SKIP  $url (placeholder parameter)"; continue ;;
    *opendata.cwa.gov.tw/api/*) echo "SKIP  $url (needs CWA API key)"; continue ;;
  esac
  skip=0
  for feed in "${!FEEDS[@]}"; do
    if [ "$url" = "$feed" ]; then skip=1; break; fi
  done
  [ "$skip" -eq 1 ] && continue
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 \
    -A 'baodao-skill-url-check' "$url")
  case "$code" in
    2*|3*) echo "OK    $code $url" ;;
    *)     echo "FAIL  $code $url"; fail=1 ;;
  esac
done
exit "$fail"
