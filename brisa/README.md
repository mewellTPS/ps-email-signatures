# Brisa Climate — email signature

Dynamic, server-side CodeTwo signature matching Brisa's supplied mockup: the combined
logo lockup on the left half, a vertical purple divider, a contact block on the right
half, and a full-width promo banner below.

**Status: FINAL** (2026-07-31) — hosted assets, all five spec-verified against ADR 0008.
Two content placeholders remain, listed at the bottom.

## Files

- `signature-brisa.html` — the **CodeTwo deliverable** (keeps dynamic `{fields}`); all five
  `src` attributes are absolute `assets.purple-standard.app` URLs, so no image upload is needed.
- `preview.html` — browser preview with sample data, pointing at the same hosted URLs.
- `assets/` — build sources and the exact-spec images that get synced.

## Assets

| Asset | Display | Source | Ratio | DPI |
|---|---|---|---|---|
| `brisa-logo.png` | 300×165 | 600×330 | 2.00× | 96 |
| `badge-{facebook,instagram,google}.png` | 25×25 | 50×50 | 2.00× | 96 |
| `banner-web.png` | 700×171 | 1400×342 | 2.00× | 96 |

- `brisa-logo.png` — **combined lockup**: Brisa mark + wordmark + "Powered by The Purple Standard"
  in one image, supplied by Michael 2026-07-31. Replaced the previous separate `logo.png` +
  `endorsement.png` pair. Its aspect is **1.82**, against the old logo's 2.51, so the display slot
  moved from 300×120 to **300×165** — same 300px width, keeping the left column aligned. Net height
  is near-identical: the old logo + 24px gap + endorsement came to 159px; the lockup is 165px.
- `badge-*.png` — white Font Awesome v6.5.2 glyph on a `#48104F` disc, glyph fit to 25px (50% of
  the disc), matching the house proportion used across the portfolio (ADR 0006).
- `banner-web.png` — promo banner; the blue→purple→red gradient bar is part of the image.
- Build sources, untouched: `assets/BC-HORIZONTAL-…-PURPLETEXT.jpg`, `assets/banner.png`
  (976 KB full-res master for `banner-web.png`).

Retired 2026-07-31 as superseded: `logo.png` and `endorsement.png` (folded into the combined
lockup), `social-{facebook,instagram,youtube}.png` (renamed to `badge-*` per ADR 0006), and
`badge-youtube.png` (YouTube replaced by Google).

Re-export recipes — `-strip` clears `pHYs`, so density is always a second pass:

```bash
# Combined logo: 2x the 300x165 slot
magick brisa-logo-source.png -resize 600x -strip brisa-logo.png
magick brisa-logo.png -density 96 -units PixelsPerInch brisa-logo.png

# Badges: white glyph fit to 25px on a 50px #48104F disc
magick -size 50x50 xc:none -fill '#48104F' -draw 'circle 24.5,24.5 24.5,-0.5' disc.png
magick -background none -density 1200 _src-google.svg -resize 25x25 -fill white -colorize 100 glyph.png
magick disc.png glyph.png -gravity center -compose Over -composite -strip badge-google.png
magick badge-google.png -density 96 -units PixelsPerInch badge-google.png
```

Brisa keeps no `_src-*.svg` of its own; the glyph sources live in `../boyette/assets/` (Google,
Facebook, Instagram) and `../tyrian/assets/` (Facebook, Instagram, YouTube).

Badges display at **25×25**, Brisa's approved size. Boyette and WTR DR use 28×28 — if the portfolio
should match exactly, regenerate at 56×56 and change the four `width`/`height`/`style` pairs.

## Social links (set 2026-07-31)

| Badge | Link |
|---|---|
| Facebook | **none — badge shown, deliberately not hyperlinked** |
| Instagram | `https://www.instagram.com/brisa.climate.solutions` |
| Google | `https://share.google/AfTfkPPBgOVDHaqi2` (Google Business Profile) |

The **banner** also links to `https://share.google/AfTfkPPBgOVDHaqi2` to collect GBP reviews — the
same URL as the Google badge, as specified.

The Facebook badge is intentionally rendered as a bare `<img>` with no surrounding `<a>`. If a
Facebook URL arrives later, wrap it to match the other two.

## Colors — ⚠ asset-derived (no official Brisa brand guide exists)

Sampled from the supplied logo/banner with ImageMagick:

- Deep purple `#48104F` — name, contact labels (`P:`/`M:`/`E:`), divider, badge discs, `www` link.
- Coral `#FB3748` — the "CLIMATE" wordmark / warm accent. Held in reserve; all signature text
  stays purple per the mockup.
- Blue `#3D82FB` — logo/gradient accent.
- Contact values `#2a2a2a`, title `#7a7a7a`.

If Brisa has an official brand guide, reconcile these against it.

## Dynamic fields (CodeTwo)

- `{First name} {Last name}`, `{Title}` — name + title.
- `{Phone}`, `{Mobile}`, `{E-mail}` — each wrapped in `{RT}...{/RT}` so an empty line auto-hides.
- `data-codetwo-visible` attributes are set for the editor's field toggles.

> **The email token is `{E-mail}`, with a hyphen.** `{Email}` is not valid; CodeTwo rejects it with
> "Unrecognized placeholder(s) found" and renders it as literal text in sent mail.

## How to load it into CodeTwo

1. Create/edit the Brisa signature rule; open the HTML source view.
2. Paste the entire contents of `signature-brisa.html`.
3. **No image upload needed** — all five `src` attributes are already absolute hosted URLs.
4. Save and preview with a Brisa test user to confirm the dynamic fields resolve and empty lines
   auto-hide.

## Hosting

`https://assets.purple-standard.app/brisa/email-signature/` — synced from
`~/Developer/purple-standard/websites/ps-assets/brisa/email-signature/`.

Verify served **bytes**, not just the status code; a 200 with `image/png` can still carry WebP,
which the Outlook Word engine cannot render:

```bash
U="https://assets.purple-standard.app/brisa/email-signature/brisa-logo.png"
curl -sS -o /tmp/p.png -w '%{http_code} %{content_type}\n' "$U?cb=$RANDOM"
file /tmp/p.png    # must report "PNG image data, 600 x 330"
```

## Still outstanding

1. **Company address** — the `Street, City` / `Zip Code, Country` cells are still placeholders.
   Brisa's real address is needed before this ships.
2. **Palette** — `#48104F` / `#FB3748` were derived from the artwork, never confirmed against a
   brand guide.
3. **Office phone** — `P:` uses the dynamic `{Phone}` directory field. If Brisa prefers a single
   fixed company line, hardcode it in the `P:` cell instead.

## Notes

- Layout is a 700px table: left half (combined logo, 300px wide), 2px `#48104F` divider,
  right-half contact grid, full-width banner.
- Custom brand fonts aren't email-safe; the signature uses Arial throughout.
