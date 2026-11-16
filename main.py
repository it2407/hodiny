from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONES = [
    "Europe/Prague","Europe/Bratislava","Europe/Berlin","Europe/Vienna","Europe/Warsaw",
    "Europe/Budapest","Europe/Paris","Europe/Rome","Europe/Madrid","Europe/London",
    "Europe/Dublin","Europe/Lisbon","Europe/Amsterdam","Europe/Brussels","Europe/Zurich",
    "Europe/Stockholm","Europe/Oslo","Europe/Copenhagen","Europe/Helsinki","Europe/Athens",
    "Europe/Istanbul","Europe/Moscow","Europe/Kyiv",
    "America/New_York","America/Chicago","America/Denver","America/Los_Angeles",
    "America/Toronto","America/Vancouver","America/Mexico_City","America/Sao_Paulo",
    "America/Buenos_Aires","America/Santiago","America/Lima","America/Bogota",
    "Asia/Tokyo","Asia/Shanghai","Asia/Hong_Kong","Asia/Singapore","Asia/Seoul",
    "Asia/Bangkok","Asia/Jakarta","Asia/Manila","Asia/Kolkata","Asia/Dubai",
    "Asia/Tehran","Asia/Jerusalem","Asia/Riyadh",
    "Africa/Cairo","Africa/Johannesburg","Africa/Lagos","Africa/Nairobi","Africa/Casablanca",
    "Australia/Sydney","Australia/Melbourne","Australia/Perth","Australia/Brisbane",
    "Pacific/Auckland","Pacific/Fiji","Pacific/Honolulu","UTC",
]

def get_tz(name):
    if name in TIMEZONES:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    return ZoneInfo("Europe/Prague")

STYLES = ['orloj','modern','cuckoo','digital','neon']

def make_nav(active, tz):
    links = []
    for s in STYLES:
        cls = 'active' if s == active else ''
        labels = {'orloj':'Orloj','modern':'Moderni','cuckoo':'Kukacky','digital':'Digitalni','neon':'Neon'}
        links.append(f'<a href="/?style={s}&tz={tz}" class="{cls}">{labels[s]}</a>')
    opts = ''.join(f'<option value="{z}" {"selected" if z==tz else ""}>{z}</option>' for z in TIMEZONES)
    return (
        '<nav class="nav">' + ''.join(links) + '</nav>'
        '<form class="tzform" method="get">'
        f'<input type="hidden" name="style" value="{active}">'
        f'<select name="tz" onchange="this.form.submit()">{opts}</select>'
        '</form>'
    )

app = Flask(__name__)

