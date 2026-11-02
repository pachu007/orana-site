#!/usr/bin/env python3
"""
Orana blog generator (no dependencies).

Usage:  python3 tools/build_blog.py
Rebuilds blog/ (index + one folder per post), sitemap.xml and the "Guías"
section of llms.txt from the POSTS list below.

TO ADD A POST: copy one entry in POSTS, change slug/title/etc, run the script,
commit and push. When the final domain is connected, change BASE only.
"""
import html, json, os, re

BASE = "https://pachu007.github.io/orana-site/"      # <- change when the domain is connected
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORG = "Orana Pilates & Balance"
STUDIO_ID = BASE + "#studio"
OG = BASE + "assets/img/og.jpg"
TODAY = "2026-11-02"
ASSET_V = "20261102b"   # bump when CSS/JS change (avoids stale cache)

WA_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# --------------------------------------------------------------------------- posts
# body = list of blocks: ("h2", text) | ("p", html) | ("ul", [html,...]) | ("table", head, rows) | ("sat",) | ("tip", html)
POSTS = [
 {
  "slug": "pilates-para-principiantes-riobamba",
  "title": "Pilates para principiantes en Riobamba: qué esperar de tu primera clase",
  "desc": "Guía para tu primera clase de pilates en Riobamba: si necesitas experiencia, qué llevar, cuánto cuesta, horarios y cómo reservar en Orana.",
  "date": TODAY,
  "read": "3 min",
  "answer": "No necesitas experiencia previa. En Orana la clase individual cuesta $5, dura 60 minutos, y reservas por WhatsApp (+593 98 583 4572). Lleva ropa deportiva cómoda y tu botella de agua, y avisa al llegar que es tu primera vez.",
  "body": [
   ("h2", "¿Necesito experiencia para empezar pilates?"),
   ("p", "No. Las sesiones de Orana están pensadas para que empieces y avances según tu propio nivel. Si nunca has hecho pilates, solo cuéntanos al llegar para que el equipo te oriente desde el primer movimiento."),
   ("h2", "¿Qué debo llevar a mi primera clase?"),
   ("ul", ["Ropa deportiva cómoda, que te deje moverte con libertad.", "Tu botella de agua.", "Ganas de probar: cada clase dura 60 minutos."]),
   ("h2", "¿Cuánto cuesta una clase de pilates en Riobamba?"),
   ("p", "En Orana puedes probar con una <b>clase individual de $5</b>. Si después quieres venir seguido, los planes mensuales bajan el costo por clase:"),
   ("table", ["Opción", "Precio", "Costo por clase"], [
      ["Clase individual", "$5", "$5,00"],
      ["Plan Harmony · 8 clases", "$25", "$3,13"],
      ["Plan Balance · 12 clases", "$35", "$2,92"],
      ["Plan Orana · 20 clases", "$45", "$2,25"]]),
   ("p", "También hay planes de 3, 6 y 12 meses. Los precios de todos están en la <a href=\"{root}#planes\">sección de planes</a>."),
   ("h2", "¿En qué horarios puedo ir?"),
   ("p", "Hay clases de 60 minutos en la mañana (06:00 a 10:00) y en la tarde-noche (17:00 a 21:00). Eso permite encajar una clase antes del trabajo o después de él."),
   ("h2", "¿Cómo reservo?"),
   ("p", "Escríbenos por WhatsApp al <b>+593 98 583 4572</b> con el día y el horario que prefieres, y reservamos tu lugar. El estudio está en Galería Shopping, Girasoles y Av. Antonio José de Sucre, Riobamba."),
   ("p", "Si prefieres probar en un ambiente más relajado, mira la <a href=\"{root}blog/que-hacer-en-riobamba-el-sabado/\">clase abierta de los sábados</a>."),
  ],
  "faq": [
   ("¿Necesito experiencia previa para hacer pilates?", "No. En Orana puedes empezar sin experiencia y avanzar a tu propio ritmo."),
   ("¿Cuánto cuesta una clase de pilates en Riobamba?", "En Orana la clase individual cuesta $5. Los planes mensuales empiezan en $25 por 8 clases."),
   ("¿Cuánto dura una clase?", "Cada clase dura 60 minutos."),
  ],
 },
 {
  "slug": "reformer-mat-barre-cual-elegir",
  "title": "Pilates Reformer, Mat o Barre: ¿cuál elegir?",
  "desc": "Diferencias entre Pilates Reformer, Pilates Mat y Barre, qué trabaja cada uno y por qué en Orana (Riobamba) no tienes que elegir solo uno.",
  "date": TODAY,
  "read": "3 min",
  "answer": "Reformer trabaja con una cama de resortes, Mat usa tu propio peso en el suelo y Barre mezcla ballet, pilates y entrenamiento funcional. En Orana no tienes que elegir uno: las sesiones combinan los tres, más pesas ligeras y cardio en algunas clases.",
  "body": [
   ("h2", "Las diferencias en una tabla"),
   ("table", ["Método", "Cómo se trabaja", "Qué se busca"], [
      ["Pilates Reformer", "En la cama Reformer, un equipo con carro deslizante y resortes", "Fuerza, estabilidad, control y movilidad"],
      ["Pilates Mat", "En el mat, con respiración y tu propio peso corporal; se pueden sumar accesorios", "Control, respiración y trabajo de todo el cuerpo"],
      ["Barre", "Movimientos pequeños y precisos inspirados en ballet, pilates y entrenamiento funcional", "Fuerza, resistencia y equilibrio"]]),
   ("h2", "¿Qué es el Pilates Reformer?"),
   ("p", "Es pilates sobre una cama Reformer. Los resortes dan resistencia y el carro se desliza, así que cada ejercicio exige control. En Orana lo usamos para trabajar fuerza, estabilidad, control y movilidad, con movimientos conscientes que ayudan a fortalecer el cuerpo y mejorar la postura."),
   ("h2", "¿Qué es el Pilates Mat?"),
   ("p", "Es pilates en el suelo, sobre un mat. No necesitas una máquina: trabajas con control, respiración y tu propio peso. A veces sumamos accesorios para que la clase sea más dinámica y desafiante."),
   ("h2", "¿Qué es Barre?"),
   ("p", "Barre toma ideas del ballet, del pilates y del entrenamiento funcional. Son movimientos pequeños y muy precisos que hacen trabajar cada músculo. Piensa en fuerza, resistencia y equilibrio."),
   ("h2", "¿Cuál me conviene si estoy empezando?"),
   ("p", "Cualquiera de los tres sirve para empezar: no se necesita experiencia previa. En Orana, además, no tienes que decidir de antemano. Un día puede ser el trabajo profundo del Reformer, otro día Barre y otro una dosis de cardio con spinning."),
   ("tip", "Si no sabes por dónde empezar, escríbenos por WhatsApp y te recomendamos horario y clase. La clase individual cuesta $5."),
   ("p", "¿Primera vez? Lee <a href=\"{root}blog/pilates-para-principiantes-riobamba/\">qué esperar de tu primera clase</a>."),
  ],
  "faq": [
   ("¿Tengo que elegir entre Reformer, Mat y Barre?", "No necesariamente. La propuesta de Orana integra diferentes disciplinas dentro de la misma experiencia."),
   ("¿Qué es el Pilates Reformer?", "Es pilates sobre una cama Reformer, un equipo con carro deslizante y resortes, para trabajar fuerza, estabilidad, control y movilidad."),
   ("¿El Pilates Mat necesita equipo?", "No. Se trabaja sobre un mat con control, respiración y tu propio peso corporal; se pueden sumar accesorios."),
  ],
 },
 {
  "slug": "que-hacer-en-riobamba-el-sabado",
  "title": "Qué hacer en Riobamba el sábado: clase de pilates abierta a todos por $5",
  "desc": "Todos los sábados Orana abre una clase especial de pilates en Riobamba por $5, para mujeres y hombres. Precios, plan de 4 sábados y cómo reservar.",
  "date": TODAY,
  "read": "2 min",
  "answer": "Cada sábado Orana abre una clase especial al público por $5, para mujeres y hombres, en Galería Shopping. Con Plan Orana activo es gratis y con otros planes activos cuesta $3. La clase y la modalidad pueden cambiar cada semana: confirma por WhatsApp.",
  "body": [
   ("sat",),
   ("h2", "¿Cuánto cuesta la clase de sábado?"),
   ("table", ["Tu situación", "Por clase"], [
      ["Plan Orana activo", "Gratis"],
      ["Otros planes activos", "$3"],
      ["Público general (mujeres y hombres)", "$5"]]),
   ("p", "Hay además un <b>Plan 4 sábados por $15</b>, es decir, $3,75 por clase si vienes los cuatro sábados."),
   ("h2", "¿Para quién es?"),
   ("p", "Para quien quiere conocer Orana sin comprometerse con un plan: el estudio, la experiencia y la comunidad. Está abierta a mujeres y hombres, y no necesitas experiencia previa."),
   ("h2", "¿Dónde y a qué hora?"),
   ("p", "En Galería Shopping, Girasoles y Av. Antonio José de Sucre, Riobamba. La hora habitual es 08H00, pero el horario y la modalidad de cada sábado pueden variar, así que confirma antes de ir."),
   ("p", "El estudio también tiene cafetería, por si quieres quedarte un rato después de la clase."),
   ("h2", "¿Cómo reservo mi lugar?"),
   ("p", "Escríbenos por WhatsApp al <b>+593 98 583 4572</b>, o toca el botón de arriba: el mensaje sale con la fecha del próximo sábado ya escrita."),
   ("p", "Si es tu primera vez, mira <a href=\"{root}blog/pilates-para-principiantes-riobamba/\">qué esperar de tu primera clase</a>."),
  ],
  "faq": [
   ("¿Hay clases de pilates los sábados en Riobamba?", "Sí. Cada sábado Orana abre una clase especial al público, para mujeres y hombres, por $5."),
   ("¿Cuánto cuesta el Plan 4 sábados?", "$15 por cuatro sábados, es decir, $3,75 por clase."),
   ("¿La clase de sábado es siempre a la misma hora?", "La hora habitual es 08H00, pero el horario y la modalidad pueden variar cada semana. Confirma por WhatsApp."),
  ],
 },
]

