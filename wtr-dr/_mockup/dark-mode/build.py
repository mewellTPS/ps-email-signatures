#!/usr/bin/env python3
"""WTR DR dark-mode variants: builds variant images + one tab-switcher preview.

Reads the shipped template (wtr-dr/default.html) and assets (wtr-dr/assets/),
so the preview is the production layout with sample data and local images.
Run: python3 wtr-dr/_mockup/dark-mode/build.py   (from the repo root or anywhere)
"""
import html
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAND = HERE.parents[1]                       # wtr-dr/
ASSETS = BRAND / "assets"
OUT = HERE / "out"
ORB = Path.home() / "Developer/visual-assets/wtrdr/logos/circle-logo/wtrdr-circle-mark-512.png"

MID_BLUE = "#3A80C0"     # ~4:1 contrast on both white and Outlook-dark #1E1E1E
WORDMARK_TOP = 156       # rows 152-161 are empty; rows >= this in the 200px logo are the "WTR DR" wordmark
DPI = ["-units", "PixelsPerInch", "-density", "96",   # ADR 0008: 96 DPI pHYs
       "-define", "png:color-type=6"]                  # always RGBA, never grayscale

# Outlook iOS dark mode, sampled from Michael's 2026-10-26 screenshot:
# text colors are recolored, border colors and images are left alone.
OUTLOOK_DARK_BG = "#1E1E1E"
OUTLOOK_TEXT_MAP = {"#1C2458": "#D8D4FF", "#2E6DA6": "#6DA2E0", "#666666": "#A2A2A2"}


def step(msg):
    print(f"==> {msg}", flush=True)


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def build_images():
    OUT.mkdir(exist_ok=True)
    logo, endo = ASSETS / "logo.png", ASSETS / "endorsement.png"
    t = OUT / "_tmp"
    t.mkdir(exist_ok=True)

    step("A: white halo around wordmark and endorsement")
    # Wordmark-only halo: dilate the alpha of the bottom band, paint it white, put logo on top.
    magick(logo, "-alpha", "extract", "-fill", "black", "-draw", f"rectangle 0,0 199,{WORDMARK_TOP - 1}",
           "-morphology", "Dilate", "Disk:5", t / "halo-mask.png")
    magick("-size", "200x200", "xc:white", t / "halo-mask.png", "-alpha", "off",
           "-compose", "CopyOpacity", "-composite", logo, "-compose", "Over", "-composite",
           *DPI, OUT / "a-logo.png")
    magick(endo, "-bordercolor", "none", "-border", "6", "-alpha", "extract",
           "-morphology", "Dilate", "Disk:4", t / "endo-mask.png")
    # Start from the color endorsement and slide the white halo underneath (DstOver),
    # so the canvas never collapses to grayscale.
    magick(endo, "-bordercolor", "none", "-border", "6",
           "(", t / "endo-mask.png", "-background", "white", "-alpha", "shape", ")",
           "-compose", "DstOver", "-composite", *DPI, OUT / "a-endorsement.png")

    step("Shared: white pill behind endorsement (same treatment as PS, ADR 0015)")
    magick("-size", "404x34", "xc:none", "-fill", "white", "-draw", "roundrectangle 0,0 403,33 17,17",
           endo, "-gravity", "center", "-compose", "Over", "-composite", *DPI, OUT / "pill-endorsement.png")

    step("B: white rounded card behind the whole logo")
    magick("-size", "232x232", "xc:none", "-fill", "white", "-draw", "roundrectangle 0,0 231,231 28,28",
           logo, "-gravity", "center", "-compose", "Over", "-composite", *DPI, OUT / "b-logo.png")

    step(f"C: wordmark recolored to mid-tone blue {MID_BLUE}")
    magick(logo, "-crop", f"200x{200 - WORDMARK_TOP}+0+{WORDMARK_TOP}", "+repage",
           "-fill", MID_BLUE, "-colorize", "100", t / "wordmark-mid.png")
    magick(logo, "-crop", f"200x{WORDMARK_TOP}+0+0", "+repage", "-background", "none",
           "-extent", "200x200", t / "drop-only.png")
    magick(t / "drop-only.png", t / "wordmark-mid.png", "-geometry", f"+0+{WORDMARK_TOP}",
           "-compose", "Over", "-composite", *DPI, OUT / "c-logo.png")

    step("D: round Glossy orb (ADR 0016) above the mid-tone wordmark")
    if not ORB.exists():
        sys.exit(f"RESULT: FAIL — orb mark missing at {ORB}; restore it or drop variant D")
    magick("-size", "200x200", "xc:none", "(", ORB, "-resize", "128x128", ")", "-gravity", "north",
           "-geometry", "+0+2", "-compose", "Over", "-composite",
           "(", t / "wordmark-mid.png", "-trim", "+repage", "-resize", "176x", ")", "-gravity", "south",
           "-geometry", "+0+4", "-compose", "Over", "-composite", *DPI, OUT / "d-logo.png")


