# Baía Azul

Website of Baía Azul, an agency for passeios and transfers based in the Pelourinho, Salvador, Bahia.

Static site. No framework, no build step on the server, no cookies, no third party requests.
Open `index.html` or serve the folder with any static host.

## Business details

All business facts live at the top of `tools/content.py`, in `SITE`. A value left empty is
simply not shown on the site.

| Field | What it does | Status |
|---|---|---|
| `whatsapp`, `whatsapp_display` | Number behind every booking button, and how it is displayed | Set |
| `street` | Location inside the Pelourinho | Set (Shopping do Pelô) |
| `url` | Public address. Drives the canonical link, social preview image and `sitemap.xml` | Set (GitHub Pages) |
| `email`, `instagram` | Shown in the footer and contact section when filled in | Left out by choice |
| `cnpj`, `cadastur` | Shown in the footer and privacy page when filled in | Left out by choice |

After editing, rebuild and push. The live site at https://mento-web.github.io/baia-azul/
is served from the `main` branch.

```bash
python3 tools/build.py
```

## How it is organised

```
index.html                 list of passeios and transfers, with two filters
passeios/<slug>.html       one page per passeio (9)
transfers.html             timetables and the private transfer
sobre.html                 the agency, the Clube Baía Azul, contact
duvidas.html               FAQ and cancellation rules
politicas.html             privacy (LGPD), cancellation, terms of use
creditos.html              photo credits
404.html

assets/css/site.css        the whole design, one file, sectioned
assets/js/site.js          menu, filters, booking dialog, sticky bar
assets/fonts/              Josefin Sans and Raleway, self hosted
assets/img/                photos in WebP (640, 1200, 1920) plus JPEG fallback

tools/content.py           every word on the site. Edit here.
tools/build.py             turns content.py into the HTML pages
tools/images.py            downloads and crops the photos, writes credits.json

docs/DESIGN.md             the design specification the site follows
docs/design-tokens.json    the same values, machine readable
```

The HTML files are generated. Change `tools/content.py` or `tools/build.py` and rebuild,
do not edit the HTML by hand.

## Common changes

**Change a price, a time or a description.** Edit the passeio in `PASSEIOS` or the transfer
in `TRANSFERS` inside `tools/content.py`, then rebuild.

**Add a passeio.** Copy one entry in `PASSEIOS`, give it a new `slug`, and point `img` at a
photo slug that exists in `assets/img/`. Rebuild. The menu, the list, the booking form and
the page are created from that one entry.

**Replace a photo with your own.** Save it in 16:9 as `assets/img/<slug>-640.webp`,
`-1200.webp`, `-1920.webp` and `-1200.jpg`, and delete that slug from
`assets/img/credits.json` so it leaves the credits page. Rebuild.

## Design

The site follows `docs/DESIGN.md`: one product per full width band, two interface colours,
thin capitals with wide tracking, pills for actions, square photos, no shadows on content,
no bold. Body text uses a darker tone than the reference so it passes WCAG AA.

## Photos

All photos come from Wikimedia Commons under free licences. Authors, licences and source
links are listed on `creditos.html`, which the licences require. Keep that page linked in
the footer for as long as those photos are used.

## Checks run on this version

- Every internal link, image and anchor resolves (782 references, 16 pages).
- axe-core accessibility audit: no violations on 9 pages at desktop and mobile width.
- No horizontal scrolling at 390, 820 and 1440 px.
- Works without JavaScript: booking buttons are plain WhatsApp links.
