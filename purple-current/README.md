# Purple Current email signature

Two designs live here. **v2 is the current design** (new template Michael supplied);
v1 is retained for reference.

---

## v2 — current (new template)

Cleaner horizontal layout: name/title, then logo (left) beside a stacked contact block,
a divider rule, the "Powered by The Purple Standard" endorsement with a **right-aligned social
icon row** in the same line, and the full-width "Purple up. Power on." banner. No disclaimer
(matches the supplied template).

### Files
- `signature-purple-current-v2.html` — the CodeTwo-ready snippet (keeps dynamic `{fields}`).
- `preview-v2.html` — open in a browser to see the rendered look (sample data).
- `assets/logo-v2.png` — horizontal primary-color logo, display 200×87 (source 400×174).
- `assets/endorsement.png` — "Powered by The Purple Standard" lockup, display 360×17 (source 600×29).
- `assets/badge-*.png` — six brand-purple `#411144` circle badges (Google, Facebook, Instagram, LinkedIn, YouTube, Yelp), 40×40 (display 18), right-aligned in the endorsement row.
- `assets/banner-v2.jpg` — "Purple up. Power on." banner, display 560×169 (source 900×271).
- Source files: `../purple_current/` (untouched).

### Layout & content
- **Order:** Name → Title → [logo | contact] → divider → endorsement + right-aligned social row → banner.
- **Social set** (v2): Google, Facebook, Instagram, LinkedIn, YouTube, Yelp — brand-purple circle badges; real profile URLs carried over from v1.
- **Contact block** is `P` (phone) → `A` (address, 2 lines) → `E` (email) — email sits under the address.
- **Phone** static `(813) 355-0865`; **Email** dynamic `{E-mail}`, auto-hides if empty.
- **Name/Title** dynamic `{First name} {Last name}` / `{Title}`.
- The **endorsement image replaces** the template's `www.purple-current.com` line above the banner.

### Colors — official Purple Current design system
- Primary purple `#411144` → name, title, contact labels, divider rule.
- Contact values `#333333`. Banner gold accent `#eaa951` (in-image).

### Links
- Logo + banner → `https://purple-current.com/`
- Endorsement → `https://www.purple-standard.com/`

### How to load it into CodeTwo
1. Signature rule → **Design** → **Edit signature** → HTML / source view.
2. Paste the contents of `signature-purple-current-v2.html`.
3. Upload the nine images from `assets/` (`logo-v2.png`, `endorsement.png`, `banner-v2.jpg`, and the six `badge-*.png`) via the editor's image tool.
4. Save and preview to confirm the dynamic fields resolve.

---

## v1 — original template (retained for reference)

Dynamic, server-side signature built from the earlier CodeTwo template (logo left,
contact block, social row, promo banner, and a disclaimer bar).

## Files
- `signature-purple-current.html` — the CodeTwo-ready snippet (keeps dynamic `{fields}`).
- `preview.html` — open in a browser to see the rendered look (sample data).
- `assets/logo.png` — trimmed stacked logo, 124×150.
- `assets/banner.png` — promo banner, 652×196 (displays at 326×98, true aspect).
- `assets/social-*.png` — six brand-purple icons (Google, Facebook, Instagram, LinkedIn, YouTube, Yelp), 46px (display 23).
- Source files: `../purple_current/` (untouched).

## Colors — from the official Purple Current design system
(`~/Downloads/PC/purple-current-design-system.md`)
- Primary purple `#411144` → name, social-contact labels, website link, social icons.
- Orange accent `#eaa951` → disclaimer divider rule (replaced the template's green `#79ca06`).
- Title/company `#2a2a2a`, contact values + address + disclaimer `#8c8c8c` (kept from the template).

## Choices
- **Phone** is static `(813) 355-0865` only (the template's mobile line was removed).
- **Email** is dynamic and auto-hides if empty. Title line is `{Title} • {Company}` (dynamic).
- **Address** on two lines: `8011 Land O' Lakes Blvd` / `Land O' Lakes, FL 34638`.
- **Banner** kept at its true 3.3:1 aspect (326×98) rather than the template's squashed 326×57 slot.
- **Social set**: Google (GMB), Facebook, Instagram, LinkedIn, YouTube, Yelp — all six you specified.
- **Disclaimer**: bar kept, text replaced with your supplied confidentiality notice, set at 8pt.

## Social icons — bundled
Pulled from Font Awesome Free brands (v6.5.2, CC-BY 4.0), recolored to `#411144`, hosted in `assets/`.
Self-contained; nothing hotlinked. (CodeTwo's gallery doesn't reliably carry GMB or Yelp, so bundling
keeps all six uniform.)

## How to load it into CodeTwo
1. Signature rule → **Design** → **Edit signature** → HTML / source view.
2. Paste the contents of `signature-purple-current.html`.
3. Upload the nine images from `assets/` (logo, banner, six icons) via the editor's image tool.
4. Save and preview to confirm the dynamic fields resolve.

## Note
Temp verification files are `_`-prefixed (`assets/_check.png`, `_render.png`) — safe to delete.
