import type { NextConfig } from "next";

// Client demo sites served from public/<slug>/.
//   Path access:      webblaze.io/<slug>/   (works on *.vercel.app immediately)
//   Subdomain access: <slug>.webblaze.io    (handled in src/proxy.ts)
const DEMOS = ["orangebeachfish", "dunebuggy", "sunfinance"] as const;

const nextConfig: NextConfig = {
  // Keep trailing slashes so demos served at /<slug>/ resolve their relative
  // asset paths (img/…) correctly. Without this Next strips the slash and
  // relative paths break to the root.
  trailingSlash: true,
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
