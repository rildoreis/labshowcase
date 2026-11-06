import json, html, os, shutil

techs = json.load(open("techs.json"))
links = json.load(open("links.json"))
OUT = "."
e = html.escape

CSS = """
  :root{--ink:#121212;--slate:#4a4a4a;--mute:#8a8a8a;--orange:#f26b1d;--orange-dark:#c24f0b;--tint:#fff1e8;
    --cloud:#f1eee9;--line:#e2ddd5;--black:#111;--white:#fff;--paper:#faf8f5;--mono:"JetBrains Mono",ui-monospace,Menlo,monospace;--max:1040px}
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;font-family:Nunito,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--paper);line-height:1.6;font-size:17px}
  a{color:var(--orange-dark)}
  h1,h2,h3{line-height:1.2;margin:0 0 .5rem;font-weight:800}
  h1{font-size:2.4rem} h2{font-size:1.5rem} h3{font-size:1.05rem;color:var(--orange-dark)}
  p{margin:0 0 1rem} ul{margin:0 0 1rem;padding-left:1.1rem} li{margin:.3rem 0} li::marker{color:var(--orange)}
  .wrap{max-width:var(--max);margin:0 auto;padding:0 1.25rem}
  .eyebrow{font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--orange)}

  .topbar{position:sticky;top:0;z-index:10;background:var(--black);border-bottom:3px solid var(--orange)}
  .topbar .wrap{display:flex;align-items:center;justify-content:space-between;height:58px}
  .brand{font-weight:800;text-decoration:none;color:#fff;font-size:1.05rem}
  .brand span{color:var(--orange)}
  .topbar nav a{text-decoration:none;color:#d6d6d6;margin-left:1.25rem;font-size:.95rem;font-weight:600}
  .topbar nav a:hover,.topbar nav a.on{color:var(--orange)}

  .hero{background:var(--black);color:#fff;padding:5rem 0 3.5rem;position:relative;overflow:hidden}
  .hero .wrap{position:relative;z-index:1}
  .hero h1{font-size:clamp(2.4rem,6vw,4.2rem);font-weight:400;margin:1.2rem 0 1rem}
  .hero h1 b{font-weight:800;color:var(--orange)}
  .hero p{max-width:40rem;font-size:1.15rem;color:#d6d6d6;margin:0}
  .hero .meta{display:flex;flex-wrap:wrap;gap:2rem;margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,.2);font-size:.95rem}
  .hero .meta div span{display:block;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--orange);font-weight:800}
  .hero.small{padding:3rem 0 2.5rem}
  .hero.small h1{font-size:clamp(1.9rem,4.5vw,2.8rem);margin:.6rem 0 .4rem}

  section.block{padding:3.5rem 0;border-bottom:1px solid var(--line)}
  section.block > .wrap > h2{margin-bottom:1.25rem}
  .strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.6rem;margin:1rem 0 1.5rem}
  .strip div{background:var(--tint);border-left:4px solid var(--orange);padding:.6rem .8rem;border-radius:0 6px 6px 0}
  .strip div span{display:block;font-size:.66rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--orange-dark)}
  .strip div b{font-weight:700;font-size:.95rem}

  /* gallery */
  .gallery{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(6,1fr);gap:1.25rem}
  .gallery li{grid-column:span 2}
  .gallery a{display:block;text-decoration:none;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;height:100%;transition:transform .15s,box-shadow .15s}
  .gallery .num{display:none}
  .gallery a:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(0,0,0,.10);border-color:var(--orange)}
  .gallery img{width:100%;aspect-ratio:4/3;object-fit:cover;object-position:center 45%;display:block;background:var(--cloud)}
  .gallery .body{padding:.9rem 1rem 1.1rem}
  .gallery .num{font-size:.68rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--orange-dark)}
  .gallery .name{font-weight:800;font-size:1.08rem;margin:.15rem 0 .2rem}
  .gallery .sub{color:var(--slate);font-size:.88rem}
  .pill{display:inline-block;margin-top:.6rem;font-size:.7rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:.2rem .55rem;border-radius:999px;background:var(--tint);color:var(--orange-dark)}
  .pill.ready{background:#e6f4ea;color:#1e7a3a}
  .pill.pending{background:var(--tint);color:var(--orange-dark)}
  .pill.training{background:#eee;color:#444}

  /* tech page */
  .band{display:inline-flex;overflow:hidden;border-radius:6px;font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin-bottom:1rem}
  .band span:first-child{background:var(--black);color:var(--orange);padding:.45rem .9rem}
  .band span:last-child{background:var(--orange);color:#fff;padding:.45rem .9rem}
  .lead{font-size:1.1rem;color:var(--slate);margin-bottom:1.5rem}
  figure{margin:0 0 1.25rem}
  figure img{width:100%;max-height:460px;object-fit:contain;display:block;border-radius:8px;background:var(--cloud);border:1px solid var(--line)}
  figcaption{font-size:.85rem;color:var(--mute);font-style:italic;margin-top:.4rem}
  .two{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}
  .cols{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin:1rem 0 1.5rem}
  .card{background:#fff;border:1px solid var(--line);border-top:4px solid var(--orange);border-radius:0 0 8px 8px;padding:1.1rem 1.25rem}
  .card ul{margin-bottom:0}
  .explore{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin-top:1rem}
  .explore a{display:block;text-decoration:none;color:var(--ink);background:var(--cloud);border-top:4px solid var(--orange);border-radius:0 0 8px 8px;padding:1.1rem 1.2rem}
  .explore a:hover{background:var(--tint)}
  .explore a b{display:block;margin-bottom:.3rem}
  .explore a small{color:var(--slate);display:block;margin-bottom:.5rem}
  .explore a em{font-style:normal;color:var(--orange-dark);font-weight:700;font-size:.9rem}

  /* interaction blocks */
  .interact{background:var(--black);color:#e6e6e6;padding:3rem 0;margin-top:3rem}
  .interact h2{color:#fff} .interact h3{color:var(--orange)}
  .interact p{color:#c9c9c9}
  .igrid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
  .ibox{background:#1e1e1e;border-left:4px solid var(--orange);border-radius:0 8px 8px 0;padding:1.2rem 1.4rem}
  .ibox.full{grid-column:1/-1}
  .embed{position:relative;width:100%;aspect-ratio:16/9;background:#0a0a0a;border-radius:8px;overflow:hidden}
  .embed iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
  .embed.tall{aspect-ratio:auto;height:560px}
  .placeholder{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%;min-height:220px;border:2px dashed #555;border-radius:8px;padding:1.5rem;color:#aaa;font-size:.95rem}
  .placeholder b{color:var(--orange);font-size:1.05rem;margin-bottom:.3rem}
  .placeholder code{background:#000;color:#ddd;padding:.1rem .4rem;border-radius:4px;font-size:.85rem}

  .pager{display:flex;justify-content:space-between;gap:1rem;padding:2rem 0;border-top:1px solid var(--line)}
  .pager a{text-decoration:none;font-weight:700;color:var(--ink);background:var(--cloud);padding:.8rem 1.1rem;border-radius:8px;flex:1}
  .pager a:hover{background:var(--tint)}
  .pager a small{display:block;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--orange-dark);font-weight:800}
  .pager .next{text-align:right}

  .collab{padding:3.5rem 0 4rem;background:var(--black);color:#e6e6e6}
  .collab h2{color:#fff} .collab h3{color:var(--orange)} .collab a{color:var(--orange)}
  .collab .boxes{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin:1.5rem 0}
  .collab .boxes div{padding:1.2rem 1.4rem;border-left:4px solid var(--orange);border-radius:0 8px 8px 0;background:#1e1e1e}
  .collab .boxes p{margin:.25rem 0} .collab strong{color:#fff}
  .collab ol{counter-reset:step;list-style:none;padding:0;margin:0 0 1.5rem}
  .collab ol li{counter-increment:step;position:relative;padding-left:2.4rem;margin:.6rem 0}
  .collab ol li::before{content:counter(step);position:absolute;left:0;top:0;width:1.7rem;height:1.7rem;border-radius:50%;background:var(--orange);color:#fff;font-weight:800;font-size:.85rem;display:flex;align-items:center;justify-content:center}
  .cta{display:inline-block;background:var(--orange);color:#fff !important;text-decoration:none;font-weight:800;padding:.8rem 1.4rem;border-radius:8px}
  .cta:hover{background:var(--orange-dark)}
  footer{background:#000;color:#9a9a9a;padding:1.5rem 0;font-size:.88rem;border-top:1px solid #2a2a2a}
  footer a{color:#cfcfcf}


  .logo{display:inline-flex;align-items:center;gap:.6rem;text-decoration:none;color:#fff;font-weight:800}
  .logo i{display:inline-grid;place-items:center;width:30px;height:30px;background:var(--orange);color:#111;font-style:normal;font-family:var(--mono);font-weight:700;font-size:.72rem;border-radius:5px;letter-spacing:.02em}
  .tag{font-family:var(--mono);font-weight:700;font-size:.72rem;letter-spacing:.04em;color:var(--orange-dark);background:var(--tint);padding:.15rem .45rem;border-radius:4px;display:inline-block}
  .hero .tag{background:#2a2a2a;color:var(--orange)}
  .ul-mark{display:inline-block;width:56px;height:6px;background:var(--orange);border-radius:3px;transform:rotate(-1.5deg);margin:.2rem 0 1.2rem}
  .filters{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.4rem}
  .filters button{font:inherit;font-weight:700;font-size:.85rem;padding:.4rem .9rem;border-radius:999px;border:1.5px solid var(--line);background:#fff;color:var(--slate);cursor:pointer}
  .filters button.on{background:var(--black);color:#fff;border-color:var(--black)}
  .filters button:hover{border-color:var(--orange)}
  .gallery li.hide{display:none}
  .gallery li.featured{grid-column:span 3}
  .gallery li.featured img{aspect-ratio:2/1}
  .gallery li.featured .name{font-size:1.3rem}
  .gallery .ready-note{display:block;margin-top:.5rem;color:var(--orange-dark);font-weight:700;font-size:.85rem}
  .used{background:#fff;border:1px solid var(--line);border-radius:10px;padding:1.1rem 1.3rem;margin:1.5rem 0}
  .used h3{margin-bottom:.3rem} .used p{margin:0;color:var(--slate)}
  .learn{list-style:none;padding:0;margin:.5rem 0 0}
  .learn li{display:grid;grid-template-columns:150px 1fr;gap:1rem;padding:.75rem 0;border-top:1px solid var(--line);margin:0}
  .learn li:last-child{border-bottom:1px solid var(--line)}
  .learn .k{font-family:var(--mono);font-size:.74rem;font-weight:700;color:var(--orange-dark);padding-top:.25rem}
  .learn a{font-weight:700;color:var(--ink)} .learn a:hover{color:var(--orange-dark)}
  .learn small{display:block;color:var(--slate)}
  .meta-line{font-family:var(--mono);font-size:.74rem;color:var(--mute);margin-top:1rem}
  .labgrid{display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start}
  .photo-ph{aspect-ratio:4/3;border:2px dashed var(--line);border-radius:10px;display:grid;place-items:center;color:var(--mute);text-align:center;padding:1rem;background:#fff}
  @media (max-width:760px){.gallery{grid-template-columns:1fr}.gallery li,.gallery li.featured{grid-column:span 1}.gallery li.featured img{aspect-ratio:4/3}.learn li{grid-template-columns:1fr;gap:.2rem}.labgrid{grid-template-columns:1fr}.two,.cols,.igrid,.collab .boxes{grid-template-columns:1fr}.topbar nav a{margin-left:.9rem;font-size:.88rem}.hero{padding:3.5rem 0 2.5rem}.embed.tall{height:480px}}
  @media print{.topbar,.pager,footer,.interact{display:none}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%23f26b1d'/%3E%3Ctext x='32' y='41' text-anchor='middle' font-family='JetBrains Mono,Menlo,monospace' font-weight='700' font-size='24' fill='%23111'%3ELAB%3C/text%3E%3C/svg%3E">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{root}images/{og}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a class="logo" href="{root}index.html"><i>LAB</i><span>What's in <span style="color:var(--orange)">the Lab</span></span></a>
    <nav>
      <a href="{root}index.html#technologies" class="{on_tech}">Technologies</a>
      <a href="{root}lab.html" class="{on_lab}">The lab</a>
      <a href="{root}collaborate.html" class="{on_collab}">Collaborate</a>
    </nav>
  </div>
</header>
"""

