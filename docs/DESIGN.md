# DESIGN.md

Design reference for the Baía Azul website, based on the Trilogy tours page.

| | |
|---|---|
| Source | https://sailtrilogy.com/tours |
| Captured | 10 October 2026 |
| Method | Computed styles read from the live page in Chrome at 1440, 820 and 390 px, cross checked against the site stylesheet |
| Companion file | `design-tokens.json` (same values, machine readable) |
| Screenshots | `Reference Trilogy Tours/` |

**How to read this file.** Parts 1 to 9 describe the reference exactly as it is built. Every number there was measured. Part 10 lists what the reference gets wrong. Part 11 is my proposal for carrying it into Baía Azul, and is opinion, not measurement.

**Fair use.** Layout patterns, spacing and open source fonts are free to reuse. The Trilogy logo, photos, video and wording are not.

---

## 1. The idea in one paragraph

The page is a price list that behaves like a magazine. Each tour gets a full width band of its own: one photo on the left, a few lines of text on the right, two buttons. There are no boxes, borders or shadows around anything. The interface uses two colours (a near black navy and a pale blue grey mist) and lets the photography supply all the saturated colour. All headings are thin geometric capitals with very wide letter spacing, which makes the page feel calm, nautical and expensive without a single bold weight.

### Seven rules that produce the look

1. **One tour, one band.** Nothing competes with the product in view.
2. **Two interface colours.** Photography supplies the rest.
3. **Capitals with air.** Wide tracking does the job that bold usually does.
4. **Pills for actions, squares for pictures.** Only two shapes exist.
5. **Flat.** No card boxes, no shadows, no gradients on content.
6. **Price is content, not a badge.** It sits in the reading flow between two hairlines.
7. **Two actions per product,** always the same two, always in the same order.

---

## 2. Colour

### 2.1 Palette

| Token | Hex | Used for |
|---|---|---|
| `ink` | `#160D3F` | Headings, primary button, select text, dropdown panel |
| `inkDeep` | `#0C052A` | Page background behind everything (only seen on overscroll) |
| `teal` | `#306F7F` | Footer, fallback behind the hero video, dropdown hover |
| `tealMuted` | `#73A6B2` | Body copy, secondary prices, duration, dropdown links |
| `tealLight` | `#77B9C9` | Small print on the footer |
| `mist` | `#EAF5F7` | Alternating band, sticky bar, tertiary button |
| `hairline` | `#CBDFE4` | 1px rules around the price row |
| `white` | `#FFFFFF` | Section background, text on dark |

Rough share of the screen: 55% white, 30% mist, 10% photography, 5% ink.

### 2.2 Semantic roles

| Role | Value |
|---|---|
| Page background | white |
| Band background | mist |
| Heading text | ink |
| Body text | tealMuted |
| Primary action | ink background, white text |
| Tertiary action on white | mist background, ink text |
| Tertiary action on mist | white background, ink text |
| Footer | teal background, white links, tealLight small print |
| Menu panel | ink background, tealMuted links |

The tertiary button swaps its fill so it always contrasts with the band it sits on. That one detail is why the alternating bands look deliberate.

### 2.3 Hero overlay

The video is tinted with a navy wash, `rgb(13, 7, 44)`, stronger at the top (35% opacity) where the navigation sits, fading to 18% at the bottom. CSS equivalent:

```css
background: linear-gradient(to bottom,
  rgba(13, 7, 44, .35) 0%,
  rgba(13, 7, 44, .23) 50%,
  rgba(13, 7, 44, .18) 100%);
```

### 2.4 Contrast (WCAG AA needs 4.5:1 for text)

| Pair | Ratio | Result |
|---|---|---|
| ink on white | 18.05 | pass |
| ink on mist | 16.25 | pass |
| white on teal (footer links) | 5.67 | pass |
| tealMuted on ink (dropdown) | 6.73 | pass |
| tealMuted on white (body copy) | 2.68 | **fail** |
| tealMuted on mist (body copy) | 2.42 | **fail** |
| tealLight on teal (footer small print) | 2.58 | **fail** |

The soft, washed out body text is a large part of the elegant look, and it is also the page's biggest usability problem. See part 11 for a fix that keeps the feeling.

---

## 3. Typography

### 3.1 Families

