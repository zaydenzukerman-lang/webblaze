import type { NextConfig } from "next";

// Static export → hosted on GitHub Pages (custom domain webblaze.io).
// Deploy = build to /docs, git push. No Vercel token / login needed.
//
// Client demo sites live in public/<slug>/ and are copied into the export as-is.
// GitHub Pages natively serves /<slug>/ -> /<slug>/index.html (directory index),
// so path-based demo access (webblaze.io/<slug>/) keeps working.
// The <slug>.webblaze.io subdomains and the live client .com domains stay on the
// existing Vercel deployment (src/proxy.ts middleware) — separate DNS records,
// untouched by moving this apex homepage to Pages.
const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: false,
  images: { unoptimized: true },
};

export default nextConfig;