# ---------------- ORLOJ ----------------
TPL_ORLOJ = r'''
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8"><title>Orloj</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;500&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0a0e1a;--bg2:#1a1f33;--gold:#d4af37;--gold2:#f5e6a3;--bronze:#8b6f3f;--text:#f5e6a3;--muted:#a89968;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;height:100%;}
body{font-family:'Inter',sans-serif;color:var(--text);background:radial-gradient(ellipse at 50% 0%,#1a2450 0%,transparent 60%),radial-gradient(ellipse at 50% 100%,#0d1224 0%,transparent 70%),linear-gradient(180deg,var(--bg1),var(--bg2));display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden;}
.stars{position:fixed;inset:0;z-index:0;pointer-events:none;}
.star{position:absolute;width:2px;height:2px;background:#fff;border-radius:50%;opacity:.7;animation:twinkle 3s ease-in-out infinite;}
@keyframes twinkle{0%,100%{opacity:.3}50%{opacity:1}}
.container{position:relative;z-index:1;text-align:center;padding:1rem;}
h1{font-family:'Cinzel',serif;font-weight:700;letter-spacing:6px;font-size:1.4rem;color:var(--gold);margin:0 0 1rem;text-shadow:0 0 12px rgba(212,175,55,.5);}
.nav{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-bottom:.8rem;}
.nav a{font-family:'Cinzel',serif;font-size:.8rem;letter-spacing:2px;color:var(--muted);text-decoration:none;padding:.4rem .8rem;border:1px solid rgba(212,175,55,.3);border-radius:20px;transition:.2s;}
.nav a:hover,.nav a.active{color:var(--gold);border-color:var(--gold);background:rgba(212,175,55,.1);}
.tzform{margin-bottom:1.2rem;}
.tzform select{font-family:'Cinzel',serif;font-size:.85rem;color:var(--gold);background:rgba(0,0,0,.4);border:1px solid rgba(212,175,55,.4);border-radius:8px;padding:.4rem .8rem;cursor:pointer;}
.orloj{position:relative;width:340px;height:340px;margin:0 auto;}
.orloj-glow{position:absolute;inset:-30px;border-radius:50%;background:radial-gradient(circle,rgba(212,175,55,.25),transparent 70%);filter:blur(20px);}
.face{position:relative;width:100%;height:100%;border-radius:50%;background:radial-gradient(circle at 50% 40%,#1c2340 0%,#0b0f1f 70%,#05070f 100%);border:6px solid var(--gold);box-shadow:0 0 0 3px var(--bronze),0 0 0 6px #2a2010,0 20px 60px rgba(0,0,0,.8),inset 0 0 40px rgba(0,0,0,.6);}
.zodiac{position:absolute;inset:24px;border-radius:50%;border:1px solid rgba(212,175,55,.3);}
.zodiac .sym{position:absolute;left:50%;top:50%;font-size:.9rem;color:var(--gold2);transform:translate(-50%,-50%) rotate(var(--a)) translateY(-125px) rotate(calc(-1*var(--a)));}
.roman{position:absolute;inset:8px;border-radius:50%;}
.roman .n{position:absolute;left:50%;top:50%;font-family:'Cinzel',serif;font-size:1rem;font-weight:700;color:var(--gold);transform:translate(-50%,-50%) rotate(var(--a)) translateY(-142px) rotate(calc(-1*var(--a)));text-shadow:0 0 6px rgba(212,175,55,.6);}
.tick{position:absolute;left:50%;top:14px;width:2px;height:10px;background:rgba(212,175,55,.4);transform-origin:center 156px;margin-left:-1px;}
.tick.major{height:16px;width:3px;background:var(--gold);margin-left:-1.5px;}
.hand{position:absolute;bottom:50%;left:50%;transform-origin:bottom center;border-radius:4px;}
.hour{width:7px;height:90px;background:linear-gradient(to top,var(--bronze),var(--gold2));margin-left:-3.5px;box-shadow:0 0 10px rgba(212,175,55,.6);z-index:3;}
.minute{width:5px;height:125px;background:linear-gradient(to top,var(--bronze),#fff);margin-left:-2.5px;box-shadow:0 0 10px rgba(255,255,255,.5);z-index:4;}
.second{width:2px;height:140px;background:#f87171;margin-left:-1px;box-shadow:0 0 8px #f87171;z-index:5;}
.sun-hand{width:3px;height:110px;background:linear-gradient(to top,#ff8c00,#ffd700);margin-left:-1.5px;z-index:2;opacity:.85;}
.center-cap{position:absolute;top:50%;left:50%;width:18px;height:18px;background:radial-gradient(circle,var(--gold2),var(--bronze));border-radius:50%;transform:translate(-50%,-50%);z-index:6;box-shadow:0 0 12px var(--gold);border:2px solid #2a2010;}
.pendulum-wrap{position:relative;width:340px;height:150px;margin:1.2rem auto 0;}
.pendulum-pivot{position:absolute;top:0;left:50%;width:14px;height:14px;background:var(--gold);border-radius:50%;transform:translateX(-50%);box-shadow:0 0 10px var(--gold);z-index:2;}
.pendulum-rod{position:absolute;top:7px;left:50%;width:3px;height:115px;background:linear-gradient(to bottom,var(--gold),var(--bronze));transform-origin:top center;margin-left:-1.5px;animation:swing 2s ease-in-out infinite;}
.pendulum-bob{position:absolute;bottom:-18px;left:50%;width:34px;height:34px;background:radial-gradient(circle at 30% 30%,var(--gold2),var(--bronze));border-radius:50%;transform:translateX(-50%);box-shadow:0 6px 18px rgba(0,0,0,.6),inset -3px -3px 6px rgba(0,0,0,.4);border:2px solid var(--gold);}
@keyframes swing{0%{transform:rotate(-18deg)}50%{transform:rotate(18deg)}100%{transform:rotate(-18deg)}}
.digital{margin-top:1.2rem;font-family:'Cinzel',serif;font-size:1.5rem;color:var(--gold2);letter-spacing:3px;text-shadow:0 0 12px rgba(212,175,55,.4);}
.sub{margin-top:.3rem;color:var(--muted);font-size:.8rem;letter-spacing:2px;}
</style>
</head>
<body>
<div class="stars" id="stars"></div>
<div class="container">
  <h1>Orloj</h1>
  NAV_PLACEHOLDER
  <div class="orloj">
    <div class="orloj-glow"></div>
    <div class="face">
      <div class="zodiac">
        {% set zodiacs = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'] %}
        {% for z in zodiacs %}<div class="sym" style="--a: {{ loop.index0*30 }}deg;">{{ z }}</div>{% endfor %}
      </div>
      <div class="roman">
        {% set romans = ['XII','I','II','III','IV','V','VI','VII','VIII','IX','X','XI'] %}
        {% for r in romans %}<div class="n" style="--a: {{ loop.index0*30 }}deg;">{{ r }}</div>{% endfor %}
      </div>
      {% for i in range(60) %}<div class="tick {% if i % 5 == 0 %}major{% endif %}" style="transform: rotate({{ i*6 }}deg);"></div>{% endfor %}
      <div class="hand sun-hand" id="sun"></div>
      <div class="hand hour" id="hour"></div>
      <div class="hand minute" id="minute"></div>
      <div class="hand second" id="second"></div>
      <div class="center-cap"></div>
    </div>
  </div>
  <div class="pendulum-wrap">
    <div class="pendulum-pivot"></div>
    <div class="pendulum-rod"><div class="pendulum-bob"></div></div>
  </div>
  <div class="digital" id="digital">{{ server_time }}</div>
  <div class="sub">{{ tz }}</div>
</div>
<script>
const TZ = {{ tz|tojson }};
const starsEl=document.getElementById('stars');
for(let i=0;i<80;i++){const s=document.createElement('div');s.className='star';s.style.left=Math.random()*100+'%';s.style.top=Math.random()*100+'%';s.style.animationDelay=(Math.random()*3)+'s';starsEl.appendChild(s);}
let serverNow=new Date("{{ server_time_iso }}");
async function sync(){try{const r=await fetch('/api/time?tz='+encodeURIComponent(TZ));const d=await r.json();serverNow=new Date(d.iso);}catch(e){}}
function hms(t){const fmt=new Intl.DateTimeFormat('en-GB',{timeZone:TZ,hour:'numeric',minute:'numeric',second:'numeric',hour12:false});const parts=fmt.formatToParts(t);let h=0,m=0,s=0;for(const p of parts){if(p.type==='hour')h=+p.value;if(p.type==='minute')m=+p.value;if(p.type==='second')s=+p.value;}return {h,m,s};}
function render(t){const {h,m,s}=hms(t);
document.getElementById('hour').style.transform='rotate('+(h%12*30+m*0.5)+'deg)';
document.getElementById('minute').style.transform='rotate('+(m*6+s*0.1)+'deg)';
document.getElementById('second').style.transform='rotate('+(s*6)+'deg)';
document.getElementById('sun').style.transform='rotate('+(h%12*30+m*0.5+180)+'deg)';
document.getElementById('digital').textContent=t.toLocaleString('cs-CZ',{timeZone:TZ});}
setInterval(sync,1000);
setInterval(()=>{serverNow=new Date(serverNow.getTime()+1000);render(serverNow);},1000);
sync().then(()=>render(serverNow));
</script>
</body></html>
'''

