#!/bin/bash
# curb-chrome — launches YOUR real Chrome (real profile, real logins) with a local
# debug port so Claude can drive it for Facebook assisted-sending.
# Usage: bash ~/bookedsolid/ops/curb-chrome.sh   (or set up an alias)
# NOTE: Chrome must be fully closed first — this script handles that check.

if pgrep -x "Google Chrome" > /dev/null; then
  echo "⚠️  Chrome is already running. Quit Chrome completely (Cmd+Q) and run this again."
  echo "   (The debug port only attaches when Chrome starts fresh.)"
  exit 1
fi

echo "Launching Chrome with assisted-sending enabled (port 9222, your normal profile)..."
open -na "Google Chrome" --args --remote-debugging-port=9222

echo "✅ Chrome is up. Tell Claude 'chrome is ready' and it can start the day's sends."
echo "   To go back to normal: just quit Chrome and reopen it like usual."