| Role | Font | Weight | Treatment |
|---|---|---|---|
| Display | **Josefin Sans** | 400 | Always capitals, always tracked 1 to 4.5 px |
| Text | **Raleway** | 500 | Always sentence case, no tracking |

Both are free on Google Fonts under the SIL Open Font License.

Rules the page never breaks:

- No bold anywhere. Hierarchy comes from size, tracking and colour.
- Display font is never set in lowercase. Text font is never set in capitals.
- Italic appears once: the word "free" in the price row.

### 3.2 Type styles

| Style | Font | Size / line height | Tracking | Colour | Mobile |
|---|---|---|---|---|---|
| Hero eyebrow | Display | 28 / 34 | 4.5px | white | 17 / 20 |
| Hero title | Display | 64 / 90 | 3px | white | 42 / 52, 2px |
| Card eyebrow | Display | 17 / 17 | 2.8px | ink | same |
| Card title | Display | 34 / 35 | 3.5px | ink | 24 / 24 |
| Price | Text | 18 / 30 | 0 | ink (first), tealMuted (rest) | same |
| Body | Text | 14 / 26 | 0 | tealMuted | same |
| Duration | Text | 14 / 26 | 0 | tealMuted | same |
| Note line | Text | 16 / 30 | 0 | tealMuted | same |
| Button | Display | 16 / 16 | 2.3px | white or ink | 14 / 14, 2px |
| Nav link | Display | 14 / 21 | 1px | white | same |
| Filter select | Display | 14 / 25 | 2px | ink | same |
| Footer link | Display | 14 / 38 | 1px | white | 14 / 26 |
| Footer small print | Text | 14 / 29 | 0 | tealLight | same |

Observations:

- The hero title is less than twice the card title (64 vs 34). The scale is compressed, so nothing shouts.
- Tracking grows with size: 1px at 14, 2.8px at 17, 3.5px at 34, 4.5px on the hero eyebrow.
- The eyebrow is exactly half the size of the title (17 vs 34) and sits 22px above it. Together they read as one two line lockup.
- Body line height is generous: 26px on 14px text, a ratio of 1.86.

---

## 4. Space, shape and depth

### 4.1 Spacing

There is no formal scale. These values recur: `6, 13, 17, 20, 21, 26, 29, 33, 40, 48, 50, 66, 80, 100, 120`.

| Where | Desktop | Tablet | Mobile |
|---|---|---|---|
| Band padding, top and bottom | 80 | 80 | 10 top, 50 bottom |
| Page margin, cards | 120 (at 1440) | 20 | 0 for photo, 20 for text |
| Page margin, navigation | 48 | 17 | 11 |
| Gap between photo and text | 66 | 40 | 36 (stacked) |
| Footer padding | 50 / 33 | 50 / 33 | 50 / 21 / 100 |

### 4.2 Shape

| Element | Radius |
|---|---|
| Buttons, filter select | 100px (full pill) |
| Photos, bands, price row | 0 |
| Chat button | circle |

### 4.3 Depth

The content is completely flat. Shadows exist only on controls that float above it.

| Element | Shadow |
|---|---|
| Filter select | `0 1px 3px 0 rgba(0,0,0,.12)` |
| Filter select, focused | `0 1px 3px 0 rgba(0,0,0,.22)` |
| Sticky bar, when fixed | `0 1px 8px 0 rgba(22,13,63,.15)` |
| Cards, buttons, photos | none |

### 4.4 Lines

One line style on the whole page: `1px solid #CBDFE4`, used above and below the price row. The footer adds 1px wide, 20px tall dividers between social icons.

---

## 5. Layout

### 5.1 Page order

