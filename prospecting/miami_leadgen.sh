#!/usr/bin/env bash
# WebBlaze — continuous Miami lead generation.
# Loops: source businesses (OSM) across Miami-area cities by niche, scan each site for
# outdated signals + email, and append GOOD leads (old site OR has email) to the master.
# Runs until killed. Safe to re-run; dedupes by domain against the master.
set -u
cd "$(dirname "$0")"
MASTER="leads_miami_master.csv"
LOG="leadgen.log"
SEEN="seen_domains.txt"
PRESETS=(trades pro clinic local)
touch "$SEEN"
[ -f "$MASTER" ] || echo "name,website,domain,email,phone,city,niche,score,https,mobile,reason" > "$MASTER"

log(){ echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

round=0
while true; do
  round=$((round+1))
  preset=${PRESETS[$(( (round-1) % ${#PRESETS[@]} ))]}
  log "=== round $round | niche=$preset | sourcing OSM across Miami cities ==="
  python3 source_osm.py --cities miami-cities.txt --out "raw_${preset}.csv" --tags "$preset" >>"$LOG" 2>&1

  # new domains not seen before
  new=0
  tail -n +2 "raw_${preset}.csv" | while IFS=, read -r name website domain email phone city niche; do
    [ -z "$domain" ] && continue
    grep -qxF "$domain" "$SEEN" && continue
    echo "$domain" >> "$SEEN"
    # scan the single domain for outdated score + email (reuse scan.sh logic inline via curl)
    row=$(bash scan.sh <(echo "$domain") "/tmp/scan_one.csv" >/dev/null 2>&1; tail -n +2 /tmp/scan_one.csv | head -1)
    score=$(echo "$row" | cut -d, -f1); shtml=$(echo "$row" | cut -d, -f3); mob=$(echo "$row" | cut -d, -f4)
    scemail=$(echo "$row" | cut -d, -f7); reason=$(echo "$row" | cut -d, -f9-)
    useemail="$email"; [ -z "$useemail" ] && useemail="$scemail"
    # keep if it has an email AND looks like a real target (old site OR any email)
    if [ -n "$useemail" ]; then
      printf '"%s",%s,%s,%s,%s,"%s",%s,%s,%s,%s,%s\n' \
        "$name" "$website" "$domain" "$useemail" "$phone" "$city" "$niche" "${score:-0}" "${shtml:-}" "${mob:-}" "$reason" >> "$MASTER"
    fi
  done

  total=$(( $(wc -l < "$MASTER") - 1 ))
  log "round $round done | master total leads (with email): $total"
  sleep 120
done
