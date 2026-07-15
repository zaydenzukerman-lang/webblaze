import type { NextConfig } from "next";

// Client demo sites served from public/<slug>/.
//   Path access:      webblaze.io/<slug>/   (works on *.vercel.app immediately)
//   Subdomain access: <slug>.webblaze.io    (handled in src/proxy.ts)
const DEMOS = ["orangebeachfish", "dunebuggy"] as const;

const nextConfig: NextConfig = {
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
