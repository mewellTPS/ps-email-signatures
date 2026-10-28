#!/usr/bin/env python3
"""Brisa stacked logo: three image treatments + compact stacked signature + preview page.

Source: Michael's stacked reference on Brisa purple (#48104F), 1122x1478 JPG, copied to
source/BC-STACKED-GRADIENT-PURPLEBACKGROUND-CROP.jpg. The flat background is keyed out by color
distance and un-premultiplied, so edges carry no purple fringe.
Run: python3 brisa/_mockup/stacked/build.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SRC = HERE / "source/BC-STACKED-GRADIENT-PURPLEBACKGROUND-CROP.jpg"
OUT = HERE / "out"
T = OUT / "_tmp"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008, RGBA
BG = (72, 16, 79)              # #48104F, sampled from all four corners
BRISA_PURPLE = "#48104F"
MID_PURPLE = "#A060C4"         # 4.23:1 on white, 3.94:1 on #1E1E1E
LOGO_W, LOGO_H = 112, 148      # display size; 2x files are 224x296 (source aspect 0.759)
BRISA_BAND = (980, 1280)       # rows of the white BRISA wordmark in the 1478px-tall source


def step(m):
    print(f"==> {m}", flush=True)


def magick(*a):
    subprocess.run(["magick", *map(str, a)], check=True)


def build_images():
    T.mkdir(parents=True, exist_ok=True)
    step("A: purple tile (reference as-is, rounded corners)")
    magick(SRC, "-resize", f"{LOGO_W * 2}x{LOGO_H * 2}!", "(", "+clone", "-alpha", "extract", "-fill", "black", "-colorize", "100",
           "-fill", "white", "-draw", f"roundrectangle 0,0 {LOGO_W * 2 - 1},{LOGO_H * 2 - 1} 18,18", ")",
           "-alpha", "off", "-compose", "CopyOpacity", "-composite", *DPI, OUT / "brisa-logo-stacked-tile.png")

    step("Key out the purple background (color distance -> alpha, then un-premultiply)")
    r, g, b = (c / 255 for c in BG)
    magick(SRC, "(", "+clone", "-fill", "#48104F", "-colorize", "100", ")", "-compose", "difference", "-composite",
           "-separate", "-evaluate-sequence", "max", "-level", "0,30%", T / "alpha.png")
    # -fx collapses its input sequence, so each channel is solved in its own call, then recombined.
    for ch, bg in (("r", r), ("g", g), ("b", b)):
        magick(SRC, T / "alpha.png", "-fx", f"v.r<0.02?0:(u.{ch}-(1-v.r)*{bg})/v.r", "-colorspace", "gray", T / f"ch-{ch}.png")
    magick(T / "ch-r.png", T / "ch-g.png", T / "ch-b.png", "-set", "colorspace", "sRGB", "-combine", T / "color.png")
    magick(T / "color.png", T / "alpha.png", "-alpha", "off", "-compose", "CopyOpacity", "-composite", T / "keyed.png")

    for name, color in (("purple", BRISA_PURPLE), ("mid", MID_PURPLE)):
        step(f"{'B' if name == 'purple' else 'C'}: transparent, BRISA wordmark -> {color}")
        top, bot = BRISA_BAND
        magick(T / "keyed.png", "-crop", f"1122x{bot - top}+0+{top}", "+repage", "-fill", color, "-colorize", "100", T / "band.png")
        magick(T / "keyed.png", "(", "-size", f"1122x{bot - top}", "xc:black", ")", "-geometry", f"+0+{top}",
               "-compose", "DstOut", "-composite", T / "nobrisa.png")
        magick(T / "nobrisa.png", T / "band.png", "-geometry", f"+0+{top}", "-compose", "Over", "-composite",
               "-resize", f"{LOGO_W * 2}x{LOGO_H * 2}!", *DPI, OUT / f"brisa-logo-stacked-{name}.png")


SAMPLE = {"{First name}": "Jordan", "{Last name}": "Rivera", "{Title}": "Service Technician",
          "{Phone}": "813-555-0142", "{Mobile}": "813-555-0177", "{E-mail}": "jrivera@brisaclimate.com"}
DARK = {"#2a2a2a": "#E0E0E0", "#48104F": "#FFC1FF", "#7a7a7a": "#A2A2A2", "#49104F": "#FFC1FF", "#808080": "#9B9B9B",
        "#A263D2": "#C17EF0", "#000000": "#FFFFFF", "#F93822": "#FF593B"}
HOST = "https://assets.purple-standard.app/brisa/email-signature/"
PS_ENDORSE = "https://assets.purple-standard.app/standard/email-signature/tps-endorsement.png"
LOCAL_ASSETS = {HOST + "badge-facebook.png": "../../assets/badge-facebook.png",
                HOST + "badge-instagram.png": "../../assets/badge-instagram.png",
                HOST + "badge-google.png": "../../assets/badge-google.png",
                HOST + "banner-web.png": "../../assets/banner-web.png",
                PS_ENDORSE: "../../../purple_standard/assets/tps-endorsement.png"}


def render(path, logo_file, drop_banner=False):
    h = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    if drop_banner:
        h = re.sub(r'<tr>\s*<td[^>]*data-codetwo-visible="Banner".*?</tr>', "", h, flags=re.S)
    for k, v in SAMPLE.items():
        h = h.replace(k, v)
    h = h.replace("{RT}", "").replace("{/RT}", "")
    h = h.replace(HOST + "brisa-logo-stacked.png", f"out/{logo_file}")
    for a, b in LOCAL_ASSETS.items():
        h = h.replace(a, b)
    return h


def dark(h):
    for a, b in DARK.items():
        h = re.sub(rf"(?<![-\w])color: ?{a}", f"color: {b}", h, flags=re.I)
    return h


OPTIONS = [("a", "A · Purple tile", "brisa-logo-stacked-tile.png",
            "Your reference as-is on its purple square, with rounded corners. Reads on any background with no changes, so it also fixes dark mode."),
           ("b", "B · Transparent, purple wordmark", "brisa-logo-stacked-purple.png",
            f"Background removed; BRISA in Brisa purple {BRISA_PURPLE}. Matches the other brands on white, but BRISA disappears in dark mode."),
           ("c", "C · Transparent, mid-tone wordmark", "brisa-logo-stacked-mid.png",
            f"Background removed; BRISA in {MID_PURPLE}, about 4:1 contrast on white and on dark (the option C dark-mode fix).")]


def build_page():
    tpl = HERE / "signature-brisa-stacked.html"
    peers = [("PS", REPO / "purple_standard/default.html"), ("Boyette", REPO / "boyette/default.html")]

    def peer_html(p):
        h = re.sub(r"<!--.*?-->", "", p.read_text(), flags=re.S)
        for k, v in SAMPLE.items():
            h = h.replace(k, v)
        return h.replace("{RT}", "").replace("{/RT}", "")
    peer_block = "".join(f'<div class="peer"><span>{n}</span>{peer_html(p)}</div>' for n, p in peers)
    tabs, panels = [], []
    for i, (oid, name, logo, note) in enumerate(OPTIONS):
        sig = render(tpl, logo)
        reply = render(tpl, logo, drop_banner=True)
        panels.append(
            f'<section data-v="{oid}"{"" if i == 0 else " hidden"}><p class="note">{html.escape(note)}</p>'
            f'<figure><figcaption>In an email (1000px reading pane; pink line = halfway), next to PS and Boyette at the same scale</figcaption>'
            f'<div class="pane"><div class="peer"><span>Brisa</span><div class="measure">{sig}</div></div>{peer_block}</div></figure>'
            f'<figure><figcaption>Outlook dark mode (approximate recolor)</figcaption><div class="mail" style="background:#1E1E1E">{dark(sig)}</div></figure>'
            f'<figure><figcaption>Reply version (no banner)</figcaption><div class="mail">{reply}</div></figure>'
            f'<p class="size"></p></section>')
        tabs.append(f'<button role="tab" data-v="{oid}"{" aria-selected=true" if i == 0 else ""}>{html.escape(name)}</button>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Brisa Stacked Signature</title>
<style>
body {{ margin:0; font:15px/1.5 -apple-system, system-ui, sans-serif; color:#1f1f24; background:#f6f6f8; }}
header {{ position:sticky; top:0; background:#fff; border-bottom:1px solid #e2e2e8; padding:14px 24px; z-index:2; }}
h1 {{ font-size:18px; margin:0 0 10px; }}
[role=tab] {{ font:inherit; padding:6px 14px; margin:0 6px 6px 0; border:1px solid #e2e2e8; border-radius:6px; background:#fff; cursor:pointer; }}
[role=tab][aria-selected=true] {{ background:#48104F; color:#fff; border-color:#48104F; }}
main {{ padding:16px 24px 48px; }}
figure {{ margin:0 0 20px; }} figcaption {{ font-size:13px; color:#5d5d66; margin-bottom:4px; }}
.pane {{ width:1000px; max-width:100%; background:#fff; border:1px solid #e2e2e8; border-radius:8px; padding:20px; box-sizing:border-box; overflow-x:auto;
  background-image:linear-gradient(to right, transparent 499px, #f0d6f2 499px, #f0d6f2 501px, transparent 501px); }}
.peer {{ margin-bottom:26px; }} .peer > span {{ display:block; font-size:12px; color:#8a8a93; margin-bottom:6px; }}
.measure {{ display:inline-block; }}
.mail {{ background:#fff; padding:20px; border:1px solid #e2e2e8; border-radius:8px; overflow-x:auto; }}
.note, .size {{ font-size:13px; color:#5d5d66; max-width:75ch; }}
</style></head><body>
<header><h1>Brisa signature: stacked logo</h1><div role="tablist">{"".join(tabs)}</div></header>
<main>{"".join(panels)}
<p class="note">Built from your stacked reference. Images are local copies at 2&times; and 96 DPI; nothing is uploaded yet. Sample person is fictional.</p></main>
<script>
const size = () => document.querySelectorAll('section:not([hidden])').forEach(s => {{ const m = s.querySelector('.measure').getBoundingClientRect();
  s.querySelector('.size').textContent = `Brisa signature here: ${{Math.round(m.width)}} × ${{Math.round(m.height)}} px (PS 500 × 204, Boyette 480 × 215).`; }});
document.querySelectorAll('[role=tab]').forEach(b => b.onclick = () => {{
  document.querySelectorAll('[role=tab]').forEach(x => x.setAttribute('aria-selected', x === b));
  document.querySelectorAll('section[data-v]').forEach(s => s.hidden = s.dataset.v !== b.dataset.v); size();
}});
const only = new URLSearchParams(location.search).get('v');
if (only) document.querySelector(`[role=tab][data-v="${{only}}"]`)?.click();
window.addEventListener('load', size);
</script></body></html>"""
    (HERE / "index.html").write_text(page)


if __name__ == "__main__":
    print("$ python3 " + " ".join(sys.argv))
    if not SRC.exists():
        sys.exit(f"RESULT: FAIL — source missing at {SRC}; copy the reference JPG there")
    try:
        build_images()
        step("Preview page")
        build_page()
    except subprocess.CalledProcessError as e:
        sys.exit(f"RESULT: FAIL — magick step failed ({e})")
    print(f"RESULT: OK — open {HERE / 'index.html'}")
