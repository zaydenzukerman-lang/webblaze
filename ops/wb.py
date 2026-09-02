#!/usr/bin/env python3
"""WebBlaze ops CLI — the control panel for the whole operation.
Every agent plugs in here. Usage:
  wb.py add <intake.json>        # Jarvis: onboard a new client
  wb.py build <slug>             # Andre: generate the site from intake
  wb.py deploy <slug>            # Andre: push live to <slug>.webblaze.io
  wb.py list [status]            # dashboard: all clients (+ recurring revenue)
  wb.py status <slug>            # one client's full record
  wb.py set <slug> <field> <val> # update any field (e.g. set x status live)
  wb.py change <slug> <request>  # Emma: log a client change request
  wb.py changes                  # Emma: list open change requests
  wb.py board                    # pipeline view (counts per stage) + recent activity
"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import db

ANDRE = os.path.expanduser("~/webblaze/andre")

def cmd_add(intake_path):
    c = json.load(open(os.path.expanduser(intake_path)))
    os.makedirs(os.path.join(ANDRE, "clients"), exist_ok=True)
    dest = os.path.join(ANDRE, "clients", c["slug"] + ".json")
    json.dump(c, open(dest, "w"), indent=2)
    db.add_client({
        "slug": c["slug"], "business": c.get("name", ""), "contact_name": c.get("contact_name", ""),
        "email": c.get("email", ""), "phone": c.get("phone", ""), "city": c.get("city", ""),
        "brand_color": c.get("brand", ""), "intake_path": dest,
        "plan": c.get("plan", "website"), "mrr": float(c.get("mrr", 0) or 0),
        "status": "onboarding",
    })
    print(f"[Jarvis] onboarded {c['slug']} — {c.get('name','')}")

def cmd_build(slug):
    c = db.get(slug)
    if not c: return print("no such client:", slug)
    subprocess.run(["python3", os.path.join(ANDRE, "generate.py"), c["intake_path"]], check=True)
    site_dir = os.path.join(ANDRE, "output", slug)
    db.update(slug, actor="andre", site_dir=site_dir, live_url=f"https://{slug}.webblaze.io", status="built")
    print(f"[Andre] built {slug} -> {site_dir}")

def cmd_deploy(slug):
    c = db.get(slug)
    if not c or not c.get("site_dir"): return print("build it first:", slug)
    # Deploy hook: wire to the Vercel/webblaze.io pipeline. Placeholder marks it live.
    db.update(slug, actor="andre", status="live")
    print(f"[Andre] deployed {slug} -> {c['live_url']}  (wire real deploy in cmd_deploy)")

def cmd_list(status=None):
    rows = db.list_clients(status)
    print(f"{'SLUG':<18}{'BUSINESS':<26}{'PLAN':<9}{'STATUS':<13}{'MRR':>7}")
    print("-" * 73)
    for r in rows:
        print(f"{r['slug']:<18}{(r['business'] or '')[:24]:<26}{r['plan']:<9}{r['status']:<13}{r['mrr']:>6.0f}")
    mrr = sum(r["mrr"] for r in rows)
    print("-" * 73)
    print(f"{len(rows)} clients  |  ${mrr:,.0f}/mo recurring  |  ${mrr*12:,.0f}/yr")

def cmd_status(slug):
    c = db.get(slug)
    print(json.dumps(c, indent=2) if c else "no such client")

def cmd_set(slug, field, *value):
    db.update(slug, **{field: " ".join(value)})
    print(f"set {slug}.{field} = {' '.join(value)}")

def cmd_change(slug, *req):
    db.add_change(slug, " ".join(req))
    print(f"[Emma] change logged for {slug}")

def cmd_changes():
    ch = db.open_changes()
    if not ch: return print("no open change requests")
    for r in ch:
        print(f"#{r['id']:<4}{r['slug']:<18}{r['ts']:<18}{r['request']}")

def cmd_board():
    rows = db.list_clients()
    stages = ["lead","contacted","interested","onboarding","building","built","live","maps-active","paused","lost"]
    counts = {s: 0 for s in stages}
    for r in rows: counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("PIPELINE")
    for s in stages:
        if counts.get(s): print(f"  {s:<14}{'#'*counts[s]} {counts[s]}")
    mrr = sum(r["mrr"] for r in rows)
    live = sum(1 for r in rows if r["status"] in ("live","maps-active"))
    print(f"\n{len(rows)} total · {live} live · ${mrr:,.0f}/mo recurring")
    print("\nRECENT ACTIVITY")
    for e in db.recent_log(8):
        print(f"  {e['ts']}  [{e['actor']}]  {e['slug']}: {e['event']}")

CMDS = {"add":cmd_add,"build":cmd_build,"deploy":cmd_deploy,"list":cmd_list,"status":cmd_status,
        "set":cmd_set,"change":cmd_change,"changes":cmd_changes,"board":cmd_board}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__); sys.exit(1)
    CMDS[sys.argv[1]](*sys.argv[2:])
