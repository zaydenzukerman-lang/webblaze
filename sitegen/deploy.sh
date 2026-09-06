#!/usr/bin/env bash
# Deploy all client sites live to webblaze.io/<slug>/  (GitHub Pages).
# Usage: bash deploy.sh "commit message"
set -e
cd ~/webblaze
npm run build >/tmp/wb_build.log 2>&1 && rm -rf docs && cp -R out docs \
  && touch docs/.nojekyll && printf 'webblaze.io' > docs/CNAME \
  && git add -A && git commit -q -m "${1:-deploy client sites}" \
  && git pull --rebase -q origin main && git push -q origin main && echo "DEPLOYED"
