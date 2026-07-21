import { NextRequest, NextResponse } from "next/server";

// Client-demo subdomains: <slug>.webblaze.io → serve that demo's static
// files from public/<slug>/. All subdomain routing lives HERE (not in
// next.config rewrites) so the prefix is applied exactly once.
const DEMOS = ["orangebeachfish", "dunebuggy", "sunfinance", "sunmortgagefunding", "sunpremium"];

export function proxy(req: NextRequest) {
  const host = req.headers.get("host")?.split(":")[0] ?? "";
  const slug = DEMOS.find((d) => host === `${d}.webblaze.io`);
  if (!slug) return NextResponse.next();

  let path = req.nextUrl.pathname;
  if (path === "/") path = "/index.html";
  // Pretty URLs on multi-page demos: /menu -> /menu.html
  else if (/^\/[a-z-]+$/.test(path)) path = `${path}.html`;

  return NextResponse.rewrite(new URL(`/${slug}${path}`, req.url));
}

export const config = {
  // Everything except Next internals and static chunks
  matcher: ["/((?!_next/|api/).*)"],
};