# ---------------- MODERN ----------------
TPL_MODERN = r'''
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8"><title>Moderni hodiny</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<style>
:root{--bg1:#0f172a;--bg2:#1e293b;--accent:#38bdf8;--accent2:#a78bfa;--text:#e2e8f0;--muted:#94a3b8;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;height:100%;}
body{font-family:'Inter',sans-serif;color:var(--text);background:radial-gradient(1200px 800px at 20% 10%,#1e3a8a 0%,transparent 60%),radial-gradient(1000px 700px at 80% 90%,#7c3aed 0%,transparent 60%),linear-gradient(135deg,var(--bg1),var(--bg2));display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden;}
.blob{position:fixed;width:400px;height:400px;border-radius:50%;filter:blur(80px);opacity:.35;z-index:0;animation:float 12s ease-in-out infinite;}
.blob.a{background:#38bdf8;top:-100px;left:-100px;}.blob.b{background:#a78bfa;bottom:-120px;right:-100px;animation-delay:-6s;}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-30px)}}
.container{position:relative;z-index:1;text-align:center;padding:2rem;}
h1{font-weight:300;letter-spacing:4px;text-transform:uppercase;font-size:1.1rem;color:var(--muted);margin:0 0 1.5rem;}
.nav{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-bottom:.8rem;}
.nav a{font-size:.8rem;letter-spacing:2px;color:var(--muted);text-decoration:none;padding:.4rem .8rem;border:1px solid rgba(56,189,248,.3);border-radius:20px;transition:.2s;}
.nav a:hover,.nav a.active{color:var(--accent);border-color:var(--accent);background:rgba(56,189,248,.1);}
.tzform{margin-bottom:1.5rem;}
.tzform select{font-size:.85rem;color:var(--accent);background:rgba(0,0,0,.4);border:1px solid rgba(56,189,248,.4);border-radius:8px;padding:.4rem .8rem;cursor:pointer;}
.clock-wrap{position:relative;width:320px;height:320px;margin:0 auto;}
.glow{position:absolute;inset:-20px;border-radius:50%;background:conic-gradient(from 0deg,var(--accent),var(--accent2),var(--accent));filter:blur(30px);opacity:.45;animation:spin 8s linear infinite;}
@keyframes spin{to{transform:rotate(360deg)}}
.clock{position:relative;width:100%;height:100%;border-radius:50%;background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.12),rgba(255,255,255,.02));backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.15);box-shadow:inset 0 0 40px rgba(0,0,0,.4),0 20px 60px rgba(0,0,0,.5);}
.tick{position:absolute;width:2px;height:10px;background:rgba(255,255,255,.25);left:50%;top:5px;transform-origin:center 155px;margin-left:-1px;border-radius:2px;}
.tick.major{height:16px;width:3px;background:var(--accent);margin-left:-1.5px;box-shadow:0 0 8px var(--accent);}
.num{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(var(--a)) translateY(-130px) rotate(calc(-1*var(--a)));font-size:.85rem;font-weight:500;color:var(--muted);}
.hand{position:absolute;bottom:50%;left:50%;transform-origin:bottom center;border-radius:6px;}
.hour{width:8px;height:80px;background:linear-gradient(to top,var(--accent),#fff);margin-left:-4px;box-shadow:0 0 12px var(--accent);z-index:3;}
.minute{width:5px;height:110px;background:linear-gradient(to top,var(--accent2),#fff);margin-left:-2.5px;box-shadow:0 0 12px var(--accent2);z-index:4;}
.second{width:2px;height:125px;background:#f87171;margin-left:-1px;box-shadow:0 0 10px #f87171;z-index:5;}
.center-dot{position:absolute;top:50%;left:50%;width:16px;height:16px;background:#fff;border-radius:50%;transform:translate(-50%,-50%);z-index:6;box-shadow:0 0 15px rgba(255,255,255,.8);}
.digital{margin-top:2rem;font-size:2rem;font-weight:500;letter-spacing:2px;background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent;}
.sub{margin-top:.5rem;color:var(--muted);font-size:.9rem;}
</style>
</head>
<body>
<div class="blob a"></div><div class="blob b"></div>
<div class="container">
  <h1>Moderni hodiny</h1>
  NAV_PLACEHOLDER
  <div class="clock-wrap">
    <div class="glow"></div>
    <div class="clock">
      {% for i in range(60) %}<div class="tick {% if i % 5 == 0 %}major{% endif %}" style="transform: rotate({{ i*6 }}deg);"></div>{% endfor %}
      {% for n in range(1,13) %}<div class="num" style="--a: {{ n*30 }}deg;">{{ n }}</div>{% endfor %}
      <div class="hand hour" id="hour"></div>
      <div class="hand minute" id="minute"></div>
      <div class="hand second" id="second"></div>
      <div class="center-dot"></div>
    </div>
  </div>
  <div class="digital" id="digital">{{ server_time }}</div>
  <div class="sub">{{ tz }}</div>
</div>
<script>
const TZ = {{ tz|tojson }};
let serverNow=new Date("{{ server_time_iso }}");
async function sync(){try{const r=await fetch('/api/time?tz='+encodeURIComponent(TZ));const d=await r.json();serverNow=new Date(d.iso);}catch(e){}}
function hms(t){const fmt=new Intl.DateTimeFormat('en-GB',{timeZone:TZ,hour:'numeric',minute:'numeric',second:'numeric',hour12:false});const parts=fmt.formatToParts(t);let h=0,m=0,s=0;for(const p of parts){if(p.type==='hour')h=+p.value;if(p.type==='minute')m=+p.value;if(p.type==='second')s=+p.value;}return {h,m,s};}
function render(t){const {h,m,s}=hms(t);
document.getElementById('hour').style.transform='rotate('+(h%12*30+m*0.5)+'deg)';
document.getElementById('minute').style.transform='rotate('+(m*6+s*0.1)+'deg)';
document.getElementById('second').style.transform='rotate('+(s*6)+'deg)';
document.getElementById('digital').textContent=t.toLocaleString('cs-CZ',{timeZone:TZ});}
setInterval(sync,1000);
setInterval(()=>{serverNow=new Date(serverNow.getTime()+1000);render(serverNow);},1000);
sync().then(()=>render(serverNow));
</script>
</body></html>
'''

