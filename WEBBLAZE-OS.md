# WebBlaze OS — the agent-run operation (scaling plan)

Goal: one 13-year-old (Zayden) runs thousands of clients by turning every repeatable task into a
**specialized agent + a playbook**. Zayden = orchestrator + the human face the brand sells.
Model: dad runs 15–20 Claude Code agents; this is that applied to WebBlaze.

## The backbone: ONE client database (build this first)
Every agent reads/writes a single source of truth. Start simple (SQLite/Supabase — Supabase MCP
already available). One row per client:
`id · business · contact name · email · phone · plan(website/maps/both) · site_repo_path ·
live_url · domain · GBP_id · review_link · status · change_queue · report_cadence ·
billing_status · notes`
Without this, agents can't coordinate. With it, every agent knows exactly what to do for whom.

## The agent org chart (each = role + tools + a skill/playbook)
1. **Prospector** (lead-gen) — scheduled daily. Source leads → `scan.sh` → verify → push to
   Instantly via API. TOOLS: scan.sh, Instantly API, verification. STATUS: pipeline built.
2. **Closer** (sales/replies) — watches Instantly unibox/replies → classifies (interested / no /
   question) → drafts or sends replies → on "interested," tells Builder to make a free preview.
   Human-approval gate optional. TOOLS: Instantly API, email. → *this is the "email replies" agent.*
3. **Builder** (fulfillment) — intake info → generate site from a TEMPLATE → deploy to
   `<slug>.webblaze.io` → update DB. Turns days-per-site into minutes. TOOLS: templates, generator,
   Vercel deploy. STATUS: build next.
4. **Editor** (changes/support) — client change request → edit the site's files → redeploy →
   confirm. This is how "unlimited changes" scales: each change is a small, well-defined edit an
   agent does in seconds. Handles the "1000 changes a day" fear. TOOLS: repo edit, deploy pipeline.
5. **Maps Manager** (local SEO) — per Maps client, runs the monthly checklist: weekly GBP posts,
   review-request nudges, citations, monthly ranking report. Light to fulfill = scales well.
   TOOLS: GBP, report generator, LOCAL-SEO-PLAYBOOK.md.
6. **Reporter** — scheduled Mondays. For EVERY client, pull analytics (`ga_full.py`) + Maps rank →
   generate report (existing templates) → deliver. Runs in PARALLEL (workflow fan-out) so 200
   reports take about the same time as 1. STATUS: engine built (Sun).
7. **Concierge** (onboarding/billing) — new sale → intake form, invoice (FreshBooks), set up site +
   GBP access, welcome email. TOOLS: FreshBooks, email.
8. **You (Zayden)** = orchestrator + relationships + approvals + the "teenager" the brand sells. An
   orchestrator surfaces only what needs a human; everything else runs.

## Triggers
- **Cron:** Prospector daily · Reporter Mondays · Maps Manager weekly.
- **Event:** reply → Closer · change-request email → Editor · new sale → Concierge + Builder.
- **Approval gates:** anything with judgment (a tricky reply, a design call) → agent drafts, Zayden approves.

## Why this beats hiring people
Agents are cheap, parallel, 24/7, and never the bottleneck. The only things that stay human are
judgment, relationships, and the face. That's how one kid out-produces an agency.

## Build order (DON'T build the whole factory at 0 clients)
- **Phase 0 (now, 0 clients):** client DB skeleton · Prospector (done) · Builder (template+generator).
  These let you land AND deliver the first clients.
- **Phase 1 (first clients):** Closer (reply handling) · Concierge (onboarding/billing).
- **Phase 2 (10+ clients):** Reporter multi-client · Editor (changes) · Maps Manager.
- **Phase 3 (scale):** cron everything, human only on approvals + relationships. Add domains/inboxes
  + Hypergrowth as volume grows.

## What already exists (tools the agents will use)
scan.sh (Prospector) · ga_full.py + report templates (Reporter) · Vercel deploy (Builder/Editor) ·
BRAND.md · LOCAL-SEO-PLAYBOOK.md · cold-email templates + outreach console. The "tools" are here;
the "agents" are thin wrappers + the client DB + schedules.

## THE NAMED CREW (each name fits the role)
- **Blaidd** (Elden Ring, the hunter) = **Prospector** — hunts down leads.
- **Patches** (Dark Souls, the smooth-talking con-man/dealmaker) = **Closer** — works replies, closes sales.
- **Andre** (Dark Souls, the blacksmith) = **Builder** — forges the websites.
- **Emma** (Sekiro, the healer who mends you) = **Editor** — website changes / fixes / support.
- **Cornifer** (Hollow Knight, the cartographer who literally draws maps) = **Maps Manager** — gets customers to find you on Google Maps.
- **Peter** (Peter Parker, reporter/photographer for the Daily Bugle) = **Reporter** — weekly analytics + Maps reports.
- **Jarvis** (Iron Man's AI that runs Tony Stark's whole operation) = **Concierge / orchestrator** — onboarding, billing, coordinating the crew. **This is me.**
- **Zayden** = owner, approvals, relationships, the face.
