# Dark-mode option C — decisions and pending actions

Option C means recoloring dark artwork that sits on a transparent background to a
mid-tone. The mid-tone has about 4:1 contrast on white and on Outlook-dark `#1E1E1E`.
The PS endorsement sits on a white pill (ADR 0015).
`build.py` builds `out/` and `index.html`.

## Approved by Michael, 2026-10-26 (not yet applied)

| Brand | Approved change | Image |
|---|---|---|
| WTR DR | Wordmark navy → `#3A80C0`; endorsement on white pill; dividers `#1C2458` → `#3A80C0` | `out/wtrdr-logo.png`, `out/wtrdr-endorsement.png` (202×17 display) |
| Boyette | **Blue wordmark**: BOYETTE → `#3C81F5`, PUMP & WELL → `#4D7FB5`, endorsement rebuilt on white pill; divider `#404040` → `#7A7A7A` | `out/boyette-logo-blue.png` (gray variant rejected) |
| PS | WTR DR strip icon wordmark → `#3A80C0`; nothing else changes | `out/brand-wtr-dr.png` |

**Hold:** Michael asked to apply nothing yet because more revisions are coming.

## When revisions are done

1. Update each `default.html`: change the image dimensions and the divider colors.
2. Copy the approved images into `~/Developer/purple-standard/websites/ps-assets`, which is the master copy.
3. Push to Cloudflare Pages project `ps-assets` (assets.purple-standard.app).
   - Michael expects Claude to have write access. It has not been tested yet.
   - Deploy the whole folder, not single files.
   - Verify the live bytes by SHA-256.
   - Add `?v=2` to the image URLs if mail clients cache the old images.
4. Send a real test email in Outlook dark mode for each brand.