FOOT = """
<footer><div class="wrap">What's in the Lab · Lab name · Building, Room · City · <a href="{root}collaborate.html">Have an idea? Let's collaborate</a><br><span style="font-family:var(--mono);font-size:.74rem">Page updated 6 Nov 2026 · kept by [name]</span></div></footer>
</body>
</html>
"""

def head(title, desc, root, on="tech", og="omni-one.jpg"):
    return HEAD.format(title=e(title), desc=e(desc), css=CSS, root=root, og=og,
                       on_tech="on" if on == "tech" else "", on_collab="on" if on == "collab" else "", on_lab="on" if on == "lab" else "")

def pill(status):
    s = status.lower()
    cls = "ready" if s.startswith("ready") else "training" if s.startswith("training") else "pending"
    return f'<span class="pill {cls}">{e(status.split(" (")[0])}</span>'

def li_pairs(items):
    return "\n".join(f"      <li><strong>{e(a)}</strong>{e(b)}</li>" for a, b in items)

def placeholder(title, lines):
    body = "<br>".join(lines)
    return f'<div class="placeholder"><b>{title}</b><span>{body}</span></div>'

def used_text(t):
    st = t["status"].lower()
    if st.startswith("ready"):
        return "Not used in a course yet — set up and waiting for its first project. Be the first and we will write it up here."
    if st.startswith("setup"):
        return "Not available yet. Once it is set up, the first session will be documented here: who used it, for what, and what we learned."
    return "Nobody in the lab has tried this one yet. If you know it, come and show us — a 20-minute walkthrough would be the first entry here."

