#!/usr/bin/env python3
"""
images.py
=========
Downloads the site photography from Wikimedia Commons and writes the optimised
files the pages use, plus the manifest behind the photo credits page.

Run:  python3 tools/images.py        (needs Pillow)

For every entry in PHOTOS this script
  1. asks the Commons API for the file, its author and its licence,
  2. downloads a 2400px wide rendition,
  3. crops it to 16:9 around the focus point,
  4. saves WebP at 640 / 1200 / 1920 px and one JPEG fallback at 1200 px,
  5. records author, licence and source link in assets/img/credits.json.

To replace a photo with one of your own: drop a 16:9 image set with the same
slug into assets/img/ and remove the entry from credits.json.
"""
import io, json, os, re, html, time, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
UA = {"User-Agent": "BaiaAzulSiteBuild/1.0 (static site image fetch)"}

# slug -> (Commons file title, focus point x, focus point y, what the photo shows)
PHOTOS = {
    "hero-morro-aerea":   ("File:MARCIO FILHO SEGUNDA PRAIA MORRO DE SÃO PAULO BAHIA (39166732230).jpg", .5, .55, "Vista aérea da Segunda Praia, em Morro de São Paulo"),
    "tinhare":            ("File:Piscinas Naturais de Garapuá 2 (51012445466).jpg", .5, .7, "Banho nas piscinas naturais de Garapuá"),
    "tinhare-agua":       ("File:Piscinas Naturais - Garapuá.jpg", .5, .6, "Água transparente nas piscinas naturais de Garapuá"),
    "day-use-morro":      ("File:Morro de São Paulo - Tirolesa.jpg", .5, .5, "Praias e vila de Morro de São Paulo vistas do alto"),
    "morro-primeira":     ("File:1ª Praia - Morro de São Paulo, Bahia.JPG", .5, .45, "Primeira Praia de Morro de São Paulo"),
    "frades":             ("File:Vista superior Ilha dos Frades.jpg", .5, .6, "Enseada da Ponta de Nossa Senhora de Guadalupe, na Ilha dos Frades"),
    "escuna":             ("File:Escunas rumo a Ilha dos Frades.jpg", .5, .5, "Escuna navegando na Baía de Todos-os-Santos"),
    "praia-do-forte":     ("File:Praia do Forte - Roberta Mendes de Sá(1).jpg", .5, .55, "Maré baixa em frente à igreja da Praia do Forte"),
    "village-itaparica":  ("File:Praia Barra do Gil na Ilha de Itaparica.JPG", .5, .6, "Praia na Ilha de Itaparica"),
    "garapua":            ("File:Garapuá Foto Tatiana Azeviche (31021819287).jpg", .5, .55, "Coqueiros na praia de Garapuá"),
    "quadriciclo":        ("File:Garapuá Foto Tatiana Azeviche (45960952171).jpg", .5, .6, "Maré baixa na praia de Garapuá, destino do passeio de quadriciclo"),
    "gamboa":             ("File:Praia da Argila.jpg", .5, .45, "Falésia de argila na Praia da Gamboa"),
    "boipeba":            ("File:MARCIO FILHO BOCA DA BARRA BOIPEBA BAHIA (39166727470).jpg", .5, .5, "Vista aérea da Boca da Barra, na Ilha de Boipeba"),
    "morere":             ("File:Praia Moreré-4 (51019497281).jpg", .5, .5, "Coqueiros na praia de Moreré, em Boipeba"),
    "terminal":           ("File:Salvador (44626032271).jpg", .5, .6, "Píer de embarque em Salvador"),
    "lacerda":            ("File:Elevador Lacerda com vista da Baía de Todos os Santos.jpg", .5, .5, "Elevador Lacerda e a Baía de Todos-os-Santos"),
    "baia":               ("File:Centro Histórico - Elevador Lacerda - Mercado Modelo e Baía de Todos- os - Santos- Foto - Tereza Torres -Setur (16277947841).jpg", .5, .55, "Baía de Todos-os-Santos vista da Cidade Alta"),
    "pelourinho":         ("File:Largo do Pelourinho Salvador 2018-0919.jpg", .5, .5, "Casario colorido do Largo do Pelourinho"),
}
SIZES = (640, 1200, 1920)


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(8):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(20 * (attempt + 1))
    raise RuntimeError("Commons API kept rate limiting")


def fetch(slug, src):
    """Download once and keep the original in tools/.cache. Commons rate limits, so wait and retry."""
    cache = os.path.join(ROOT, "tools", ".cache")
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, slug + ".jpg")
    if os.path.exists(path):
        return open(path, "rb").read()
    for attempt in range(8):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=120).read()
            open(path, "wb").write(raw)
            time.sleep(4)
            return raw
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(20 * (attempt + 1))
    raise RuntimeError("Commons kept rate limiting " + slug)


def clean(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", value or ""))).strip()


def crop_16_9(im, fx, fy):
    """Crop to 16:9, keeping the focus point as close to the centre as the frame allows."""
    w, h = im.size
    if w / h > 16 / 9:
        nw, nh = int(h * 16 / 9), h
    else:
        nw, nh = w, int(w * 9 / 16)
    left = min(max(int(w * fx - nw / 2), 0), w - nw)
    top = min(max(int(h * fy - nh / 2), 0), h - nh)
    return im.crop((left, top, left + nw, top + nh))


def main():
    os.makedirs(OUT, exist_ok=True)
    credits = {}
    for slug, (title, fx, fy, alt) in PHOTOS.items():
        r = api({"action": "query", "format": "json", "titles": title, "prop": "imageinfo",
                 "iiprop": "url|size|extmetadata", "iiurlwidth": 2400})
        info = next(iter(r["query"]["pages"].values()))["imageinfo"][0]
        meta = info.get("extmetadata", {})
        src = info.get("thumburl") or info["url"]
        raw = fetch(slug, src)
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
        im = crop_16_9(im, fx, fy)
        for width in SIZES:
            w = min(width, im.size[0])
            out = im.resize((w, round(w * 9 / 16)), Image.LANCZOS)
            out.save(os.path.join(OUT, f"{slug}-{width}.webp"), "WEBP", quality=78, method=6)
            if width == 1200:
                out.save(os.path.join(OUT, f"{slug}-1200.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
        credits[slug] = {
            "alt": alt,
            "title": title.replace("File:", ""),
            "author": clean(meta.get("Artist", {}).get("value")) or "Autor não informado",
            "license": clean(meta.get("LicenseShortName", {}).get("value")),
            "license_url": clean(meta.get("LicenseUrl", {}).get("value")),
            "source": info["descriptionurl"],
        }
        print(f"{slug:20s} {im.size}  {credits[slug]['license']:14s} {credits[slug]['author'][:50]}")
    with open(os.path.join(OUT, "credits.json"), "w") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
