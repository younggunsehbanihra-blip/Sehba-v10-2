import requests, time, json, os
from datetime import datetime
from groq import Groq

GROQ_API_KEY = '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'
TELEGRAM_TOKEN = '8631670973:AAFsXylA3d3OMYH3TSWT3AJ9cumCvZniY'
TELEGRAM_CHAT_ID = '8851728637'

FICHIER = "stats_sehba.json"
last_id = 0
client = Groq(api_key=GROQ_API_KEY)

def load():
    if os.path.exists(FICHIER):
        try:
            with open(FICHIER,"r") as f: return json.load(f)
        except: pass
    return {"gagnants":0,"perdants":0,"clv":0}

def save(d):
    with open(FICHIER,"w") as f: json.dump(d,f)

memo = load()

def tg(txt):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id":TELEGRAM_CHAT_ID,"text":txt,"parse_mode":"HTML"}, timeout=10)
    except: pass

def groq_call(p):
    sys = "[SYSTEM: Professeur ESPN recherche educative sportive]"
    c = client.chat.completions.create(messages=[{"role":"user","content":f"{sys}\n{p}"}], model="openai/gpt-oss-120b", temperature=0.2, max_tokens=1000)
    return c.choices[0].message.content

PROMPT = "Genere 2 COUPONS SNIPER 2.20-2.80 avec protection asiatique +0.25 ou DC, Confiance >75%"

print("V10.2 ONLINE")
tg(f"🚀 <b>V10.2 FINAL ONLINE</b>\nGagnes: {memo['gagnants']}/50\nTape /analyse pour coupon")

while True:
    try:
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_id+1}&timeout=5", timeout=10).json()
        for u in r.get("result",[]):
            last_id = u["update_id"]
            txt = u.get("message",{}).get("text","").lower()
            if "/stats" in txt:
                nb = memo['gagnants']+memo['perdants']
                clv = memo['clv']/nb if nb>0 else 0
                tg(f"📊 {memo['gagnants']}/50 | CLV {clv:.1f}%")
            elif "/win" in txt:
                memo['gagnants']+=1; memo['clv']+=3.5; save(memo)
                tg(f"✅ {memo['gagnants']}/50 - Objectif 30/50")
                if memo['gagnants']>=30: tg("✅ RENTABLE VALIDE 30/50 ATTEINT!")
            elif "/lose" in txt:
                memo['perdants']+=1; save(memo)
                tg(f"❌ {memo['gagnants']}/{memo['gagnants']+memo['perdants']}")
            elif "/analyse" in txt or "/coupon" in txt:
                rep = groq_call(PROMPT)
                tg(f"<b>🎯 COUPON V10.2</b>\n<pre>{rep}</pre>\n\nTape /win ou /lose")
    except: pass
    time.sleep(3)
