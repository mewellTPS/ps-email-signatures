# WTR DR email signature

Dynamic, server-side signature for CodeTwo. Condensed three-zone layout:
**logo | name + contact | address + social**, no headshot.

## Files
- `signature-wtrdr.html` — the **live** CodeTwo-ready snippet (Option 2, three-zone). Keeps dynamic `{fields}`.
- `signature-wtrdr-option1.html` — **alternate** layout (Option 1, compact stack: logo + single column, Boyette-style). Kept on hand in case you want to switch.
- `preview.html` — open in a browser to see both layouts rendered (sample data + stand-in icons).
- `assets/logo.png` — logo, 230×230 (displays at 100×100).
- `assets/_preview-*.png` — navy icon **stand-ins for the preview only** (not used in the real signature).
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
3. **Social icons**: use **Insert → Social media icons** (see below) — don't rely on the pasted `img` refs.
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

## Social icons — using CodeTwo's resources (vs. the bundled approach)
You asked to source these from CodeTwo this time. Here's the difference:

| | CodeTwo gallery (this one) | Bundled PNGs (Boyette) |
|---|---|---|
| Hosting | CodeTwo hosts the images | You host them in `assets/` |
| Look | CodeTwo's house style; limited recolor | Any glyph, exact brand color |
| Coverage | Their gallery only | Anything you can find/draw |
| Effort | Click to insert in editor | Fetch + recolor + manage files |

**How to add them in CodeTwo:**
1. Paste `signature-wtrdr.html` into the editor (HTML/source view).
2. In the social-icons cell, use **Insert → Social media icons** and add Facebook + Instagram,
   pointing them at the URLs already in the HTML. CodeTwo will host these and rewrite the `src`.
3. **Google (GMB):** CodeTwo's gallery may not include a Google Business icon. If it does, insert it
   the same way. If it doesn't, two options — drop GMB, or I'll bundle just that one icon (navy, to match).
   Let me know which.

The `img_fb_...` / `img_ig_...` references in the HTML are CodeTwo's built-in icon names; if they show
as broken after pasting, just re-insert via the editor (step 2) and they'll resolve.

## Note
Preview images are `_`-prefixed (`assets/_preview-*.png`) — safe to delete; not part of the live signature.
