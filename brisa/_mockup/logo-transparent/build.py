#!/usr/bin/env python3
"""Brisa stacked logo: purple-background JPG -> transparent PNG with a legible BRISA wordmark.

Source: Michael's copy/pasted JPG (../stacked/source/), solid #48104F background,
gradient bear, white BRISA, red CLIMATE. Steps:
  1. Color-to-alpha against the #48104F background (GIMP-style: alpha is the largest
     per-channel distance from the background, color is un-premultiplied), so the
     anti-aliased edges carry no purple fringe.
  2. Recolor the white BRISA band to a mid-tone that reads on white AND on Outlook-dark
     #1E1E1E (dark-mode option C, ADR 0020). One PNG per candidate color.
  3. Trim, 96 DPI RGBA (ADR 0008). Full-resolution masters; signature sizing comes later.
Then writes index.html: every candidate on white and on #1E1E1E.

Run from anywhere: python3 brisa/_mockup/logo-transparent/build.py
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "stacked/source/BC-STACKED-GRADIENT-PURPLEBACKGROUND-CROP.jpg"
OUT = HERE / "out"
WORK = HERE / "_work"      # intermediates, overwritten each run
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]

BG = (72, 16, 79)                 # #48104F, sampled at the corners
BRISA_BAND = "1122x300+0+985"     # rows holding the BRISA wordmark (CLIMATE starts ~1325)
DARK_BG = "#1E1E1E"
EDGE_DIST = 0.3                   # artwork's nearest-to-background pixel is ~0.45 away
NOISE_FLOOR = 0.08                # JPEG noise in the flat background stays below this

# name -> (color, contrast on white, contrast on #1E1E1E, note)
CANDIDATES = {
    "purple": ("#9A5FBF", 4.41, 3.78, "Brand purple lifted to a mid-tone"),
    "blue": ("#3C81F6", 3.72, 4.49, "The bear's own blue (sampled)"),
    "gradient": ("#F23A54:#3C81F6", 3.7, 4.5, "The bear's red-to-blue gradient, left to right"),
}


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def color_to_alpha(dst):
    r, g, b = (c / 255 for c in BG)

    def dist(ch, bgv):
        return f"({ch}>{bgv}?({ch}-{bgv})/{1 - bgv}:({bgv}-{ch})/{bgv})"

    # Pure color-to-alpha would make the bear's purple-ish middle semi-transparent (washed
    # out on white). Saturate instead: anything EDGE_DIST away from the background is fully
    # opaque, so only the anti-aliased rim gets partial alpha.
    # NOISE_FLOOR drops JPEG speckle in the flat background to fully transparent.
    d = f"max(max({dist('u.r', r)},{dist('u.g', g)}),{dist('u.b', b)})"
    a = f"min(1,max(0,({d}-{NOISE_FLOOR})/({EDGE_DIST}-{NOISE_FLOOR})))"
    alpha = WORK / "alpha.png"
    magick(SRC, "-colorspace", "sRGB", "-fx", a, "-colorspace", "Gray", alpha)
    # un-premultiply each channel into its own gray plane: c' = (c - bg) / a + bg
    planes = []
    for ch, bgv in zip("rgb", (r, g, b)):
        p = WORK / f"{ch}.png"
        magick(SRC, alpha, "-fx", f"v.r<0.004?{bgv}:(u.{ch}-{bgv})/v.r+{bgv}",
               "-colorspace", "Gray", p)
        planes.append(p)
    magick(*planes, "-set", "colorspace", "sRGB", "-combine",
           alpha, "-alpha", "off", "-compose", "CopyOpacity", "-composite", dst)


def recolor(base, color, dst):
    # fill the BRISA band with the new color (solid or gradient), keep the band's alpha
    if ":" in color:
        a, b = color.split(":")
        fill = ["-size", "300x1122", f"gradient:{a}-{b}", "-rotate", "-90"]   # a at left
    else:
        fill = ["-size", "1122x300", f"xc:{color}"]
    mask, band = WORK / "band-alpha.png", WORK / "band.png"
    magick(base, "-crop", BRISA_BAND, "+repage", "-alpha", "extract", mask)
    magick(*fill, mask, "-alpha", "off", "-compose", "CopyOpacity", "-composite", band)
    magick(base, band, "-geometry", "+0+985", "-compose", "Copy", "-composite",
           "-trim", "+repage", *DPI, dst)


def page():
    cards = []
    for name, (color, cw, cd, note) in CANDIDATES.items():
        img = f"out/brisa-logo-stacked-{name}.png"
        cells = "".join(
            f'<div class="cell" style="background:{bg}"><img src="{img}" alt="Brisa Climate"></div>'
            for bg in ("#FFFFFF", DARK_BG))
        cards.append(f'<section><h2>{name.title()} <code>{color}</code></h2>'
                     f'<p>{note}. Contrast: {cw}:1 on white, {cd}:1 on {DARK_BG}.</p>'
                     f'<div class="pair">{cells}</div></section>')
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>Brisa logo transparent</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:24px;color:#222;background:#f4f4f4}}
h1{{font-size:22px}}h2{{font-size:18px;margin:28px 0 4px}}p{{margin:0 0 10px}}
.pair{{display:flex;gap:16px;flex-wrap:wrap}}
.cell{{padding:24px;border:1px solid #ccc;border-radius:6px}}
.cell img{{height:220px;display:block}}</style>
<h1>Brisa stacked logo: transparent PNG, BRISA recolored</h1>
<p>Each candidate on white (light mode) and on {DARK_BG} (Outlook dark mode). CLIMATE and the bear are unchanged.</p>
{''.join(cards)}
""")


def main():
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    base = WORK / "base-transparent.png"
    print("step 1/3: color-to-alpha", flush=True)
    color_to_alpha(base)
    print("step 2/3: recolor BRISA", flush=True)
    for name, (color, *_rest) in CANDIDATES.items():
        recolor(base, color, OUT / f"brisa-logo-stacked-{name}.png")
        print(f"  wrote out/brisa-logo-stacked-{name}.png", flush=True)
    print("step 3/3: preview page", flush=True)
    page()
    print("RESULT: ok", HERE / "index.html")


if __name__ == "__main__":
    main()