```
┌──────────────────────────────────────────────────────────┐
│ logo                    TOURS  OUR STORY  SHOP  ...      │  transparent nav, over the video
│                                                          │
│                     SAIL WITH US                         │
│                     #1 ON MAUI                           │  hero, 600px
│                   ( ALL TOURS  ⌄ )                       │
│                          ⌄                               │
├──────────────────────────────────────────────────────────┤
│                                                          │  sticky bar, 100px, mist
├──────────────────────────────────────────────────────────┤
│   ┌────────────┐   DISCOVER                       8 hr   │
│   │   photo    │   LANAI SNORKEL                         │  card band, mist
│   │   16:9     │   ─────────────────────────────────     │
│   │            │   Adult $295  Youth $265  Child $199    │
│   └────────────┘   ─────────────────────────────────     │
│                    Description, two lines.               │
│                    (BOOK NOW) (EXPLORE)                  │
├──────────────────────────────────────────────────────────┤
│   ┌────────────┐   DISCOVER                       5 hr   │
│   │   photo    │   WEST MAUI SNORKEL                     │  card band, white
│   ...                                                    │
├──────────────────────────────────────────────────────────┤
│  CAREERS   BLOG   SHOP   CHARTERS   FAQ   PRIVACY  ...   │
│               f  |  t  |  ig  |  y  |  ta                │  footer, teal
│            small print, centred, three paragraphs        │
└──────────────────────────────────────────────────────────┘
```

Measured at 1440px wide: hero 600, sticky bar 100, 18 cards between 486 and 538 each, footer 590. Total page height about 10,400px.

### 5.2 Containers

| Container | Max width |
|---|---|
| Navigation | 1344 (48px margin each side) |
| Cards | 1200 |
| Footer small print | 1120 |
| Social icons | 680 |

### 5.3 Breakpoints

| Name | Width | What changes |
|---|---|---|
| Mobile | below 769 | Cards stack, all bands white, prices stack, video replaced by a still |
| Tablet | 769 to 1023 | Photo 5/12, text 7/12, burger menu |
| Desktop | 1024 and up | Full navigation, photo and text 50/50 |
| Wide | 1216 and 1408 | Framework defaults, no visible change on this page |

---

## 6. Components

### 6.1 Navigation

- **Placement.** The bar is 60px tall and transparent. The hero is pulled up by 60px so the video runs behind it. It does not stick when scrolling.
- **Logo.** 185 x 20, white, 48px from the left and 47px from the top. It is a row of nautical signal flags with no wordmark.
- **Links.** Five, right aligned: Tours, Our Story, Shop, Private Charters, Contact. Nav link style, 26px apart. Two carry a small chevron for a dropdown.
- **Hover.** Opacity fade over 200ms.
- **Dropdown.** A 400px wide ink panel that opens 40px below the link. Links are tealMuted, 14px, padded `11px 0 11px 38px`. A hovered row turns teal with white text. The Tours dropdown lists every tour by name, then Private Charters and All Tours.
- **No book button** in the navigation.
- **Below 1024.** Links collapse into a burger: three 16px wide, 1px thick white lines, 5px apart. Open state rotates the outer lines into a cross in 86ms. The menu panel is ink.

### 6.2 Hero

| Property | Desktop | Tablet | Mobile |
|---|---|---|---|
| Height | 600 | 550 | 420 |
| Media | Looping video | Looping video | Still image (poster) |
| Text block position | Vertical centre | Vertical centre | 30% from top |

- **Video.** Autoplay, muted, loop, plays inline, with a poster. `object-fit: cover`. Fallback colour behind it is teal.
- **Curtain reveal.** The video layer is `position: fixed` and 700px tall. The page content has a solid background and scrolls up over it, so the video appears to stay still while the page slides across it.
- **Copy.** Two lines only. Eyebrow "SAIL WITH US", title "#1 ON MAUI". Six words in total.
- **Stack.** Eyebrow, 6px, title, 26px, filter select. All centred.
- **Scroll cue.** A thin 29px chevron, 30px from the bottom, that bounces every 3.5 seconds (up 30px, settle, up 15px, settle, then rest). Clicking it jumps to the first section.

### 6.3 Filter select

A native `<select>` restyled as a pill.

| Property | Value |
|---|---|
| Size | 288 x 50 |
| Radius | 100px |
| Background | `rgba(255,255,255,.92)`, solid white on hover |
| Shadow | `0 1px 3px 0 rgba(0,0,0,.12)` |
| Padding | 8px top, 35px right, 4px bottom, 20px left |
| Text | Display, 14px, 2px tracking, capitals, ink |
| Chevron | 7.7px square, 1px ink stroke on two sides, rotated 45 degrees, 25px from the right |

Options, in order: All Tours, Dinner Cruise, Snorkeling, Sunset, Whale Watching, SNUBA, Depart from: Maalaea, Depart from: Lahaina, Depart from: Kaanapali, Lanai Excursions.

