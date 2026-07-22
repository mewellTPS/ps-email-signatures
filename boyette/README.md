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
- `assets/boy-logo.png` — logo icon, 320×221 (displays at 160×110). Used by the separate-logo variant.
- `assets/endorsement.png` — "Powered by The Purple Standard" strip, display 180×9 (source 600×29).
  Used by the separate-logo variant.
- `assets/boyette-combined.png` — combined lockup: icon + "Boyette Pump & Well" wordmark +
  "Powered by The Purple Standard" endorsement in one image, 1082×824 (displays at 190×145).
  Used by the combined-logo variant.
- `assets/badge-google.png` / `badge-facebook.png` / `badge-instagram.png` / `badge-yelp.png`
  — white glyph on brand-orange `#F93822` filled circles, 56×56 (display at 28px). Supersede the
  older bare-glyph `social-*.png` (still in `assets/`, now unused).
- Source logo: `../resources/boyette/BOY-LOGO-STACKED-COLOR-DARK.png` (untouched).

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
3. Upload that variant's images from `assets/` via the editor's image tool (CodeTwo hosts them
   and rewrites the `src`):
   - separate-logo variant: `boy-logo.png`, `endorsement.png`, + the four `badge-*.png` (six total).
   - combined-logo variant: `boyette-combined.png` + the four `badge-*.png` (five total).
4. Save and preview to confirm dynamic fields resolve against the directory.

## Note
Temp verification images may exist as `assets/_*.png` — safe to delete.
