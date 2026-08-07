# multi-brand — PS signature v2 / v3 (testing)

Sandbox for the cross-brand work on the Purple Standard signature. Kept separate from
`purple_standard/` on purpose: nothing here is loaded into CodeTwo yet, and nothing outside
this folder was modified.

Started 2026-08-04. Icon treatment **C (native shapes)** selected 2026-08-05.
Updated 2026-08-06: real Brisa bear mark in, MOR/ENG placeholders out, preview.html
rebuilt as a single self-contained file.

## Open these two

| File | What it shows |
|---|---|
| `preview.html` | v1, v2, v3 and v3+strip. **Fully self-contained** — every image base64-embedded, no iframes, no scripts. Opens offline and can be sent as an email attachment. Regenerate with `build-preview.py`. |
| `compare.html` | The four icon treatments (C selected, A/B/D kept as demo material) + strip spacing. |

Both are plain `file://` pages — `open -a "Google Chrome" preview.html`.

## The three signatures

| File | Differs from v1 by |
|---|---|
| `signature-purple-standard-v2.html` | one inserted `<tr>` — the 6-icon brand strip above the endorsement |
| `signature-purple-standard-v3.html` | one line — the badge `<img>` src becomes the animated GIF. No strip. |
| `signature-purple-standard-v3-with-strip.html` | both of the above. Generated, not hand-written. |

v2 and v3 are **alternatives**, not steps. Both answer "show the whole portfolio": v2 with a
static row, v3 by animating the badge slot v1 already has. The combined file exists so the
choice can be judged three ways; it does state the portfolio twice.

Verify the "only difference" claims yourself:

```sh
strip() { awk '/^<table/{p=1} p' "$1"; }
diff <(strip ../signature-purple-standard.html) <(strip signature-purple-standard-v2.html)
diff <(strip ../signature-purple-standard.html) <(strip signature-purple-standard-v3.html)
```

v2 should show one pure insertion; v3 one changed line.

> **Supersedes part of ADR 0005.** That ADR's v2 also removed the website URL line and moved
> the address up. Michael's 2026-08-04 direction is that v2 differ from v1 by the strip alone,
> so the URL line and v1's address wording are back. ADR 0005 needs amending or superseding.

## Rebuild

```sh
bash build-icons.sh              # all icon treatments + ball frames, into out/
bash build-ball-gif.sh           # the animated GIF (needs build-icons.sh first)
python3 build-v3-with-strip.py   # regenerate the combined variant from v2 + v3
python3 build-preview.py         # rebuild the self-contained preview.html
python3 verify-phys.py out       # re-check every PNG is 96 DPI
```

Every script reads only from this folder and `../assets/`, and writes only into `out/`. No
scratch or temp directories in the chain, so a rebuild works on any future day.

## Source assets and what had to be done to them

Michael supplied six raw brand files. None were usable as-is; crops were **measured**, not
eyeballed.

| Source | Was | Needed |
|---|---|---|
| `ace-logo.png` | 1800² full-bleed circle | resize only |
| `pc-icon.png` | 500² circle | resize only |
| `boyette-icon.png` | 500² blue ring, **transparent interior** | white field added inside the ring |
| `brisa-logo.png` | 3366×3745 bear mark, gradient outline on transparent | trim + scale only (supplied 2026-08-06; supersedes `brisa-icon.png`, the 1080² badge whose ring text was illegible at 40px) |
| `wtrdr-logo.png` | 200² **wordmark lockup**, not an icon | drop is x49–147, y2–148; wordmark starts y=148 |
| `tyrian-logo.png` | 500² **shield crest**, 414×498 | not a circle at all |

Not one was at 96 DPI. WTR DR and Tyrian are cropped from marketing material — neither is real
brand artwork, and it shows at 40px.

## Icon treatments in `out/`

`c-native` is the selected set. The others are kept for future demos.

- **`c-native/`** ← **selected.** No shape forcing; each mark trimmed and scaled to fit 80×80.
  Honest to the sources: WTR DR keeps its wordmark, Tyrian stays a shield, Brisa is the bear.
  All canvases are 80×80 so the row's slots still align.