# ---------------- CUCKOO ----------------
TPL_CUCKOO = r'''
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8"><title>Kukacky</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;500&display=swap" rel="stylesheet">
<style>
:root{--wood:#6b3f1d;--wood2:#8b5a2b;--roof:#3a1f0e;--gold:#d4af37;--text:#f5e6a3;--muted:#a89968;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;height:100%;}
body{font-family:'Inter',sans-serif;color:var(--text);background:linear-gradient(180deg,#2a3a2a 0%,#1a2a1a 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden;}
.container{position:relative;z-index:1;text-align:center;padding:1rem;}
h1{font-family:'Cinzel',serif;font-weight:700;letter-spacing:6px;font-size:1.4rem;color:var(--gold);margin:0 0 1rem;text-shadow:0 0 12px rgba(212,175,55,.5);}
.nav{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-bottom:.8rem;}
.nav a{font-family:'Cinzel',serif;font-size:.8rem;letter-spacing:2px;color:var(--muted);text-decoration:none;padding:.4rem .8rem;border:1px solid rgba(212,175,55,.3);border-radius:20px;transition:.2s;}
.nav a:hover,.nav a.active{color:var(--gold);border-color:var(--gold);background:rgba(212,175,55,.1);}
.tzform{margin-bottom:1.2rem;}
.tzform select{font-family:'Cinzel',serif;font-size:.85rem;color:var(--gold);background:rgba(0,0,0,.4);border:1px solid rgba(212,175,55,.4);border-radius:8px;padding:.4rem .8rem;cursor:pointer;}
.house{position:relative;width:260px;height:300px;margin:0 auto;background:var(--wood);border:4px solid var(--roof);border-radius:8px;box-shadow:0 20px 40px rgba(0,0,0,.6);}
.roof{position:absolute;top:-60px;left:-20px;width:300px;height:80px;background:var(--roof);clip-path:polygon(50% 0%,0% 100%,100% 100%);border:3px solid #2a1508;}
.door{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:60px;height:80px;background:#2a1508;border:3px solid var(--roof);border-radius:6px 6px 0 0;overflow:hidden;}
.cuckoo{position:absolute;bottom:0;left:50%;transform:translateX(-50%) translateY(100%);width:40px;height:40px;transition:transform .6s ease;font-size:2rem;}
.cuckoo.show{transform:translateX(-50%) translateY(0);}
.clock-face{position:absolute;top:60px;left:50%;transform:translateX(-50%);width:120px;height:120px;border-radius:50%;background:#f5e6a3;border:4px solid var(--roof);box-shadow:inset 0 0 10px rgba(0,0,0,.3);}
.hand{position:absolute;bottom:50%;left:50%;transform-origin:bottom center;border-radius:3px;}
.ch{width:4px;height:35px;background:#3a1f0e;margin-left:-2px;z-index:2;}
.cm{width:3px;height:48px;background:#3a1f0e;margin-left:-1.5px;z-index:3;}
.cs{width:2px;height:52px;background:#c0392b;margin-left:-1px;z-index:4;}
.center{position:absolute;top:50%;left:50%;width:8px;height:8px;background:#3a1f0e;border-radius:50%;transform:translate(-50%,-50%);z-index:5;}
.pendulum-wrap{position:absolute;bottom:-90px;left:50%;transform:translateX(-50%);width:40px;height:90px;}
.pendulum-rod{position:absolute;top:0;left:50%;width:2px;height:70px;background:#3a1f0e;transform-origin:top center;margin-left:-1px;animation:swing 2s ease-in-out infinite;}
.pendulum-bob{position:absolute;bottom:-12px;left:50%;width:24px;height:24px;background:radial-gradient(circle at 30% 30%,#8b5a2b,#3a1f0e);border-radius:50%;transform:translateX(-50%);border:2px solid #2a1508;}
@keyframes swing{0%{transform:rotate(-20deg)}50%{transform:rotate(20deg)}100%{transform:rotate(-20deg)}}
.weights{position:absolute;bottom:-120px;left:50%;transform:translateX(-50%);display:flex;gap:40px;}
.weight{width:14px;height:30px;background:#3a1f0e;border-radius:4px;}
.digital{margin-top:9rem;font-family:'Cinzel',serif;font-size:1.5rem;color:var(--gold);letter-spacing:3px;}
.sub{margin-top:.3rem;color:var(--muted);font-size:.8rem;letter-spacing:2px;}
</style>
</head>
<body>
<div class="container">
  <h1>Kukacky</h1>
  NAV_PLACEHOLDER
  <div class="house">
    <div class="roof"></div>
    <div class="clock-face">
      <div class="hand ch" id="hour"></div>
      <div class="hand cm" id="minute"></div>
      <div class="hand cs" id="second"></div>
      <div class="center"></div>
    </div>
    <div class="door">
      <div class="cuckoo" id="cuckoo">🐦</div>
    </div>
    <div class="pendulum-wrap">
      <div class="pendulum-rod"><div class="pendulum-bob"></div></div>
    </div>
    <div class="weights"><div class="weight"></div><div class="weight"></div></div>
  </div>
  <div class="digital" id="digital">{{ server_time }}</div>
  <div class="sub">{{ tz }}</div>
</div>
<script>
const TZ = {{ tz|tojson }};
let serverNow=new Date("{{ server_time_iso }}");
async function sync(){try{const r=await fetch('/api/time?tz='+encodeURIComponent(TZ));const d=await r.json();serverNow=new Date(d.iso);}catch(e){}}
function hms(t){const fmt=new Intl.DateTimeFormat('en-GB',{timeZone:TZ,hour:'numeric',minute:'numeric',second:'numeric',hour12:false});const parts=fmt.formatToParts(t);let h=0,m=0,s=0;for(const p of parts){if(p.type==='hour')h=+p.value;if(p.type==='minute')m=+p.value;if(p.type==='second')s=+p.value;}return {h,m,s};}
function render(t){const {h,m,s}=hms(t);
document.getElementById('hour').style.transform='rotate('+(h%12*30+m*0.5)+'deg)';
document.getElementById('minute').style.transform='rotate('+(m*6+s*0.1)+'deg)';
document.getElementById('second').style.transform='rotate('+(s*6)+'deg)';
document.getElementById('digital').textContent=t.toLocaleString('cs-CZ',{timeZone:TZ});
const c=document.getElementById('cuckoo');
if(m===0 && t.getSeconds()<4){c.classList.add('show');}else{c.classList.remove('show');}}
setInterval(sync,1000);
setInterval(()=>{serverNow=new Date(serverNow.getTime()+1000);render(serverNow);},1000);
sync().then(()=>render(serverNow));
</script>
</body></html>
'''

