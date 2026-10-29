#!/usr/bin/env python3
"""Boyette Pump & Well signature for Danny Boyette: his own layout, dark mode fixed, Pledge added.

Danny is happy with his layout (logo | divider | contact), so it stays. Changes (Michael, 2026-10-28):
  - logo: the approved dark-mode C blue wordmark (BOYETTE #3C81F5, PUMP & WELL #4D7FB5; ADR 0020)
    with the baked-in endorsement cut off; the Purple Standard Pledge replaces it
  - divider #404040 -> #7A7A7A (approved), so it shows on dark
  - text >= 10pt (no tiny text); addresses in the ADR 0021 format; 8011 -> 21516 Carson Dr, Reddick kept
  - two versions, as for Brisa: C (Pledge with badge left) and E (Pledge text, TPS badge top right)
Text stays black and the website red: Outlook dark recolors text (#000000 -> white, #F93822 -> #FF593B,
both sampled 2026-10-26). The red social discs read on white and on dark, so they are unchanged.

Hardcoded person fields (Entra is missing his title; see docs/entra-fixes.md).

Writes:
  out/                      2x / 96 DPI logo
  signature-<variant>.html  CodeTwo paste source, hosted URLs
  index.html                preview: each variant on white and simulated Outlook dark
Run from anywhere: python3 boyette/_mockup/danny/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOYETTE = HERE.parents[1]
REPO = BOYETTE.parent
OUT = HERE / "out"
WORK = HERE / "_work"             # intermediates, overwritten each run
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
RED = "#F93822"
DIVIDER = "#7A7A7A"               # approved dark-mode C divider
DARK_BG = "#1E1E1E"

PERSON = {
    "name": "Danny Boyette",
    "title": "Co-Owner/Operator",  # Michael, 2026-10-29; hardcoded until Ntiva fixes Entra
    "phone": "(813) 923-0008",    # Michael, 2026-10-28 (his live signature)
    "tel": "+18139230008",
    "email": "dboyette@BoyettePumpWell.com",   # casing as in his live signature
}
ADDRESSES = ["21516 Carson Dr, Land O' Lakes, FL 34639",   # ADR 0019 + 0021
             "15215 N Hwy 329, Reddick, FL 32686"]         # Reddick location kept (Michael, 2026-10-28)
SOCIAL = [("google", "https://share.google/F9yOsah8sVpCjubV7"),
          ("facebook", "https://www.facebook.com/BoyettePumpandWell/"),
          ("instagram", "https://www.instagram.com/boyettepumpwellserviceinc"),
          ("yelp", "https://www.yelp.com/biz/boyette-pump-and-well-service-masaryktown-3")]

LOGO_SRC = REPO / "_mockup/dark-mode-c/out/boyette-logo-blue.png"   # 380x290, endorsement pill in rows 260+
ART_ROWS = 260                    # rows 0-259 are the logo; below is the endorsement
LOGO_W = 170                      # display width (was 190): fits the 480px width with the address line
PAD = 22                          # logo-to-divider = divider-to-text, as in his signature
PLEDGE_OUT = REPO / "purple_standard/pledge/out"
PLEDGES = {"pledge": ("tps-pledge-clear.png", PLEDGE_OUT / "tps-pledge-clear-flow.png"),          # badge left
           "pledge-text": ("tps-pledge-clear-text.png", PLEDGE_OUT / "tps-pledge-clear-text-flow.png")}   # no badge
CORNER_BADGE_PX = 64              # TPS badge top right; 75 would push the contact block down further
CORNER_BADGE = PLEDGE_OUT / "tps-badge-clear.png"

# Outlook dark recolors text; both sampled 2026-10-26 (dark-mode-c).
OUTLOOK_TEXT_MAP = {"#000000": "#FFFFFF", RED: "#FF593B"}


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def size(png):
    w, h = subprocess.run(["magick", "identify", "-format", "%w %h", str(png)],
                          check=True, capture_output=True, text=True).stdout.split()
    return int(w), int(h)


def build_images():
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    print("step 1/3: images", flush=True)
    sw, _ = size(LOGO_SRC)
    magick(LOGO_SRC, "-crop", f"{sw}x{ART_ROWS}+0+0", "+repage", "-trim", "+repage",
           "-resize", f"{LOGO_W * 2}x", WORK / "logo.png")
    w, h = size(WORK / "logo.png")
    # pad to exactly LOGO_W*2 wide and an even height, so display = file / 2
    magick(WORK / "logo.png", "-background", "none", "-gravity", "center",
           "-extent", f"{LOGO_W * 2}x{h + h % 2}", *DPI, OUT / "boyette-logo-clear.png")


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; color: #000000; {style}"{v}>{inner}</p>'


def contact_lines():
    line = "font-size: 10pt; line-height: 1.4"
    name = [p("font-size: 13pt; line-height: 1.15", f"<b>{PERSON['name']}</b>", "Name"),
            p("margin: 2px 0 0 0; font-size: 10pt", PERSON["title"], "Job title"),
            p(f"margin: 10px 0 0 0; {line}", f'<b>P:</b> <a href="tel:{PERSON["tel"]}" style="color: #000000; text-decoration: none">{PERSON["phone"]}</a>', "Phone")]
    rest = [p(line, a, "Company address") for a in ADDRESSES] + [
        p(f"margin: 8px 0 0 0; {line}", f'<b>E:</b> <a href="mailto:{PERSON["email"]}" style="color: #000000; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        p(line, f'<a href="https://www.boyettepumpwell.com/" target="_blank" style="color: {RED}; text-decoration: none">www.boyettepumpwell.com</a>', "Website"),
        p("margin: 10px 0 0 0; font-size: 0; line-height: 0", "".join(
            f'<a href="{u}" target="_blank" style="text-decoration: none"><img src="{HOST}boyette/email-signature/badge-{b}.png" '
            f'border="0" alt="{b.title()}" width="28" height="28" style="width: 28px; height: 28px; display: inline-block'
            f'{"" if i == len(SOCIAL) - 1 else "; margin-right: 12px"}"></a>'
            for i, (b, u) in enumerate(SOCIAL)), "Social links")]
    return name, rest


def signature(footer, corner=False):
    lw, lh = (x // 2 for x in size(OUT / "boyette-logo-clear.png"))
    name, rest = contact_lines()
    j = "\n        "
    if corner:
        # badge beside the name block only, so the long address lines below keep the full width
        contact = f"""<table cellspacing="0" cellpadding="0" style="width: 100%; border-collapse: collapse">
          <tr>
            <td style="padding: 0; vertical-align: top">
              {(j + "      ").join(name)}
            </td>
            <td width="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; padding: 0; vertical-align: top; text-align: right; line-height: 0" data-codetwo-visible="TPS badge">
              <a href="https://www.purple-standard.com" target="_blank"><img src="{HOST}standard/email-signature/tps-badge-clear.png" border="0" alt="Purple Standard" width="{CORNER_BADGE_PX}" height="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; height: {CORNER_BADGE_PX}px; display: inline-block"></a>
            </td>
          </tr>
        </table>
        {j.join(rest)}"""
    else:
        contact = j.join(name + rest)
    name_, png = PLEDGES[footer]
    ph = size(png)[1] // 2
    return f"""<!-- Boyette Pump & Well - Danny Boyette. Person fields are HARDCODED (Entra lacks his title; see docs/entra-fixes.md). -->
