# Tyrian Roofing — Email Signature

Brand-correct email signature for Tyrian Roofing (Purple Standard portfolio),
built on the standard per-brand deliverable pattern and CodeTwo Email
Signatures 365 dynamic fields.

**Status: FINAL** (2026-08-03) — hosted assets, all four spec-verified against ADR 0008.
Three content items still need confirming; see below.

## Files

| File | Purpose |
|---|---|
| `signature-tyrian.html` | **The CodeTwo deliverable.** Dynamic template; all four `src` attributes are absolute hosted URLs, so no image upload is needed. |
| `preview.html` | Same layout with **sample data**, pointing at the same hosted URLs. |
| `_render.png` | Rendered snapshot of `preview.html` for visual verification. |
| `assets/` | Build masters plus the exact-spec images that get synced. |

## Layout

Two-column: **combined logo lockup** (left) │ gold divider │ **name / title /
contact / social** (right). Mirrors the approved Tyrian reference mockup.

## Colors (extracted from the supplied logo)

| Use | Color |
|---|---|
| Name, `P:` / `M:` / `E:` labels, email + website links, social discs | Tyrian purple `#531757` |
| Vertical divider | Gold `#E59519` (the logo chevron) |
| Title + contact text | Grey `#666666` |

## Assets

| Asset | Display | Source | Ratio | DPI |
|---|---|---|---|---|
| `tyrian-logo.png` | 260×98 | 520×196 | 2.00× | 96 |
| `badge-{facebook,instagram,youtube}.png` | 28×28 | 56×56 | 2.00× | 96 |

`tyrian-logo.png` is a **combined lockup** — the Tyrian chevron mark, "TYRIAN ROOFING"
wordmark, and "Powered by The Purple Standard" in one image — supplied by Michael 2026-07-31.
It replaced the previous separate `logo.png` + `endorsement.png` pair, so the separate
endorsement image was removed from the markup; leaving it would have printed the endorsement
twice. Its aspect is **2.64** against the old logo's 3.25, so the display slot moved from
260×80 to **260×98**, keeping the 260px width. Net left-column height barely changes: the old
logo + 14px gap + endorsement came to 105px; the lockup is 98px.

It arrived at 1480×560 @ **300 DPI**, which Outlook's 96 DPI baseline would have rendered at
roughly a third of intended size. Now 520×196 @ 96.

Badges were already the correct house style *and* already exactly 2×, so they were **not
rebuilt** — only the DPI was added and the files renamed `social-*` → `badge-*` per ADR 0006.
Pixel data was verified **bit-identical** before and after, so the approved artwork is untouched.

Retired 2026-08-03 as superseded: `logo.png` and `endorsement.png` (folded into the lockup),
and `social-{facebook,instagram,youtube}.png` (renamed).

Masters retained in `assets/` so every derived asset can be regenerated:
`_src-logo-full.png` (2812×878), `_src-endorsement.png`, `_src-{facebook,instagram,youtube}.svg`
(Font Awesome Free **v6.5.2**, per ADR 0002; pinned).

Re-export recipes — `-strip` clears `pHYs`, so density is always a second pass:

```bash
# Combined logo: 2x the 260x98 slot
magick tyrian-logo-source.png -resize 520x196! -strip tyrian-logo.png
magick tyrian-logo.png -density 96 -units PixelsPerInch tyrian-logo.png

# Badges: white FA glyph on a 56px #531757 disc, glyph at 50% of the disc
magick -size 56x56 xc:none -fill '#531757' -draw 'circle 27.5,27.5 27.5,-0.5' disc.png
magick -background none -density 1200 _src-facebook.svg -resize 28x28 -fill white -colorize 100 glyph.png
magick disc.png glyph.png -gravity center -compose Over -composite -strip badge-facebook.png
magick badge-facebook.png -density 96 -units PixelsPerInch badge-facebook.png
```

Verify DPI by parsing the `pHYs` chunk, not ImageMagick's report — it prints a correct 96 DPI as
`37.79 PixelsPerCentimeter`, which looks wrong but is right (PNG stores `pHYs` in pixels per
metre; 3779 px/m ≈ 95.99 DPI).

## Dynamic fields (CodeTwo)

- `{First name} {Last name}`, `{Title}`, `{Phone}`, `{Mobile}`, `{E-mail}`
- `{RT}…{/RT}` wraps the **Mobile** segment and the **Email** segment so an empty directory
  field collapses cleanly (no orphaned `M:` / `E:` label).

> **The email token is `{E-mail}`, with a hyphen.** `{Email}` is not valid; CodeTwo rejects it
> with "Unrecognized placeholder(s) found" and renders it as literal text in sent mail.

## ⚠ Confirm before loading

1. **Social handles** — the Facebook / Instagram / YouTube hrefs are **best-guess**
   (`/tyrianroofing`, `@tyrianroofing`). Replace with the real Tyrian accounts before going live.
2. **Office address** — currently the placeholder `Street, City · Zip Code, Country`.
3. **Website** — assumed `tyrianroofing.com`. Confirm the production domain.

## Hosting

`https://assets.purple-standard.app/tyrian/email-signature/` — synced from
`~/Developer/purple-standard/websites/ps-assets/tyrian/email-signature/`.

Verify served **bytes**, not just the status code; a 200 with `image/png` can still carry WebP,
which the Outlook Word engine cannot render:

```bash
U="https://assets.purple-standard.app/tyrian/email-signature/tyrian-logo.png"
curl -sS -o /tmp/p.png -w '%{http_code} %{content_type}\n' "$U?cb=$RANDOM"
file /tmp/p.png    # must report "PNG image data, 520 x 196"
```

## Load into CodeTwo

1. Create/edit the Tyrian signature rule → paste the entire contents of `signature-tyrian.html`
   into the HTML editor.
2. **No image upload needed** — all four `src` attributes are already absolute hosted URLs.
3. Confirm the dynamic fields map to the correct M365 directory attributes.
4. Send a test from a Tyrian mailbox; verify on desktop + mobile.

## Re-render

```bash
# from tyrian/
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --force-device-scale-factor=2 \
  --screenshot="$PWD/_render.png" --window-size=900,320 "file://$PWD/preview.html"
magick _render.png -trim +repage -bordercolor white -border 24 _render.png
```