# --------------------------------------------------------------------------- templates
e = html.escape

def shell(root, title, desc, canonical, body, schema, og_type="article"):
    return f"""<!doctype html>
<html lang="es-EC">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#F5F0E8">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="es_EC">
<meta property="og:image" content="{OG}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css?v={ASSET_V}">
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="nav">
  <div class="nav-in">
    <a class="logo" href="{root}" aria-label="Orana pilates &amp; balance, inicio"><img class="logo-img" src="{root}assets/img/wordmark-mocha.png" width="863" height="305" alt="Orana pilates &amp; balance"></a>
    <nav class="links" aria-label="Principal">
      <a href="{root}#experiencia">Experiencia</a>
      <a href="{root}#sabados">Sábados</a>
      <a href="{root}#horarios">Horarios</a>
      <a href="{root}#planes">Planes</a>
      <a href="{root}blog/">Blog</a>
      <a href="{root}#visitanos">Visítanos</a>
    </nav>
    <a class="btn btn-dark" data-wa="Hola Orana, quiero reservar mi clase." href="#">Reserva tu clase {WA_ARROW}</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="ft">
      <div>
        <a class="logo" href="{root}" aria-label="Orana pilates &amp; balance, inicio"><img class="logo-img logo-foot" src="{root}assets/img/logo-cream.png" width="863" height="599" alt="Orana pilates &amp; balance" loading="lazy"></a>
        <p style="margin-top:16px">Galería Shopping<br>Girasoles y Av. Antonio José de Sucre<br>Riobamba, Ecuador</p>
      </div>
      <ul>
        <li><a data-wa="Hola Orana, tengo una pregunta." href="#">WhatsApp: +593 98 583 4572</a></li>
        <li><a href="https://www.instagram.com/oranapilates.ec/" target="_blank" rel="noopener">Instagram: @oranapilates.ec</a></li>
        <li><a href="{root}blog/">Blog</a></li>
      </ul>
    </div>
    <p class="copy">© <span id="yr">2026</span> Orana Pilates &amp; Balance. Todos los derechos reservados.</p>
  </div>
</footer>
<script src="{root}assets/js/site-data.js?v={ASSET_V}"></script>
<script src="{root}assets/js/main.js?v={ASSET_V}"></script>
</body>
</html>
"""

