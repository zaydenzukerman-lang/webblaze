# Curb — Fulfillment Runbooks

What we actually DO after they pay. Claude executes the build/content steps; Zayden executes
anything requiring account logins, phone calls, or client contact.

## BUILD STANDARD (mandatory, added 2026-07-15) — run ui-ux-pro-max on EVERY site
Before writing/cloning any client site, invoke the `ui-ux-pro-max` skill and run its
`--design-system` search for the client's industry to lock: pattern, color palette, font pairing,
and the anti-patterns to avoid. Websites ARE our product — never ship a raw-template build again.
Non-negotiables it enforces that we kept skipping: (a) contact info PROMINENT (phone in nav+hero;
"hidden contact info" is a flagged anti-pattern), (b) SVG icons, never emoji, (c) social proof
before the CTA, (d) one primary CTA per screen, (e) AA contrast + focus states + reduced-motion +
44px targets + real form labels. Our own rule still overrides: NO fabricated reviews on a live
client site — use real facts (years in business, family-owned) as social proof until we have their
real Google/FB reviews. Skill lives at ~/.claude/skills/ui-ux-pro-max/. First use: Orange Beach
Fish Charter rebuild (clients/orangebeachfish/).

## Website (any package) — target: live in 3–5 days
1. Onboarding checklist complete (see CLIENT-ONBOARDING.md) — don't start without photos + phone + service list
2. Run ui-ux-pro-max --design-system for the industry (see BUILD STANDARD above)
3. Clone TidalWave template → swap brand, colors, towns, services, prices, photos
3. Wire quote form → client email (Web3Forms access key)
4. tel:/sms: buttons → client number (Growth+: CallRail tracked number instead)
5. Reviews section ← their real Google reviews
6. Deploy → connect client domain (registered in THEIR name) → HTTPS
7. QA on a phone: every button, form test-submit, load speed
8. Send client the link + ask them to test the form themselves

## Lead Gen Launch — Month 1 (all tiers)
**Week 1 — Foundations**
- GBP: get Manager access → rewrite description (keyword-rich), fix categories, add ALL services
  + service areas, upload 15+ photos, add Q&A
- Review system: their GBP review link → QR card + copy-paste SMS templates → teach owner:
  "send after EVERY job"
- On-page SEO on site: titles, meta, schema, per-service headings
**Week 2 — Pipes (Growth & up)**
- CallRail: tracked number → site + GBP; call recording on; whisper tag "call from your website"
- LSA: owner starts Google screening (licenses/insurance docs) — DAY 1 of week 2 at the latest
- Distribb: NAP citation submissions kicked off
**Weeks 3–4 — Rhythm**
- 4 GBP posts scheduled (1/week: job spotlight, seasonal tip, offer, review highlight)
- Reply to all new reviews
- Full Funnel: Meta campaign live (before/after creative + lead form) + 1 landing page per campaign

## Monthly cycle (every client, months 2+)
- Weekly: 1 GBP post, review replies, monitor calls (flag missed calls to owner SAME DAY)
- Monthly by the 5th: report — tracked calls + sources, review growth, GBP views/actions,
  next month's plan. Growth+: call recap ("14 calls, 9 answered, ~5 booked — answer rate is
  costing you ~$X").
- Month 3 (end of launch): results review → roll to month-to-month. This conversation decides
  retention — lead with the call numbers.

## Tool accounts needed (first client triggers signup)
| Tool | Cost | When |
|---|---|---|
| Web3Forms | free | first site |
| CallRail | ~$45/mo | first Growth client |
| Distribb | per their pricing | first Growth client |
| GoHighLevel (optional, replaces several) | ~$97/mo | when 2+ retainer clients |
| Meta Business Manager | free (ad spend client's) | first Full Funnel client |

## Rules
- Never promise rankings. Report honestly, even bad months.
- Missed-call flag = same-day text to owner. Speed-to-lead is the #1 thing owners feel.
- Every report ends with "what we're doing next month" — momentum kills churn.