SAMPLE = {"{First name}": "Jordan", "{Last name}": "Rivera", "{Title}": "Service Technician",
          "{Phone}": "813-555-0142", "{E-mail}": "jrivera@wtrdr.com"}


def render(tpl, logo, logo_px, endo, endo_w, endo_h, divider):
    h = tpl
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = re.sub(r'\s*<p[^>]*data-codetwo-visible="Mobile".*?</p>', "", h, flags=re.S)   # sample has no mobile
    for k, v in SAMPLE.items():
        h = h.replace(k, v)
    h = h.replace("{RT}", "").replace("{/RT}", "")
    h = h.replace("https://assets.purple-standard.app/wtrdr/email-signature/logo.png", logo)
    h = re.sub(r'(alt="WTR DR logo" )width="100" height="100" style="width: 100px; height: 100px"',
               rf'\1width="{logo_px}" height="{logo_px}" style="width: {logo_px}px; height: {logo_px}px"', h)
    h = h.replace("https://assets.purple-standard.app/wtrdr/email-signature/endorsement.png", endo)
    h = re.sub(r'width="190" height="9" style="display: block; width: 190px; height: 9px',
               f'width="{endo_w}" height="{endo_h}" style="display: block; width: {endo_w}px; height: {endo_h}px', h)
    h = h.replace("https://assets.purple-standard.app/wtrdr/email-signature/", "../../assets/")
    h = h.replace("border-left: 2px solid #1C2458", f"border-left: 2px solid {divider}")
    return h


def outlook_dark(h):
    # Recolor text (color:) only; borders keep their color, like the screenshot.
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: {src}", f"color: {dst}", h)
    return h


VARIANTS = [
    ("now", "Current", "What ships today. The navy wordmark and purple endorsement sit on transparency, "
     "so on a dark background they are about 1.2:1 contrast and disappear. The navy dividers vanish too.",
     ("../../assets/logo.png", 100, "../../assets/endorsement.png", 190, 9, "#1C2458")),
    ("a", "A · White halo", "A thin white outline traces the wordmark and the endorsement letters. "
     "Invisible on white mail; on dark mail the letters read as outlined stickers. Least change to the look.",
     ("out/a-logo.png", 100, "out/a-endorsement.png", 196, 15, MID_BLUE)),
    ("b", "B · White card", "The whole logo sits on a white rounded tile, and the endorsement gets the white "
     "pill PS already ships (ADR 0015). Invisible on white; on dark it is a clean light badge. Most robust.",
     ("out/b-logo.png", 116, "out/pill-endorsement.png", 202, 17, MID_BLUE)),
    ("c", "C · Mid-tone wordmark", f"The wordmark changes from navy to {MID_BLUE}, which holds about 4:1 contrast "
     "on both white and dark. No box at all. Endorsement uses the PS white pill. Changes the brand color of the wordmark.",
     ("out/c-logo.png", 100, "out/pill-endorsement.png", 202, 17, MID_BLUE)),
    ("d", "D · Glossy orb", "Swaps the drop for the round Glossy orb (ADR 0016), whose white ring and filled "
     "circle read on any background, above the mid-tone wordmark from C. Endorsement uses the PS pill.",
     ("out/d-logo.png", 100, "out/pill-endorsement.png", 202, 17, MID_BLUE)),
]

