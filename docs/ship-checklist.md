# Ship checklist: operator signatures (2026-10-28)

C-suite review page (picks: E for all, C for Boyette): `docs/review/signatures-c-suite-review.html`, built by `python3 docs/review/build-c-suite.py`.

Michael ships everything at once after approval. Nothing below is uploaded or pasted yet.
Ship order: copy images into `~/Developer/purple-standard/websites/ps-assets/` → deploy the
WHOLE folder to Cloudflare Pages `ps-assets` (first Claude write; verify live bytes by SHA-256)
→ paste each signature into its CodeTwo rule in Michael's signed-in Chrome → test emails.

## Brisa (BRS): Victor Rodriguez

Status: sent to Victor for a pick (Michael expects C or E). Build: `python3 brisa/_mockup/victor/build.py`.

| Version | Paste file | Images it needs beyond the Brisa set |
|---|---|---|
| A · banner + endorsement | `brisa/_mockup/victor/signature-a.html` | none |
| B · endorsement only | `signature-b.html` | none |
| C · pledge, badge left | `signature-c.html` | `standard/email-signature/tps-pledge-clear.png` ← `purple_standard/pledge/out/tps-pledge-clear-flow.png` |
| D · pledge, badge right | `signature-d.html` | `standard/email-signature/tps-pledge-clear-right.png` ← `.../tps-pledge-clear-right-flow.png` |
| E · pledge text + corner badge | `signature-e.html` | `standard/email-signature/tps-pledge-clear-text.png` ← `.../tps-pledge-clear-text-flow.png`; `standard/email-signature/tps-badge-clear.png` ← `.../tps-badge-clear.png` |

Brisa set, already copied into ps-assets (checksums matched): `brisa/email-signature/brisa-logo-stacked.png`,
`badge-facebook-blue.png`, `badge-instagram-blue.png`, `badge-google-blue.png`.

Hardcoded fields to revert after the Entra fix: see `docs/entra-fixes.md`.

## WTR DR (WTR): Sean Myatt

Status: C and E saved as options; waiting on Sean's pick. Possible follow-up: a larger WTR DR logo (current 200x200 file caps display at 100px). Michael makes WTR DR logo files himself (Kahawai did not do the branding); source https://wtrdr.com/wp-content/uploads/2025/02/qtq_95-1.webp. Build: `python3 wtr-dr/_mockup/sean/build.py`.

| Version | Paste file | Images it needs |
|---|---|---|
| C · pledge, badge left | `wtr-dr/_mockup/sean/signature-c.html` | `wtrdr/email-signature/wtrdr-logo-clear.png` ← `wtr-dr/_mockup/sean/out/wtrdr-logo-clear.png`; `standard/email-signature/tps-pledge-clear.png` (shared with Brisa C) |
| E · pledge text + corner badge | `signature-e.html` | `wtrdr-logo-clear.png` as above; `standard/email-signature/tps-pledge-clear-text.png` + `tps-badge-clear.png` (shared with Brisa E) |

Social badges reuse the hosted `wtrdr/email-signature/badge-{google,facebook,instagram}.png` (byte-identical to `wtr-dr/assets/`).

## Tyrian Roofing (TYR): John Rodrigues

Status: C and E sent to John for a pick. Logo from Michael's stacked master; wordmark and social discs #642164 (Michael accepted the weak dark-mode contrast); Pledge and TPS badge Neon Purple like the others. Build: `python3 tyrian/_mockup/john/build.py`.
Social: Google (`https://share.google/wNanv1cHcJi2GktCp`) and Instagram only; Facebook and YouTube dropped (Michael).

| Version | Paste file | Images it needs |
|---|---|---|
| C · pledge, badge left | `tyrian/_mockup/john/signature-c.html` | `tyrian/email-signature/{tyrian-logo-stacked,badge-google-mid,badge-instagram-mid}.png` ← `tyrian/_mockup/john/out/`; `standard/email-signature/tps-pledge-clear.png` (shared) |
| E · pledge text + corner badge | `signature-e.html` | the same three Tyrian images; `standard/email-signature/tps-pledge-clear-text.png` + `tps-badge-clear.png` (shared) |

## Boyette Pump & Well (BPW): Danny Boyette

Status: Michael picked **C** (2026-10-28); sent to Danny. His own layout kept; dark mode fixed; endorsement removed; Pledge added.
Build: `python3 boyette/_mockup/danny/build.py`. Social badges reuse the hosted red `boyette/email-signature/badge-*.png`.

| Version | Paste file | Images it needs |
|---|---|---|
| C · pledge, badge left | `boyette/_mockup/danny/signature-c.html` | `boyette/email-signature/boyette-logo-clear.png` ← `boyette/_mockup/danny/out/`; `standard/email-signature/tps-pledge-clear.png` (shared with Brisa C) |
| E · pledge text + corner badge | `signature-e.html` | `boyette-logo-clear.png` as above; `standard/email-signature/tps-pledge-clear-text.png` + `tps-badge-clear.png` (shared with Brisa E) |

## Purple Current (PC): Kenny Morrow

Status: sent to Kenny for a pick; art tone #A861B3 (Michael picked, 2026-10-28).
Build: `python3 purple-current/_mockup/kenny/build.py`. All new images ← `purple-current/_mockup/kenny/out/` into `current/email-signature/`.

| Version | Paste file | Images it needs |
|---|---|---|
| C · pledge, badge left | `purple-current/_mockup/kenny/signature-c.html` | `pc-logo-stacked.png`, `badge-{google,facebook,instagram,linkedin,youtube,yelp}-mid.png`; `standard/email-signature/tps-pledge-clear.png` (shared) |
| E · pledge text + corner badge | `signature-e.html` | same PC images as C; `standard/email-signature/tps-pledge-clear-text.png` + `tps-badge-clear.png` (shared) |
| Current layout + name, title | `signature-current.html` | `pc-logo-wide.png`, `endorsement-mid.png`, the six `badge-*-mid.png`; hosted `banner-standard.jpg` (unchanged) |

## Purple Standard (PS): default, Michael Ewell as the sample

Status: Michael picked **E** (2026-10-28). PS (and ACE) need one hardcoded rule per person
(shared-mailbox issue). **The phone (813) 555-0100 is a placeholder: replace it per person before shipping.**
Build: `python3 purple_standard/_mockup/michael/build.py`.

| Version | Paste file | Images it needs (all in `standard/email-signature/`) |
|---|---|---|
| Current (endorsement) | `purple_standard/_mockup/michael/signature-current.html` | `tps-endorsement-clear.png`, `brand-wtr-dr-drop.png` ← `purple_standard/_mockup/michael/out/`; `tps-badge-clear.png` (shared) |
| C · pledge, badge left | `signature-c.html` | `brand-wtr-dr-drop.png`; `tps-pledge-clear.png` (shared) |
| E · pledge text + corner badge | `signature-e.html` | `brand-wtr-dr-drop.png`; `tps-pledge-clear-text.png` + `tps-badge-clear.png` (shared) |
