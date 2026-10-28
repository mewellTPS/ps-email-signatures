#!/usr/bin/env python3
"""The Purple Standard Pledge: email-signature band image + standalone check icon.

From Michael's Photoshop rough (2026-10-28): The Standard purple band, Neon Purple check
bullets, white Lexend text, the four pledge lines from the brand guide. The band is an
image because Lexend is not email-safe. It sits on its own purple, so it reads the same in
light and dark mode.

The bullet is a plain check in a circle, NOT the brand checkmark: the brand guide's misuse
list says "Use the brand checkmark for checks" is a don't.

Rendered by headless Chrome at 2x from local HTML (fonts in resources/purple_standard/fonts),
then stamped 96 DPI (ADR 0008). Writes out/tps-pledge-<layout>.png, out/tps-pledge-check.png
and index.html. Run from anywhere: python3 purple_standard/pledge/build.py
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FONTS = REPO / "resources/purple_standard/fonts"
OUT = HERE / "out"
WORK = HERE / "_work"             # intermediates, overwritten each run
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]

STANDARD = "#49104F"              # band
NEON = "#A263D2"                  # check disc; also the mid-tone for transparent use:
                                  # 4.0:1 on white, 5.25:1 on black, 4.17:1 on Outlook-dark #1E1E1E
PLEDGE = ["Clear communication", "Technology and solutions driven",
          "Professionalism in action", "Exceeding expectations"]   # brand guide, verbatim
WIDTH = 480                       # display width = the signature width (= the endorsement it replaces)
FONT_PX = 14                      # display size; ~10.5pt, no tiny text
BADGE = REPO / "purple_standard/assets/tps-badge.png"   # 150x150, purple art, white interior (ADR 0015)
BADGE_PX = (64, 62, 60, 58, 56)   # clear styles: largest that fits wins (64 = +45%); 2x <= 150 source
MIN_GAP = 12                      # right-side badge: minimum space after "solutions driven"


def check_svg(s, disc, tick):
    return (f'<svg viewBox="0 0 20 20" width="{s}" height="{s}"><circle cx="10" cy="10" r="10" fill="{disc}"/>'
            f'<path d="M5.6 10.4l3 3 5.8-6.4" fill="none" stroke="{tick}" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


# band:  the basic reusable template: white text on The Standard purple (reads the same in any mode)
# clear: transparent, everything in the NEON mid-tone (dark mode option C, ADR 0020), TPS badge at left
# clear-right: the same with the badge at the right edge, at least MIN_GAP after the text (A/B)
STYLES = {
    "band": dict(bg=STANDARD, text="#fff", disc=NEON, tick=STANDARD, pad="9px 14px", badge=False, layouts=("flow", "grid"), css=""),
    "clear": dict(bg="transparent", text=NEON, disc=NEON, tick="#fff", pad="0", badge="left", layouts=("flow",),   # grid overflows 480px
                  css="#band{gap:7px;letter-spacing:0}.row{gap:8px}.i{gap:4px}"),   # room for the big badge
    # clear-text: no badge; for signatures that show the TPS badge elsewhere (e.g. top-right corner)
    "clear-text": dict(bg="transparent", text=NEON, disc=NEON, tick="#fff", pad="0", badge=False, layouts=("flow",),
                       css="#band{letter-spacing:0}.row{gap:8px}.i{gap:4px}"),
    "clear-right": dict(bg="transparent", text=NEON, disc=NEON, tick="#fff", pad="0", badge="right", layouts=("flow",),
                        css=f"#band{{gap:{MIN_GAP}px;letter-spacing:0;justify-content:space-between}}.row{{gap:8px}}.i{{gap:4px}}"),
}


def item(text, st):
    return f'<span class="i">{check_svg(15, st["disc"], st["tick"])}<span>{text}</span></span>'


def layouts(st):
    return {
        # rows as in the rough: 1+2 on top, 3+4 below, each row flowing left to right
        "flow": f'<div><div class="row">{item(PLEDGE[0], st)}{item(PLEDGE[1], st)}</div>'
                f'<div class="row">{item(PLEDGE[2], st)}{item(PLEDGE[3], st)}</div></div>',
        # the same four lines in two aligned columns
        "grid": f'<div class="grid">{"".join(item(t, st) for t in PLEDGE)}</div>',
    }


def band_html(body, st, badge_px=0):
    badge = (f'<img src="{WORK / badge_file(st.get("badge_color", NEON))}" width="{badge_px}" height="{badge_px}" alt="">'
             if st["badge"] else "")
    left, right = (badge, "") if st["badge"] == "left" else ("", badge)
    return f"""<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:LexendLocal;font-weight:400;src:url("{FONTS / 'Lexend-Regular.ttf'}")}}