# ---------------- DIGITAL ----------------
TPL_DIGITAL = r'''
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8"><title>Digitalni hodiny</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@300;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#05070f;--accent:#00ff9d;--accent2:#00b8ff;--muted:#5a6b7a;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;height:100%;}
body{font-family:'Inter',sans-serif;color:var(--accent);background:radial-gradient(circle at 50% 50%,#0a1a2a 0%,#05070f 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden;}
.container{position:relative;z-index:1;text-align:center;padding:2rem;}
h1{font-family:'Orbitron',sans-serif;letter-spacing:6px;font-size:1.2rem;color:var(--accent2);margin:0 0 1.5rem;text-shadow:0 0 12px rgba(0,184,255,.5);}
.nav{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-bottom:.8rem;}
.nav a{font-family:'Orbitron',sans-serif;font-size:.75rem;letter-spacing:2px;color:var(--muted);text-decoration:none;padding:.4rem .8rem;border:1px solid rgba(0,255,157,.3);border-radius:8px;transition:.2s;}
.nav a:hover,.nav a.active{color:var(--accent);border-color:var(--accent);background:rgba(0,255,157,.1);}
.tzform{margin-bottom:2rem;}
.tzform select{font-family:'Orbitron',sans-serif;font-size:.8rem;color:var(--accent);background:rgba(0,0,0,.4);border:1px solid rgba(0,255,157,.4);border-radius:8px;padding:.4rem .8rem;cursor:pointer;}
.display{font-family:'Orbitron',sans-serif;font-size:4rem;font-weight:700;letter-spacing:6px;color:var(--accent);text-shadow:0 0 20px rgba(0,255,157,.6),0 0 40px rgba(0,255,157,.3);padding:2rem 3rem;border:2px solid rgba(0,255,157,.4);border-radius:16px;background:rgba(0,255,157,.05);box-shadow:inset 0 0 30px rgba(0,255,157,.1);}
.date{margin-top:1.5rem;font-family:'Orbitron',sans-serif;font-size:1.2rem;color:var(--accent2);letter-spacing:4px;}
.sub{margin-top:.5rem;color:var(--muted);font-size:.85rem;letter-spacing:2px;}
.scan{position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent 0px,transparent 2px,rgba(0,255,157,.03) 2px,rgba(0,255,157,.03) 4px);pointer-events:none;}
</style>
</head>
<body>
<div class="scan"></div>
<div class="container">
  <h1>Digitalni hodiny</h1>
  NAV_PLACEHOLDER
  <div class="display" id="digital">{{ server_time }}</div>
  <div class="date" id="date"></div>
  <div class="sub">{{ tz }}</div>
</div>
<script>
const TZ = {{ tz|tojson }};
let serverNow=new Date("{{ server_time_iso }}");
async function sync(){try{const r=await fetch('/api/time?tz='+encodeURIComponent(TZ));const d=await r.json();serverNow=new Date(d.iso);}catch(e){}}
function pad(n){return String(n).padStart(2,'0');}
function hms(t){const fmt=new Intl.DateTimeFormat('en-GB',{timeZone:TZ,hour:'numeric',minute:'numeric',second:'numeric',hour12:false});const parts=fmt.formatToParts(t);let h=0,m=0,s=0;for(const p of parts){if(p.type==='hour')h=+p.value;if(p.type==='minute')m=+p.value;if(p.type==='second')s=+p.value;}return {h,m,s};}
function render(t){const {h,m,s}=hms(t);
document.getElementById('digital').textContent=pad(h)+':'+pad(m)+':'+pad(s);
document.getElementById('date').textContent=t.toLocaleDateString('cs-CZ',{timeZone:TZ,weekday:'long',day:'numeric',month:'long',year:'numeric'});}
setInterval(sync,1000);
setInterval(()=>{serverNow=new Date(serverNow.getTime()+1000);render(serverNow);},1000);
sync().then(()=>render(serverNow));
</script>
</body></html>
'''

