# Boyette Pump & Well email signature

Dynamic, server-side signature recreated from the reference layout (left logo,
vertical divider, right-side content with a social icon row).

**Status: FINAL.** One variant, hosted assets, spec-verified against ADR 0008.

## Files
- `signature-boyette-combined.html` — **the CodeTwo deliverable.** Keeps the dynamic `{fields}`;
  the left cell is a single combined lockup (icon + wordmark + endorsement in one image). All five
  `src` attributes are absolute `assets.purple-standard.app` URLs — paste as-is, no image upload.
- `preview-combined.html` — browser preview with sample data. Points at the **same hosted URLs**,
  so opening it verifies exactly what recipients will load.
- `assets/boyette-logo.png` — the combined lockup, 380×290, displays at 190×145. **Hosted.**
- `assets/boyette-combined.png` — full-resolution master, 1082×824. Kept only as the re-export
  source for the recipe below; never hosted or referenced.
- `assets/badge-google.png` / `badge-facebook.png` / `badge-instagram.png` / `badge-yelp.png`
  — white glyph on brand-orange `#F93822` filled circles, 56×56, display at 28px. **Hosted.**
- `assets/_src-*.svg` — Font Awesome v6.5.2 glyph sources for the badges.
- Source logo: `../resources/boyette/BOY-LOGO-STACKED-COLOR-DARK.png` (untouched).

The separate-logo variant (`signature-boyette.html`, `preview.html`) was **retired** — the
combined lockup is the final design, and its two assets (`boy-logo.png`, `endorsement.png`) are
superseded by `boyette-logo.png`.

## Hosting

Assets live at `https://assets.purple-standard.app/boyette/email-signature/`, served from the
Cloudflare-backed `ps-assets` project. The local source of truth for what gets synced is:

```
~/Developer/purple-standard/websites/ps-assets/boyette/email-signature/
```

Workflow: build the exact-spec image here in `assets/`, copy it to that folder, sync to
Cloudflare, then re-probe the URL to confirm served bytes (see caveat below).

## Asset spec (CodeTwo + Outlook)

Every hosted or embedded image in this signature follows the same two rules:

| Rule | Value | Why |
|---|---|---|
| Source dimensions | **exactly 2× the display size** | Sharp on retina/HiDPI. CodeTwo recommends double-sized PNG/JPG for HD/4K/retina screens, and states Outlook honors width/height scaling correctly. |
| DPI metadata | **explicit 96 DPI** (`pHYs` = 3779 px/m) | Outlook's Word engine renders at a 96 DPI baseline and rescales images whose metadata differs — a 150 DPI image renders at 64% size, a 72 DPI one at 133%. |
| Display size | set in **both** the HTML `width`/`height` attributes **and** inline `style` | Outlook ignores CSS-only sizing; attribute-only sizing is ignored by some clients. Belt and braces per CodeTwo. |
| Format | PNG only | Outlook (Word engine) has no WebP or SVG support. |

Current spec for this signature:

| Asset | Display | Source | DPI |
|---|---|---|---|
| `boyette-logo.png` | 190×145 | 380×290 | 96 |
| `badge-*.png` (×4) | 28×28 | 56×56 | 96 |

Re-export recipe (ImageMagick — `-strip` clears `pHYs`, so density must be a second pass):

```bash
magick boyette-combined.png -resize 380x290! -strip boyette-logo.png
magick boyette-logo.png -density 96 -units PixelsPerInch boyette-logo.png
```

**Known residual risk:** CodeTwo notes Apple Mail can disregard scaling instructions,
most often when a message is replied to — a 2× source would then render at full size.
Accepted trade-off: Outlook is the primary target and handles scaling correctly.

## Design decisions
- Brand colors sampled from the logo: red-orange `#F93822` (website link + social icons),
  blues `#3C81F5` / `#335E89` (logo only).
- Name, title, P:/M:/E: labels, phone, email, and address are **black**; only the website
  link is orange — matching the reference.
- Font: Arial / Helvetica (web-safe). No brand font was specified; say the word if Boyette
  has one and I'll swap the stack.
- Two locations, both **static**, stacked as paired phone + address blocks (no mobile line, no location labels):
  - `(813) 923-0008` — 8011 Land O' Lakes Blvd, Land O' Lakes, FL 34638 (primary, listed first)
  - `(352) 830-7444` — 15215 N Hwy 329, Reddick, FL 32686
  Email and website are shared (one each), below the location blocks.
- Social set: Google Business, Facebook, Instagram, Yelp (LinkedIn/YouTube dropped per your call).
- Vertical divider is a 2px dark-gray rule (`border-left`). The reference's small orange tick
  at the top of the divider is omitted — it's unreliable across email clients. Easy to add back
  with a nested element if you want it.

## Social icons — sourcing
Font Awesome Free brand glyphs (v6.5.2, CC-BY 4.0) rendered white and composited onto
brand-orange `#F93822` filled circles, rasterized locally. Self-contained; nothing hotlinked.

## How to load it into CodeTwo
1. Signature rule → **Design** step → **Edit signature** → HTML / source view.
2. Paste the entire contents of `signature-boyette-combined.html`.
3. **No image upload needed** — all five `src` attributes are already absolute hosted URLs.
4. Save and preview to confirm the dynamic fields resolve against the directory.

## Hosting caveat — verify served bytes, not just the URL

A 200 response is not proof of PNG. The previous interim host (ACE's WordPress + Cloudflare)
returned **WebP bytes from `.png` URLs**: a WebP plugin generated a `.png.webp` sibling and
Cloudflare cached it under the `.png` key with no `Vary: Accept`, so every recipient got WebP —
which the Outlook Word engine cannot render. The origin was fine; only the cached edge response
was wrong. `assets.purple-standard.app` was verified clean, but re-check after any host change:

```bash
U="https://assets.purple-standard.app/boyette/email-signature/boyette-logo.png"
curl -sS -o /tmp/p.png -w '%{http_code} %{content_type}\n' "$U?cb=$RANDOM"
file /tmp/p.png    # must report "PNG image data, 380 x 290" — not WebP
```

Check the **bytes**, not the `content-type` header alone; a misconfigured host can send
`image/png` over WebP payload.
