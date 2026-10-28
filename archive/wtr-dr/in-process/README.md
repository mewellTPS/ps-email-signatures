# WTR DR email signature

Dynamic, server-side signature for CodeTwo. Condensed three-zone layout:
**logo | name + contact | address + social**, no headshot.

**Status: FINAL** (2026-07-30) — hosted assets, all five spec-verified against ADR 0008.

## Files
- `signature-wtrdr.html` — the **CodeTwo deliverable** (Option 2, three-zone). Keeps dynamic
  `{fields}`; all five `src` attributes are absolute `assets.purple-standard.app` URLs.
- `signature-wtrdr-option1.html` — **alternate** layout (Option 1, compact stack: logo + single
  column, Boyette-style). Not updated to hosted URLs; still points at relative `assets/` paths.
- `preview.html` — browser preview (sample data). Not updated to hosted URLs.
- `assets/logo.png` — logo, **200×200 @ 96 DPI**, displays at 100×100. **Hosted.**
- `assets/badge-{google,facebook,instagram}.png` — white glyph on link-blue `#2E6DA6` filled
  circles, **56×56 @ 96 DPI**, display at 28×28. **Hosted.**
- `assets/endorsement.png` — "Powered by The Purple Standard", **380×18 @ 96 DPI**, displays at
  190×9, original purple. **Hosted.**
- `assets/_preview-*.png` — old navy preview stand-ins, unused (safe to delete).
- `assets/headshot.png` — leftover from the previous headshot layout; **no longer referenced**.
- Source files: `../resources/wtr_dr/` (untouched).

## Asset spec (ADR 0008 — 2× source at explicit 96 DPI, PNG only)

| Asset | Display | Source | Ratio | DPI |
|---|---|---|---|---|
| `logo.png` | 100×100 | 200×200 | 2.00× | 96 |
| `badge-*.png` (×3) | 28×28 | 56×56 | 2.00× | 96 |
| `endorsement.png` | 190×9 | 380×18 | 2.00× | 96 |

**The logo was rebuilt on 2026-07-30.** WTR DR has no light-background logo — the only asset
(and its 2048×2048 source) is a **white wordmark with a drop shadow**, made for dark backgrounds,
which on white reads as a gray smudge. The wordmark was recoloured to navy `#1C2458` and the
shadow removed, rebuilt from the 2048px source. Recipe:

```bash
# Split the 2048×2048 source: droplet y=191-1468, wordmark y=1510-1952
magick WTRDR1.png -crop 2048x1278+0+191  +repage droplet.png
magick WTRDR1.png -crop 2048x443+0+1510  +repage wm-raw.png
# Isolate the letters (high alpha AND high luminance) — excludes the soft shadow
magick wm-raw.png \( -clone 0 -alpha extract -threshold 50% \) \
       \( -clone 0 -alpha off -colorspace gray -threshold 72% \) \
       -delete 0 -compose Multiply -composite wm-mask.png
magick -size WxH xc:'#1C2458' wm-mask.png -alpha off -compose CopyOpacity -composite wm-navy.png
# Recompose, then normalize to spec (-strip clears pHYs, so density is a second pass)
magick droplet.png \( -size 10x110 xc:none \) wm-navy.png -append -trim +repage \
       -resize 200x200 -background none -gravity center -extent 200x200 -strip logo.png
magick logo.png -density 96 -units PixelsPerInch logo.png
```

Badges were rebuilt from Font Awesome 6.5.2 sources (borrowed from `../boyette/assets/_src-*.svg`),
white glyph fit to a 28px box on a 56px `#2E6DA6` disc — proportions measured off Boyette's badges
so the house style matches. The endorsement was **downscaled** from the 3697×179 master in
`../resources/purple_standard/tps-endorsement-purple.png`, never upscaled from the 600×29 copy.

## Hosting

`https://assets.purple-standard.app/wtrdr/email-signature/` — synced from
`~/Developer/purple-standard/websites/ps-assets/wtrdr/email-signature/`.

Verify served **bytes**, not just the status code — a 200 with `image/png` can still carry WebP,
which Outlook's Word engine cannot render:

```bash
U="https://assets.purple-standard.app/wtrdr/email-signature/logo.png"
curl -sS -o /tmp/p.png -w '%{http_code} %{content_type}\n' "$U?cb=$RANDOM"
file /tmp/p.png   # must report "PNG image data, 200 x 200"
```

## Colors (pulled from the logo — WTR DR has no brand guide)
- Dark navy `#1C2458` (drop base) → name, labels (Phone:/Email:), the zone dividers.
- Link blue `#2E6DA6` — deepened from the logo's `#5D9ACE` highlight for readability → email + website links.
- Gray `#666666` → title and body values (kept from the template for readability).

## Pasting into CodeTwo (important)
Pasting the HTML source only lays out the **structure**. Dynamic fields and images must be
re-inserted through CodeTwo's ribbon so the program links them — otherwise they show as literal
`{placeholders}` / broken image text (as seen in the first editor test).

1. **Placeholders** (`{First name}`, `{Last name}`, `{Title}`, `{E-mail}`): after pasting, delete each
   typed placeholder and re-insert it via **Placeholder** on the ribbon. Typed/pasted placeholders can
   fail to link to Entra ID.

   > **The email token is `{E-mail}` — with a hyphen.** `{Email}` is *not* a valid CodeTwo
   > placeholder; the template editor rejects it with "Unrecognized placeholder(s) found" and
   > renders it as literal plain text in sent mail. This file used `{Email}` until 2026-07-30
   > and was the only signature in the portfolio to do so — the other eight all use `{E-mail}`.
   > Use `{From e-mail}` instead if you want the alias the message was actually sent from.
2. **Images: nothing to upload.** All five `src` attributes are already absolute hosted URLs, so
   skip the image button entirely. (This differs from the earlier instruction to upload assets —
   that applied when the file used relative `assets/` paths.)
3. **RT tags**: `{RT}…{/RT}` wrap the Email element so an empty value removes the whole line. Keep the
   closing `{/RT}` at the start of the following line (already set up this way in the file).
4. **Verify by send/preview**, not by the editor view — placeholders always look literal while editing.

## Layout
Single table row, three vertically-centered zones separated by 2px navy dividers (`border-left`):
1. **Logo** (100×100) — sets the row height; the other zones center against it.
2. **Name / Title / Phone / Email.**
3. **Address / Website / social icons.**

No fixed height and no photo, so the zones sit tight against their content — the empty space from the
old headshot layout is gone. (Note: `vertical-align: middle` renders correctly in browsers and webmail;
Outlook's Word engine may center less precisely.)

## Choices
- **Headshot removed** — `{Photo 1}` is gone; the signature no longer depends on a directory photo.
- **Phone** is static `813-429-8737` only (Mobile line removed).
- **Email** is dynamic and auto-hides if empty (`{RT}…{/RT}`).
- **Address** condensed to two lines (`8011 Land O' Lakes Blvd` / `Land O' Lakes, FL 34638`).
- **Social set**: Google (GMB), Facebook, Instagram — only the three you specified.

## Social icons — hosted badges
White Font Awesome Free brand glyphs (v6.5.2, CC-BY 4.0) composited onto link-blue `#2E6DA6` filled
circles — the unified circle-badge house style (ADR 0006), so all brands match. Nothing hotlinked
from a third party; served from our own Cloudflare-backed host. This replaced the earlier
CodeTwo-gallery plan and settled the blue-vs-navy question in favor of link-blue `#2E6DA6`.

Display size went **18×18 → 28×28** on 2026-07-30 (only three icons, so they can carry more visual
weight on the line), with the inter-icon gap nudged 13→15px. 28×28 now matches Boyette, so the two
brands share one badge spec.

**In CodeTwo:** paste `signature-wtrdr.html` and you're done — no image upload, no gallery step.
The profile URLs are already in the HTML.

## Note
Preview images are `_`-prefixed (`assets/_preview-*.png`) — safe to delete; not part of the live
signature. A stale 600×29 `endorsement.png` also sits in this folder alongside the README (the live
one is `assets/endorsement.png`) — safe to delete.