def render_block(b, root):
    k = b[0]
    if k == "h2":
        return f"<h2>{e(b[1])}</h2>"
    if k == "p":
        return "<p>" + b[1].replace("{root}", root) + "</p>"
    if k == "ul":
        return "<ul>" + "".join(f"<li>{i}</li>" for i in b[1]) + "</ul>"
    if k == "tip":
        return f'<p class="tip">{b[1]}</p>'
    if k == "table":
        head = "".join(f'<th scope="col">{e(h)}</th>' for h in b[1])
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b[2])
        return f'<div class="tbl-wrap"><table class="post-tbl"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    if k == "sat":
        return ('<div class="callout"><p class="eyebrow">Próxima clase de sábado</p>'
                '<p class="callout-big" id="sat-date">Este sábado</p>'
                '<p class="callout-sub"><span id="sat-time">08H00</span> · Valor $5 · Galería Shopping</p>'
                f'<a class="btn btn-dark" data-sat-wa href="#">Reservar sábado {WA_ARROW}</a></div>')
    raise ValueError(k)

def post_page(p):
    root = "../../"
    url = f"{BASE}blog/{p['slug']}/"
    body_html = "\n".join(render_block(b, root) for b in p["body"])
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    others = [o for o in POSTS if o["slug"] != p["slug"]]
    more = "".join(f'<li><a href="{root}blog/{o["slug"]}/">{e(o["title"])}</a></li>' for o in others)
    schema = {"@context": "https://schema.org", "@graph": [
      {"@type": "Article", "@id": url + "#article", "headline": p["title"], "description": p["desc"],
       "inLanguage": "es-EC", "datePublished": p["date"], "dateModified": p["date"],
       "mainEntityOfPage": url, "image": [OG],
       "author": {"@id": STUDIO_ID}, "publisher": {"@id": STUDIO_ID}},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "blog/"},
        {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
      {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]}
    body = f"""<article class="post">
  <div class="wrap post-in">
    <nav class="crumbs" aria-label="Migas de pan"><a href="{root}">Inicio</a> / <a href="{root}blog/">Blog</a></nav>
    <p class="eyebrow">Guía · {p['read']} de lectura</p>
    <h1>{e(p['title'])}</h1>
    <p class="post-meta">Por el equipo de Orana · Actualizado <time datetime="{p['date']}">{p['date']}</time></p>
    <div class="answer"><b>Respuesta rápida.</b> {e(p['answer'])}</div>
    <div class="prose">
{body_html}
    <h2>Preguntas frecuentes</h2>
    <div class="faq post-faq">{faq_html}</div>
    </div>
    <aside class="post-cta">
      <h2>¿Lista para tu clase?</h2>
      <p>Escríbenos por WhatsApp y reservamos tu lugar en Galería Shopping, Riobamba.</p>
      <a class="btn btn-light" data-wa="Hola Orana, leí su blog y quiero reservar una clase." href="#">Reservar por WhatsApp {WA_ARROW}</a>
    </aside>
    <div class="more"><p class="eyebrow">Sigue leyendo</p><ul>{more}</ul></div>
  </div>
</article>"""
    return shell(root, f"{p['title']} | Orana Pilates & Balance", p["desc"], url, body, schema)

def index_page():
    root = "../"
    url = BASE + "blog/"
    cards = "".join(f"""<a class="post-card" href="{root}blog/{p['slug']}/">
  <p class="eyebrow">Guía · {p['read']}</p>
  <h2>{e(p['title'])}</h2>
  <p>{e(p['desc'])}</p>
  <span class="more-link">Leer guía {WA_ARROW}</span>
</a>""" for p in POSTS)
    schema = {"@context": "https://schema.org", "@graph": [
      {"@type": "Blog", "@id": url + "#blog", "url": url, "name": "Blog de Orana Pilates & Balance",
       "inLanguage": "es-EC", "publisher": {"@id": STUDIO_ID},
       "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{BASE}blog/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]},
    ]}
    body = f"""<section class="post blog-index">
  <div class="wrap post-in">
    <p class="eyebrow">Blog Orana</p>
    <h1>Pilates en Riobamba, <em>explicado simple.</em></h1>
    <p class="lede">Guías cortas con precios, horarios y respuestas reales del estudio.</p>
    <div class="post-grid">{cards}</div>
  </div>
</section>"""
    return shell(root, "Blog | Orana Pilates & Balance, Riobamba", "Guías de pilates en Riobamba: primera clase, Reformer vs Mat vs Barre, clase de sábado, precios y horarios de Orana.", url, body, schema, "website")

def write(path, text):
    full = os.path.join(ROOT_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)

def main():
    write("blog/index.html", index_page())
    for p in POSTS:
        write(f"blog/{p['slug']}/index.html", post_page(p))
    urls = [(BASE, "1.0", "weekly"), (BASE + "blog/", "0.8", "weekly")] + [(f"{BASE}blog/{p['slug']}/", "0.7", "monthly") for p in POSTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <!-- Generated by tools/build_blog.py. BASE is set there. -->\n'
    sm += "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n" for u, pr, c in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    lp = os.path.join(ROOT_DIR, "llms.txt")
    txt = open(lp, encoding="utf-8").read()
    txt = re.split(r"\n## Guías\n", txt)[0].rstrip() + "\n\n## Guías\n" + "".join(f"- {p['title']}: {BASE}blog/{p['slug']}/\n" for p in POSTS)
    open(lp, "w", encoding="utf-8").write(txt)
    print("built", len(POSTS), "posts")

if __name__ == "__main__":
    main()
