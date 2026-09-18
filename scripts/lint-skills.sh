#!/usr/bin/env bash
set -uo pipefail
fail=0
shopt -s nullglob
skills=(*/SKILL.md)
[ "${#skills[@]}" -gt 0 ] || { echo "FAIL  no */SKILL.md files found"; exit 1; }
for f in "${skills[@]}"; do
  dir=$(dirname "$f")
  fm=$(awk 'NR==1 && /^---$/ {inside=1; next} inside && /^---$/ {exit} inside {print}' "$f")
  if [ -z "$fm" ]; then echo "FAIL  $f: no frontmatter"; fail=1; continue; fi
  ok=1
  for key in name description license metadata; do
    if ! grep -q "^${key}:" <<<"$fm"; then echo "FAIL  $f: missing '$key'"; fail=1; ok=0; fi
  done
  for key in category locale; do
    if ! grep -qE "^[[:space:]]+${key}:" <<<"$fm"; then echo "FAIL  $f: missing 'metadata.${key}'"; fail=1; ok=0; fi
  done
  name=$(sed -n 's/^name:[[:space:]]*//p' <<<"$fm" | head -1)
  license=$(sed -n 's/^license:[[:space:]]*//p' <<<"$fm" | head -1)
  [ "$name" = "$dir" ] || { echo "FAIL  $f: name '$name' != directory '$dir'"; fail=1; ok=0; }
  [ "$license" = "MIT" ] || { echo "FAIL  $f: license must be MIT"; fail=1; ok=0; }
  grep -qE 'English|英語|英文' "$f" || { echo "FAIL  $f: no English summary marker"; fail=1; ok=0; }
  [ "$ok" -eq 1 ] && echo "OK    $f"
done
while IFS= read -r f; do
  if grep -nE '[[:blank:]]+$' "$f" >/tmp/trailing.$$; then
    echo "FAIL  $f: trailing whitespace"; cat /tmp/trailing.$$; fail=1
  fi
done < <(find . -type f \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' \) -not -path './.git/*' | sort)
rm -f /tmp/trailing.$$
exit "$fail"