# ------------------------------------------------------------------ tech pages
def tech_page(i, t):
    root = "../"
    prev_t = techs[i - 1] if i > 0 else None
    next_t = techs[i + 1] if i < len(techs) - 1 else None
    kinds = {"Watch a quick demonstration": "WATCH", "Explore a beginner tutorial": "START HERE", "See example applications": "IN THE CLASSROOM"}
    ex = "\n".join(
        f'      <li><span class="k">{kinds.get(ti, "LINK")}</span><div><a href="{e(u)}" target="_blank" rel="noopener">{e(d.rstrip("."))}</a><small>{e(u.split("/")[2].replace("www.", ""))}</small></div></li>'
        for ti, d, u, lbl in links.get(t["id"], []))
    form_hint = e(t["name"])
    pager = '<div class="pager">'
    pager += (f'<a href="{prev_t["id"]}.html"><small>← Previous</small>{e(prev_t["name"])}</a>' if prev_t else '<a href="../index.html#technologies"><small>← Back</small>All technologies</a>')
    pager += (f'<a class="next" href="{next_t["id"]}.html"><small>Next →</small>{e(next_t["name"])}</a>' if next_t else '<a class="next" href="../collaborate.html"><small>Next →</small>Have an idea? Let\'s collaborate</a>')
    pager += '</div>'

    return head(f"{t['name']} — What's in the Lab", t["lead"], root) + f"""
<section class="hero small">
  <div class="wrap">
    <span class="tag">LAB-{t['num']}</span> &nbsp;<span class="tag">{e(t['type'])}</span> &nbsp;<span class="tag">{e(t['use'])}</span>
    <h1>{e(t['name'])}</h1>
    <p>{e(t['lead'])}</p>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="two">
      <div>
        <figure>
          <img src="../{t['image']}" alt="{e(t['name'])}">
          <figcaption>{e(t['caption'])}</figcaption>
        </figure>
      </div>
      <div>
        <div class="strip" style="grid-template-columns:1fr 1fr">
          <div><span>Type of tech</span><b>{e(t['type'])}</b></div>
          <div><span>Use</span><b>{e(t['use'])}</b></div>
          <div><span>Quantity</span><b>{e(t['quantity'])}</b></div>
          <div><span>Status</span><b>{e(t['status'])}</b></div>
        </div>
        <h3>What is it?</h3>
        <p>{e(t['summary'])}</p>
      </div>
    </div>

    <h3>What's in the kit</h3>
    <ul>
{li_pairs(t['kit'])}
    </ul>

    <div class="used">
      <h3>Used so far</h3>
      <!-- Replace with real history: course, semester, what happened, who ran it. One to three lines. -->
      <p>{used_text(t)}</p>
    </div>

    <h2 style="margin-top:2rem">Ideas for teaching and research</h2><span class="ul-mark"></span>
    <div class="cols">
      <div class="card"><h3>Teaching ideas</h3><ul>
{li_pairs(t['teaching'])}
      </ul></div>
      <div class="card"><h3>Research ideas</h3><ul>
{li_pairs(t['research'])}
      </ul></div>
    </div>

    <h3>Good to know</h3>
    <ul>
{chr(10).join(f'      <li>{e(n)}</li>' for n in t['notes'])}
    </ul>

    <h2 style="margin-top:2rem">Learn and explore</h2>
    <ul class="learn">
{ex}
    </ul>
    <p class="meta-line">Inventory LAB-{t['num']} · {e(t['quantity'])} · status: {e(t['status'])}</p>
  </div>
</section>

<section class="interact" id="interact">
  <div class="wrap">
    <span class="tag">Get involved</span>
    <h2>Try it, tell us, share an idea</h2>
    <div class="igrid">

      <div class="ibox full">
        <h3>Watch our demo</h3>
        <p>A short video recorded in the lab with this equipment.</p>
        <div class="embed">
          <!-- VIDEO: replace the placeholder below with the YouTube embed code.
               YouTube → Share → Embed → copy the <iframe …></iframe> and paste it here. -->
          {placeholder("Demo video placeholder", ["Upload the demo to YouTube (unlisted is fine).", "Share → Embed → paste the <code>&lt;iframe&gt;</code> here."])}
        </div>
      </div>

      <div class="ibox">
        <h3>I'm interested</h3>
        <p>Thirty seconds: tell us you would like to try the <strong>{form_hint}</strong> and we will get in touch.</p>
        <div class="embed tall">
          <!-- GOOGLE FORM "I'm interested": Forms → Send → < > (Embed HTML) → paste the <iframe> here.
               Pre-fill the "Technology" question with "{form_hint}" using Forms → ⋮ → Get pre-filled link. -->
          {placeholder("Google Form placeholder — I'm interested", ["Create the “I'm interested” form (questions in FORMS.docx).", "Send → <code>&lt;&gt;</code> Embed HTML → paste the <code>&lt;iframe&gt;</code> here.", f"Use a pre-filled link with Technology = “{form_hint}”."])}
        </div>
      </div>

      <div class="ibox">
        <h3>How would you use it?</h3>
        <p>Post an idea, a question or a link on the wall — and see what colleagues have already suggested.</p>
        <div class="embed tall">
          <!-- PADLET: Share → Embed in your blog or website → copy the <iframe> and paste it here. -->
          {placeholder("Padlet placeholder", ["Create a Padlet wall for this technology.", "Share → Embed in your blog or website → paste the <code>&lt;iframe&gt;</code> here."])}
        </div>
      </div>

    </div>
  </div>
</section>

<div class="wrap">{pager}</div>
""" + FOOT.format(root=root)

