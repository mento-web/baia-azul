#!/usr/bin/env python3
"""
build.py
========
Generates every HTML page of the Baía Azul site from tools/content.py.

    python3 tools/build.py

No dependencies beyond the Python standard library. Output goes to the
repository root so the folder can be served as it is by any static host:

    index.html                  list of passeios and transfers, with filters
    passeios/<slug>.html        one page per passeio
    transfers.html              timetables and the private transfer
    sobre.html                  the agency, where it is, contact
    duvidas.html                FAQ and cancellation rules
    politicas.html              privacy, cancellation, terms of use
    creditos.html               photo credits (required by the photo licences)
    404.html, robots.txt, sitemap.xml (only when SITE["url"] is set)

Structure of this file
  1. Small helpers (escaping, links, images)
  2. Shared page parts (head, navigation, booking dialog, footer)
  3. Reusable blocks (hero, tour band, fact rows)
  4. Pages
  5. Write everything to disk
"""
import html
import json
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE, PASSEIOS, TRANSFERS, FAQ, CANCELAMENTO, TIPOS, SAIDAS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDITS = json.load(open(os.path.join(ROOT, "assets", "img", "credits.json")))
CSS_VERSION = "1"


# =============================================================================
# 1. HELPERS
# =============================================================================
def e(text):
    """Escape text for HTML."""
    return html.escape(str(text), quote=True)


def whatsapp_base():
    """Address every WhatsApp link starts with. Falls back to the contact picker when no number is set."""
    return f"https://wa.me/{SITE['whatsapp']}" if SITE["whatsapp"] else "https://api.whatsapp.com/send"


def whatsapp(message):
    return f"{whatsapp_base()}?text={quote(message)}"


def book_message(name):
    return f"Olá! Quero reservar com a Baía Azul: *{name}*."


def ask_message(name):
    return f"Olá! Tenho uma dúvida sobre: *{name}*."


def picture(slug, sizes, root, lazy=True, cls=""):
    """Responsive photo: WebP in three widths, JPEG fallback, alt text from the credits manifest."""
    base = f"{root}assets/img/{slug}"
    alt = CREDITS[slug]["alt"]
    loading = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (
        f'<picture>'
        f'<source type="image/webp" srcset="{base}-640.webp 640w, {base}-1200.webp 1200w, {base}-1920.webp 1920w" sizes="{sizes}">'
        f'<img src="{base}-1200.jpg" alt="{e(alt)}" width="1200" height="675" {loading}{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
        f'</picture>'
    )


def bullets_to_text(card):
    """Card copy keeps its bullet facts on the same line, separated by a middle dot."""
    return e(card).replace(" • ", ' <span aria-hidden="true">•</span> ')


LOGO_MARK = (
    '<svg viewBox="0 0 30 20" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" aria-hidden="true">'
    '<circle cx="15" cy="6" r="4.2"/>'
    '<path d="M1 13.5c2.3 0 2.3-1.8 4.7-1.8s2.3 1.8 4.6 1.8 2.4-1.8 4.7-1.8 2.3 1.8 4.7 1.8 2.3-1.8 4.6-1.8 2.4 1.8 4.7 1.8"/>'
    '<path d="M1 18.3c2.3 0 2.3-1.8 4.7-1.8s2.3 1.8 4.6 1.8 2.4-1.8 4.7-1.8 2.3 1.8 4.7 1.8 2.3-1.8 4.6-1.8 2.4 1.8 4.7 1.8"/>'
    '</svg>'
)


