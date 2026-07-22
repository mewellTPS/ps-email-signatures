# Brisa Climate — email signature

Dynamic, server-side CodeTwo signature matching Brisa's supplied mockup:
logo + "Powered by The Purple Standard" endorsement on the left half, a vertical
purple divider, a contact block on the right half, and a full-width promo banner
below. Built **mock-first** (2026-07-22).

## Files

- `signature-brisa.html` — the CodeTwo-ready snippet (keeps dynamic `{fields}`; paste this into CodeTwo).
- `preview.html` — open in a browser to see the rendered look (sample data). Not for CodeTwo.
- `assets/` — self-hosted, retina-sized images (nothing hotlinked).

## Assets

- `logo.png` — Brisa horizontal logo, 600×239 (displays 300×120). Trimmed from the supplied JPG; white background kept (signature canvas is white).
- `banner-web.png` — promo banner, 1400×342 (displays 700×171). The blue→purple→red gradient bar is part of the image.
- `endorsement.png` — shared "Powered by The Purple Standard" strip, 600×29 (displays 300×15). Same width as the logo.
- `social-{facebook,instagram,youtube}.png` — 52×52 (display 25). White Font Awesome glyph on a `#48104F` circle.
- Source: `assets/BC-HORIZONTAL-…-PURPLETEXT.jpg`, `assets/banner.png` (originals, untouched).

## Colors — ⚠ asset-derived (no official Brisa brand guide exists)

Sampled from the supplied logo/banner with ImageMagick:

- Deep purple `#48104F` — name, contact labels (`P:`/`M:`/`E:`), divider, endorsement, `www` link.
- Coral `#FB3748` — the "CLIMATE" wordmark / warm accent. Held in reserve; all signature text stays purple per the mockup.
- Blue `#3D82FB` — logo/gradient accent.
- Contact values `#2a2a2a`, title `#7a7a7a`.

If Brisa has an official brand guide, reconcile these against it.

## Dynamic fields (CodeTwo)

- `{First name} {Last name}`, `{Title}` — name + title.
- `{Phone}`, `{Mobile}`, `{E-mail}` — each wrapped in `{RT}...{/RT}` so an empty line auto-hides. Nothing broken ships if a value is missing.
- `data-codetwo-visible` attributes are set for the editor's field toggles.

## Mock-first — replace before / at CodeTwo load

Nothing ships as a dead `#`; interim links work, marked with `TODO`:

1. **Company address** — the `Street, City` / `Zip Code, Country` cells are placeholders. Swap in Brisa's real address.
2. **Social profile URLs** — Facebook / Instagram / YouTube currently point at each platform's root. Swap each `href` for Brisa's real profile URL.
3. **Banner link** — points at `https://brisaclimate.com/`. Point it at the real "leave a review" landing page when available.
4. **Office phone** — `P:` uses the dynamic `{Phone}` directory field. If Brisa prefers a single fixed company main line, hardcode it in the `P:` cell instead.

## How to load it into CodeTwo

1. Create/edit the Brisa signature rule; open the HTML source view.
2. Paste the contents of `signature-brisa.html`.
3. Upload the five images from `assets/` (logo, banner-web, endorsement, three social icons) via the editor's image tool, and confirm the `src` paths resolve to the hosted URLs.
4. Save and preview with a Brisa test user to confirm the dynamic fields resolve and empty lines auto-hide.

## Notes

- Layout is a 700px table: left half (logo 300px + endorsement 300px, equal width), 2px `#48104F` divider, right-half contact grid, full-width banner.
- Custom brand fonts aren't email-safe; the signature uses Arial throughout (expected to render in all clients).
- Not yet loaded into CodeTwo — same status as the other brands.