PANES = [("Light mode", "#FFFFFF", False),
         ("Outlook dark mode (recolors text, as in your screenshot)", OUTLOOK_DARK_BG, True),
         ("Dark, no recolor (rare in practice; shows how the images hold up on their own)", "#1E1E1E", False)]


def build_page():
    tpl = (BRAND / "default.html").read_text()
    tabs, panels = [], []
    for i, (vid, name, note, args) in enumerate(VARIANTS):
        sig = render(tpl, *args)
        panes = "".join(
            f'<figure><figcaption>{html.escape(cap)}</figcaption>'
            f'<div class="mail" style="background:{bg}">{outlook_dark(sig) if recolor else sig}</div></figure>'
            for cap, bg, recolor in PANES)
        tabs.append(f'<button role="tab" data-v="{vid}"{" aria-selected=true" if i == 0 else ""}>{html.escape(name)}</button>')
        panels.append(f'<section data-v="{vid}"{"" if i == 0 else " hidden"}><p class="note">{html.escape(note)}</p>{panes}</section>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>WTR DR Dark Mode</title>
<style>
:root {{ --ink:#1f1f24; --muted:#5d5d66; --line:#e2e2e8; --accent:#49104F; --bg:#f6f6f8; }}
body {{ margin:0; font:15px/1.5 -apple-system, system-ui, sans-serif; color:var(--ink); background:var(--bg); }}
header {{ position:sticky; top:0; background:#fff; border-bottom:1px solid var(--line); padding:14px 24px; z-index:2; }}
h1 {{ font-size:18px; margin:0 0 10px; }}
[role=tab] {{ font:inherit; padding:6px 14px; margin:0 6px 6px 0; border:1px solid var(--line); border-radius:6px; background:#fff; cursor:pointer; }}
[role=tab][aria-selected=true] {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
main {{ padding:20px 24px 48px; max-width:1100px; }}
.note {{ max-width:70ch; color:var(--muted); margin:0 0 18px; }}
figure {{ margin:0 0 18px; }}
figcaption {{ font-size:13px; color:var(--muted); margin-bottom:6px; }}
.mail {{ padding:28px 24px; border:1px solid var(--line); border-radius:8px; overflow-x:auto; }}
.foot {{ font-size:13px; color:var(--muted); max-width:70ch; }}
</style></head><body>
<header><h1>WTR DR signature: dark-mode options</h1><div role="tablist">{"".join(tabs)}</div></header>
<main>{"".join(panels)}
<p class="foot">All options also change the two divider lines from navy to {MID_BLUE}: Outlook recolors text in dark mode
but leaves border colors alone, so navy dividers disappear. The Outlook pane maps colors sampled from your
Outlook iOS screenshot; other clients differ, so the chosen option still gets a real test send.
Sample person is fictional.</p></main>
<script>
document.querySelectorAll('[role=tab]').forEach(b => b.onclick = () => {{
  document.querySelectorAll('[role=tab]').forEach(x => x.setAttribute('aria-selected', x === b));
  document.querySelectorAll('section[data-v]').forEach(s => s.hidden = s.dataset.v !== b.dataset.v);
}});
const only = new URLSearchParams(location.search).get('v');   // ?v=b opens one tab (used by headless checks)
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
        sys.exit(f"RESULT: FAIL — magick step failed ({e}); check ImageMagick is installed")
    print(f"RESULT: OK — open {HERE / 'index.html'}")
