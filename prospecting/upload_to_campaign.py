import csv,io,json,os,time,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
KEY=open(os.path.expanduser("~/.instantly-key")).read().strip()
UA="Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
CAMP=open("/tmp/wb_campaign_id").read().strip()
rows=list(csv.DictReader(io.open("all_leads.csv",encoding="utf-8")))
ok=[0];fail=[0]
def add(r):
    body=json.dumps({"campaign":CAMP,"email":r["email"],"company_name":r.get("company",""),
        "website":("https://"+r["company"]) if r.get("company") else "",
        "custom_variables":{"niche":r.get("niche",""),"city":r.get("city","")}}).encode()
    req=urllib.request.Request("https://api.instantly.ai/api/v2/leads",data=body,method="POST",
        headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":UA})
    for a in range(4):
        try: urllib.request.urlopen(req,timeout=30).read(); ok[0]+=1; return
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(2*(a+1)); continue
            fail[0]+=1; return
        except Exception: time.sleep(1.5); continue
    fail[0]+=1
print("adding",len(rows),"leads to campaign",CAMP,flush=True)
with ThreadPoolExecutor(max_workers=6) as ex:
    for i,_ in enumerate(ex.map(add,rows),1):
        if i%1000==0: print("  %d/%d ok=%d fail=%d"%(i,len(rows),ok[0],fail[0]),flush=True)
print("DONE campaign ok=%d fail=%d"%(ok[0],fail[0]),flush=True)
