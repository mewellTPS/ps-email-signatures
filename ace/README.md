# ACE Septic & Waste email signature

Dynamic, server-side signature built on the supplied CodeTwo template, adapted
to the ACE brand. This is the first of several department variants.

## Files
- `signature-ace.html` — the CodeTwo-ready snippet (keeps dynamic `{fields}` and `{RT}` auto-hide tags).
- `preview.html` — open in a browser to see the rendered look (placeholders filled with sample data).
- `assets/`
  - `ace-logo.png` — primary logo (Water Blue ACE wordmark), displays 151×58.
  - `badge-facebook.png` / `badge-google.png` / `badge-instagram.png` / `badge-linkedin.png` — white glyph on Sailfish `#335E89` filled circles, display 24×24. Supersede the older bare-glyph `social-*.png` (still in `assets/`, now unused).
  - `ps-endorsement.png` — "Powered by The Purple Standard®" banner, displays 232×11.
  - `banner-save50.png` — promo banner, displays 440×85 (**placeholder copy** — see below).
- `ACE_Logo_Primary_Light_Transparent_Small.png` — original full-size source logo (untouched).

## Layout
New template structure (440px wide):
1. **Top row** — name + title (left) / logo (right).
2. **Contact block** (full width) — Mobile | Phone, Email, Company + address.
3. **Website (left) / social icons (right).**
4. **Powered by The Purple Standard** endorsement.
5. **Promo banner.**

Because the contact block spans the full width below the name/logo row, a long
(2–3 line) title pushes the whole block down evenly — both sides stay balanced.

## Design decisions
- **Palette ("match-current"):** name black `#000000`; title Sailfish `#335E89`;
  contact values gray `#808080` with black bold labels; website Lawn Green
  `#0BA94B`; social icons Sailfish `#335E89`.
- **Font:** Arial (web-safe; the template's default).
- **Phone pattern:** `Mobile:` and `Phone:` on one line. Mobile is dynamic
  (`{Mobile}`) and auto-hides — its trailing ` | ` separator is inside the same
  `{RT}` block so it disappears too when there's no mobile. Office phone is static.
- **Email** added above the phones' line in the contact block (the supplied
  template included an Email field; ACE's current signature shows one too).
- **Socials:** Facebook, Google (GMB review link), Instagram, LinkedIn — the four
  ACE maintains. Dropped the template's X / YouTube / Pinterest. Icons are Font
  Awesome Free brands v6.5.2, rendered white and composited onto Sailfish `#335E89` filled circles, self-hosted.
- **Endorsement above the banner**, per request.
- **Address** is static; `{Company}` stays dynamic (resolves to "ACE Septic & Waste").

## ⚠️ Placeholder banner
`banner-save50.png` reads **"Save $50 on your next service. — Find out how!"**
(Sailfish `#335E89` background, ACE CTA orange `#F16522` button). This copy and
offer are a **mockup for review** — confirm/replace before go-live, and point the
banner link at the real landing page (currently the homepage). No HEARTH messaging
per direction.

## How to load it into CodeTwo
1. In the signature rule, open the **Design** step → **Edit signature**.
2. Switch the editor to **HTML / source view**.
3. Paste the contents of `signature-ace.html`.
4. Replace each `assets/...` image reference by uploading the matching file from
   `assets/` through the editor's image tool (CodeTwo rehosts uploaded images and
   rewrites the `src`).
5. Save and use CodeTwo's preview to confirm the dynamic fields resolve against
   the directory, and that the Mobile line auto-hides for anyone without a mobile.

## Notes
- `_`-prefixed and `-A`/`-B`-suffixed files in `_mockup/` and `assets/` are
  working artifacts from the design exploration — safe to delete (sandbox denied
  `rm` this session).