# ---------------- NEON ----------------
TPL_NEON = r'''
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8"><title>Neon hodiny</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@300&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0014;--pink:#ff2d95;--cyan:#00f0ff;--purple:#b026ff;--muted:#7a5a9a;}
*{box-sizing:border-box;} html,body{margin:0;padding:0;height:100%;}
body{font-family:'Inter',sans-serif;color:#fff;background:radial-gradient(circle at 50% 50%,#1a0033 0%,#0a0014 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;overflow:hidden;}
.container{position:relative;z-index:1;text-align:center;padding:2rem;}
h1{font-family:'Orbitron',sans-serif;letter-spacing:6px;font-size:1.2rem;color:var(--cyan);margin:0 0 1.5rem;text-shadow:0 0 12px var(--cyan);}
.nav{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-bottom:.8rem;}
.nav a{font-family:'Orbitron',sans-serif;font-size:.75rem;letter-spacing:2px;color:var(--muted);text-decoration:none;padding:.4rem .8rem;border:1px solid rgba(255,45,149,.4);border-radius:20px;transition:.2s;}
.nav a:hover,.nav a.active{color:var(--pink);border-color:var(--pink);background:rgba(255,45,149,.1);text-shadow:0 0 8px var(--pink);}
.tzform{margin-bottom:2rem;}
.tzform select{font-family:'Orbitron',sans-serif;font-size:.8rem;color:var(--pink);background:rgba(0,0,0,.4);border:1px solid rgba(255,45,149,.4);border-radius:20px;padding:.4rem .8rem;cursor:pointer;}
.clock-wrap{position:relative;width:320px;height:320px;margin:0 auto;}
.ring{position:absolute;inset:0;border-radius:50%;border:3px solid var(--pink);box-shadow:0 0 20px var(--pink),inset 0 0 20px rgba(255,45,149,.3);}
.ring2{position:absolute;inset:20px;border-radius:50%;border:2px solid var(--cyan);box-shadow:0 0 15px var(--cyan);}
.hand{position:absolute;bottom:50%;left:50%;transform-origin:bottom center;border-radius:4px;}
.nh{width:6px;height:80px;background:var(--pink);margin-left:-3px;box-shadow:0 0 12px var(--pink),0 0 24px var(--pink);z-index:3;}
.nm{width:4px;height:110px;background:var(--cyan);margin-left:-2px;box-shadow:0 0 12px var(--cyan),0 0 24px var(--cyan);z-index:4;}
.ns{width:2px;height:130px;background:var(--purple);margin-left:-1px;box-shadow:0 0 10px var(--purple);z-index:5;}
.center{position:absolute;top:50%;left:50%;width:14px;height:14px;background:#fff;border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 15px #fff;z-index:6;}
.dot{position:absolute;width:6px;height:6px;background:var(--pink);border-radius:50%;box-shadow:0 0 8px var(--pink);}
.digital{margin-top:2rem;font-family:'Orbitron',sans-serif;font-size:2rem;color:var(--pink);letter-spacing:4px;text-shadow:0 0 15px var(--pink);}
.sub{margin-top:.5rem;color:var(--muted);font-size:.85rem;letter-spacing:2px;}
</style>
</head>
<body>
<div class="container">
  <h1>Neon hodiny</h1>
  NAV_PLACEHOLDER
  <div class="clock-wrap">
    <div class="ring"></div>
    <div class="ring2"></div>
    {% for i in range(12) %}<div class="dot" style="left:50%;top:50%;transform:translate(-50%,-50%) rotate({{ i*30 }}deg) translateY(-145px);"></div>{% endfor %}
    <div class="hand nh" id="hour"></div>
    <div class="hand nm" id="minute"></div>
    <div class="hand ns" id="second"></div>
    <div class="center"></div>
  </div>
  <div class="digital" id="digital">{{ server_time }}</div>
  <div class="sub">{{ tz }}</div>
</div>
<script>
const TZ = {{ tz|tojson }};
let serverNow=new Date("{{ server_time_iso }}");
async function sync(){try{const r=await fetch('/api/time?tz='+encodeURIComponent(TZ));const d=await r.json();serverNow=new Date(d.iso);}catch(e){}}
function hms(t){const fmt=new Intl.DateTimeFormat('en-GB',{timeZone:TZ,hour:'numeric',minute:'numeric',second:'numeric',hour12:false});const parts=fmt.formatToParts(t);let h=0,m=0,s=0;for(const p of parts){if(p.type==='hour')h=+p.value;if(p.type==='minute')m=+p.value;if(p.type==='second')s=+p.value;}return {h,m,s};}
function render(t){const {h,m,s}=hms(t);
document.getElementById('hour').style.transform='rotate('+(h%12*30+m*0.5)+'deg)';
document.getElementById('minute').style.transform='rotate('+(m*6+s*0.1)+'deg)';
document.getElementById('second').style.transform='rotate('+(s*6)+'deg)';
document.getElementById('digital').textContent=t.toLocaleString('cs-CZ',{timeZone:TZ});}
setInterval(sync,1000);
setInterval(()=>{serverNow=new Date(serverNow.getTime()+1000);render(serverNow);},1000);
sync().then(()=>render(serverNow));
</script>
</body></html>
'''

