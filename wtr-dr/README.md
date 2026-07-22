# WTR DR email signature

Dynamic, server-side signature for CodeTwo. Condensed three-zone layout:
**logo | name + contact | address + social**, no headshot.

## Files
- `signature-wtrdr.html` — the **live** CodeTwo-ready snippet (Option 2, three-zone). Keeps dynamic `{fields}`.
- `signature-wtrdr-option1.html` — **alternate** layout (Option 1, compact stack: logo + single column, Boyette-style). Kept on hand in case you want to switch.
- `preview.html` — open in a browser to see both layouts rendered (sample data). Uses the real self-hosted badges.
- `assets/logo.png` — logo, 230×230 (displays at 100×100).
- `assets/badge-{google,facebook,instagram}.png` — self-hosted social badges: white glyph on link-blue `#2E6DA6` filled circles, 40×40 (display 18). Used by both the signature and the preview.
- `assets/_preview-*.png` — old navy preview stand-ins, now unused (superseded by the badges; safe to delete).
- `assets/headshot.png` — leftover from the previous headshot layout; **no longer referenced** (safe to remove).
- Source files: `../resources/wtr_dr/` (untouched).

## Colors (pulled from the logo — WTR DR has no brand guide)
- Dark navy `#1C2458` (drop base) → name, labels (Phone:/Email:), the zone dividers.
- Link blue `#2E6DA6` — deepened from the logo's `#5D9ACE` highlight for readability → email + website links.
- Gray `#666666` → title and body values (kept from the template for readability).

## Pasting into CodeTwo (important)
Pasting the HTML source only lays out the **structure**. Dynamic fields and images must be
re-inserted through CodeTwo's ribbon so the program links them — otherwise they show as literal
`{placeholders}` / broken image text (as seen in the first editor test).

1. **Placeholders** (`{First name}`, `{Last name}`, `{Title}`, `{Email}`): after pasting, delete each
   typed placeholder and re-insert it via **Placeholder** on the ribbon. Typed/pasted placeholders can
   fail to link to Entra ID. The email token is **`{Email}`** (primary address); use `{From e-mail}` if
   you want the alias the message was sent from.
2. **Logo**: click the logo spot and insert `assets/logo.png` via the image button so CodeTwo hosts it.
   The local `src="assets/logo.png"` path will not resolve on its own.
3. **Social icons**: self-hosted badges in `assets/` — upload the three `badge-*.png` with the logo (image button); no CodeTwo gallery step needed.
4. **RT tags**: `{RT}…{/RT}` wrap the Email element so an empty value removes the whole line. Keep the
   closing `{/RT}` at the start of the following line (already set up this way in the file).
5. **Verify by send/preview**, not by the editor view — placeholders always look literal while editing.

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

## Social icons — self-hosted badges
White Font Awesome Free brand glyphs (v6.5.2, CC-BY 4.0) composited onto link-blue `#2E6DA6` filled
circles, hosted in `assets/` — the same bundled approach as the other brands, so all signatures look
uniform. Self-contained; nothing hotlinked. This replaced the earlier CodeTwo-gallery plan and settles
the open blue-vs-navy question in favor of link-blue `#2E6DA6`.

**In CodeTwo:** paste `signature-wtrdr.html`, then upload `logo.png` and the three `badge-*.png`
(plus `endorsement.png`) via the image button so CodeTwo hosts them. The profile URLs are already in the HTML.

## Note
Preview images are `_`-prefixed (`assets/_preview-*.png`) — safe to delete; not part of the live signature.