- `a-plain/` — bare circles. WTR DR and Tyrian get no visible edge on white.
- `b-ring/` — brand ring on every icon. Most consistent, but circles-inside-circles shrink the
  four round marks by about a third.
- `d-hybrid/` — round marks bare, only WTR DR and Tyrian get a ring.
- `ball/`, `ball-c/` — 150×150 GIF frames (treatment C) + the built GIF.

**MOR and ENG were removed from the strip on 2026-08-06** at Michael's direction — it now shows
only brands with real artwork. Grey placeholder discs are still generated into `out/` for the
demo treatments, but no signature references them. This narrows ADR 0005's "reflect the true end
state" call; fold it in when that ADR is amended.

## The GIF

`out/ball/tps-badge-cycle.gif` — 150×150, **63 frames, 158 KiB, loops forever, 13.2 s cycle.**

Seven marks, each held 1.4 s then turned over 8 frames. The turn is a horizontal squeeze: the
outgoing mark compresses to edge-on at the centre line, the incoming one expands out of it.
Width follows a **cosine, not a linear ramp** — linear reads as a squash, cosine as rotation.

**Frame 0 is tps-badge deliberately.** Any client that declines to animate shows frame 1, so the
fallback is exactly the static badge v1 and v2 ship. `build-ball-gif.sh` asserts this by scoring
frame 0 against all seven marks (badge RMSE 0.011; nearest other mark 0.34).

Quantisation was chosen by comparing against source **at the 75 px shipping size**, not zoomed:

| Setting | Weight | Result |
|---|---|---|
| `+dither`, 64 colours | 164 KiB | visible banding across Brisa's gradient |
| **Riemersma, 128 colours** | **158 KiB** | near-indistinguishable from source ✓ |

Riemersma beats Floyd–Steinberg here because its error diffusion follows a space-filling curve,
producing less high-frequency noise for LZW to encode.

## Still outstanding

1. **Pick one:** v2, v3, or the combined variant.
2. **Icon `src` swap.** `out/c-native/*.png` are relative paths. Upload alongside the existing
   hosted assets and point at
   `https://assets.purple-standard.app/standard/email-signature/brand-<slug>.png`.
   Same for the GIF if v3 is chosen. **Verify served bytes with a cache-buster before shipping**
   (ADR 0008) — the ACE host returns HTTP 200 with WebP bytes from `.png` URLs, and a status
   code will not reveal it. `assets.purple-standard.app` was checked this session and serves
   genuine PNG for both existing assets.
3. **Per-brand links.** All six icons currently point at purple-standard.com; each `TODO`
   marks a link awaiting that brand's real site URL.
4. **Confirm CodeTwo still accepts an animated GIF in a template** before committing to v3.
   Reports from mid-2026 suggest signature platforms are tightening on them. If CodeTwo strips
   or flattens it, v3 degrades to v1 rather than breaking — which is the point of frame 0.
5. **ACE's icon is the weakest of the six at 40 px** — a detailed illustration that reads as a
   coloured blob. Nothing post-processing can fix; it needs a simplified icon from ACE.

## Gotchas worth not rediscovering

- **`magick identify` is not a DPI oracle.** PNG stores only pixels-per-metre, so a correct
  96 DPI file reports `37.79 PixelsPerCentimeter`. Use `verify-phys.py`, which parses the `pHYs`
  chunk (96 DPI = 3780 px/m).
- **`-layers Optimize` crops frames to their changed region.** Reading `gif[n]` gives a partial
  tile; `-coalesce` first to get composed frames.
- **`magick compare` exits non-zero whenever images differ**, which under `set -e` aborts the
  script mid-loop. Wrap in `|| true`.
- **The session shell is zsh**, which does not word-split unquoted variables — a file list built
  into a string arrives as one argument. Use arrays, or `bash -c`.
- **Cloudflare 403s urllib's default User-Agent** on `assets.purple-standard.app` while curl gets
  through. `build-preview.py` sends a browser UA.
- **Counting tags to check HTML balance must skip comments** — these files mention `<tr>` in their
  comment headers, which reports a phantom imbalance on good markup.
- **Comparing a GIF frame to a source PNG must flatten the PNG first.** GIF frames are composited
  on white; a transparent-background reference scores as wildly different and the check lies.