# =============================================================================
# 2. SHARED PAGE PARTS
# =============================================================================
def head(title, description, root, path, image="hero-morro-aerea", schema=None):
    full_title = f"{title} · {SITE['name']}" if title != SITE["name"] else f"{SITE['name']} · {SITE['tagline']}"
    tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{e(full_title)}</title>",
        f'<meta name="description" content="{e(description)}">',
        '<meta name="theme-color" content="#004777">',
        '<meta name="format-detection" content="telephone=no">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:locale" content="pt_BR">',
        f'<meta property="og:site_name" content="{e(SITE["name"])}">',
        f'<meta property="og:title" content="{e(full_title)}">',
        f'<meta property="og:description" content="{e(description)}">',
    ]
    if SITE["url"]:
        url = SITE["url"].rstrip("/")
        tags += [
            f'<link rel="canonical" href="{url}/{path}">',
            f'<meta property="og:url" content="{url}/{path}">',
            f'<meta property="og:image" content="{url}/assets/img/{image}-1200.jpg">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
    tags += [
        f'<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">',
        f'<link rel="preload" href="{root}assets/fonts/josefin-sans-regular.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="preload" href="{root}assets/fonts/raleway-regular.woff2" as="font" type="font/woff2" crossorigin>',
        # The hero photo is the largest element on every page, so the browser is told about it early
        f'<link rel="preload" as="image" type="image/webp" fetchpriority="high" '
        f'imagesrcset="{root}assets/img/{image}-640.webp 640w, {root}assets/img/{image}-1200.webp 1200w, {root}assets/img/{image}-1920.webp 1920w" imagesizes="100vw">',
        f'<link rel="stylesheet" href="{root}assets/css/site.css?v={CSS_VERSION}">',
    ]
    if schema:
        tags.append('<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>")
    return "<head>\n  " + "\n  ".join(tags) + "\n</head>"


def nav(root, current):
    def link(label, href, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a class="nav__link" href="{root}{href}"{cur}>{label}</a></li>'

    tours = "".join(f'<li><a href="{root}passeios/{p["slug"]}.html">{e(p["name"])}</a></li>' for p in PASSEIOS)
    return f"""
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
<header class="nav">
  <div class="nav__inner">
    <a class="logo" href="{root}index.html" aria-label="Baía Azul, página inicial">{LOGO_MARK}<span>Baía Azul</span></a>
    <button class="nav__burger" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    <nav class="nav__menu" id="menu" aria-label="Principal">
      <ul class="nav__list">
        <li class="nav__item">
          <button class="nav__link" type="button" aria-expanded="false" aria-controls="menu-passeios">Passeios <span class="nav__chevron" aria-hidden="true"></span></button>
          <div class="nav__dropdown" id="menu-passeios">
            <ul>
              {tours}
              <li><a href="{root}index.html#passeios">Todos os passeios</a></li>
            </ul>
          </div>
        </li>
        {link("Transfers", "transfers.html", "transfers")}
        {link("Sobre", "sobre.html", "sobre")}
        {link("Dúvidas", "duvidas.html", "duvidas")}
        {link("Contato", "sobre.html#contato", "contato")}
      </ul>
      <a class="btn btn--white nav__cta" href="{whatsapp('Olá! Quero fazer uma reserva com a Baía Azul.')}" target="_blank" rel="noopener" data-reservar="">Reservar</a>
    </nav>
  </div>
</header>"""


def booking_dialog():
    """One dialog per page. site.js opens it from any element that has data-reservar."""
    options = "".join(f'<option>{e(p["name"])}</option>' for p in PASSEIOS)
    transfer_options = "".join(f'<option>{e(t["name"])}</option>' for t in TRANSFERS)
    return f"""
<dialog class="dialog" id="reserva" aria-labelledby="reserva-titulo">
  <div class="dialog__inner">
    <button class="dialog__close" type="button" aria-label="Fechar"></button>
    <p class="eyebrow">Reserva</p>
    <h2 class="title" id="reserva-titulo">Monte o seu pedido</h2>
    <p class="dialog__intro">Preencha o que já souber. Ao enviar, o WhatsApp abre com a mensagem pronta e a nossa equipe confirma disponibilidade, horário e ponto de encontro.</p>
    <form class="form" id="reserva-form" data-whatsapp="{whatsapp_base()}">
      <div class="field field--full">
        <label for="r-produto">Passeio ou transfer</label>
        <div class="select"><select id="r-produto" name="produto" required>
          <optgroup label="Passeios">{options}</optgroup>
          <optgroup label="Transfers">{transfer_options}</optgroup>
          <option>Ainda não sei, quero uma sugestão</option>
        </select></div>
      </div>
      <div class="field field--wide-mobile">
        <label for="r-data">Data</label>
        <input id="r-data" name="data" type="date">
      </div>
      <div class="field">
        <label for="r-adultos">Adultos</label>
        <input id="r-adultos" name="adultos" type="number" min="1" max="60" value="2" inputmode="numeric" required>
      </div>
      <div class="field">
        <label for="r-criancas">Crianças</label>
        <input id="r-criancas" name="criancas" type="number" min="0" max="60" value="0" inputmode="numeric">
      </div>
      <div class="field field--full">
        <label for="r-nome">Seu nome</label>
        <input id="r-nome" name="nome" type="text" autocomplete="name">
      </div>
      <div class="field field--full">
        <label for="r-hospedagem">Onde você está hospedado</label>
        <input id="r-hospedagem" name="hospedagem" type="text" placeholder="Hotel, pousada ou bairro">
      </div>
      <div class="field field--full">
        <label for="r-obs">Observações</label>
        <textarea id="r-obs" name="obs" rows="2"></textarea>
      </div>
      <div class="form__foot">
        <button class="btn btn--primary btn--large" type="submit">Enviar pelo WhatsApp</button>
        <p class="form__hint">Nada é gravado neste site. Os dados seguem apenas na mensagem que você envia.</p>
      </div>
    </form>
  </div>
</dialog>"""


def footer(root):
    facts = [f"<span>{e(SITE['street'] + ', ' if SITE['street'] else '')}{e(SITE['neighbourhood'])}<br>{e(SITE['city'])}</span>",
             ]
    if SITE["hours"]:
        facts.append(f"<span>{e(SITE['hours'])}</span>")
    contact = [f'<a href="{whatsapp("Olá! Quero falar com a Baía Azul.")}" target="_blank" rel="noopener">'
               f'{e(SITE["whatsapp_display"]) if SITE["whatsapp_display"] else "Atendimento pelo WhatsApp"}</a>']
    if SITE["email"]:
        contact.append(f'<a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a>')
    if SITE["instagram"]:
        contact.append(f'<a href="https://www.instagram.com/{e(SITE["instagram"])}/" target="_blank" rel="noopener">@{e(SITE["instagram"])}</a>')
    facts.append("<span>" + "<br>".join(contact) + "</span>")

    legal = [f"© {SITE['year']} {e(SITE['name'])}"]
    if SITE["cnpj"]:
        legal.append(f"CNPJ {e(SITE['cnpj'])}")
    if SITE["cadastur"]:
        legal.append(f"Cadastur {e(SITE['cadastur'])}")

    return f"""
<footer class="footer">
  <nav class="footer__links" aria-label="Rodapé">
    <a href="{root}index.html#passeios">Passeios</a>
    <a href="{root}transfers.html">Transfers</a>
    <a href="{root}sobre.html">Sobre</a>
    <a href="{root}duvidas.html">Dúvidas</a>
    <a href="{root}duvidas.html#cancelamento">Cancelamento</a>
    <a href="{root}politicas.html">Privacidade e termos</a>
    <a href="{root}creditos.html">Créditos das fotos</a>
  </nav>
  <div class="footer__brand"><a class="logo" href="{root}index.html" aria-label="Baía Azul, página inicial">{LOGO_MARK}<span>Baía Azul</span></a></div>
  <div class="footer__facts">{''.join(facts)}</div>
  <div class="footer__small">
    <p>Os valores publicados são os de partida e são confirmados na reserva. Taxas de embarque e de entrada, quando existem, são pagas à parte e estão indicadas em cada passeio.</p>
    <p>{' · '.join(legal)}</p>
  </div>
</footer>"""


def page(title, description, root, path, current, body, image="hero-morro-aerea", schema=None, bar=""):
    return f"""<!doctype html>
<html lang="pt-BR">
{head(title, description, root, path, image, schema)}
<body>
{nav(root, current)}
<main id="conteudo">
{body}
</main>
{footer(root)}
{bar}
{booking_dialog()}
<script src="{root}assets/js/site.js?v={CSS_VERSION}" defer></script>
</body>
</html>
"""


# =============================================================================
# 3. REUSABLE BLOCKS
# =============================================================================
def hero(root, image, eyebrow, title, extra="", short=False, cue=True):
    long_title = " hero__title--long" if len(title) > 16 else ""
    return f"""
<section class="hero{' hero--short' if short else ''}">
  <div class="hero__bg">{picture(image, "100vw", root, lazy=False)}</div>
  <div class="hero__inner">
    <p class="hero__eyebrow">{e(eyebrow)}</p>
    <h1 class="hero__title{long_title}">{e(title)}</h1>
    {extra}
  </div>
  {'<a class="hero__cue" href="#inicio" aria-label="Ir para o conteúdo"></a>' if cue else ''}
</section>"""


def facts_row(items):
    return '<p class="facts">' + "".join(f"<span>{e(i)}</span>" for i in items) + "</p>"


def tour_band(root, index, item, kind):
    """One full width band. `kind` is "passeio" or "transfer"."""
    if kind == "passeio":
        href = f"{root}passeios/{item['slug']}.html"
        tipo, second = item["tipo"], "Ver detalhes"
    else:
        href = f"{root}transfers.html#{item['id']}"
        tipo, second = "transfer", "Ver horários" if item["go"] else "Saber mais"
    tint = " band--tint" if index % 2 == 0 else ""
    duration = f'<p class="tour__duration">{e(item["duration"])}</p>' if item["duration"] else ""
    return f"""
<section class="tour band{tint}" data-tipo="{tipo}" data-saida="{item['saida']}">
  <div class="container">
    <div class="tour__inner">
      <a class="tour__photo" href="{href}" tabindex="-1" aria-hidden="true">{picture(item['img'], "(max-width: 768px) 100vw, (max-width: 1023px) 42vw, 567px", root)}</a>
      <div class="tour__text">
        <div class="tour__top"><p class="eyebrow">{e(item['eyebrow'])}</p>{duration}</div>
        <h2 class="title"><a href="{href}">{e(item['title'])}</a></h2>
        {facts_row(item['facts'])}
        <p class="tour__desc">{bullets_to_text(item['card'])}</p>
        <div class="actions">
          <a class="btn btn--primary" href="{whatsapp(book_message(item['name']))}" target="_blank" rel="noopener" data-reservar="{e(item['name'])}">Reservar</a>
          <a class="btn btn--tertiary" href="{href}">{second}<span class="visually-hidden">: {e(item['name'])}</span></a>
        </div>
      </div>
    </div>
  </div>
</section>"""


def rows(pairs):
    out = ['<dl class="rows">']
    for label, value in pairs:
        if isinstance(value, list):
            value_html = "".join(f"<span>{e(v)}</span>" for v in value)
        else:
            value_html = e(value)
        out.append(f"<div><dt>{e(label)}</dt><dd>{value_html}</dd></div>")
    out.append("</dl>")
    return "".join(out)


def closing(root, eyebrow, title, text, name="", tint=True, second=None):
    message = book_message(name) if name else "Olá! Quero fazer uma reserva com a Baía Azul."
    second = second or ("Tirar dúvidas", f"{root}duvidas.html")
    return f"""
<section class="band{' band--tint' if tint else ''} closing">
  <div class="container">
    <p class="eyebrow">{e(eyebrow)}</p>
    <h2 class="title">{e(title)}</h2>
    <p>{e(text)}</p>
    <div class="actions">
      <a class="btn btn--primary btn--large" href="{whatsapp(message)}" target="_blank" rel="noopener" data-reservar="{e(name)}">Reservar</a>
      <a class="btn btn--tertiary btn--large" href="{second[1]}">{second[0]}</a>
    </div>
  </div>
</section>"""


# =============================================================================
# 4. PAGES
# =============================================================================
def page_home():
    root = ""
    tipo_options = "".join(f'<option value="{v}">{e(label)}</option>' for v, label in TIPOS)
    saida_options = "".join(f'<option value="{v}">{e(label)}</option>' for v, label in SAIDAS)
    filters = f"""
    <form class="filters" action="#passeios" aria-label="Filtrar passeios e transfers">
      <div class="select"><label class="visually-hidden" for="filtro-tipo">Tipo de passeio</label>
        <select id="filtro-tipo" name="tipo"><option value="">Todos os passeios</option>{tipo_options}</select></div>
      <div class="select"><label class="visually-hidden" for="filtro-saida">Ponto de saída</label>
        <select id="filtro-saida" name="saida"><option value="">Qualquer saída</option>{saida_options}</select></div>
    </form>
    <p class="visually-hidden" id="filtro-status" role="status" aria-live="polite"></p>"""

    bands, i = [], 0
    for p in PASSEIOS:
        bands.append(tour_band(root, i, p, "passeio")); i += 1
    for t in TRANSFERS:
        bands.append(tour_band(root, i, t, "transfer")); i += 1

    body = f"""
{hero(root, "hero-morro-aerea", "Salvador, Bahia", "Nossos passeios", filters).replace('href="#inicio"', 'href="#passeios"')}
<div id="passeios"></div>
{''.join(bands)}
<section class="band filter-empty" hidden>
  <div class="container">
    <h2 class="title">Nada por aqui</h2>
    <p>Nenhum passeio combina com os dois filtros ao mesmo tempo.</p>
    <div class="actions" style="justify-content:center;margin-top:29px"><button class="btn btn--primary" type="button" id="filtro-limpar">Ver todos</button></div>
  </div>
</section>
<section class="band band--tint">
  <div class="container">
    <div class="heading-center"><p class="eyebrow">Do Pelourinho para o mar</p><h2 class="title">Por que a Baía Azul</h2></div>
    <div class="cols">
      <div><h3 class="subtitle">Buscamos você</h3><p>No Aeroporto de Salvador, no seu hotel ou direto no Terminal Marítimo. Você diz onde está e nós organizamos o resto, para você e para a sua família.</p></div>
      <div><h3 class="subtitle">Gente daqui</h3><p>Uma equipe experiente, que conhece cada travessia, e guias bilíngues que gostam do que fazem. A viagem começa bem antes de você chegar à praia.</p></div>
      <div><h3 class="subtitle">Conforto no caminho</h3><p>Ônibus executivos com banheiro, TV, ar-condicionado e Wi-Fi, além de barcos, vans e carros privativos modernos. Segurança em cada trecho.</p></div>
    </div>
  </div>
</section>
{closing(root, "Reserva pelo WhatsApp", "Vamos montar a sua viagem", "Conte para onde quer ir e em que data. Respondemos pelo WhatsApp com disponibilidade, horário e ponto de encontro. Pagamento por cartão, PIX ou transferência.", tint=False)}"""

    schema = {
        "@context": "https://schema.org", "@type": "TravelAgency", "name": SITE["name"],
        "description": SITE["description"],
        "address": {"@type": "PostalAddress", "addressLocality": "Salvador", "addressRegion": "BA", "addressCountry": "BR",
                    "streetAddress": (SITE["street"] + ", " if SITE["street"] else "") + SITE["neighbourhood"]},
        "areaServed": "Bahia", "paymentAccepted": "Cartão de crédito, cartão de débito, PIX, transferência bancária",
    }
    if SITE["url"]:
        schema["url"] = SITE["url"]
    return page(SITE["name"], SITE["description"], root, "", "home", body, schema=schema)


def page_passeio(p, index):
    root = "../"
    nxt = PASSEIOS[(index + 1) % len(PASSEIOS)]
    price_line = p["facts"][0]

    steps = ""
    if p["steps"]:
        steps = f"""
<section class="band">
  <div class="container split split--narrow-first">
    <div><p class="eyebrow">Roteiro</p><h2 class="title">Como é o dia</h2></div>
    <ol class="steps">{''.join(f'<li><span>{e(s)}</span></li>' for s in p['steps'])}</ol>
  </div>
</section>"""

    photo2 = ""
    if p["img2"]:
        photo2 = f'<div class="photo-wide">{picture(p["img2"], "(max-width: 1023px) 100vw, 567px", root)}</div>'
    else:
        photo2 = f'<div class="photo-wide">{picture(p["img"], "(max-width: 1023px) 100vw, 567px", root)}</div>'

    body = f"""
{hero(root, p["img"], p["eyebrow"], p["title"], f'<p class="hero__lede">{e(p["lede"])}</p><a class="btn btn--white btn--large" href="{whatsapp(book_message(p["name"]))}" target="_blank" rel="noopener" data-reservar="{e(p["name"])}">Reservar</a>')}
<section class="band band--tint" id="inicio">
  <div class="container split">
    <div class="text">
      <p class="eyebrow">O passeio</p>
      <h2 class="title">{e(p['name'])}</h2>
      {''.join(f'<p>{e(par)}</p>' for par in p['body'])}
    </div>
    <div>
      {rows(p['rows'])}
      <div class="actions">
        <a class="btn btn--primary" href="{whatsapp(book_message(p['name']))}" target="_blank" rel="noopener" data-reservar="{e(p['name'])}">Reservar</a>
        <a class="btn btn--tertiary" href="{whatsapp(ask_message(p['name']))}" target="_blank" rel="noopener">Tirar dúvida no WhatsApp</a>
      </div>
    </div>
  </div>
</section>
{steps}
<section class="band{'' if not p['steps'] else ' band--tint'}">
  <div class="container split">
    {photo2}
    <div>
      <p class="eyebrow">Antes de ir</p>
      <h2 class="title">Bom saber</h2>
      <ul class="list">{''.join(f'<li>{e(k)}</li>' for k in p['know'])}</ul>
      <p style="margin-top:20px" class="text">Regras de cancelamento e formas de pagamento estão em <a href="{root}duvidas.html#cancelamento">Dúvidas</a>.</p>
    </div>
  </div>
</section>
<div class="visually-hidden"><h2>Próximo passeio</h2></div>
{tour_band(root, 0 if not p['steps'] else 1, nxt, "passeio").replace('<h2 class="title">', '<h3 class="title">').replace('</a></h2>', '</a></h3>')}
{closing(root, "Pronto para ir?", "Reserve pelo WhatsApp", "Escolha a data e o número de pessoas. A mensagem chega pronta e respondemos com a confirmação.", p["name"], tint=bool(p['steps']))}"""

    schema = {"@context": "https://schema.org", "@type": "TouristTrip", "name": p["name"], "description": p["lede"],
              "provider": {"@type": "TravelAgency", "name": SITE["name"]}}
    if p["price"]:
        schema["offers"] = {"@type": "AggregateOffer", "priceCurrency": "BRL", "lowPrice": p["price"]}

    bar = f"""
<div class="bar" aria-hidden="true">
  <div class="container bar__inner">
    <p class="bar__name">{e(p['name'])}</p>
    <div class="bar__side">
      <p class="bar__price">{e(price_line)}</p>
      <a class="btn btn--primary" href="{whatsapp(book_message(p['name']))}" target="_blank" rel="noopener" data-reservar="{e(p['name'])}">Reservar</a>
    </div>
  </div>
</div>"""
    return page(p["name"], f"{p['lede']} {p['facts'][0]}. Reserve pelo WhatsApp com a Baía Azul, em Salvador.",
                root, f"passeios/{p['slug']}.html", "passeios", body, image=p["img"], schema=schema, bar=bar)


def page_transfers():
    root = ""
    sections = []
    for i, t in enumerate(TRANSFERS):
        timetable = ""
        if t["go"]:
            timetable = (f'<h3 class="subtitle" style="margin-bottom:12px">{e(t["go_title"])}</h3>{rows(t["go"])}'
                         f'<h3 class="subtitle" style="margin-bottom:12px">{e(t["back_title"])}</h3>{rows(t["back"])}')
        else:
            timetable = f'<div class="photo-wide" style="margin-bottom:29px">{picture(t["img"], "(max-width: 1023px) 100vw, 567px", root)}</div>'
        sections.append(f"""
<section class="band{' band--tint' if i % 2 == 0 else ''}" id="{t['id']}">
  <div class="container split">
    <div class="text">
      <p class="eyebrow">{e(t['eyebrow'])}</p>
      <h2 class="title">{e(t['title'])}</h2>
      {''.join(f'<p>{e(par)}</p>' for par in t['body'])}
      {facts_row(t['facts'])}
    </div>
    <div>
      {timetable}
      <div class="actions">
        <a class="btn btn--primary" href="{whatsapp(book_message(t['name']))}" target="_blank" rel="noopener" data-reservar="{e(t['name'])}">Reservar</a>
        <a class="btn btn--tertiary" href="{whatsapp(ask_message(t['name']))}" target="_blank" rel="noopener">Tirar dúvida no WhatsApp</a>
      </div>
    </div>
  </div>
</section>""")

    body = f"""
{hero(root, "baia", "Todos os dias do ano", "Transfers", '<p class="hero__lede">De Salvador a Morro de São Paulo e a Boipeba, com busca no aeroporto, no hotel ou no Terminal Marítimo.</p>')}
<div id="inicio"></div>
{''.join(sections)}
<section class="band">
  <div class="container">
    <div class="heading-center"><p class="eyebrow">Como funciona</p><h2 class="title">Da sua porta até a ilha</h2></div>
    <div class="cols">
      <div><h3 class="subtitle">Buscamos você</h3><p>No Aeroporto de Salvador, no hotel em que você está ou no próprio Terminal Marítimo. É só avisar na reserva.</p></div>
      <div><h3 class="subtitle">Barco e estrada</h3><p>A viagem é semiterrestre: alterna trechos de mar e de terra. A nossa equipe acompanha as conexões, e você só precisa seguir o grupo.</p></div>
      <div><h3 class="subtitle">Conforto a bordo</h3><p>Ônibus executivos com banheiro, TV, ar-condicionado e Wi-Fi, além de barcos e vans modernos, com equipe experiente e guias bilíngues.</p></div>
    </div>
  </div>
</section>
{closing(root, "Todos os dias do ano", "Reserve o seu transfer", "Informe a data, o número de pessoas e de onde você sai. Se vier de avião, mande também o horário do voo.", "", tint=True)}"""
    return page("Transfers para Morro de São Paulo e Boipeba",
                "Transfer diário de Salvador para Morro de São Paulo e Boipeba, com busca no aeroporto, no hotel ou no Terminal Marítimo. Horários e transfer privativo.",
                root, "transfers.html", "transfers", body, image="baia")


def page_sobre():
    root = ""
    address = (SITE["street"] + ", " if SITE["street"] else "") + SITE["neighbourhood"] + ", " + SITE["city"]
    contact_rows = [("Onde", address)]
    if SITE["hours"]:
        contact_rows.append(("Atendimento", SITE["hours"]))
    if SITE["whatsapp_display"]:
        contact_rows.append(("WhatsApp", SITE["whatsapp_display"]))
    if SITE["email"]:
        contact_rows.append(("E-mail", SITE["email"]))
    if SITE["instagram"]:
        contact_rows.append(("Instagram", "@" + SITE["instagram"]))
    contact_rows.append(("Pagamento", "Cartão de crédito e débito, PIX e transferência"))

    body = f"""
{hero(root, "pelourinho", "Pelourinho, Salvador", "Sobre a Baía Azul", short=True)}
<section class="band band--tint" id="inicio">
  <div class="container split">
    <div class="text">
      <p class="eyebrow">Quem somos</p>
      <h2 class="title">Uma agência do Centro Histórico</h2>
      <p>A Baía Azul é uma agência de passeios e transfers com base no Pelourinho, em Salvador. Trabalhamos só com a Bahia, e é por isso que conhecemos bem cada trecho do caminho.</p>
      <p>Levamos você do Litoral Sul, com destaque para Morro de São Paulo e Boipeba, ao Litoral Norte de Salvador, passando pelas ilhas da Baía de Todos-os-Santos e pela Costa do Dendê.</p>
      <p>A nossa equipe é formada por profissionais experientes e atenciosos, e o atendimento é pessoal: você fala com gente, do primeiro contato ao desembarque.</p>
    </div>
    <div class="photo-wide">{picture("lacerda", "(max-width: 1023px) 100vw, 567px", root)}</div>
  </div>
</section>
<section class="band">
  <div class="container">
    <div class="heading-center"><p class="eyebrow">O que fazemos</p><h2 class="title">Três jeitos de viajar com a gente</h2></div>
    <div class="cols">
      <div><h3 class="subtitle">Passeios de um dia</h3><p>De escuna pela baía, de barco pelas piscinas naturais de Tinharé, de 4x4 até Garapuá ou de ônibus até a Praia do Forte. Você sai de manhã e volta no fim da tarde.</p><div class="actions" style="margin-top:20px"><a class="btn btn--tertiary" href="{root}index.html#passeios">Ver passeios</a></div></div>
      <div><h3 class="subtitle">Transfers diários</h3><p>Saídas de Salvador para Morro de São Paulo e Boipeba nos 365 dias do ano, com busca no aeroporto, no hotel ou no Terminal Marítimo.</p><div class="actions" style="margin-top:20px"><a class="btn btn--tertiary" href="{root}transfers.html">Ver horários</a></div></div>
      <div><h3 class="subtitle">Transfer privativo</h3><p>Carro, van ou ônibus só para o seu grupo, no horário que você escolher, com motoristas profissionais e experientes.</p><div class="actions" style="margin-top:20px"><a class="btn btn--tertiary" href="{root}transfers.html#privativo">Saber mais</a></div></div>
    </div>
  </div>
</section>
<section class="band band--tint" id="clube">
  <div class="container split">
    <div class="photo-wide">{picture("morro-primeira", "(max-width: 1023px) 100vw, 567px", root)}</div>
    <div class="text">
      <p class="eyebrow">Para quem volta</p>
      <h2 class="title">Clube Baía Azul</h2>
      <p>Quem viaja com a gente entra para o Clube Baía Azul, o nosso programa de vantagens. Os participantes recebem descontos, cupons e sorteios, além de um atendimento ainda mais próximo nas viagens seguintes.</p>
      <div class="actions"><a class="btn btn--primary" href="{whatsapp('Olá! Quero saber mais sobre o *Clube Baía Azul*.')}" target="_blank" rel="noopener">Quero participar</a></div>
    </div>
  </div>
</section>
<section class="band" id="contato">
  <div class="container split">
    <div class="text">
      <p class="eyebrow">Contato</p>
      <h2 class="title">Onde estamos</h2>
      <p>A nossa base fica no Pelourinho, no coração do Centro Histórico de Salvador, a poucos minutos do Elevador Lacerda e do Terminal Marítimo, de onde partem os barcos.</p>
      <p>O jeito mais rápido de falar com a gente é o WhatsApp. É por lá que tiramos dúvidas, enviamos valores e confirmamos as reservas.</p>
      <div class="actions">
        <a class="btn btn--primary" href="{whatsapp('Olá! Quero falar com a Baía Azul.')}" target="_blank" rel="noopener">Chamar no WhatsApp</a>
        <a class="btn btn--tertiary" href="{SITE['map_url']}" target="_blank" rel="noopener">Ver no mapa</a>
      </div>
    </div>
    <div>{rows(contact_rows)}</div>
  </div>
</section>"""
    return page("Sobre a Baía Azul", "A Baía Azul é uma agência de passeios e transfers com base no Pelourinho, em Salvador. Conheça a agência, o Clube Baía Azul e os canais de contato.",
                root, "sobre.html", "sobre", body, image="pelourinho")


def cancel_rows():
    return '<dl class="rows rows--stack">' + "".join(
        f'<div style="display:block"><dt style="margin-bottom:2px">{e(a)}</dt><dd style="text-align:left;font-size:16px;line-height:28px">{e(b)}</dd></div>'
        for a, b in CANCELAMENTO) + "</dl>"


def page_duvidas():
    root = ""
    groups = []
    for name, items in FAQ:
        qa = "".join(
            f'<details><summary>{e(q)}</summary><div class="faq__answer">{"".join(f"<p>{e(par)}</p>" for par in a)}</div></details>'
            for q, a in items)
        groups.append(f'<div class="faq-group"><h2 class="title">{e(name)}</h2><div class="faq">{qa}</div></div>')

    body = f"""
{hero(root, "escuna", "Antes de embarcar", "Dúvidas", short=True)}
<section class="band" id="inicio">
  <div class="container" style="max-width:860px">
    {''.join(groups)}
  </div>
</section>
<section class="band band--tint" id="cancelamento">
  <div class="container split split--narrow-first">
    <div class="text">
      <p class="eyebrow">Política</p>
      <h2 class="title">Cancelamento e reembolso</h2>
      <p>As regras dependem de onde a compra foi feita e de quanto tempo falta para o passeio. Para pedir um cancelamento, fale com a gente pelo WhatsApp.</p>
    </div>
    <div>{cancel_rows()}</div>
  </div>
</section>
{closing(root, "Não achou a resposta?", "Pergunte para a gente", "Chame no WhatsApp e a nossa equipe responde com o que você precisa saber.", "", tint=False, second=("Ver passeios", f"{root}index.html#passeios"))}"""

    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}}
        for _, items in FAQ for q, a in items]}
    return page("Dúvidas frequentes", "Respostas sobre transfers, passeios, reserva, pagamento e cancelamento na Baía Azul.",
                root, "duvidas.html", "duvidas", body, image="escuna", schema=schema)


