#!/usr/bin/env bash
# WebBlaze outdated-site scanner v2.
# Usage: bash scan.sh domains.txt [results.csv]
#   domains.txt = one domain per line (no scheme). CSV of results is written too.
# Philosophy: weight RENDER-INDEPENDENT signals (no-HTTPS, no-mobile) that truly mean
# "this site is bad in 2026", and DON'T penalize Wix/Weebly/etc for old jQuery/tables
# (builders trip those flags but render fine). Auto-writes a "reason" line for the cold email.
# SCORE >=4 = strong target. Always eyeball score>=3 before emailing.
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
OUT="${2:-results.csv}"
echo "score,domain,https,mobile,builder,year,email,phone,reason" > "$OUT"

scanone(){
  d=$(printf '%s' "$1" | sed 's|https\?://||;s|/.*||;s|^www\.||' | tr -d '[:space:]')
  [ -z "$d" ] && return
  # fetch html (try https, https+www, then http)
  html=""; for u in "https://$d" "https://www.$d"; do
    html=$(curl -s -A "$UA" -L --max-time 15 "$u" 2>/dev/null); [ -n "$html" ] && break; done
  [ -z "$html" ] && html=$(curl -s -A "$UA" -L --max-time 15 "http://$d" 2>/dev/null)
  if [ -z "$html" ]; then printf "SCORE --  %-32s DEAD/again\n" "$d"; echo "0,$d,dead,,,,,,\"did not load\"" >> "$OUT"; return; fi
  # https support? (000 on both = no https)
  h1=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://$d" 2>/dev/null)
  h2=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://www.$d" 2>/dev/null)
  https="yes"; { [ "$h1" = "000" ] && [ "$h2" = "000" ]; } && https="no"
  score=0; flags=""; reason=""
  # builder?
  builder="-"
  echo "$html" | grep -qiE 'wix\.com|wixstatic'   && builder="Wix"
  echo "$html" | grep -qiE 'weebly'               && builder="Weebly"
  echo "$html" | grep -qiE 'squarespace'          && builder="Squarespace"
  echo "$html" | grep -qiE 'godaddy|websitebuilder' && builder="GoDaddy"
  echo "$html" | grep -qiE 'dudamobile|duda\.co'  && builder="Duda"
  # mobile?
  mobile="yes"; echo "$html" | grep -iq 'name="viewport"' || mobile="no"
  # ---- scoring (strongest, verifiable signals first) ----
  if [ "$https" = "no" ]; then score=$((score+4)); flags="$flags NO-HTTPS";
     reason='the site loads without HTTPS, so browsers show visitors a "Not Secure" warning'; fi
  if [ "$mobile" = "no" ]; then score=$((score+3)); flags="$flags NO-MOBILE";
     [ -z "$reason" ] && reason="the site doesn't resize for phones, which is where most customers will find you"; fi
  yr=$(echo "$html" | grep -oiE '(©|&copy;|copyright)[^<]{0,25}20[0-2][0-9]' | grep -oE '20[0-2][0-9]' | sort -n | tail -1)
  if [ -n "$yr" ] && [ "$yr" -le 2021 ]; then score=$((score+2)); flags="$flags YEAR($yr)";
     [ -z "$reason" ] && reason="the site looks unmaintained — the footer still shows $yr"; fi
  if echo "$html" | grep -qiE 'swfobject|\.swf|shockwave'; then score=$((score+3)); flags="$flags FLASH";
     [ -z "$reason" ] && reason="the site still uses Flash, which no current browser supports"; fi
  # old jQuery / tables ONLY count against hand-built sites, not builders
  jq=$(echo "$html" | grep -oiE 'jquery[/.-][0-9]+\.[0-9]+' | head -1)
  if [ "$builder" = "-" ] && echo "$jq" | grep -qiE 'jquery[/.-][12]\.'; then score=$((score+2)); flags="$flags OLD-JQ"; fi
  tbl=$(echo "$html" | grep -ciE '<table')
  if [ "$builder" = "-" ] && [ "$tbl" -ge 4 ]; then score=$((score+1)); flags="$flags TABLES($tbl)"; fi
  echo "$html" | grep -qiE 'name="description"' || { score=$((score+1)); flags="$flags NO-METADESC"; }
  # contact
  email=$(echo "$html" | grep -oiE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' | grep -viE 'sentry|wixpress|\.png|\.jpg|@2x|w3\.org|example|godaddy|@sentry' | sort -u | head -1)
  phone=$(echo "$html" | grep -oE '\(?[0-9]{3}\)?[-. ][0-9]{3}[-.][0-9]{4}' | head -1)
  [ -z "$reason" ] && reason="the site is dated and plain — a modern refresh would stand out"
  echo "$score,$d,$https,$mobile,$builder,${yr:-},$email,$phone,\"$reason\"" >> "$OUT"
  printf "SCORE %-2s  %-32s https:%-3s mob:%-3s %-11s%s\n" "$score" "$d" "$https" "$mobile" "$builder" "$flags"
  [ -n "$email" ] && printf "            %-34s %s\n" "$email" "$phone"
}
while IFS= read -r line; do scanone "$line"; done < "${1:-/dev/stdin}"
echo "--- results CSV: $OUT (sort by column 1 desc for best targets) ---"