# ------------------------------------------------------------------ index
def index_page():
    def cat(t):
        ty = t["type"].lower()
        return "robotics" if "robot" in ty else "immersive" if ("immersive" in ty or "wearable" in ty) else "fabrication" if "fabrication" in ty else "media"
    def stat(t):
        st = t["status"].lower()
        return "ready" if st.startswith("ready") else "training" if st.startswith("training") else "pending"
    ordered = sorted(techs, key=lambda t: {"ready": 0, "pending": 1, "training": 2}[stat(t)])
    cards = "\n".join(f"""      <li class="{'featured ' if stat(t)=='ready' else ''}" data-cat="{cat(t)}" data-stat="{stat(t)}"><a href="tech/{t['id']}.html">
        <img src="{t['image']}" alt="{e(t['name'])}" loading="lazy">
        <div class="body"><span class="tag">LAB-{t['num']}</span><div class="name">{e(t['name'])}</div>
        <div class="sub">{e(t['type'])} · {e(t['use'])}</div>{pill(t['status'])}{'<span class="ready-note">Book a demo this week →</span>' if stat(t)=='ready' else ''}</div></a></li>""" for t in ordered)
    return head("What's in the Lab — Technology Showcase", "Technologies available in the lab for teaching and research, with ideas for putting them to work.", "", on="tech") + f"""
<section class="hero" id="top">
  <div class="wrap">
    <span class="tag">Technology showcase · Fall 2026</span>
    <h1>What's in <b>the Lab</b></h1>
    <p>Eleven pieces of equipment, two of them ready to demo this week, the rest being set up. Pick one, see what it does, and tell us how you would use it.</p>
    <div class="meta">
      <div><span>Lab</span>Lab name</div>
      <div><span>Institution</span>Department · University</div>
      <div><span>Contact</span>Coordinator name · email</div>
    </div>
  </div>
</section>

<section class="block" id="technologies">
  <div class="wrap">
    <h2>Technologies</h2><span class="ul-mark"></span>
    <div class="filters" id="filters">
      <button class="on" data-f="all">All</button>
      <button data-f="stat:ready">Ready now</button>
      <button data-f="stat:pending">Being set up</button>
      <button data-f="stat:training">Nobody has tried yet</button>
      <button data-f="cat:robotics">Robotics</button>
      <button data-f="cat:immersive">Immersive &amp; wearable</button>
      <button data-f="cat:fabrication">Fabrication</button>
      <button data-f="cat:media">Audio &amp; electronics</button>
    </div>
    <ul class="gallery" id="gallery">
{cards}
    </ul>
  </div>
</section>

<section class="block" id="about">
  <div class="wrap">
    <h2>How this works</h2><span class="ul-mark"></span>
    <p>One page per piece of equipment: our own photo, what it is in plain words, what is in the box, who has used it so far, and ideas for courses and studies. Every page ends with a short demo video, a thirty-second “I'm interested” form and an idea wall where you can see what colleagues have already proposed. The inventory code (LAB-01, LAB-02…) is the same one printed on the label of the equipment itself.</p>
    <h3>Status labels</h3>
    <div class="strip">
      <div><span>Ready to demo</span><b>Set up and working; book a session</b></div>
      <div><span>Setup pending</span><b>Assembly, charging or configuration still needed</b></div>
      <div><span>Training needed</span><b>No one has used it yet</b></div>
      <div><span>In use</span><b>Currently booked by a project</b></div>
    </div>
  </div>
</section>

<section class="collab">
  <div class="wrap">
    <span class="tag">Next steps</span>
    <h2 style="font-size:2rem;margin-top:.6rem">Have an idea? Let's collaborate</h2>
    <p>If a technology sparks an idea for a lesson, an assignment, a thesis or a study, we would like to hear it — and we can help with setup, training and design.</p>
    <a class="cta" href="collaborate.html">Book a demo or share an idea</a>
  </div>
</section>
<script>
  (function () {{
    var btns = document.querySelectorAll('#filters button'), items = document.querySelectorAll('#gallery li');
    btns.forEach(function (b) {{ b.addEventListener('click', function () {{
      btns.forEach(function (x) {{ x.classList.remove('on'); }}); b.classList.add('on');
      var f = b.dataset.f.split(':');
      items.forEach(function (li) {{
        var show = f[0] === 'all' || li.dataset[f[0]] === f[1];
        li.classList.toggle('hide', !show);
      }});
    }}); }});
  }})();
</script>
""" + FOOT.format(root="")