def page_politicas():
    root = ""
    who = SITE["name"] + (", CNPJ " + SITE["cnpj"] if SITE["cnpj"] else "") + ", " + SITE["neighbourhood"] + ", " + SITE["city"]
    body = f"""
{hero(root, "baia", "Transparência", "Privacidade e termos", short=True)}
<section class="band" id="inicio">
  <div class="container text" style="max-width:860px">
    <p class="eyebrow">Privacidade</p>
    <h2 class="title" style="margin-bottom:21px">Como tratamos os seus dados</h2>
    <p>Este site foi feito para coletar o mínimo possível. Ele não usa cookies, não tem ferramentas de análise ou de publicidade e não carrega conteúdo de terceiros. As fontes e as imagens são servidas pelo próprio site.</p>

    <h3 class="subtitle">Quem é o responsável</h3>
    <p>{e(who)}.</p>

    <h3 class="subtitle">Que dados recebemos</h3>
    <p>Apenas os que você decide enviar. O formulário de reserva não grava nem transmite nada por conta própria: ele só organiza as informações (passeio, data, número de pessoas, nome, hospedagem e observações) em uma mensagem, que você mesmo envia pelo WhatsApp.</p>

    <h3 class="subtitle">Para que usamos</h3>
    <p>Para responder ao seu pedido, confirmar a reserva, combinar horário e ponto de encontro e prestar o serviço contratado. Não vendemos nem cedemos os seus dados para ações de marketing de terceiros.</p>

    <h3 class="subtitle">Com quem compartilhamos</h3>
    <p>Somente com quem participa da execução do seu passeio ou transfer, como operadores de embarcações, motoristas e guias, e apenas o necessário para isso. Também podemos ser obrigados a apresentar informações a autoridades, quando a lei exigir.</p>

    <h3 class="subtitle">WhatsApp e mapa</h3>
    <p>Ao tocar em um botão de WhatsApp ou em “Ver no mapa”, você sai deste site. A partir daí valem as políticas de privacidade do WhatsApp e do Google Maps.</p>

    <h3 class="subtitle">Por quanto tempo guardamos</h3>
    <p>Pelo tempo necessário para prestar o serviço e cumprir obrigações legais e fiscais. Depois disso, as conversas e os registros são apagados.</p>

    <h3 class="subtitle">Os seus direitos</h3>
    <p>A Lei Geral de Proteção de Dados (Lei 13.709/2018) garante a você o direito de confirmar se tratamos os seus dados, de acessá-los, corrigi-los e pedir a sua exclusão. Para exercer qualquer um deles, fale com a gente pelo WhatsApp.</p>
  </div>
</section>
<section class="band band--tint" id="cancelamento">
  <div class="container split split--narrow-first">
    <div class="text">
      <p class="eyebrow">Reservas</p>
      <h2 class="title">Cancelamento e reembolso</h2>
      <p>As mesmas regras valem para passeios e transfers.</p>
    </div>
    <div>{cancel_rows()}</div>
  </div>
</section>
<section class="band" id="termos">
  <div class="container text" style="max-width:860px">
    <p class="eyebrow">Termos de uso</p>
    <h2 class="title" style="margin-bottom:21px">Sobre as informações do site</h2>
    <h3 class="subtitle">Valores e horários</h3>
    <p>Os valores publicados são os de partida e podem mudar conforme a data. Horários, valores e pontos de encontro só ficam garantidos depois da confirmação da reserva pela nossa equipe.</p>
    <h3 class="subtitle">Taxas</h3>
    <p>Taxas de embarque e de entrada cobradas por terceiros não estão incluídas nos valores e são pagas à parte. Quando existem, estão indicadas na página do passeio.</p>
    <h3 class="subtitle">Roteiros</h3>
    <p>Passeios de barco dependem da maré e das condições do mar. A ordem das paradas pode ser ajustada no dia para garantir a segurança e o melhor aproveitamento.</p>
    <h3 class="subtitle">Fotos</h3>
    <p>As fotos do site mostram os destinos e servem de ilustração. Os autores e as licenças estão na página de <a href="{root}creditos.html">créditos das fotos</a>.</p>
    <h3 class="subtitle">Uso do site</h3>
    <p>Ao usar este site, você concorda em não o utilizar para fins ilegais nem tentar prejudicar o seu funcionamento.</p>
  </div>
</section>"""
    return page("Privacidade e termos", "Como a Baía Azul trata os seus dados, as regras de cancelamento e reembolso e os termos de uso do site.",
                root, "politicas.html", "politicas", body, image="baia")


