import { NextRequest, NextResponse } from "next/server";

// Client-demo subdomains: <slug>.webblaze.io → serve that demo's static
// files from public/<slug>/. All subdomain routing lives HERE (not in
// next.config rewrites) so the prefix is applied exactly once.
const DEMOS = ["orangebeachfish", "dunebuggy", "sunfinance", "sunmortgagefunding", "sunpremium", "fetchero", "thetownagency"];
// These slugs are static mirrors of the client's real WordPress sites: pages
// live in directories (/team/ -> team/index.html), not flat .html files.
const DIR_MIRRORS = ["sunfinance", "sunmortgagefunding", "sunpremium"];

export function proxy(req: NextRequest) {
  const host = req.headers.get("host")?.split(":")[0] ?? "";
  const slug = DEMOS.find((d) => host === `${d}.webblaze.io`);
  if (!slug) return NextResponse.next();

  let path = req.nextUrl.pathname;
  if (DIR_MIRRORS.includes(slug)) {
    // Directory-index behavior for WordPress-style mirrors.
    if (path === "/") path = "/index.html";
    else if (path.endsWith("/")) path = `${path}index.html`;
    else if (!/\.[a-z0-9]+$/i.test(path)) path = `${path}/index.html`; // extensionless -> dir index
    // else: real asset (has extension) -> pass through unchanged
  } else {
    if (path === "/") path = "/index.html";
    // Pretty URLs on multi-page demos: /menu -> /menu.html
    else if (/^\/[a-z-]+$/.test(path)) path = `${path}.html`;
  }

  return NextResponse.rewrite(new URL(`/${slug}${path}`, req.url));
}

export const config = {
  // Everything except Next internals and static chunks
  matcher: ["/((?!_next/|api/).*)"],
};
