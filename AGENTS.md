<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Homepage is a STATIC file, not a Next route (build-safe since 2026-11-08)

The apex homepage (webblaze.io) is `public/index.html` — a self-contained static page
(sharp-editorial design Zayden approved). It is intentionally NOT a Next app route:
there is no `src/app/page.tsx`. `next build` copies `public/index.html` verbatim to
`out/index.html` (zero React/layout/globals.css interference), so the normal
"build → copy out/ → docs/ → push" deploy reproduces the real homepage and can never
clobber it back to an old React page.

TO EDIT THE HOMEPAGE: edit `public/index.html` (keep `docs/new/index.html` in sync as the
staging mirror). Do NOT recreate `src/app/page.tsx` — a `/` route would override the static
file and reintroduce the clobber bug. `/privacy` and `/terms` remain normal Next routes.