Choosing one hides the cards that do not match, with no page reload, and re-stripes the remaining bands so the alternation stays intact.

Elsewhere on the site the same control has a glass variant: `rgba(255,255,255,.5)` with a 10px backdrop blur and white text.

### 6.4 Sticky bar

A 100px mist band directly under the hero. On desktop it scrolls away with the page, then fixes to the top with a soft shadow. On mobile it is fixed to the bottom of the screen from the start. On the home page it holds Tour, Dates, Who and a Search button. On the tours page it is empty (see part 10).

### 6.5 Tour card

The central component. One per band.

**Band**

- Odd bands are mist, even bands are white. On mobile every band is white.
- Padding 80px top and bottom. No border between bands. The colour change is the divider.

**Grid**

| | Desktop 1440 | Tablet 820 | Mobile 390 |
|---|---|---|---|
| Columns | 50 / 50 | 5/12 and 7/12 | Stacked |
| Gap | 66 | 40 | Text 36 below photo |
| Photo | 567 x 318 | 302 x 169 | 390 x 219, edge to edge |
| Text column | 567 | 438 | 350 (20px side margin) |
| Band height | 486 to 538 | 486 to 590 | 700 to 840 |

**Photo**

- 16:9 landscape. Source files are 854 x 479.
- Square corners, no border, no shadow, no hover effect, no caption or badge on top.
- The whole photo links to the tour page.
- One strong, saturated landscape or aerial per tour. No people close up, no collage.

**Text column, top to bottom**

| # | Element | Style | Space below |
|---|---|---|---|
| 1 | Eyebrow (left) and duration (right) | Card eyebrow, Duration | 22 |
| 2 | Title | Card title | 21 |
| 3 | Price row | Price, between two hairlines, 64 tall | 29 |
| 4 | Note (optional), for example "SNUBA Available" | Note line | 8 |
| 5 | Description | Body, 2 or 3 lines | 29 |
| 6 | Actions | Two pills | |

The eyebrow starts 16px below the top edge of the photo. The duration label sits level with the top edge, right aligned, so the text column has a clear top right corner.

**The title split.** Every tour name is broken into a small qualifier and a large product name. This keeps the big line short and turns a list of long names into a scannable column.

| Eyebrow | Title |
|---|---|
| DISCOVER | LANAI SNORKEL |
| LANA'I | ADVENTURE SNORKEL |
| SNORKEL | TURTLE REEF |
| DELUXE KAANAPALI | SUNSET SAIL |
| MAALAEA | WHALE WATCH |
| LAHAINA CAPTAIN'S SUNSET | DINNER SAIL |
| NEW YEAR'S EVE | FIREWORKS SAIL |

The eyebrow carries whatever distinguishes this tour from its siblings (place, tier, occasion). The title carries the product type.

**Description pattern.** One sentence of benefit, then facts separated by bullets on the same line: `Sentence. • 5 hrs • Departs from Maalaea • Snuba upgrade`.

### 6.6 Price row

| Property | Value |
|---|---|
| Rules | 1px hairline above and below |
| Padding | 17px top, 15px bottom |
| Height | 64 |
| Text | Raleway 18 / 30 |
| Desktop | Up to four items on one line, spread across the full column |
| Mobile | One item per line, 30px each |

- Format: `Adult $295   Youth $265   Child $199   Infant free`. Label, space, currency symbol, whole number.
- The first item is ink. The others are tealMuted. The eye lands on the adult price.
- "free" is italic.
- Variants: four tiers, three tiers, or adult only for dinner sails and adults only events.
- The tax disclaimer appears once, in the footer, not on each card.

### 6.7 Buttons

| | Primary | Tertiary |
|---|---|---|
| Label | BOOK NOW | EXPLORE |
| Background | ink | mist on white bands, white on mist bands |
| Text | white | ink |
| Width as measured | 194 | 171 |

Shared:

- Radius 100px, no border, no shadow.
- Padding `13px 40px 12px` (the compact size used in cards), 41px tall. The default size is `16px 40px 15px`, 47px tall.
- One pixel more padding on top than on the bottom, because Josefin Sans capitals sit high in their line box.
- Text: Display, 16px, 2.3px tracking. On mobile 14px, 2px tracking, 39px tall.
- Pair: primary first, 6px gap, tertiary second. On mobile they stay side by side and are centred.
- Hover: shrinks to 96% and darkens (`transform: scale(.96); filter: brightness(.9) contrast(1.2)`) over 200ms ease-in-out. The button presses in, it does not lift.

A secondary variant (teal background, white text) exists in the stylesheet but is not used on this page.

### 6.8 Footer

Teal background, everything centred, three rows.

| Row | Content | Desktop | Mobile |
|---|---|---|---|
| Links | 9 text links, Footer link style | One line, spread edge to edge, 80px below | Stacked, about 10px apart, 40px below |
| Social | 5 white icons, 33px tall | Max width 680, thin dividers between, 68px below | Icons at 75%, no dividers, 54px below |
| Small print | 3 paragraphs, max width 1120 | 14 / 29, tealLight | Same |

What is missing on purpose: logo, address, phone, newsletter form, copyright line, payment icons. The footer is a quiet sign off, not a second navigation.

### 6.9 Chat button

A third party widget. 56px circle, blue (`#166D98`), white speech bubble icon, 20px from the right and bottom edges. It is the only element on the page that is not navy, teal or white.

---

## 7. Motion

| What | How |
|---|---|
| Default transition | 200ms ease-in-out |
| Button hover | Scale to 96%, darken |
| Nav link hover | Opacity fade, 200ms |
| Burger to cross | 86ms ease-out |
| Scroll cue | Bounce, 3.5s loop |
| Hero | Fixed video, page slides over it |
| Filter | Instant show and hide, no animation |
| Cards entering the viewport | No animation |

Motion is sparse. Nothing fades in on scroll, nothing parallaxes except the hero, nothing moves on photo hover.

---

## 8. Content model

Each tour needs exactly these fields:

| Field | Shape | Example |
|---|---|---|
| Eyebrow | 1 to 3 words | DISCOVER |
| Title | About 2 words | MOLOKINI SNORKEL |
| Duration | Short string | 5 hr |
| Photo | One 16:9 landscape | |
| Prices | List of label and amount | Adult $219, Youth $204, Child $153, Infant free |
| Note | Optional, one short line | SNUBA Available |
| Description | 1 or 2 sentences plus bullet facts | Only accessible by boat... • 5 hrs • Departs from Maalaea |
| Filter tags | Activity and departure point | snorkel, maalaea |
| Links | Book and detail | |

Order of the list: flagship and most expensive tour first, then grouped by family (snorkel, sunset and whale watch, dinner, seasonal, volunteering).

---

## 9. Voice

- Hero: six words, a claim, no verb.
- Tour names: nouns only, place plus activity.
- Descriptions: one benefit sentence, then hard facts. Words that recur: premier, flagship, luxury, all inclusive, convenient.
- Buttons: two words at most, imperative.
- No exclamation marks in the interface. No emojis. No urgency messages, countdowns or "only 3 left".

---

## 10. What not to copy

| Problem | Detail |
|---|---|
| Body copy contrast | 2.68:1 on white, 2.42:1 on mist. AA needs 4.5:1. |
| Footer small print contrast | 2.58:1. |
| Empty sticky bar | On this page the 100px bar has no content, yet it fixes to the top on desktop and covers a tenth of the screen at the bottom on mobile. |
| Zoom disabled | The viewport tag blocks pinch zoom. |
| No alt text | Card photos are injected without an alt attribute. |
| No book action in the navigation | Most strong operator sites keep one visible at all times. |
| One filter for two questions | Activity and departure point share a list, so they cannot be combined. |
| Footer links at tablet width | Nine links stay in one row at 820px and touch. |
| Page length | 18 cards, about 10,400px, no way to jump. |
| Font weight | Buttons and nav ask for Josefin Sans 500, which is not loaded, so the browser shows 400. |

---

## 11. Carrying it into Baía Azul

This part is my recommendation. It keeps the structure and feeling of the reference and swaps in the existing Blue Horizon palette.

### 11.1 Colour mapping

