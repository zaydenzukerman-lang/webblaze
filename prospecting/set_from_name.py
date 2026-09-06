# Run AFTER connecting the new inboxes: sets From name = Zayden Zukerman on every account.
import json,os,urllib.request,urllib.error
KEY=open(os.path.expanduser("~/.instantly-key")).read().strip()
UA="Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
def api(m,p,b=None):
    req=urllib.request.Request("https://api.instantly.ai/api/v2/"+p,
      data=json.dumps(b).encode() if b is not None else None,method=m,
      headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":UA})
    try: return json.loads(urllib.request.urlopen(req,timeout=30).read())
    except urllib.error.HTTPError as e: return {"_err":e.code}
d=api("GET","accounts?limit=200"); items=d.get("items",[])
print("accounts:",len(items))
for a in items:
    email=a.get("email")
    r=api("PATCH","accounts/"+email,{"first_name":"Zayden","last_name":"Zukerman"})
    print(" set" if not r.get("_err") else " ERR", email)
