# Purple Current email signature

Two designs live here. **v2 is the current design** (new template Michael supplied);
v1 is retained for reference.

---

## v2 — current (new template)

**Status: FINAL** (2026-07-30) — hosted assets, spec-verified against ADR 0008.

Cleaner horizontal layout: name/title, then logo (left) beside a stacked contact block,
a divider rule, the "Powered by The Purple Standard" endorsement with a **right-aligned social
icon row** in the same line, and the full-width "Purple up. Power on." banner. No disclaimer
(matches the supplied template).

### Files
- `signature-purple-current-v2.html` — the **CodeTwo deliverable** (keeps dynamic `{fields}`);
  all nine `src` attributes are absolute `assets.purple-standard.app` URLs.
- `preview-v2.html` — browser preview (sample data), pointing at the same hosted URLs.
- `assets/current-logo.png` — horizontal primary-color logo, **400×174 @ 96 DPI**, display 200×87.
- `assets/endorsement.png` — "Powered by The Purple Standard" lockup, **720×34 @ 96 DPI**, display 360×17.
- `assets/badge-*.png` — six brand-purple `#411144` circle badges (Google, Facebook, Instagram,
  LinkedIn, YouTube, Yelp), **36×36 @ 96 DPI**, display 18×18, right-aligned in the endorsement row.
- `assets/banner-standard.jpg` — "Purple up. Power on." banner, **900×271 JPEG @ 96 DPI**, display 560×169.
- `assets/_src-*.svg` — Font Awesome v6.5.2 glyph sources the badges are rebuilt from. **Keep these.**
- Source files: `../purple_current/` (untouched).

### Asset spec (ADR 0008)

| Asset | Display | Source | Ratio | DPI | Notes |
|---|---|---|---|---|---|
| `current-logo.png` | 200×87 | 400×174 | 2.00× | 96 | metadata only; pixels bit-identical |
| `endorsement.png` | 360×17 | 720×34 | 2.00× | 96 | rebuilt from the 3697×179 master |
| `badge-*.png` (×6) | 18×18 | 36×36 | 2.00× | 96 | rebuilt from FA 6.5.2 |
| `banner-standard.jpg` | 560×169 | 900×271 | **1.61×** | 96 | **documented exception — see below** |

At audit on 2026-07-30 **all nine assets failed**: the logo and all six badges carried no DPI
metadata at all, the badges were 2.22× rather than 2×, the endorsement was 150 DPI (rendering at
roughly 64% size in Outlook), and the banner had no density metadata and was 1.61×.

Badges are deliberately **18×18, not the 28×28 used by Boyette and WTR DR.** Those brands have three
icons; Purple Current has six, and at 28px the row totals 213px against a 360px endorsement, which
overflows the 560px table.

Re-export recipes:

```bash
# Badges — white FA glyph fit to an 18px box on a 36px #411144 disc (glyph at 50% of disc,
# matching the house proportion measured off Boyette). -strip clears pHYs, so density is a 2nd pass.
magick -size 36x36 xc:none -fill '#411144' -draw 'circle 17.5,17.5 17.5,-0.5' disc.png
magick -background none -density 1200 _src-google.svg -resize 18x18 -fill white -colorize 100 glyph.png
magick disc.png glyph.png -gravity center -compose Over -composite -strip badge-google.png
magick badge-google.png -density 96 -units PixelsPerInch badge-google.png

# Endorsement — downscale the master; never upscale the 600×29 copy
magick ../resources/purple_standard/tps-endorsement-purple.png -resize 720x34! -strip endorsement.png
magick endorsement.png -density 96 -units PixelsPerInch endorsement.png
```

### The banner is a documented exception to ADR 0008

ADR 0008 says PNG only, at exactly 2× the display size. `banner-standard.jpg` is neither, **deliberately**:

- **900×271 is the largest banner that exists.** There is no higher-resolution master in the repo.
  Its display size is 560×169, so 2× would be 1120×338 — reachable only by *upscaling*, which
  invents no detail. A retina-scale crop comparison confirmed the "compliant" 1120×338 PNG is
  visually indistinguishable from the 900px JPEG, because both carry the same real information.
- **The PNG costs 211 KB against 49 KB** — 4.3× the weight in every email sent, for no visible gain.
- **ADR 0008's rationale for "PNG only" does not actually cover JPEG.** It reasons that the Word
  engine supports neither WebP nor SVG. Outlook renders JPEG correctly, so the rule as written is
  broader than its own justification.

What *was* fixed is the part that genuinely affected rendering: the file carried **no density
metadata** (`Units: Undefined`), so Outlook would assume 72 DPI and upscale it by 1.33×. The JFIF
APP0 density fields were **patched directly in place** rather than through ImageMagick, because
re-encoding a JPEG costs generation loss:

```python
d = bytearray(open("banner-standard.jpg","rb").read())
i = d.find(b"JFIF\x00")            # +7 = units, +8..9 = Xdensity, +10..11 = Ydensity
d[i+7] = 1                          # 1 = pixels per inch
d[i+8:i+10] = (96).to_bytes(2,"big")
d[i+10:i+12] = (96).to_bytes(2,"big")
open("banner-standard.jpg","wb").write(d)
```

Five bytes changed; pixels verified bit-identical; file size unchanged at 49,454 B.

**If a larger banner is ever exported (≥1120×338), redo this as a 2× PNG and drop the exception.**

### Hosting

`https://assets.purple-standard.app/current/email-signature/` — synced from
`~/Developer/purple-standard/websites/ps-assets/current/email-signature/`.

Verify served **bytes**, not just the status code; a 200 with `image/png` can still carry WebP,
which the Outlook Word engine cannot render:

```bash
U="https://assets.purple-standard.app/current/email-signature/current-logo.png"
curl -sS -o /tmp/p.png -w '%{http_code} %{content_type}\n' "$U?cb=$RANDOM"
file /tmp/p.png    # must report "PNG image data, 400 x 174"
```

### Layout & content
- **Order:** Name → Title → [logo | contact] → divider → endorsement + right-aligned social row → banner.
- **Social set** (v2): Google, Facebook, Instagram, LinkedIn, YouTube, Yelp — brand-purple circle badges; real profile URLs carried over from v1.
- **Contact block** is `P` (phone) → `A` (address, 2 lines) → `E` (email) — email sits under the address.
- **Phone** static `(813) 355-0865`; **Email** dynamic `{E-mail}`, auto-hides if empty.
- **Name/Title** dynamic `{First name} {Last name}` / `{Title}`.
- The **endorsement image replaces** the template's `www.purple-current.com` line above the banner.

### Colors — official Purple Current design system
- Primary purple `#411144` → name, title, contact labels, divider rule.
- Contact values `#333333`. Banner gold accent `#eaa951` (in-image).

### Links
- Logo + banner → `https://purple-current.com/`
- Endorsement → `https://www.purple-standard.com/`

### How to load it into CodeTwo
1. Signature rule → **Design** → **Edit signature** → HTML / source view.
2. Paste the entire contents of `signature-purple-current-v2.html`.
3. **No image upload needed** — all nine `src` attributes are already absolute hosted URLs.
4. Save and preview to confirm the dynamic fields resolve.

> **The email token is `{E-mail}`, with a hyphen.** `{Email}` is not valid; CodeTwo rejects it with
> "Unrecognized placeholder(s) found" and renders it as literal text in sent mail.

---

## v1 — original template (retained for reference)

Dynamic, server-side signature built from the earlier CodeTwo template (logo left,
contact block, social row, promo banner, and a disclaimer bar).

## Files
- `signature-purple-current.html` — the CodeTwo-ready snippet (keeps dynamic `{fields}`).
- `preview.html` — open in a browser to see the rendered look (sample data).
- `assets/logo.png` — trimmed stacked logo, 124×150.
- `assets/banner.png` — promo banner, 652×196 (displays at 326×98, true aspect).
- `assets/social-*.png` — six brand-purple icons (Google, Facebook, Instagram, LinkedIn, YouTube, Yelp), 46px (display 23).
- Source files: `../purple_current/` (untouched).

## Colors — from the official Purple Current design system
(`~/Downloads/PC/purple-current-design-system.md`)
- Primary purple `#411144` → name, social-contact labels, website link, social icons.
- Orange accent `#eaa951` → disclaimer divider rule (replaced the template's green `#79ca06`).
- Title/company `#2a2a2a`, contact values + address + disclaimer `#8c8c8c` (kept from the template).

## Choices
- **Phone** is static `(813) 355-0865` only (the template's mobile line was removed).
- **Email** is dynamic and auto-hides if empty. Title line is `{Title} • {Company}` (dynamic).
- **Address** on two lines: `8011 Land O' Lakes Blvd` / `Land O' Lakes, FL 34638`.
- **Banner** kept at its true 3.3:1 aspect (326×98) rather than the template's squashed 326×57 slot.
- **Social set**: Google (GMB), Facebook, Instagram, LinkedIn, YouTube, Yelp — all six you specified.
- **Disclaimer**: bar kept, text replaced with your supplied confidentiality notice, set at 8pt.

## Social icons — bundled
Pulled from Font Awesome Free brands (v6.5.2, CC-BY 4.0), recolored to `#411144`, hosted in `assets/`.
Self-contained; nothing hotlinked. (CodeTwo's gallery doesn't reliably carry GMB or Yelp, so bundling
keeps all six uniform.)

## How to load it into CodeTwo
1. Signature rule → **Design** → **Edit signature** → HTML / source view.
2. Paste the contents of `signature-purple-current.html`.
3. Upload the nine images from `assets/` (logo, banner, six icons) via the editor's image tool.
4. Save and preview to confirm the dynamic fields resolve.

## Note
Temp verification files are `_`-prefixed (`assets/_check.png`, `_render.png`) — safe to delete.
