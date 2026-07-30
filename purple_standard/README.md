# Purple Standard — email signature

Server-side CodeTwo Email Signatures 365 template. Per-person fields (name, title,
mobile, email) come from the M365 directory; the design is applied uniformly to all
outgoing mail.

**Status: FINAL** (2026-07-30) — hosted assets, both images spec-verified against ADR 0008.

## Files

| File | Purpose |
|---|---|
| `signature-purple-standard.html` | **The CodeTwo deliverable.** Dynamic template (keeps `{fields}`); both `src` attributes are absolute hosted URLs. |
| `preview.html` | Browser preview with sample data. Loads the same hosted URLs, so it shows exactly what recipients get. |
| `signature-purple-standard-v2.html` | **Shelved.** The cross-brand icon-strip experiment (ADR 0005). Not shipping — see below. |
| `preview-v2.html`, `_render-v2.png` | v2 preview + snapshot (working artifacts). |
| `assets/` | `tps-badge.png` (150×150 @ 96 DPI), `tps-endorsement.png` (1000×48 @ 96 DPI), `brands/` (v2 placeholder chips, unused). |

## Design

Single 500px table:

1. **Name + title** (left) with the **badge logo** (right, 75×75).
2. **Contact block** — `T:` / `M:` on one line, `E:` beneath, then `www.purple-standard.com`.
3. **Company address**, directly beneath the website URL.
4. **Endorsement banner**, full 500px width, as the closing element.

Two decisions from the 2026-07-30 review:

- **Address sits under the URL**, not below the banner. This groups every piece of contact
  information in one block and lets the signature end on the endorsement. (Chosen over the
  alternative of leaving it as a footer line beneath the banner.)
- **"Purple Standard," was dropped from the address line** — it was redundant beside the logo,
  the endorsement banner, and the domain.

## Font: Arial (deliberately)

The stack is `Arial, Helvetica, sans-serif`.

The signature previously specified `'Trade Gothic Next', 'Trade Gothic', Arial, Helvetica, sans-serif`.
**That first choice could never reach a recipient.** Outlook's Word rendering engine loads only fonts
installed on the reader's own machine — there is no webfont mechanism — and Trade Gothic Next is a
licensed face that is not installed anywhere by default. It silently resolved to Arial for
essentially every recipient, so the stack was expressing an intent that never took effect.

Arial is now specified outright, which changes nothing visually and removes the false expectation.
Alternatives considered and rejected: **Tahoma** (closest safe analogue to Trade Gothic's
utilitarian feel, marginally more distinctive), **Trebuchet MS** (warmer, less corporate),
**Helvetica Neue** (refined on Apple, falls back to Arial on Windows anyway), **Verdana** (most
legible but widest — 307px vs Arial's 273px on the address line), and **Arial Narrow** (closest to
Trade Gothic proportionally, but Outlook on Windows substitutes it unreliably, producing
inconsistent results between recipients).

Measured at 9pt against the 400px contact column, every candidate fit without wrapping, so the
choice was aesthetic rather than structural.

## Asset spec (ADR 0008 — 2× source at explicit 96 DPI, PNG only)

| Asset | Display | Source | Ratio | DPI |
|---|---|---|---|---|
| `tps-badge.png` | 75×75 | 150×150 | 2.00× | 96 |
| `tps-endorsement.png` | 500×24 | 1000×48 | 2.00× | 96 |

Both were already correctly sized at 2× but carried **no DPI metadata at all**, which makes a client
that assumes 72 DPI upscale them by 1.33×. The 96 DPI `pHYs` chunk was added on 2026-07-30 with the
pixel data verified **bit-identical** before and after — nothing was resampled.

```bash
# Add density without touching pixels (already correctly sized)
magick tps-badge.png -density 96 -units PixelsPerInch tps-badge.png
```

Verify by parsing the chunk, not by ImageMagick's report — it prints a correct 96 DPI as
`37.79 PixelsPerCentimeter`, which looks wrong but is right (PNG stores `pHYs` in pixels per metre;
3779 px/m ≈ 95.99 DPI).

## Hosting

`https://assets.purple-standard.app/standard/email-signature/` — synced from
`~/Developer/purple-standard/websites/ps-assets/standard/email-signature/`.

Verify served **bytes**, not just the status code. A 200 with `content-type: image/png` can still
carry WebP, which the Outlook Word engine cannot render:

```bash
U="https://assets.purple-standard.app/standard/email-signature/tps-badge.png"
curl -sS -o /tmp/p.png -w '%{http_code} %{content_type}\n' "$U?cb=$RANDOM"
file /tmp/p.png    # must report "PNG image data, 150 x 150"
```

## Load into CodeTwo

1. Paste the entire contents of `signature-purple-standard.html` into the signature editor
   (HTML / source mode).
2. **No image upload needed** — both `src` attributes are already absolute hosted URLs.
3. Re-insert the placeholders via the ribbon's **Placeholder** button rather than trusting the
   pasted text: `{First name}`, `{Last name}`, `{Title}`, `{Mobile}`, `{E-mail}`. Typed or pasted
   placeholders can fail to bind to Entra ID.
4. The `{RT}…{/RT}` tags auto-hide the mobile line when the directory value is empty.
5. Verify by send or preview, not the editor view — placeholders always look literal while editing.

> **The email token is `{E-mail}`, with a hyphen.** `{Email}` is not valid; CodeTwo rejects it with
> "Unrecognized placeholder(s) found" and renders it as literal text in sent mail.

## v2 — shelved, not shipping

`signature-purple-standard-v2.html` added a row of eight brand icons above the endorsement to build
cross-brand recognition (ADR 0005). It was reviewed on 2026-07-30 and set aside in favour of this
layout. It cannot ship as-is regardless: all eight icons in `assets/brands/` are **placeholder
chips** (coloured square + initials, generated in ImageMagick), every `href` points at
`purple-standard.com` behind a `<!-- TODO -->` marker, and MOR and ENG have no branding at all. If
it is revived it needs real brand art, per-brand destination URLs, and normalizing to ADR 0008
(the chips are 120×120 against a 40×40 display — 3×, not 2×).

## Open / assumed values

- **Hyperlink colour** is `#A263D2` on the email and website links — **assumed, never confirmed**
  against a brand spec (vault concern `0005-ps-hyperlink-blue-unconfirmed`).
- Office phone `(813) 303-9975` and the company address are static; only name, title, mobile and
  email are dynamic.