TEMPLATES = {
    'orloj': TPL_ORLOJ,
    'modern': TPL_MODERN,
    'cuckoo': TPL_CUCKOO,
    'digital': TPL_DIGITAL,
    'neon': TPL_NEON,
}

@app.route('/')
def index():
    style = request.args.get('style', 'orloj')
    if style not in TEMPLATES:
        style = 'orloj'
    tz_name = request.args.get('tz', 'Europe/Prague')
    if tz_name not in TIMEZONES:
        tz_name = 'Europe/Prague'
    tz = get_tz(tz_name)
    now = datetime.now(tz)
    tpl = TEMPLATES[style].replace('NAV_PLACEHOLDER', make_nav(style, tz_name))
    return render_template_string(
        tpl,
        server_time=now.strftime('%Y-%m-%d %H:%M:%S'),
        server_time_iso=now.isoformat(),
        tz=tz_name,
        style=style,
    )

@app.route('/api/time')
def api_time():
    tz_name = request.args.get('tz', 'Europe/Prague')
    if tz_name not in TIMEZONES:
        tz_name = 'Europe/Prague'
    tz = get_tz(tz_name)
    now = datetime.now(tz)
    return jsonify({'iso': now.isoformat(), 'timestamp': now.timestamp(), 'tz': tz_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