# ------------------------------------------------------------------ lab page
def lab_page():
    return head("The lab — What's in the Lab", "Who we are, where we are, and how to use the lab.", "", on="lab") + """
<section class="hero small">
  <div class="wrap">
    <span class="tag">Who we are</span>
    <h1>The <b>lab</b></h1>
    <p>A small space with a lot of equipment and a short list of rules.</p>
  </div>
</section>
<section class="block">
  <div class="wrap">
    <div class="labgrid">
      <div>
        <!-- Replace with a wide photo of the room, with people in it if possible: images/lab-room.jpg -->
        <div class="photo-ph">Photo of the room<br><small>images/lab-room.jpg · wide shot, people welcome</small></div>
      </div>
      <div>
        <h2>What this place is for</h2><span class="ul-mark"></span>
        <!-- Two or three sentences in your own words: why the lab exists, who set it up, what you hope people do here. -->
        <p>[Two or three sentences in the team's own words: why the lab exists, who set it up, and what you hope people will do here. Mention one thing that already happened in it.]</p>
        <h3>Where and when</h3>
        <div class="strip" style="grid-template-columns:1fr 1fr">
          <div><span>Room</span><b>Building · Room</b></div>
          <div><span>Open hours</span><b>Mon–Fri, 9 am – 5 pm</b></div>
          <div><span>Coordinator</span><b>Name</b></div>
          <div><span>Email</span><b>name@university.edu</b></div>
        </div>
      </div>
    </div>

    <h2 style="margin-top:2.5rem">Team</h2><span class="ul-mark"></span>
    <!-- One line per person: name, role, what to ask them about. Add a photo if you like. -->
    <ul>
      <li><strong>[Name]</strong> — coordinator. Ask about: bookings, new equipment, collaborations.</li>
      <li><strong>[Name]</strong> — graduate assistant. Ask about: VR headsets, Omni One.</li>
      <li><strong>[Name]</strong> — graduate assistant. Ask about: robots, 3D printers, Cricut.</li>
    </ul>

    <h2 style="margin-top:2.5rem">House rules</h2><span class="ul-mark"></span>
    <ul>
      <li>Book first. Even a quick look — it keeps the equipment where we expect it.</li>
      <li>Sign the sheet when you take something out; loans are up to two weeks.</li>
      <li>Put it back charged. Batteries and chargers live in the labelled drawer.</li>
      <li>Recording people? Ask them first. Consent forms are in the folder by the door.</li>
      <li>Something broke? Tell us the same day. Nobody will be upset; silence is the only problem.</li>
    </ul>
  </div>
</section>
""" + FOOT.format(root="")

