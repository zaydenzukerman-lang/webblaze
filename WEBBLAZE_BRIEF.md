# WebBlaze — Brand + Build Brief

> For Zayden's Claude Code. Everything you need to build and publish webblaze.io.
> Prepared by Concierge (Forest's agent), 2026-07-15.

---

## 1. What this is

**WebBlaze** is Zayden's web development company. The brand name was chosen by Forest.
The website you're building lives at **webblaze.io**.

**Domain facts (already handled — don't re-buy):**
- `webblaze.io` is REGISTERED and owned (Forest Zukerman / Proactium.ai)
- Registrar: **Namecheap** — Order #207922026, DomainID 104502906, registered 1yr w/ WhoisGuard
- Current DNS: Namecheap BasicDNS (`dns1.registrar-servers.com` / `dns2.registrar-servers.com`)
- Right now it points at a **Namecheap parking page** — that's expected. It gets pointed at Vercel once the site is ready to ship.
- `webblaze.ai` is still available (~$70) if you ever want it. `webblaze.com` is taken.

---

## 2. The logos

Four variations are on this machine at **`~/webblaze/branding/`**. All were generated with
Gemini's image model (nano banana). All are 1024x1024 PNG on white.

| File | Direction | Best for |
|---|---|---|
| `01_flame_wordmark.png` | Flame glyph + "WebBlaze" wordmark, horizontal lockup | **Primary logo** — site header, docs |
| `02_W_monogram_flame.png` | Bold "W" whose right stroke becomes a flame | **App icon / favicon** — works square |
| `03_speed_blaze_trail.png` | Blaze/speed trail treatment | Motion, hero backgrounds |
| `04_ember_minimal.png` | Minimal ember + light wordmark | Footer, dark mode, understated use |

**Forest hasn't picked a winner yet.** Don't assume — if you need one for the build, use
`01_flame_wordmark.png` as the header logo and `02_W_monogram_flame.png` as the favicon,
and flag to Forest that it's a placeholder pick.

### Color system (read off the actual logo files)

```
Flame red        #D32F2F   (top of flame gradient)
Flame orange     #F4511E   (mid)
Ember orange     #FF7A18   (bright tip / accent)
Deep burnt       #C1440E   (W monogram base, shadow side)
Slate wordmark   #3E4A54   (the "WebBlaze" text — NOT pure black)
Off-white bg     #FFFFFF
Ink / body text  #1C2126
```

The signature move is the **vertical gradient red → orange, bottom-lit** (fire reads hottest
at the base). Keep that direction consistent everywhere — don't flip it.

---

## 3. How to recreate / modify the logos (nano banana)

The **`nano-banana`** plugin is already enabled in your Claude Code (`nano-banana-2-skill-marketplace`).
You can regenerate or restyle any of these yourself. You'll need a `GEMINI_API_KEY` —
if the skill errors on a missing key, ask Forest for it (Concierge has it in the fleet `.env`).

The four logos were generated from prompts along these lines — reuse and tweak:

**01 — Flame + wordmark (primary lockup)**
```
Minimal flat vector logo for a web development company called "WebBlaze".
A clean stylized flame glyph on the left, gradient from deep red (#D32F2F) at the
tip to bright orange (#F4511E) at the base, next to the wordmark "WebBlaze" in a
bold geometric sans-serif, slate gray (#3E4A54), single word, capital W and capital B.
Horizontal lockup, generous whitespace, pure white background, no shadows,
no 3D, no gloss. Corporate-clean, modern SaaS logo. Vector style.
```

**02 — W monogram (app icon)**
```
Minimal flat vector monogram app icon: a bold geometric capital letter "W" where the
final stroke transforms into a stylized flame. Warm gradient from burnt orange
(#C1440E) to bright orange (#FF7A18). White background, centered, square composition,
no text, no shadows. Modern tech app icon, vector style.
```

**03 — Speed blaze trail**
```
Minimal flat vector logo mark: a stylized flame with horizontal speed/motion trails
streaking behind it, suggesting velocity and fast websites. Red-to-orange gradient,
white background, no text, clean vector, no 3D.
```

**04 — Ember minimal**
```
Ultra-minimal logo: a small simple ember/flame dot mark beside the wordmark "WebBlaze"
in a light-weight modern sans-serif, thin letterforms, slate gray. Lots of negative
space, white background, understated and premium. Vector style.
```

### Rules when you regenerate
- **Always ask for "flat vector, white background, no 3D, no gloss, no shadows"** — otherwise Gemini gives you a glossy 3D blob that won't work as a logo.
- **Text in AI images garbles.** If the wordmark comes out misspelled, don't fight it — generate the *mark only* and set "WebBlaze" in real type (CSS/SVG) in the site. That's what a real designer would do anyway, and it stays crisp at every size.
- Generate at **2K** and eyeball it before you use it.
- For a favicon you need a real square export — take `02`, trim the whitespace, export 512/192/32.

---

## 4. Publishing to Vercel

The **`vercel`** plugin is enabled in your Claude Code and the **Vercel CLI is installed**
(`/opt/homebrew/bin/vercel`, `node` v25.9.0 at `/opt/homebrew/bin/node`).

**Status: AUTHENTICATED** ✅ (`vercel whoami` → `forest-9003`). You can deploy.

Publishing:
```bash
cd ~/webblaze
vercel            # preview deploy
vercel --prod     # production deploy
```

### ⚠️ READ THIS BEFORE YOU RUN ANY vercel COMMAND

The CLI on this machine is authenticated with **Forest's personal Vercel token**. That token is
**account-wide** — it can see and delete **all 25 of Forest's projects**, including live production
businesses: `courtcounsel-app`, `hqintake-portal`, `legalleadzai-website`, `proactium`, and others.
Your Claude Code runs with `bypassPermissions`, which means **nothing will stop you** from wrecking
them by accident. There is no undo and no confirmation prompt.

**Hard rules:**
1. **Only ever operate on the `webblaze` project.** Always `cd ~/webblaze` first.
2. **NEVER run** `vercel remove`, `vercel rm`, `vercel project rm`, or any delete/destructive command
   against *any* project — not even webblaze. If something needs deleting, ask Forest.
3. **NEVER run** `vercel ls` / `vercel projects ls` and then act on what you find. Other projects
   are not yours. Don't touch them, don't "clean them up," don't "fix" them.
4. **NEVER** change environment variables, domains, or settings on a project that isn't webblaze.
5. If a `vercel` command errors in a way that tempts you to run something broader or more forceful
   — **stop and ask Forest.** A confused deploy is fine. A deleted production app is not.

If you follow rule 1, you cannot cause a problem. Stay in your lane.

Then the domain gets attached (`vercel domains add webblaze.io`) and Namecheap DNS gets
pointed at Vercel:
```
A     @     76.76.21.21
CNAME www   cname.vercel-dns.com
```
**Concierge will do the Namecheap DNS change** — it's Forest's registrar account, not yours.
Just tell Forest when the site is ready to go live.

---

## 5. Suggested stack (not mandatory)

Nothing's committed yet, so it's your call. Sensible default for this:
**Next.js + Tailwind, deployed on Vercel** — zero-config deploys, and the `vercel` +
`modern-web-design` plugins you have are built around that flow.

Build it in **`~/webblaze/`** (already created, logos are in `~/webblaze/branding/`).

---

## 6. Who to ask

- **Forest** — brand decisions, which logo wins, what the site should say, going live
- **Concierge** (Forest's agent) — domain/DNS, Vercel account access, the GEMINI_API_KEY, anything account-level

Don't touch anything outside `~/webblaze` and your own home directory.
