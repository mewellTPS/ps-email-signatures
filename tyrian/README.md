# Tyrian Roofing — Email Signature

Brand-correct email signature for Tyrian Roofing (Purple Standard portfolio),
built on the standard per-brand deliverable pattern and CodeTwo Email
Signatures 365 dynamic fields.

## Files

| File | Purpose |
|---|---|
| `signature-tyrian.html` | **CodeTwo-ready** dynamic template (paste into a CodeTwo signature rule) |
| `preview.html` | Same layout with **sample data** — open in a browser to see the real thing |
| `_render.png` | Rendered snapshot of `preview.html` for visual verification |
| `assets/` | Self-hosted, retina-sized images (upload to CodeTwo during loading) |

## Layout

Two-column: **logo + endorsement** (left) │ gold divider │ **name / title /
contact / social** (right). Mirrors the approved Tyrian reference mockup.

## Colors (extracted from the supplied logo)

| Use | Color |
|---|---|
| Name, `P:` / `M:` / `E:` labels, email + website links, social discs | Tyrian purple `#531757` |
| Vertical divider | Gold `#E59519` (the logo chevron) |
| Title + contact text | Grey `#666666` |
| Endorsement | Original purple `#4D1553` (see note) |

**Endorsement — using the original for now.** A Pale Grey `#F5EFFB` recolor was
tried but that tint (RGB 245,239,251) is too light to read on white — it
collapsed into a faint bar. Reverted to the **original purple** master
(white background made transparent). If a muted/greyscale treatment is wanted
later, use Purple Grey `#BAB0C6` (the brand guide's "muted text" color), which
stays legible on white:

```bash
# from tyrian/assets/ — recolor the master to a legible muted grey, transparent bg
magick _src-endorsement.png \
  \( -clone 0 -fill '#BAB0C6' -colorize 100 \) \
  \( -clone 0 -colorspace gray -negate \) \
  -delete 0 -alpha off -compose CopyOpacity -composite \
  -resize 464x endorsement.png
```

## Assets & provenance

| Asset | Source | Processing |
|---|---|---|
| `logo.png` (520×160, 2×) | `_src-logo-full.png` (2812×878 master) | trimmed + resized to 260px display |
| `endorsement.png` (464×22, 2×) | `_src-endorsement.png` (purple master) | recolored to Pale Grey `#F5EFFB`, transparent bg |
| `social-{facebook,instagram,youtube}.png` (56×56, 2×) | Font Awesome Free **v6.5.2** brand SVGs (`_src-*.svg`) | white glyph composited on `#531757` disc |

Icon sourcing follows **ADR 0002** (bundled Font Awesome, recolored, self-hosted
— used where a brand color is required). Font Awesome pinned to v6.5.2.

## Dynamic fields (CodeTwo)

- `{First name} {Last name}`, `{Title}`, `{Phone}`, `{Mobile}`, `{E-mail}`
- `{RT}…{/RT}` wraps the **Mobile** segment and the **Email** segment so an
  empty directory field collapses cleanly (no orphaned `M:` / `E:` label).

## ⚠ Confirm before loading

1. **Social handles** — the Facebook / Instagram / YouTube hrefs are
   **best-guess** (`/tyrianroofing`, `@tyrianroofing`). Replace with the real
   Tyrian accounts before going live.
2. **Office address** — currently the placeholder `Street, City · Zip Code,
   Country`. Supply the real Tyrian office address.
3. **Website** — assumed `tyrianroofing.com`. Confirm the production domain.

## Load into CodeTwo

1. Create/edit the Tyrian signature rule → paste `signature-tyrian.html` into
   the HTML editor.
2. Upload `assets/logo.png`, `assets/endorsement.png`, and the three
   `assets/social-*.png` so CodeTwo hosts them; repoint the `src` paths to the
   hosted URLs.
3. Confirm the dynamic fields map to the correct M365 directory attributes.
4. Send a test from a Tyrian mailbox; verify on desktop + mobile.

## Re-render / re-build

```bash
# from tyrian/
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --force-device-scale-factor=2 \
  --screenshot="$PWD/_render.png" --window-size=900,320 "file://$PWD/preview.html"
magick _render.png -trim +repage -bordercolor white -border 24 _render.png
```

Asset rebuild commands (logo resize, endorsement recolor, social discs) are in
the session that produced this signature; the `_src-*` masters are retained in
`assets/` so every derived asset can be regenerated.
