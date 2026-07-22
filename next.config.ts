import type { NextConfig } from "next";

// Client demo sites served from public/<slug>/.
//   Path access:      webblaze.io/<slug>/   (works on *.vercel.app immediately)
//   Subdomain access: <slug>.webblaze.io    (handled in src/proxy.ts)
const DEMOS = ["orangebeachfish", "dunebuggy", "sunfinance", "sunmortgagefunding", "sunpremium"] as const;

const nextConfig: NextConfig = {
  // trailingSlash:false — pretty URLs (subdomain /apply, /about, …) must NOT
  // gain a trailing slash, or the pages' relative asset paths (img/…, styles.css)
  // resolve against /apply/ and 404. With it off, subdomain /apply stays /apply,
  // relative img/ -> /img/ and the proxy (src/proxy.ts) prefixes the slug. A
  // stray /apply/ self-heals via Next's redirect back to /apply. (Trade-off:
  // path-based apex access uses /<slug>/index.html or /<slug>/<page> — see proxy.)
  trailingSlash: false,
  async rewrites() {
    return {
      beforeFiles: [
        // Directory-index: /<slug> and /<slug>/ -> /<slug>/index.html
        ...DEMOS.map((slug) => ({
          source: `/${slug}`,
          destination: `/${slug}/index.html`,
        })),
        ...DEMOS.map((slug) => ({
          source: `/${slug}/`,
          destination: `/${slug}/index.html`,
        })),
      ],
      afterFiles: [
        // Pretty URLs inside demos: /<slug>/menu -> /<slug>/menu.html
        ...DEMOS.map((slug) => ({
          source: `/${slug}/:page([a-z-]+)`,
          destination: `/${slug}/:page.html`,
        })),
      ],
      fallback: [],
    };
  },
};

export default nextConfig;
