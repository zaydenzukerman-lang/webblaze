import { NextRequest, NextResponse } from "next/server";

// Client-demo subdomains: <slug>.webblaze.io → serve public/<slug>/ files.
const DEMOS = ["orangebeachfish", "dunebuggy", "sunfinance", "sunmortgagefunding", "sunpremium", "fetchero", "thetownagency"];
// WordPress-style static mirrors: pages live in directories (/team/ -> team/index.html).
const DIR_MIRRORS = ["sunfinance", "sunmortgagefunding", "sunpremium"];

// Real client domains we now HOST (Namecheap origin down). Point their DNS at
// Vercel and each maps to its static mirror.
const REAL_DOMAINS: Record<string, string> = {
  "sunfinance.com": "sunfinance",
  "www.sunfinance.com": "sunfinance",
  "sunpremium.com": "sunpremium",
  "www.sunpremium.com": "sunpremium",
  "sunmortgagefunding.com": "sunmortgagefunding",
  "www.sunmortgagefunding.com": "sunmortgagefunding",
};

export function proxy(req: NextRequest) {
  const host = req.headers.get("host")?.split(":")[0] ?? "";
  const slug = DEMOS.find((d) => host === `${d}.webblaze.io`) ?? REAL_DOMAINS[host];
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
    else if (/^\/[a-z-]+$/.test(path)) path = `${path}.html`;
  }

  const res = NextResponse.rewrite(new URL(`/${slug}${path}`, req.url));
  // Only the real client domains should be indexed; keep our webblaze.io
  // staging subdomains out of Google to avoid duplicate content.
  if (host.endsWith(".webblaze.io")) res.headers.set("X-Robots-Tag", "noindex");
  return res;
}

export const config = {
  matcher: ["/((?!_next/|api/).*)"],
};