| Role | Reference | Baía Azul | Note |
|---|---|---|---|
| Ink (headings) | `#160D3F` | `#16344E` | Existing `--ink`. 12.84:1 on white. |
| Band | `#EAF5F7` | `#EAF6FB` | New. Lighter than the existing `--brand-soft`, which is too saturated for large areas. Warmer option: `#F1E6CC` (`--cream`). |
| Body text | `#73A6B2` | `#54718A` | Existing `--ink-soft`. 5.11:1 on white, 4.65:1 on the band. Fixes the contrast failure. |
| Hairline | `#CBDFE4` | `#CFE6F2` | New. |
| Primary button | `#160D3F` | `#0061AA` | Existing `--brand`. 6.38:1 with white text. Use `#16344E` for the closest match to the reference. |
| Tertiary button | mist or white | `#EAF6FB` or white | Same swap rule as the reference. |
| Footer | `#306F7F` | `#004777` | Existing `--brand-deep`. |
| Footer small print | `#77B9C9` | `#A9D4EA` | 6.13:1 on the footer. |
| Accent | none | `#E8A33D` | Existing `--sand`. At most one small element per screen. |

Hero overlay: `linear-gradient(to bottom, rgba(22,52,78,.38), rgba(22,52,78,.22) 50%, rgba(22,52,78,.16))`.

### 11.2 Typography

Keep both fonts. They are free and they are most of the look.

```html
<link href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@400;600&family=Raleway:ital,wght@0,500;1,500&display=swap" rel="stylesheet">
```

Adjustments for Portuguese:

- Give uppercase headings a line height of at least 1.2 so accents on capitals (Á, Ã, É) are not clipped. The reference uses 1.0.
- Long names wrap quickly at 3.5px tracking. Keep titles under about 22 characters, or reduce tracking to 2.5px on mobile.
- Set body copy at 16px, not 14px.

### 11.3 Copy

| Slot | Portuguese |
|---|---|
| Hero eyebrow | SALVADOR, BAHIA |
| Hero title | NOSSOS PASSEIOS |
| Filter default | TODOS OS PASSEIOS |
| Filter options | Ilhas, Praias, Cultura, Transfers, Saída: Salvador, Saída: Morro de São Paulo |
| Primary button | RESERVAR |
| Tertiary button | VER DETALHES |
| Price labels | Adulto, Criança, Colo grátis |
| Disclaimer | Valores por pessoa. Taxas de embarque não incluídas. |

### 11.4 Current tours in the card format

Names and prices come from the current Baía Azul landing page. Durations marked with an asterisk are placeholders to confirm.

| Eyebrow | Title | Duration | Price row | Description |
|---|---|---|---|---|
| VOLTA ÀS ILHAS | TINHARÉ | 7h30 | Adulto R$ 350 | Saída de Morro de São Paulo. • 09h30 às 17h00 |
| DAY USE | MORRO DE SÃO PAULO | dia inteiro* | Adulto R$ 290 | Catamarã saindo de Salvador. • Travessia de cerca de 3h |
| ESCUNA | FRADES + ITAPARICA | dia inteiro* | Adulto R$ 140 | Passeio pela Baía de Todos-os-Santos. • 2h em cada ilha |
| LITORAL NORTE | PRAIA DO FORTE | 8h | Adulto R$ 140 | Com Guarajuba e parada no Projeto Tamar. • 09h às 17h |
| DAY USE | VILLAGE ITAPARICA | dia inteiro* | Adulto R$ 140 | Piscinas, praia e almoço. |
| CITY TOUR | SALVADOR | sob consulta* | Consulte | Pelourinho, Elevador Lacerda, Bonfim e Farol da Barra. |

With six tours instead of eighteen, the page will be about 3,900px tall on desktop, which removes the length problem.

### 11.5 Improvements over the reference

1. Body text colour that passes AA.
2. A RESERVAR pill in the navigation, visible at all times.
3. Sticky bar only when it has something in it: chosen tour, date, people, WhatsApp.
4. WhatsApp as a third, lighter action on mobile.
5. Two filters, not one: type of passeio and departure point.
6. Zoom allowed, alt text on every photo, visible focus rings.
7. A footer with address, phone, WhatsApp, CNPJ and Cadastur number, which Brazilian visitors look for before paying.

### 11.6 Starter CSS