def page_creditos():
    root = ""
    trs = []
    for slug, c in CREDITS.items():
        name = {"Public domain": "Domínio público"}.get(c["license"], c["license"])
        licence = f'<a href="{e(c["license_url"])}" target="_blank" rel="noopener license">{e(name)}</a>' if c["license_url"] else e(name)
        trs.append(
            f'<tr><td><img src="{root}assets/img/{slug}-640.webp" alt="" width="120" height="68" loading="lazy"></td>'
            f'<td>{e(c["alt"])}</td><td>{e(c["author"])}</td><td class="nowrap">{licence}</td>'
            f'<td><a href="{e(c["source"])}" target="_blank" rel="noopener">Original<span class="visually-hidden"> da foto: {e(c["alt"])}</span></a></td></tr>')
    body = f"""
{hero(root, "morere", "Obrigado a quem fotografa a Bahia", "Créditos das fotos", short=True)}
<section class="band" id="inicio">
  <div class="container text">
    <p style="max-width:860px">As fotos deste site vêm do acervo livre Wikimedia Commons. Todas foram recortadas para o formato 16:9 e redimensionadas. As obras sob licença Creative Commons continuam disponíveis nos mesmos termos da licença original.</p>
    <table class="credits" style="margin-top:40px">
      <thead><tr><th scope="col"><span class="visually-hidden">Foto</span></th><th scope="col">O que mostra</th><th scope="col">Autoria</th><th scope="col">Licença</th><th scope="col">Fonte</th></tr></thead>
      <tbody>{''.join(trs)}</tbody>
    </table>
  </div>
</section>"""
    return page("Créditos das fotos", "Autoria e licenças das fotos usadas no site da Baía Azul.", root, "creditos.html", "creditos", body, image="morere")


