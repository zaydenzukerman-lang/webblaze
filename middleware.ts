import type { NextRequest } from "next/server";
import { proxy } from "./src/proxy";

// Host-based routing for client-demo subdomains AND the real client domains we
// now host. All logic lives in src/proxy.ts.
export function middleware(req: NextRequest) {
  return proxy(req);
}

export const config = {
  // everything except Next internals, api routes, and files with an extension
  matcher: ["/((?!_next/|api/).*)"],
};
