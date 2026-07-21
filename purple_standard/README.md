# Purple Standard — email signature

Server-side CodeTwo Email Signatures 365 template. Per-person fields (name, title,
phone, email) come from the M365 directory; the design is applied uniformly to all
outgoing mail.

## Files

| File | Purpose |
|---|---|
| `signature-purple-standard-v2.html` | **Active design.** CodeTwo-ready dynamic template (keeps `{fields}`). |
| `signature-purple-standard.html` | v1 (prior design — website line, address at bottom, no brand-icon row). Kept for reference. |
| `preview-v2.html` | Browser-renderable preview of v2 with sample data + placeholder chips. |
| `preview.html` | v1 preview. |
| `_render-v2.png` | Rendered snapshot of the v2 preview (working artifact). |
| `assets/` | `tps-badge.png` (75×75), `tps-endorsement.png` (500×24), `brands/` (icon chips). |

## v2 changes vs v1

1. **Website URL line removed** from the contact block.
2. **Company address moved up** — now sits directly below the T/M + E lines (where the URL used to be), instead of at the very bottom.
3. **New brand-icon row** added above the "Powered by The Purple Standard" endorsement banner, to build cross-brand recognition across the portfolio.

## Brand-icon row — placeholders, needs real assets

The icons in `assets/brands/` are **placeholder chips** (color square + initials,
generated with ImageMagick) standing in until the real brand images are hosted.
Every icon link currently points to `https://www.purple-standard.com` as an interim
target and is marked `<!-- TODO -->` in the HTML.

Icon order (left → right) and status:

| # | Brand | Chip file | Status |
|---|---|---|---|
| 1 | ACE Septic & Waste | `brand-ace.png` | Placeholder — needs real icon + ACE site URL |
| 2 | Purple Current | `brand-purple-current.png` | Placeholder — needs real icon + site URL |
| 3 | Boyette Pump & Well | `brand-boyette.png` | Placeholder — needs real icon + site URL |
| 4 | WTR DR | `brand-wtr-dr.png` | Placeholder — needs real icon + site URL |
| 5 | Brisa Climate | `brand-brisa.png` | Placeholder — needs real icon + site URL |
| 6 | Tyrian Roofing | `brand-tyrian.png` | Placeholder — needs real icon + site URL |
| 7 | MOR | `brand-mor.png` | Gray — **branding pending** (no logo yet) |
| 8 | ENG | `brand-eng.png` | Gray — **branding pending** (no logo yet) |

SWD is intentionally **excluded** (not a Purple Standard company).

### To swap in real icons

For each brand icon in `signature-purple-standard-v2.html`:
1. Replace the `src` with the hosted image URL (e.g. `https://www.purple-standard.com/…/brand-ace.png`) once images are live on the site — CodeTwo needs a publicly reachable URL, not a relative path.
2. Replace the `href` (currently `https://www.purple-standard.com`) with that brand's own site URL, and remove the `<!-- TODO -->` comment.
3. Keep display size at 40×40; source chips are 120×120 for retina. Match that ratio if the real art is a different aspect — icons should stay square and uniform.
4. Add MOR / ENG art (and un-gray them) once those brands have branding.

## Load into CodeTwo

1. Paste the contents of `signature-purple-standard-v2.html` into the CodeTwo signature editor (HTML/source mode).
2. Upload/host `tps-badge.png`, `tps-endorsement.png`, and the brand icons; point every `src` at its hosted URL.
3. Confirm the dynamic fields (`{First name}`, `{Title}`, `{Mobile}`, `{E-mail}`) map to the correct directory attributes; the `{RT}…{/RT}` tags auto-hide the mobile line when empty.

## Open / assumed values

- **Hyperlink color** is `#A263D2` (light purple) on the email + website links — assumed, not confirmed (see vault concern `0005-ps-hyperlink-blue-unconfirmed`).
- Body font is Trade Gothic Next with Arial fallback; most clients render Arial.
