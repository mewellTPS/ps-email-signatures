# Brisa Climate email signature — design spec

**Date:** 2026-07-22
**Brand:** Brisa Climate (Purple Standard portfolio — HVAC / climate)
**Status:** Approved (visual mockup approved 2026-07-22)
**Build:** email-signatures (6th brand; follows the established per-brand deliverable pattern)

## Overview

One dynamic, CodeTwo-ready HTML signature for Brisa Climate, matching the
supplied mockup: a two-column top zone (logo + endorsement on the left half, a
vertical divider, contact block on the right half) over a full-width promo
banner. Built **mock-first** — per-person fields come from the M365 directory
via CodeTwo; brand-level items that Brisa hasn't supplied yet (office phone,
company address, social profile URLs) ship as clearly-marked placeholders that
point at working interim targets, never dead `#`.

## Layout

- Outer table: **700px** wide, `border-collapse: collapse`.
- **Top row, left half (`td` width 340px):** Brisa horizontal logo (300px wide)
  on top; the shared "✓ Powered by The Purple Standard" endorsement strip (300px
  wide — **same width as the logo**) beneath it, separated by white space so it
  sits at the bottom-left, aligned with the social row.
- **Vertical divider:** 2px solid `#48104F`, implemented as the left border of
  the contact cell (spans the top row only, stops above the banner).
- **Top row, right half (contact cell, 30px left padding):**
  - Name — `{First name} {Last name}`, 14pt bold `#48104F`
  - Title — `{Title}`, 10.5pt `#7a7a7a`
  - Aligned 2-column grid (10.5pt): row 1 `P: ｜ M:`, row 2 `E: ｜ www`,
    row 3 `Street, City ｜ Zip Code, Country`
  - Social icons — Facebook, Instagram, YouTube, grouped tight (~7px gap)
- **Bottom row:** full-width promo banner (700px), `colspan=2`. The
  blue→purple→red gradient bar is baked into the banner asset.

## Palette (asset-derived — ⚠ no official Brisa brand guide exists)

Sampled directly from the supplied logo/banner with ImageMagick:

- **Deep purple `#48104F`** — name, contact labels (`P:`/`M:`/`E:`), vertical
  divider, endorsement, `www` link. (Nearly identical to PS Standard `#49104F`.)
- **Coral `#FB3748`** — the "CLIMATE" wordmark / warm accent. Held in reserve;
  the mockup keeps all signature text purple.
- **Blue `#3D82FB`** — logo/gradient accent (appears in the logo and banner bar).
- Contact values `#2a2a2a`; title `#7a7a7a`.

**Assumption to confirm:** if Brisa has an official brand guide with exact
hexes, these asset-derived values should be reconciled against it.

## Fields — dynamic vs. static/mock

| Element | Treatment | Source |
|---|---|---|
| Name | Dynamic `{First name} {Last name}` | M365 directory |
| Title | Dynamic `{Title}` | M365 directory |
| Office phone (`P:`) | Dynamic `{Phone}`, `{RT}` auto-hide if empty | M365 directory |
| Mobile (`M:`) | Dynamic `{Mobile}`, `{RT}` auto-hide if empty | M365 directory |
| Email (`E:`) | Dynamic `{E-mail}`, `{RT}` auto-hide if empty | M365 directory |
| Website (`www`) | Static `www.brisaclimate.com` | brand domain (real) |
| Company address | **Static** placeholder `Street, City` / `Zip Code, Country` (`TODO` real address) | brand-level |
| Social URLs | **Mock** — platform root URLs + `TODO` handle comments | brand-level |

All three contact-number/email lines (`P:`/`M:`/`E:`) are dynamic directory
fields wrapped in `{RT}` so any empty one auto-hides — nothing broken ships if
loaded before values exist. This favors "nothing broken ships" over the older
"office phone static" default; if Brisa wants a fixed company main line instead,
hardcode `P:` — noted in the README. Only the genuinely brand-static items
(company address, social profile URLs) remain fill-in placeholders.

## Assets (retina 2×, self-hosted in `brisa/assets/`)

| Asset | Source | Output | Display |
|---|---|---|---|
| `logo.png` | `BC-HORIZONTAL-…-PURPLETEXT.jpg` 1202×524, `-fuzz 6% -trim` (white bg kept), resize 600w | 600×239 | 300×120 |
| `banner-web.png` | `banner.png` 3115×760, resize 1400w | 1400×342 | 700×171 |
| `endorsement.png` | shared PS strip (unchanged) | 600×29 | 300×15 |
| `social-{facebook,instagram,youtube}.png` | Font Awesome Free brands v6.5.2 SVG (reused from `purple-current/assets/_src-*.svg`) → white glyph on `#48104F` 52px disc | 52×52 | 25×25 |

Social-badge recipe: `magick -size 52x52 xc:none -fill "#48104F" -draw "circle 26,26 26,3"` for the disc; render each glyph SVG at 26px and recolor to white via `-channel RGB -evaluate set 100%`; composite `-gravity center`.

## Deliverable files (`brisa/`)

- `signature-brisa.html` — CodeTwo-ready snippet with dynamic `{fields}` + `{RT}` tags + `data-codetwo-visible` attributes
- `preview.html` — browser-renderable, sample data (approved mockup)
- `README.md` — decisions, mock-first TODOs, CodeTwo load steps
- `assets/` — the images above (self-hosted, nothing hotlinked)

## Mock-first links (interim → `TODO` real)

- Logo, banner, `www` → `https://brisaclimate.com/`
- Endorsement → `https://www.purple-standard.com/`
- Facebook/Instagram/YouTube → platform root URLs, each with a `TODO` comment to
  insert the real Brisa profile URL. No dead `#`.

## Open items to confirm with Michael

1. Brand palette vs. an official Brisa guide (if one exists).
2. Real Brisa office phone, company address, and social profile URLs.
3. Office phone static (current) vs. dynamic `{Phone}`.
4. CodeTwo load: paste HTML, upload the 5 `assets/` images, confirm dynamic
   fields resolve. (Not yet loaded — same status as the other brands.)

## Out of scope

- Loading into CodeTwo (project-wide, pending for all brands).
- Outlook desktop render verification.
- Any per-person customization beyond directory fields.