def page_404():
    root = (SITE["url"].rstrip("/") + "/") if SITE["url"] else ""
    body = f"""
{hero(root, "tinhare-agua", "Erro 404", "Página não encontrada", f'<p class="hero__lede">Esse endereço não existe mais, mas o mar continua no mesmo lugar.</p><a class="btn btn--white btn--large" href="{root}index.html">Ver os passeios</a>', cue=False)}"""
    return page("Página não encontrada", "Página não encontrada.", root, "404.html", "", body, image="tinhare-agua")


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#004777"/>'
           '<g fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round"><circle cx="16" cy="11" r="4.6"/>'
           '<path d="M5 19.5c1.8 0 1.8-1.7 3.7-1.7s1.8 1.7 3.6 1.7 1.9-1.7 3.7-1.7 1.8 1.7 3.7 1.7 1.8-1.7 3.6-1.7 1.9 1.7 3.7 1.7"/>'
           '<path d="M5 24.5c1.8 0 1.8-1.7 3.7-1.7s1.8 1.7 3.6 1.7 1.9-1.7 3.7-1.7 1.8 1.7 3.7 1.7 1.8-1.7 3.6-1.7 1.9 1.7 3.7 1.7"/></g></svg>')


# =============================================================================
# 5. WRITE
# =============================================================================
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {path}")