html,body{{margin:0;background:transparent}}
#band{{width:{WIDTH}px;box-sizing:border-box;background:{st["bg"]};color:{st["text"]};padding:{st["pad"]};
font:400 {FONT_PX}px/1 LexendLocal;letter-spacing:.1px;display:flex;align-items:center;gap:10px}}
#band img{{display:block;flex:none}}
.row{{display:flex;gap:14px;white-space:nowrap}}.row+.row{{margin-top:7px}}
.grid{{display:grid;grid-template-columns:auto auto;justify-content:start;column-gap:22px;row-gap:7px;white-space:nowrap}}
.i{{display:inline-flex;align-items:center;gap:6px}}svg{{flex:none}}
{st["css"]}
</style><div id="band">{left}{body}{right}</div>"""


def badge_file(color):
    return "badge-mid.png" if color == NEON else f"badge-{color[1:].lower()}.png"


def badge_mid(color=NEON, out_name="tps-badge-clear.png"):
    """TPS badge for transparent use: white interior -> transparent, purple art -> color.
    t = how purple a pixel is (0 white, 1 #49104F, by the green channel); alpha *= t."""
    t = "clamp((1-u.g)/(1-0.063))"
    magick_run(BADGE, "-channel", "A", "-fx", f"u.a*{t}", "+channel",
               "-fill", color, "-colorize", "100", WORK / badge_file(color))
    # standalone copy for signatures that place the badge on its own (150px = 2x of a 75px display)
    magick_run(WORK / badge_file(color), *DPI, OUT / out_name)


def magick_run(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def shoot(html_path, png, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--default-background-color=00000000",
                    f"--window-size={w},{h}", f"--screenshot={png}", f"file://{html_path}"],
                   check=True, capture_output=True)


def measure(html_path):
    """Band height in CSS px, read from Chrome's layout. Raises ValueError if the content
    overflows WIDTH or a right-side badge sits closer than MIN_GAP to the text."""
    probe = WORK / "probe.html"
    # measure only after Lexend loads: the fallback font is narrower and hides overflow
    probe.write_text(html_path.read_text() + '<script>document.fonts.ready.then(()=>{'
                     'if(!document.fonts.check("14px LexendLocal"))return;const b=document.getElementById("band");'
                     'const r=Math.max(...[...b.querySelectorAll(".i,img")].map(e=>e.getBoundingClientRect().right));'
                     'const t=Math.max(...[...b.querySelectorAll(".i")].map(e=>e.getBoundingClientRect().right));'
                     'const i=b.querySelector("img");const g=i&&i.getBoundingClientRect().left>t?i.getBoundingClientRect().left-t:999;'
                     'document.title=b.offsetHeight+" "+Math.ceil(r)+" "+Math.floor(g)})</script>')
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=5000",
                          "--dump-dom", f"file://{probe}"],
                         check=True, capture_output=True, text=True).stdout
    title = dom.split("<title>")[1].split("</title>")[0] if "<title>" in dom else ""
    if not title:
        raise SystemExit(f"RESULT: FAILED: {html_path.name}: Lexend did not load. Next: check {FONTS}.")
    h, sw, gap = map(int, title.split())
    if sw > WIDTH:
        raise ValueError(f"content is {sw}px, wider than {WIDTH}px")
    if gap < MIN_GAP:
        raise ValueError(f"badge is {gap}px from the text, under {MIN_GAP}px")
    return h


def main():
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    print("step 1/3: pledge images", flush=True)
    badge_mid()
    sizes = {}
    for style, st in STYLES.items():
        for name in st["layouts"]:
            body = layouts(st)[name]
            key = f"{style}-{name}"
            src = WORK / f"{key}.html"
            for px in (BADGE_PX if st["badge"] else (0,)):
                src.write_text(band_html(body, st, px))
                try:
                    h = measure(src)
                    break
                except ValueError as e:
                    print(f"  {key}: badge {px}px does not fit ({e})", flush=True)
            else:
                raise SystemExit(f"RESULT: FAILED: {key} does not fit at any badge size. "
                                 "Next: tighten gaps in STYLES or add smaller BADGE_PX sizes.")
            raw = WORK / f"{key}.png"
            shoot(src, raw, WIDTH, h)
            magick_run(raw, "-crop", f"{WIDTH * 2}x{h * 2}+0+0", "+repage", *DPI, OUT / f"tps-pledge-{key}.png")
            sizes[key] = h
            print(f"  out/tps-pledge-{key}.png  display {WIDTH}x{h}, file {WIDTH * 2}x{h * 2}"
                  + (f", badge {px}px" if px else ""), flush=True)

    print("step 2/3: check icon", flush=True)
    icon = WORK / "check.html"
    icon.write_text(f'<!doctype html><style>html,body{{margin:0;background:transparent}}svg{{display:block}}</style>'
                    f'{check_svg(40, NEON, STANDARD)}')
    shoot(icon, WORK / "check.png", 40, 40)
    subprocess.run(["magick", WORK / "check.png", "-crop", "80x80+0+0", "+repage", *DPI,
                    OUT / "tps-pledge-check.png"], check=True)
    print("  out/tps-pledge-check.png  80x80 (40px display)", flush=True)

    print("step 3/3: preview page", flush=True)
    cells = "".join(
        f'<h2>{n.title()} ({WIDTH}x{h})</h2><div class="pair">'
        + "".join(f'<div class="cell" style="background:{bg}"><img src="out/tps-pledge-{n}.png" width="{WIDTH}" height="{h}"></div>'
                  for bg in ("#FFFFFF", "#1E1E1E", "#000000")) + "</div>"
        for n, h in sizes.items())
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Purple Standard Pledge</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:24px;color:#222;background:#f4f4f4}}h1{{font-size:20px}}h2{{font-size:16px;margin:24px 0 8px}}
.pair{{display:flex;gap:16px;flex-wrap:wrap}}.cell{{padding:24px;border:1px solid #ccc;border-radius:6px}}img{{display:block}}</style>
<h1>The Purple Standard Pledge: signature band</h1>
<p>Lexend Regular {FONT_PX}px. <b>Band</b> (basic template): white on The Standard {STANDARD}, {NEON} check discs.
<b>Clear</b>: transparent; text, checks and TPS badge in {NEON}. Shown on white, Outlook dark #1E1E1E, and black.</p>
{cells}
<h2>Check icon (80x80 file, shown at 40px)</h2><img src="out/tps-pledge-check.png" width="40" height="40">
""")
    print("RESULT: ok", HERE / "index.html")


if __name__ == "__main__":
    main()
