# Boyette Pump & Well email signature

Dynamic, server-side signature recreated from the reference layout (left logo,
vertical divider, right-side content with a social icon row).

There are two variants of the signature — same right-side content (two locations, social row),
different logo treatment on the left. Pick one when loading into CodeTwo.

## Files
- `signature-boyette.html` — **separate-logo variant.** The CodeTwo-ready snippet (keeps dynamic
  `{fields}`) using the logo icon + a separate "Powered by The Purple Standard" endorsement strip.
- `preview.html` — browser preview of the separate-logo variant (sample data).
- `signature-boyette-combined.html` — **combined-logo variant.** Same snippet but the left cell is
  a single combined lockup (icon + wordmark + endorsement in one image).
- `preview-combined.html` — browser preview of the combined-logo variant (sample data).
- `assets/boyette-logo.png` — **upload/hosting master** for the combined lockup: 380×290,
  displays at 190×145. Derived from `boyette-combined.png`. This is the file to host.
- `assets/boyette-combined.png` — full-resolution combined lockup: icon + "Boyette Pump & Well"
  wordmark + "Powered by The Purple Standard" endorsement in one image, 1082×824. Master source
  for re-exports; too large to host directly.
- `assets/badge-google.png` / `badge-facebook.png` / `badge-instagram.png` / `badge-yelp.png`
  — white glyph on brand-orange `#F93822` filled circles, 56×56 (display at 28px). Supersede the
  older bare-glyph `social-*.png` (still in `assets/`, now unused).
- Source logo: `../resources/boyette/BOY-LOGO-STACKED-COLOR-DARK.png` (untouched).

> **`assets/boy-logo.png` and `assets/endorsement.png` were deleted**, so
> `signature-boyette.html` (the separate-logo variant) currently references two missing
> images. Either re-export them from the source logo or retire that variant.

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
2. Paste the contents of your chosen variant — `signature-boyette.html` (separate logo) or
   `signature-boyette-combined.html` (combined lockup).
3. Images — pick one of:
   - **Embedded (CodeTwo's own recommendation):** upload from `assets/` via the editor's image
     tool, choosing *Embedded picture*. CodeTwo attaches them as hidden attachments, so they
     always render and no external host can rewrite the format. For the combined variant:
     `boyette-logo.png` + the four `badge-*.png` (five total).
   - **Externally hosted:** replace each `src="assets/..."` with its hosted URL. Verify each URL
     serves genuine PNG bytes before shipping — see the WebP caveat below.
4. Save and preview to confirm dynamic fields resolve against the directory.

## Hosting caveat — verify served bytes, not just the URL

The interim host (ACE's WordPress + Cloudflare) serves **WebP bytes from `.png` URLs**. A WebP
plugin generates a `.png.webp` sibling and Cloudflare caches it under the `.png` cache key with
no `Vary: Accept`, so every recipient gets WebP regardless of their client — which the Outlook
Word engine cannot render. The origin itself is fine; only the cached edge response is wrong.

Check any candidate URL like this — a cache-buster reveals what the origin actually holds:

```bash
curl -sI "$URL"          | grep -i content-type   # what recipients get
curl -sI "$URL?cb=$RANDOM" | grep -i content-type # what the origin holds
```

If those disagree, the CDN is serving a converted variant. Fix at the host (purge + exclude
`/wp-content/uploads/` from the WebP rewrite), or use embedded images instead.

## Note
Temp verification images may exist as `assets/_*.png` — safe to delete.
