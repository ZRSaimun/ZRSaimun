import json, os, urllib.request, html, re
from datetime import datetime, timezone

USER="ZRSaimun"
HEADERS={"Accept":"application/vnd.github+json","User-Agent":"ZR-Research-Constellation"}
token=os.getenv("GITHUB_TOKEN")
if token: HEADERS["Authorization"]=f"Bearer {token}"

def get(url):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=20) as r: return json.load(r)

repos=[r for r in get(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated") if not r.get("fork")]
repos.sort(key=lambda r:r.get("pushed_at") or "",reverse=True)

domains=[
 ("CYBERSECURITY",("security","cyber","forensic","network","pentest","secure")),
 ("AI / ML",("ai","machine","learning","model","neural","cnn","vision","dataset","classification")),
 ("COMPUTER VISION",("vision","image","cnn","camera","detection","classification")),
 ("OCEAN INTELLIGENCE",("ocean","underwater","aqua","marine","fish","coral","aquatic")),
 ("SOFTWARE ENGINEERING",("app","api","web","portfolio","system","software","java","python","react","vue"))
]
scores={d:0 for d,_ in domains}
evidence={d:[] for d,_ in domains}
for r in repos:
    blob=" ".join([r.get("name") or "",r.get("description") or "",r.get("language") or ""]).lower()
    for d,keys in domains:
        s=sum(1 for k in keys if k in blob)
        if s:
            scores[d]+=s
            if len(evidence[d])<2: evidence[d].append(r["name"])

# Software is a broad baseline only when public repo metadata supports it.
positions=[(600,138),(310,225),(455,345),(745,345),(890,225)]
maxscore=max(max(scores.values()),1)
now=datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")

links=[]
for i in range(len(positions)):
    x,y=positions[i]
    if i: links.append(f'<path d="M600 188 Q600 250 {x} {y}" fill="none" stroke="#75b9c5" stroke-opacity=".18" stroke-dasharray="5 9"><animate attributeName="stroke-dashoffset" values="28;0" dur="{3+i*.4}s" repeatCount="indefinite"/></path>')

nodes=[]
for i,(domain,_) in enumerate(domains):
    x,y=positions[i]; score=scores[domain]; strength=.35+.65*(score/maxscore)
    ev=" • ".join(evidence[domain]) if evidence[domain] else "metadata signal pending"
    ev=html.escape(ev[:44])
    nodes.append(f'''<g transform="translate({x} {y})">
    <circle r="42" fill="#071923" stroke="#bda36a" stroke-opacity="{strength:.2f}"/>
    <circle r="50" fill="none" stroke="#6fb7c4" stroke-opacity=".14"><animate attributeName="r" values="45;55;45" dur="{4+i*.7}s" repeatCount="indefinite"/></circle>
    <circle r="5" fill="#d6c18b"><animate attributeName="opacity" values=".35;1;.35" dur="{2.2+i*.2}s" repeatCount="indefinite"/></circle>
    <text y="72" text-anchor="middle" fill="#d9e5e7" font-family="Arial" font-size="12" font-weight="700">{domain}</text>
    <text y="90" text-anchor="middle" fill="#718c92" font-family="Arial" font-size="9">{ev}</text>
    </g>''')

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="470" viewBox="0 0 1200 470">
<defs><radialGradient id="bg"><stop stop-color="#0a2a37"/><stop offset=".58" stop-color="#061a25"/><stop offset="1" stop-color="#030e16"/></radialGradient><radialGradient id="core"><stop stop-color="#d8c38a" stop-opacity=".32"/><stop offset="1" stop-color="#d8c38a" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="470" rx="24" fill="url(#bg)"/>
<text x="58" y="50" fill="#eef6f7" font-family="Arial" font-size="19" font-weight="700" letter-spacing="4">RESEARCH CONSTELLATION</text>
<text x="58" y="76" fill="#829da3" font-family="Arial" font-size="11" letter-spacing="2">AUTOMATIC DOMAIN SIGNALS FROM PUBLIC REPOSITORY METADATA</text>
<g transform="translate(600 138)"><circle r="82" fill="url(#core)"><animate attributeName="r" values="72;88;72" dur="5s" repeatCount="indefinite"/></circle><circle r="48" fill="#081b25" stroke="#d5bf86" stroke-opacity=".7"/><circle r="7" fill="#e0cb94"><animate attributeName="opacity" values=".4;1;.4" dur="1.8s" repeatCount="indefinite"/></circle><text y="5" text-anchor="middle" fill="#edf5f6" font-family="Arial" font-size="10" letter-spacing="2">RESEARCH CORE</text></g>
{''.join(links)}
{''.join(nodes)}
<line x1="58" y1="424" x2="1142" y2="424" stroke="#bda36a" stroke-opacity=".24"/>
<text x="58" y="448" fill="#718c92" font-family="Arial" font-size="10">SIGNAL STRENGTH IS DERIVED FROM REPOSITORY NAMES, DESCRIPTIONS &amp; LANGUAGES</text>
<text x="1142" y="448" text-anchor="end" fill="#61787e" font-family="Arial" font-size="10">SYNC {now}</text>
</svg>'''
os.makedirs("generated",exist_ok=True)
open("generated/research-constellation.svg","w",encoding="utf-8").write(svg)
