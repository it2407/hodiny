from flask import Flask, render_template_string, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Prague")

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <title>Orloj - Cas serveru</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg1:#0a0e1a; --bg2:#1a1f33;
      --gold:#d4af37; --gold2:#f5e6a3; --bronze:#8b6f3f;
      --text:#f5e6a3; --muted:#a89968;
      --night:#0b1026;
    }
    * { box-sizing:border-box; }
    html,body { margin:0; padding:0; height:100%; }
    body {
      font-family:'Inter',sans-serif; color:var(--text);
      background: radial-gradient(ellipse at 50% 0%, #1a2450 0%, transparent 60%),
                  radial-gradient(ellipse at 50% 100%, #0d1224 0%, transparent 70%),
                  linear-gradient(180deg, var(--bg1), var(--bg2));
      display:flex; flex-direction:column; align-items:center; justify-content:center;
      min-height:100vh; overflow:hidden;
    }
    .stars { position:fixed; inset:0; z-index:0; pointer-events:none; }
    .star { position:absolute; width:2px; height:2px; background:#fff; border-radius:50%; opacity:.7; animation:twinkle 3s ease-in-out infinite; }
    @keyframes twinkle { 0%,100%{opacity:.3} 50%{opacity:1} }

    .container { position:relative; z-index:1; text-align:center; padding:1rem; }
    h1 { font-family:'Cinzel',serif; font-weight:700; letter-spacing:6px; font-size:1.4rem; color:var(--gold); margin:0 0 1.5rem; text-shadow:0 0 12px rgba(212,175,55,.5); }

    .orloj { position:relative; width:360px; height:360px; margin:0 auto; }
    .orloj-glow { position:absolute; inset:-30px; border-radius:50%; background:radial-gradient(circle, rgba(212,175,55,.25), transparent 70%); filter:blur(20px); }
    .face {
      position:relative; width:100%; height:100%; border-radius:50%;
      background: radial-gradient(circle at 50% 40%, #1c2340 0%, #0b0f1f 70%, #05070f 100%);
      border: 6px solid var(--gold);
      box-shadow: 0 0 0 3px var(--bronze), 0 0 0 6px #2a2010, 0 20px 60px rgba(0,0,0,.8), inset 0 0 40px rgba(0,0,0,.6);
    }
    /* zodiac ring */
    .zodiac { position:absolute; inset:24px; border-radius:50%; border:1px solid rgba(212,175,55,.3); }
    .zodiac .sym { position:absolute; left:50%; top:50%; font-size:.9rem; color:var(--gold2); transform: translate(-50%,-50%) rotate(var(--a)) translateY(-132px) rotate(calc(-1*var(--a))); }
    /* roman numerals outer */
    .roman { position:absolute; inset:8px; border-radius:50%; }
    .roman .n { position:absolute; left:50%; top:50%; font-family:'Cinzel',serif; font-size:1.05rem; font-weight:700; color:var(--gold); transform: translate(-50%,-50%) rotate(var(--a)) translateY(-150px) rotate(calc(-1*var(--a))); text-shadow:0 0 6px rgba(212,175,55,.6); }

    .tick { position:absolute; left:50%; top:14px; width:2px; height:10px; background:rgba(212,175,55,.4); transform-origin:center 166px; margin-left:-1px; }
    .tick.major { height:16px; width:3px; background:var(--gold); margin-left:-1.5px; }

    .hand { position:absolute; bottom:50%; left:50%; transform-origin:bottom center; border-radius:4px; }
    .hour { width:7px; height:95px; background:linear-gradient(to top, var(--bronze), var(--gold2)); margin-left:-3.5px; box-shadow:0 0 10px rgba(212,175,55,.6); z-index:3; }
    .minute { width:5px; height:130px; background:linear-gradient(to top, var(--bronze), #fff); margin-left:-2.5px; box-shadow:0 0 10px rgba(255,255,255,.5); z-index:4; }
    .second { width:2px; height:148px; background:#f87171; margin-left:-1px; box-shadow:0 0 8px #f87171; z-index:5; }
    .sun-hand { width:3px; height:115px; background:linear-gradient(to top, #ff8c00, #ffd700); margin-left:-1.5px; z-index:2; opacity:.85; }
    .center-cap { position:absolute; top:50%; left:50%; width:18px; height:18px; background:radial-gradient(circle, var(--gold2), var(--bronze)); border-radius:50%; transform:translate(-50%,-50%); z-index:6; box-shadow:0 0 12px var(--gold); border:2px solid #2a2010; }

    /* pendulum */
    .pendulum-wrap { position:relative; width:360px; height:160px; margin:1.5rem auto 0; }
    .pendulum-pivot { position:absolute; top:0; left:50%; width:14px; height:14px; background:var(--gold); border-radius:50%; transform:translateX(-50%); box-shadow:0 0 10px var(--gold); z-index:2; }
    .pendulum-rod {
      position:absolute; top:7px; left:50%; width:3px; height:120px;
      background:linear-gradient(to bottom, var(--gold), var(--bronze));
      transform-origin:top center; margin-left:-1.5px;
      animation:swing 2s ease-in-out infinite;
    }
    .pendulum-bob {
      position:absolute; bottom:-18px; left:50%; width:36px; height:36px;
      background:radial-gradient(circle at 30% 30%, var(--gold2), var(--bronze));
      border-radius:50%; transform:translateX(-50%);
      box-shadow:0 6px 18px rgba(0,0,0,.6), inset -3px -3px 6px rgba(0,0,0,.4);
      border:2px solid var(--gold);
    }
    @keyframes swing { 0%{transform:rotate(-18deg)} 50%{transform:rotate(18deg)} 100%{transform:rotate(-18deg)} }

    .digital { margin-top:1.5rem; font-family:'Cinzel',serif; font-size:1.6rem; color:var(--gold2); letter-spacing:3px; text-shadow:0 0 12px rgba(212,175,55,.4); }
    .sub { margin-top:.4rem; color:var(--muted); font-size:.85rem; letter-spacing:2px; }

    .footer { margin-top:1rem; color:var(--muted); font-size:.75rem; }
  </style>
</head>
<body>
  <div class="stars" id="stars"></div>
  <div class="container">
    <h1>Orloj</h1>
    <div class="orloj">
      <div class="orloj-glow"></div>
      <div class="face" id="face">
        <div class="zodiac">
          {% set zodiacs = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'] %}
          {% for z in zodiacs %}
          <div class="sym" style="--a: {{ loop.index0*30 }}deg;">{{ z }}</div>
          {% endfor %}
        </div>
        <div class="roman">
          {% set romans = ['XII','I','II','III','IV','V','VI','VII','VIII','IX','X','XI'] %}
          {% for r in romans %}
          <div class="n" style="--a: {{ loop.index0*30 }}deg;">{{ r }}</div>
          {% endfor %}
        </div>
        {% for i in range(60) %}
        <div class="tick {% if i % 5 == 0 %}major{% endif %}" style="transform: rotate({{ i*6 }}deg);"></div>
        {% endfor %}
        <div class="hand sun-hand" id="sun"></div>
        <div class="hand hour" id="hour"></div>
        <div class="hand minute" id="minute"></div>
        <div class="hand second" id="second"></div>
        <div class="center-cap"></div>
      </div>
    </div>
    <div class="pendulum-wrap">
      <div class="pendulum-pivot"></div>
      <div class="pendulum-rod">
        <div class="pendulum-bob"></div>
      </div>
    </div>
    <div class="digital" id="digital">{{ server_time }}</div>
    <div class="sub">cas serveru - Praha</div>
  </div>

  <script>
    // stars
    const starsEl = document.getElementById('stars');
    for (let i=0;i<80;i++){
      const s=document.createElement('div'); s.className='star';
      s.style.left=Math.random()*100+'%'; s.style.top=Math.random()*100+'%';
      s.style.animationDelay=(Math.random()*3)+'s';
      starsEl.appendChild(s);
    }

    let serverNow = new Date("{{ server_time_iso }}");
    async function sync() {
      try {
        const r = await fetch('/api/time');
        const d = await r.json();
        serverNow = new Date(d.iso);
      } catch (e) {}
    }
    function render(t) {
      const h = t.getHours() % 12;
      const m = t.getMinutes();
      const s = t.getSeconds() + t.getMilliseconds()/1000;
      document.getElementById('hour').style.transform = 'rotate(' + (h*30 + m*0.5) + 'deg)';
      document.getElementById('minute').style.transform = 'rotate(' + (m*6 + s*0.1) + 'deg)';
      document.getElementById('second').style.transform = 'rotate(' + (s*6) + 'deg)';
      // sun hand approximates hour angle over 12h (decorative)
      document.getElementById('sun').style.transform = 'rotate(' + (h*30 + m*0.5 + 180) + 'deg)';
      document.getElementById('digital').textContent = t.toLocaleString('cs-CZ');
    }
    setInterval(sync, 1000);
    setInterval(() => { serverNow = new Date(serverNow.getTime() + 1000); render(serverNow); }, 1000);
    sync().then(() => render(serverNow));
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    now = datetime.now(TZ)
    return render_template_string(
        TEMPLATE,
        server_time=now.strftime('%Y-%m-%d %H:%M:%S'),
        server_time_iso=now.isoformat(),
    )

@app.route('/api/time')
def api_time():
    now = datetime.now(TZ)
    return jsonify({'iso': now.isoformat(), 'timestamp': now.timestamp()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