<!-- His own layout, dark-mode option C (ADR 0020). Built by boyette/_mockup/danny/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="boyette-signature" style="width: 480px; border-collapse: collapse; line-height: initial">
  <tbody>
    <tr>
      <td width="{lw}" style="width: {lw}px; padding: 0; vertical-align: middle; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://www.boyettepumpwell.com/" target="_blank"><img src="{HOST}boyette/email-signature/boyette-logo-clear.png" border="0" alt="Boyette Pump &amp; Well" width="{lw}" height="{lh}" style="width: {lw}px; height: {lh}px; display: block"></a>
      </td>
      <!-- fixed spacer = the same {PAD}px as the divider-to-text padding -->
      <td width="{PAD}" style="width: {PAD}px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 0 0 0 {PAD}px; vertical-align: top; border-left: 2px solid {DIVIDER}">
        {contact}
      </td>
    </tr>
    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark (replaces the endorsement). Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="3" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{HOST}standard/email-signature/{name_}" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="480" height="{ph}" style="width: 480px; height: {ph}px; display: block"></a>
      </td>
    </tr>
  </tbody>
</table>
"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = h.replace(HOST + "boyette/email-signature/boyette-logo-clear.png", "out/boyette-logo-clear.png")
    h = h.replace(HOST + "boyette/email-signature/", str(PS_ASSETS / "boyette/email-signature") + "/")
    for name, png in [*PLEDGES.values(), ("tps-badge-clear.png", CORNER_BADGE)]:
        h = h.replace(HOST + "standard/email-signature/" + name + '"', f'{png}"')
    return h


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


# same letters as Victor's Brisa versions, so operators can pick the same design
VARIANTS = [("c", "C · Pledge, badge left", "pledge"),
            ("e", "E · Pledge text, TPS badge top right", "pledge-text", True)]


def page():
    cols = []
    for key, label, footer, *corner in VARIANTS:
        html = signature(footer, *corner)
        (HERE / f"signature-{key}.html").write_text(html)
        lo = local(html)
        cols.append(f"""<div class="col"><h2>{label}</h2>
<h3>Light mode</h3><div class="mail" style="background:#fff">{lo}</div>
<h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{outlook_dark(lo)}</div></div>""")
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>Boyette Danny signature</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px;width:480px}}</style>
<main><h1>Boyette Pump &amp; Well: Danny Boyette</h1>
<p>Real data, hardcoded. Dark mode is simulated: Outlook recolors text but not images or borders.
The text mappings (black to white, red to #FF593B) were sampled from Outlook.</p>
<div class="grid">{''.join(cols)}</div></main>
""")


def main():
    build_images()
    print("step 2/3: signatures", flush=True)
    page()
    print("step 3/3: done", flush=True)
    print("RESULT: ok", HERE / "index.html")


if __name__ == "__main__":
    main()
