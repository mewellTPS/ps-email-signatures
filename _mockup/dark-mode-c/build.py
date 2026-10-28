#!/usr/bin/env python3
"""Dark-mode option C (mid-tone artwork) for WTR DR, Boyette and PS: images + one preview page.

Option C (picked 2026-10-26 on the WTR DR mockup): dark artwork that sits on
transparency is recolored to a mid-tone with ~4:1 contrast on both white and
Outlook-dark #1E1E1E; the PS endorsement gets its white pill (ADR 0015);
dark dividers move to the mid-tone, because Outlook recolors text but not borders.

Reads each brand's shipped default.html and its images (repo assets/ or the
ps-assets master folder), so the preview is the production layout with sample
data and local images. Run from anywhere: python3 _mockup/dark-mode-c/build.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "out"
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008, RGBA

WTR_BLUE = "#3A80C0"      # WTR DR navy wordmark -> 4.18:1 on white, 3.99:1 on #1E1E1E
BOY_GRAY = "#7A7A7A"      # Boyette black wordmark -> 4.29 / 3.88
BOY_BLUE = "#3C81F5"      # Boyette's own wave blue -> 3.72 / 4.49
BOY_TAG = "#4D7FB5"       # Boyette #335E89 tagline, same hue lifted -> 4.18 / 3.98

# Outlook iOS dark mode, sampled from Michael's 2026-10-26 screenshots (text recolored;
# borders and images untouched). Colors not sampled are left as-is.
OUTLOOK_TEXT_MAP = {
    "#1C2458": "#D8D4FF", "#2E6DA6": "#6DA2E0", "#666666": "#A2A2A2",   # WTR DR
    "#000000": "#FFFFFF", "#F93822": "#FF593B",                          # Boyette
    "#49104F": "#FFC1FF", "#A263D2": "#C17EF0", "#808080": "#9B9B9B",   # PS
}
DARK_BG = "#1E1E1E"

SAMPLE = {"{First name}": "Jordan", "{Last name}": "Rivera", "{Title}": "Service Technician",
          "{Phone}": "813-555-0142", "{Mobile}": "813-555-0177", "{E-mail}": "jrivera@example.com"}


def step(msg):
    print(f"==> {msg}", flush=True)


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def clear(src, dst, width, height, top):
    """Make rows [top, top+height) fully transparent (DstOut with an opaque block)."""
    magick(src, "(", "-size", f"{width}x{height}", "xc:black", ")", "-geometry", f"+0+{top}",
           "-compose", "DstOut", "-composite", dst)


def size(img):
    w, h = subprocess.run(["magick", "identify", "-format", "%w %h", str(img)],
                          check=True, capture_output=True, text=True).stdout.split()
    return int(w), int(h)


def recolor_band(src, dst, top, height, color, width):
    """Paint every opaque pixel in rows [top, top+height) with one color; rest untouched."""
    t = OUT / "_tmp"
    magick(src, "-crop", f"{width}x{height}+0+{top}", "+repage", "-fill", color, "-colorize", "100", t / "band.png")
    clear(src, t / "cleared.png", width, height, top)
    magick(t / "cleared.png", t / "band.png", "-geometry", f"+0+{top}", "-compose", "Over", "-composite",
           *DPI, dst)


def build_images():
    (OUT / "_tmp").mkdir(parents=True, exist_ok=True)
    t = OUT / "_tmp"

    step(f"WTR DR: wordmark rows 156-199 -> {WTR_BLUE}; endorsement on white pill")
    recolor_band(REPO / "wtr-dr/assets/logo.png", OUT / "wtrdr-logo.png", 156, 44, WTR_BLUE, 200)
    magick("-size", "404x34", "xc:none", "-fill", "white", "-draw", "roundrectangle 0,0 403,33 17,17",
           REPO / "wtr-dr/assets/endorsement.png", "-gravity", "center", "-compose", "Over", "-composite",
           *DPI, OUT / "wtrdr-endorsement.png")

    # Boyette logo (380x290): BOYETTE rows 160-221, PUMP & WELL 226-257, endorsement 262-283.
    boy = REPO / "boyette/assets/boyette-logo.png"
    step("Boyette: cut the baked-in endorsement out, rebuild it on a white pill")
    magick(boy, "-crop", "380x24+0+262", "+repage", "-trim", "+repage", t / "boy-endo.png")
    w, h = size(t / "boy-endo.png")
    pw, ph = w + 24, h + 10
    magick("-size", f"{pw}x{ph}", "xc:none", "-fill", "white",
           "-draw", f"roundrectangle 0,0 {pw - 1},{ph - 1} {ph // 2},{ph // 2}",
           t / "boy-endo.png", "-gravity", "center", "-compose", "Over", "-composite", t / "boy-pill.png")
    clear(boy, t / "boy-noendo.png", 380, 30, 260)
    for name, word, tag in (("gray", BOY_GRAY, BOY_TAG), ("blue", BOY_BLUE, BOY_TAG)):
        step(f"Boyette {name}: BOYETTE -> {word}, PUMP & WELL -> {tag}")
        recolor_band(t / "boy-noendo.png", t / "boy-1.png", 160, 62, word, 380)
        recolor_band(t / "boy-1.png", t / "boy-2.png", 226, 32, tag, 380)
        magick(t / "boy-2.png", "(", t / "boy-pill.png", ")", "-gravity", "south", "-geometry", "+0+0",
               "-compose", "Over", "-composite", *DPI, OUT / f"boyette-logo-{name}.png")

    step(f"PS strip: WTR DR icon wordmark rows 62-79 -> {WTR_BLUE}")
    recolor_band(PS_ASSETS / "standard/email-signature/brand-wtr-dr.png", OUT / "brand-wtr-dr.png",
                 62, 18, WTR_BLUE, 80)


def render(tpl, images, swaps):
    h = re.sub(r"<!--.*?-->", "", tpl, flags=re.S)
    for k, v in SAMPLE.items():
        h = h.replace(k, v)
    h = h.replace("{RT}", "").replace("{/RT}", "")
    for url, local in images.items():
        h = h.replace(url, local)
    for a, b in swaps:
        h = h.replace(a, b)
    return h


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


def brand_images(prefix, local_dir):
    """Map every hosted URL under prefix to the local file of the same name."""
    return lambda tpl: {u: f"{local_dir}/{u.rsplit('/', 1)[1]}"
                        for u in re.findall(rf'{re.escape(prefix)}[\w.-]+', tpl)}


H = "https://assets.purple-standard.app/"
BRANDS = [
    ("wtrdr", "WTR DR", REPO / "wtr-dr/default.html", brand_images(H + "wtrdr/email-signature/", "../../wtr-dr/assets"), [
        ("Current", "", []),
        ("C · Mid-tone", f"Wordmark navy → {WTR_BLUE}. Endorsement on the PS white pill. Dividers navy → {WTR_BLUE}.", [
            ("../../wtr-dr/assets/logo.png", "out/wtrdr-logo.png"),
            ('../../wtr-dr/assets/endorsement.png" border="0" alt="Powered by The Purple Standard" width="190" height="9" style="display: block; width: 190px; height: 9px',
             'out/wtrdr-endorsement.png" border="0" alt="Powered by The Purple Standard" width="202" height="17" style="display: block; width: 202px; height: 17px'),
            ("border-left: 2px solid #1C2458", f"border-left: 2px solid {WTR_BLUE}")]),
    ]),
    ("boyette", "Boyette", REPO / "boyette/default.html", brand_images(H + "boyette/email-signature/", "../../boyette/assets"), [
        ("Current", "", []),
        ("C · Gray wordmark", f"BOYETTE black → gray {BOY_GRAY}. PUMP & WELL #335E89 → {BOY_TAG} (same hue, lifted). "
         f"The baked-in endorsement is rebuilt on a white pill. Divider #404040 → {BOY_GRAY}.", [
            ("../../boyette/assets/boyette-logo.png", "out/boyette-logo-gray.png"),
            ("border-left: 2px solid #404040", f"border-left: 2px solid {BOY_GRAY}")]),
        ("C · Blue wordmark", f"Same as gray, but BOYETTE uses the logo's own wave blue {BOY_BLUE}. "
         "Black has no brand mid-tone, so this is the choice to make for Boyette.", [
            ("../../boyette/assets/boyette-logo.png", "out/boyette-logo-blue.png"),
            ("border-left: 2px solid #404040", f"border-left: 2px solid {BOY_GRAY}")]),
    ]),
    ("ps", "PS", REPO / "purple_standard/default.html", brand_images(H + "standard/email-signature/", f"file://{PS_ASSETS}/standard/email-signature"), [
        ("Current", "", []),
        ("C · Mid-tone", f"Only the WTR DR strip icon changes: its navy wordmark → {WTR_BLUE}, matching WTR DR's own signature. "
         "The badge and endorsement already have white fills (ADR 0015), and Outlook recolors the purple text itself.", [
            (f"file://{PS_ASSETS}/standard/email-signature/brand-wtr-dr.png", "out/brand-wtr-dr.png")]),
    ]),
]


def build_page():
    tabs, panels = [], []
    for bi, (bid, bname, tpl_path, img_map, options) in enumerate(BRANDS):
        tpl = tpl_path.read_text()
        tpl_rel = tpl_path.relative_to(REPO)
        body = []
        for oname, note, swaps in options:
            sig = render(tpl, img_map(tpl), swaps)
            body.append(
                f'<h2>{html.escape(oname)}</h2>' + (f'<p class="note">{html.escape(note)}</p>' if note else "") +
                f'<div class="pair"><figure><figcaption>Light</figcaption><div class="mail" style="background:#fff">{sig}</div></figure>'
                f'<figure><figcaption>Outlook dark</figcaption><div class="mail" style="background:{DARK_BG}">{outlook_dark(sig)}</div></figure></div>')
        tabs.append(f'<button role="tab" data-v="{bid}"{" aria-selected=true" if bi == 0 else ""}>{html.escape(bname)}</button>')
        panels.append(f'<section data-v="{bid}"{"" if bi == 0 else " hidden"}><p class="src">Template: {tpl_rel}</p>{"".join(body)}</section>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Dark Mode Option C</title>
<style>
:root {{ --ink:#1f1f24; --muted:#5d5d66; --line:#e2e2e8; --accent:#49104F; --bg:#f6f6f8; }}
body {{ margin:0; font:15px/1.5 -apple-system, system-ui, sans-serif; color:var(--ink); background:var(--bg); }}
header {{ position:sticky; top:0; background:#fff; border-bottom:1px solid var(--line); padding:14px 24px; z-index:2; }}
h1 {{ font-size:18px; margin:0 0 10px; }}
h2 {{ font-size:16px; margin:26px 0 4px; }}
[role=tab] {{ font:inherit; padding:6px 14px; margin:0 6px 6px 0; border:1px solid var(--line); border-radius:6px; background:#fff; cursor:pointer; }}
[role=tab][aria-selected=true] {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
main {{ padding:6px 24px 48px; }}
.note {{ max-width:75ch; color:var(--muted); margin:0 0 10px; }}
.src {{ font-size:13px; color:var(--muted); margin:14px 0 0; }}
.pair {{ display:grid; grid-template-columns:1fr; gap:10px; }}
figure {{ margin:0; }}
figcaption {{ font-size:13px; color:var(--muted); margin-bottom:4px; }}
.mail {{ padding:22px 20px; border:1px solid var(--line); border-radius:8px; overflow-x:auto; }}
.foot {{ font-size:13px; color:var(--muted); max-width:75ch; margin-top:28px; }}
</style></head><body>
<header><h1>Dark-mode option C: mid-tone artwork</h1><div role="tablist">{"".join(tabs)}</div></header>
<main>{"".join(panels)}
<p class="foot">Outlook dark panes apply the text recoloring sampled from your Outlook iOS screenshots; images and
borders are left alone, as Outlook does. Mid-tones are chosen for about 4:1 contrast on both white and #1E1E1E.
Templates still show the 8011 address (ADR 0019 change not applied yet). Sample person is fictional.</p></main>
<script>
document.querySelectorAll('[role=tab]').forEach(b => b.onclick = () => {{
  document.querySelectorAll('[role=tab]').forEach(x => x.setAttribute('aria-selected', x === b));
  document.querySelectorAll('section[data-v]').forEach(s => s.hidden = s.dataset.v !== b.dataset.v);
}});
const only = new URLSearchParams(location.search).get('v');   // ?v=ps opens one tab (headless checks)
if (only) document.querySelector(`[role=tab][data-v="${{only}}"]`)?.click();
</script></body></html>"""
    (HERE / "index.html").write_text(page)


if __name__ == "__main__":
    print("$ python3 " + " ".join(sys.argv))
    try:
        build_images()
        step("Preview page")
        build_page()
    except subprocess.CalledProcessError as e:
        sys.exit(f"RESULT: FAIL — magick step failed ({e}); check ImageMagick and the source images")
    except FileNotFoundError as e:
        sys.exit(f"RESULT: FAIL — missing source ({e}); is ps-assets at {PS_ASSETS}?")
    print(f"RESULT: OK — open {HERE / 'index.html'}")