# ------------------------------------------------------------------ collaborate
def collaborate_page():
    return head("Have an idea? Let's collaborate — What's in the Lab", "Book a demo, borrow equipment or propose a project.", "", on="collab") + f"""
<section class="hero small">
  <div class="wrap">
    <span class="tag">Next steps</span>
    <h1>Have an idea? <b>Let's collaborate</b></h1>
    <p>Nothing in this catalogue needs to be used exactly as described. Small experiments are welcome; most of our projects started as one.</p>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <h2>How it usually goes</h2>
    <div class="collab" style="padding:1.5rem 1.5rem 1rem;border-radius:10px">
    <ol>
      <li><strong>Share the idea.</strong> Tell us the idea in a few lines — the course or project, the technology, and what you would like students or participants to do.</li>
      <li><strong>Book a demo.</strong> We set up the equipment and walk you through it in about 30 minutes. Bring a colleague or a student assistant if you like.</li>
      <li><strong>Run a pilot.</strong> Try it in one class or one pilot session. We can be present the first time.</li>
      <li><strong>Build on it.</strong> Together we refine the activity or protocol, document it, and add it to this catalogue as an example for others.</li>
    </ol>
    </div>

    <div class="strip" style="margin-top:2rem">
      <div><span>Coordinator</span><b>Name</b></div>
      <div><span>Email</span><b>name@university.edu</b></div>
      <div><span>Office</span><b>Building · Room</b></div>
      <div><span>Open hours</span><b>Mon–Fri, 9 am – 5 pm</b></div>
    </div>
    <h3>What we can offer</h3>
    <ul>
      <li>Hands-on training sessions for instructors, students and research assistants.</li>
      <li>Help designing activities, assessment rubrics and research protocols around the equipment.</li>
      <li>Technical support during the first sessions and troubleshooting afterwards.</li>
      <li>Space for workshops, recordings and small group work; equipment loans of up to two weeks.</li>
    </ul>
  </div>
</section>

<section class="interact">
  <div class="wrap">
    <span class="tag">Get involved</span>
    <h2>Book a demo, propose a project</h2>
    <div class="igrid">
      <div class="ibox">
        <h3>Book a demo</h3>
        <p>Pick a 30-minute slot and tell us which technologies you want to see.</p>
        <div class="embed tall">
          <!-- GOOGLE CALENDAR appointment schedule: Calendar → appointment schedule → Share → Embed → paste the <iframe> here.
               Or embed the "Book a demo" Google Form (questions in FORMS.docx). -->
          {placeholder("Booking placeholder", ["Option A: Google Calendar appointment schedule → Share → Embed.", "Option B: the “Book a demo” Google Form → Send → <code>&lt;&gt;</code> → paste the <code>&lt;iframe&gt;</code> here."])}
        </div>
      </div>
      <div class="ibox">
        <h3>Propose a project or activity</h3>
        <p>A few lines are enough. We will reply within a week.</p>
        <div class="embed tall">
          <!-- GOOGLE FORM "Project idea": Forms → Send → < > → paste the <iframe> here. -->
          {placeholder("Google Form placeholder — Project idea", ["Create the “Propose a project” form (questions in FORMS.docx).", "Send → <code>&lt;&gt;</code> Embed HTML → paste the <code>&lt;iframe&gt;</code> here."])}
        </div>
      </div>
      <div class="ibox full">
        <h3>What should we add next?</h3>
        <p>One question, one click: vote for the technology you would most like to see in the lab, or the training you would attend.</p>
        <div class="embed" style="aspect-ratio:auto;height:420px">
          <!-- GOOGLE FORM "Quick poll" (single question; share the results chart link next to it). -->
          {placeholder("Google Form placeholder — Quick poll", ["Create the “Quick poll” form (questions in FORMS.docx).", "Send → <code>&lt;&gt;</code> → paste the <code>&lt;iframe&gt;</code> here."])}
        </div>
      </div>
    </div>
  </div>
</section>
""" + FOOT.format(root="")

# ------------------------------------------------------------------ write
if False:
    shutil.rmtree(OUT)
os.makedirs(f"{OUT}/tech", exist_ok=True); 
open(f"{OUT}/index.html", "w").write(index_page())
open(f"{OUT}/collaborate.html", "w").write(collaborate_page())
open(f"{OUT}/lab.html", "w").write(lab_page())
for i, t in enumerate(techs):
    open(f"{OUT}/tech/{t['id']}.html", "w").write(tech_page(i, t))
print("pages:", 2 + len(techs))
