import json, os, urllib.request, html
from datetime import datetime, timezone

USER = "ZRSaimun"
HEADERS = {"Accept":"application/vnd.github+json","User-Agent":"ZR-Live-Profile"}
token=os.getenv("GITHUB_TOKEN")
if token: HEADERS["Authorization"]=f"Bearer {token}"

def get(url):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.load(r)

repos=get(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated")
events=get(f"https://api.github.com/users/{USER}/events/public?per_page=30")
active=[r for r in repos if not r.get("fork")]
active.sort(key=lambda r:r.get("pushed_at") or "",reverse=True)
top=active[:4]
langs={}
for r in active[:12]:
    lang=r.get("language")
    if lang: langs[lang]=langs.get(lang,0)+1
langline=" • ".join(k.upper() for k,_ in sorted(langs.items(),key=lambda x:-x[1])[:5]) or "ENGINEERING"
now=datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
last=(events[0].get("type","GitHub event").replace("Event","") if events else "SYNC")
repo_count=len(active)

nodes=[]
xs=[170,420,700,970]
for i,r in enumerate(top):
    name=html.escape(r["name"][:22])
    nodes.append(f'''<g transform="translate({xs[i]} 170)">
      <circle r="29" fill="#071a24" stroke="#bfa66a" stroke-opacity=".55"/>
      <circle r="36" fill="none" stroke="#73b9c6" stroke-opacity=".18"><animate attributeName="r" values="31;43;31" dur="{4+i}s" repeatCount="indefinite"/></circle>
      <circle r="4" fill="#d8c38a"><animate attributeName="opacity" values=".35;1;.35" dur="{2.4+i*.3}s" repeatCount="indefinite"/></circle>
      <text y="58" text-anchor="middle" fill="#b8c8cc" font-size="11" font-family="Arial">{name}</text>
    </g>''')
links=''.join(f'<path d="M{xs[i]+30} 170 C{xs[i]+80} 130 {xs[i+1]-80} 210 {xs[i+1]-30} 170" fill="none" stroke="#73b9c6" stroke-opacity=".2" stroke-dasharray="5 8"><animate attributeName="stroke-dashoffset" values="26;0" dur="3s" repeatCount="indefinite"/></path>' for i in range(max(0,len(top)-1)))

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="285" viewBox="0 0 1200 285">
<defs><linearGradient id="b" x2="1" y2="1"><stop stop-color="#06121d"/><stop offset=".55" stop-color="#082331"/><stop offset="1" stop-color="#041019"/></linearGradient><linearGradient id="a"><stop stop-color="#806a40"/><stop offset=".5" stop-color="#d8c38a"/><stop offset="1" stop-color="#806a40"/></linearGradient></defs>
<rect width="1200" height="285" rx="22" fill="url(#b)"/>
<text x="62" y="52" fill="#eef5f6" font-family="Arial" font-size="19" font-weight="700" letter-spacing="4">AUTONOMOUS ENGINEERING SIGNAL</text>
<text x="62" y="78" fill="#8ea8ae" font-family="Arial" font-size="11" letter-spacing="2">LIVE GITHUB DATA • SCHEDULED SYSTEM • NO MANUAL COUNTERS</text>
<circle cx="1110" cy="54" r="5" fill="#8bc7a4"><animate attributeName="opacity" values=".3;1;.3" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="1094" y="58" text-anchor="end" fill="#9bb0b5" font-family="Arial" font-size="11">ONLINE</text>
{links}{''.join(nodes)}
<line x1="62" y1="235" x2="1138" y2="235" stroke="url(#a)" stroke-opacity=".35"/>
<text x="62" y="260" fill="#8ea8ae" font-family="Arial" font-size="11">ACTIVE REPOS  {repo_count:02d}</text>
<text x="300" y="260" fill="#8ea8ae" font-family="Arial" font-size="11">LAST SIGNAL  {html.escape(last.upper())}</text>
<text x="560" y="260" fill="#8ea8ae" font-family="Arial" font-size="11">{html.escape(langline)}</text>
<text x="1138" y="260" text-anchor="end" fill="#6f858a" font-family="Arial" font-size="10">SYNC {now}</text>
</svg>'''
os.makedirs("generated",exist_ok=True)
open("generated/live-engine.svg","w",encoding="utf-8").write(svg)