```css
/* ---------- Tokens ---------- */
:root {
  --ba-ink: #16344E;
  --ba-ink-soft: #54718A;
  --ba-brand: #0061AA;
  --ba-brand-deep: #004777;
  --ba-band: #EAF6FB;
  --ba-hairline: #CFE6F2;
  --ba-sand: #E8A33D;
  --ba-font-display: 'Josefin Sans', 'Century Gothic', Futura, sans-serif;
  --ba-font-text: 'Raleway', 'Helvetica Neue', Arial, sans-serif;
  --ba-ease: 200ms ease-in-out;
}

/* ---------- Card band ---------- */
.tour { padding: 80px 0; background: #fff; }
.tour:nth-child(odd) { background: var(--ba-band); }
.tour__inner {
  max-width: 1200px; margin: 0 auto; padding: 0 20px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 66px; align-items: start;
}
.tour__photo { aspect-ratio: 16 / 9; width: 100%; object-fit: cover; display: block; }

/* ---------- Text column ---------- */
.tour__top { display: flex; justify-content: space-between; align-items: baseline; }
.tour__eyebrow {
  font: 400 17px/1.2 var(--ba-font-display);
  letter-spacing: 2.8px; text-transform: uppercase; color: var(--ba-ink); margin: 16px 0 6px;
}
.tour__duration { font: 500 14px/26px var(--ba-font-text); color: var(--ba-ink-soft); }
.tour__title {
  font: 400 34px/1.2 var(--ba-font-display);
  letter-spacing: 3.5px; text-transform: uppercase; color: var(--ba-ink); margin: 0 0 21px;
}
.tour__prices {
  display: flex; justify-content: space-between; gap: 16px;
  padding: 17px 0 15px; margin: 0 0 29px;
  border-top: 1px solid var(--ba-hairline); border-bottom: 1px solid var(--ba-hairline);
  font: 500 18px/30px var(--ba-font-text); color: var(--ba-ink-soft);
}
.tour__prices > :first-child { color: var(--ba-ink); }
.tour__desc { font: 500 16px/28px var(--ba-font-text); color: var(--ba-ink-soft); margin: 0 0 29px; }

/* ---------- Buttons ---------- */
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 13px 40px 12px; border: 0; border-radius: 100px;
  font: 400 16px/16px var(--ba-font-display); letter-spacing: 2.3px; text-transform: uppercase;
  text-decoration: none; cursor: pointer; transition: all var(--ba-ease);
}
.btn:hover { transform: scale(.96); filter: brightness(.9) contrast(1.2); }
.btn:focus-visible { outline: 2px solid var(--ba-brand); outline-offset: 3px; }
.btn--primary { background: var(--ba-brand); color: #fff; }
.btn--tertiary { background: var(--ba-band); color: var(--ba-ink); }
.tour:nth-child(odd) .btn--tertiary { background: #fff; }
.tour__actions { display: flex; gap: 6px; flex-wrap: wrap; }

/* ---------- Tablet ---------- */
@media (max-width: 1023px) {
  .tour__inner { grid-template-columns: 5fr 7fr; gap: 40px; }
}

/* ---------- Mobile ---------- */
@media (max-width: 768px) {
  .tour, .tour:nth-child(odd) { background: #fff; padding: 10px 0 50px; }
  .tour__inner { grid-template-columns: 1fr; gap: 0; padding: 0; }
  .tour__text { margin: 36px 20px 0; }
  .tour__title { font-size: 24px; letter-spacing: 2.5px; }
  .tour__prices { display: block; }
  .tour__actions { justify-content: center; }
  .tour:nth-child(odd) .btn--tertiary { background: var(--ba-band); }
  .btn { font-size: 14px; line-height: 14px; letter-spacing: 2px; }
}
```

### 11.7 Checklist before calling a page done

- [ ] Only two interface colours on screen, plus photography.
- [ ] Every heading is uppercase Josefin Sans at weight 400 with tracking.
- [ ] No bold text anywhere.
- [ ] Every clickable thing is a pill. Every photo is square cornered.
- [ ] No shadow on anything that does not float.
- [ ] Each tour has an eyebrow, a short title, a duration, a price row, a description and exactly two buttons.
- [ ] Bands alternate, and the tertiary button fill swaps with them.
- [ ] Body text passes 4.5:1.
- [ ] A booking action is reachable from every scroll position.