def main():
    print("Building Baía Azul")
    write("index.html", page_home())
    for i, p in enumerate(PASSEIOS):
        write(f"passeios/{p['slug']}.html", page_passeio(p, i))
    write("transfers.html", page_transfers())
    write("sobre.html", page_sobre())
    write("duvidas.html", page_duvidas())
    write("politicas.html", page_politicas())
    write("creditos.html", page_creditos())
    write("404.html", page_404())
    write("assets/img/favicon.svg", FAVICON)

    robots = "User-agent: *\nAllow: /\n"
    if SITE["url"]:
        url = SITE["url"].rstrip("/")
        pages = ["", "transfers.html", "sobre.html", "duvidas.html", "politicas.html", "creditos.html"] + \
                [f"passeios/{p['slug']}.html" for p in PASSEIOS]
        write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
              + "".join(f"  <url><loc>{url}/{p}</loc></url>\n" for p in pages) + "</urlset>\n")
        robots += f"Sitemap: {url}/sitemap.xml\n"
    write("robots.txt", robots)

    # Only the fields the site cannot work without are reported. The optional ones
    # (email, instagram, cnpj, cadastur) are left out of the pages when empty.
    missing = [k for k in ("whatsapp", "url") if not SITE[k]]
    if missing:
        print("\nRequired and not set in tools/content.py: " + ", ".join(missing))


if __name__ == "__main__":
    main()
