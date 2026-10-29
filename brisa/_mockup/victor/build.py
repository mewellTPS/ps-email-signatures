#!/usr/bin/env python3
"""Brisa signature for Victor Rodriguez: compact layout, new stacked logo, light + dark mode.

Hardcoded person fields (Entra is missing his title and phone; see docs/entra-fixes.md).
Dark mode follows option C (ADR 0020): artwork on transparency uses mid-tones, and the
divider is a mid-tone because Outlook recolors text but not borders or images.

Writes:
  out/                      2x / 96 DPI images (logo, badges with mid-tone discs)
  signature-<variant>.html  CodeTwo paste source, hosted URLs
  index.html                preview: each variant on white and simulated Outlook dark
Run from anywhere: python3 brisa/_mockup/victor/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRISA = HERE.parents[1]
OUT = HERE / "out"
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
VER = ""                          # new filenames, so no cache-buster needed
BLUE = "#3C81F6"                  # BRISA wordmark + bear blue: 3.72:1 on white, 4.49:1 on #1E1E1E
PURPLE = "#48104F"
DARK_BG = "#1E1E1E"

PERSON = {
    "name": "Victor Rodriguez",
    "title": "Co-Owner/Operator",   # Michael, 2026-10-29: hardcoded until Ntiva fixes Entra
    "phone": "(813) 461-5972",
    "email": "vrodriguez@brisaclimate.com",
}
ADDRESS = "21516 Carson Dr, Land O' Lakes, FL 34639"   # ADR 0019 + 0021 spelling

LOGO_W, LOGO_H = 105, 140         # display size; file is 2x
GAP = 18                          # logo-to-bar = bar-to-text
# footer -> (hosted name, local build output from purple_standard/pledge/build.py); display = file / 2
PLEDGE_OUT = BRISA.parent / "purple_standard/pledge/out"
PLEDGES = {"pledge": ("tps-pledge-clear.png", PLEDGE_OUT / "tps-pledge-clear-flow.png"),          # badge left
           "pledge-right": ("tps-pledge-clear-right.png", PLEDGE_OUT / "tps-pledge-clear-right-flow.png"),
           "pledge-text": ("tps-pledge-clear-text.png", PLEDGE_OUT / "tps-pledge-clear-text-flow.png")}   # no badge
CORNER_BADGE_PX = 75              # TPS badge top right, placed as in purple_standard/default.html
CORNER_BADGE = PLEDGE_OUT / "tps-badge-clear.png"   # transparent, Neon Purple (not the white-fill PS badge)


def display_h(png):
    return int(subprocess.run(["magick", "identify", "-format", "%h", str(png)],
                              check=True, capture_output=True, text=True).stdout) // 2

# Outlook dark recolors text. #48104F -> #FFC1FF matches the sampled PS purple (#49104F);
# the grays are estimates, labeled as such on the page.
OUTLOOK_TEXT_MAP = {PURPLE: "#FFC1FF", "#2A2A2A": "#E6E6E6", "#6E6E6E": "#A8A8A8"}


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def build_images():
    OUT.mkdir(exist_ok=True)
    print("step 1/3: images", flush=True)
    magick(BRISA / "assets/brisa-logo-stacked-master.png", "-resize", f"{LOGO_W * 2}x{LOGO_H * 2}!",
           *DPI, OUT / "brisa-logo-stacked.png")
    # badges: white glyph on a #48104F disc, which vanishes on dark; disc -> BLUE, glyph stays white
    for b in ("facebook", "instagram", "google"):
        r, g, bl = (int(BLUE[i:i + 2], 16) / 255 for i in (1, 3, 5))
        src = PS_ASSETS / f"brisa/email-signature/badge-{b}.png"
        # t = how far a pixel is from the purple disc toward white (0 disc, 1 glyph)
        t = "clamp((u.g-0.063)/(1-0.063))"
        magick(src, "-channel", "R", "-fx", f"(1-{t})*{r}+{t}",
               "-channel", "G", "-fx", f"(1-{t})*{g}+{t}",
               "-channel", "B", "-fx", f"(1-{t})*{bl}+{t}", "+channel", *DPI, OUT / f"badge-{b}-blue.png")


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; {style}"{v}>{inner}</p>'


def signature(footer, corner=False):
    cols = 4 if corner else 3
    img = lambda path: HOST + path + VER
    badge = lambda b, url, last=False: (
        f'<a href="{url}" target="_blank" style="text-decoration: none"><img src="{img(f"brisa/email-signature/badge-{b}-blue.png")}" '
        f'border="0" alt="{b.title()}" width="24" height="24" style="width: 24px; height: 24px; display: inline-block'
        f'{"" if last else "; margin-right: 6px"}"></a>')
    line = "font-size: 10pt; line-height: 1.5; color: #2A2A2A"
    contact = "\n        ".join([
        p(f"font-size: 13pt; line-height: 1.15; color: {PURPLE}", f"<b>{PERSON['name']}</b>", "Name"),
        p("margin: 2px 0 0 0; font-size: 10pt; color: #6E6E6E", PERSON["title"], "Job title"),
        p(f"margin: 8px 0 0 0; {line}", f'<b style="color: {PURPLE}">P:</b> <a href="tel:+18134615972" style="color: #2A2A2A; text-decoration: none">{PERSON["phone"]}</a>', "Phone"),
        p(line, f'<b style="color: {PURPLE}">E:</b> <a href="mailto:{PERSON["email"]}" style="color: #2A2A2A; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        p(line, ADDRESS, "Company address"),
        p(line, f'<a href="https://brisaclimate.com/" target="_blank" style="color: {PURPLE}; text-decoration: none"><b>www.brisaclimate.com</b></a>', "Website"),
        p("margin: 8px 0 0 0; font-size: 0; line-height: 0",
          badge("facebook", "https://www.facebook.com/profile.php?id=61589534684038")
          + badge("instagram", "https://www.instagram.com/brisa.climate.solutions/")
          + badge("google", "https://share.google/jLJBkU8jqKbZe51le", last=True), "Social links"),
    ])
    rows = f"""    <tr>
      <td width="{LOGO_W}" style="width: {LOGO_W}px; padding: 0; vertical-align: middle; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://brisaclimate.com/" target="_blank"><img src="{img('brisa/email-signature/brisa-logo-stacked.png')}" border="0" alt="Brisa Climate" width="{LOGO_W}" height="{LOGO_H}" style="width: {LOGO_W}px; height: {LOGO_H}px; display: block"></a>
      </td>
      <!-- fixed spacer = the same {GAP}px as the bar-to-text padding, so the bar sits centered in the gap -->
      <td width="{GAP}" style="width: {GAP}px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 0 0 0 {GAP}px; vertical-align: middle; border-left: 2px solid {BLUE}">
        {contact}
      </td>""" + (f"""
      <!-- TPS badge, top right, as in the Purple Standard signature -->
      <td width="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; padding: 0; vertical-align: top; text-align: right; line-height: 0" data-codetwo-visible="TPS badge">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/tps-badge-clear.png')}" border="0" alt="Purple Standard" width="{CORNER_BADGE_PX}" height="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; height: {CORNER_BADGE_PX}px; display: inline-block"></a>
      </td>""" if corner else "") + """
    </tr>"""
    if footer in PLEDGES:
        name, png = PLEDGES[footer]
        ph = display_h(png)
        rows += f"""
    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark (replaces both the banner and the endorsement). Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="{cols}" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/' + name)}" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="480" height="{ph}" style="width: 480px; height: {ph}px; display: block"></a>
      </td>
    </tr>"""
    if footer == "banner":
        rows += f"""
    <!-- Promo banner: Google "Leave Us a Review" deep link (distinct from the badge's general GMB link; do not merge). -->
    <tr data-codetwo-visible="Banner">
      <td colspan="{cols}" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://share.google/AfTfkPPBgOVDHaqi2" target="_blank"><img src="{img('brisa/email-signature/banner-web.png')}" border="0" alt="The reason you keep your cool. Help spread the word, leave us a review." width="480" height="117" style="width: 480px; height: 117px; display: block"></a>
      </td>
    </tr>"""
    if footer in ("banner", "endorsement"):
        rows += f"""
    <tr data-codetwo-visible="Endorsement">
      <td colspan="{cols}" style="padding: 10px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/tps-endorsement.png')}" border="0" alt="Powered by The Purple Standard" width="480" height="23" style="width: 480px; height: 23px; display: block"></a>
      </td>
    </tr>"""
    return f"""<!-- Brisa Climate - Victor Rodriguez. Person fields are HARDCODED (Entra lacks title and phone; see docs/entra-fixes.md). -->
<!-- Compact layout (ADR 0024), dark-mode option C (ADR 0020). Built by brisa/_mockup/victor/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="brisa-signature" style="width: 480px; border-collapse: collapse; line-height: initial">
  <tbody>
{rows}
  </tbody>
</table>
"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S).replace(VER, "")
    h = h.replace(HOST + "brisa/email-signature/brisa-logo-stacked.png", "out/brisa-logo-stacked.png")
    for b in ("facebook", "instagram", "google"):
        h = h.replace(HOST + f"brisa/email-signature/badge-{b}-blue.png", f"out/badge-{b}-blue.png")
    h = h.replace(HOST + "brisa/email-signature/", str(PS_ASSETS / "brisa/email-signature") + "/")
    for name, png in [*PLEDGES.values(), ("tps-badge-clear.png", CORNER_BADGE)]:
        h = h.replace(HOST + "standard/email-signature/" + name + '"', f'{png}"')
    return h.replace(HOST + "standard/email-signature/", str(PS_ASSETS / "standard/email-signature") + "/")


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


VARIANTS = [("a", "A · Review banner + endorsement", "banner"),
            ("b", "B · Endorsement only (most compact)", "endorsement"),
            ("c", "C · Pledge, badge left", "pledge"),
            ("d", "D · Pledge, badge right", "pledge-right"),
            ("e", "E · Pledge text, TPS badge top right", "pledge-text", True)]


def page():
    # all variants side by side: one column per variant, light row then dark row
    cols = []
    for key, label, footer, *corner in VARIANTS:
        html = signature(footer, *corner)
        (HERE / f"signature-{key}.html").write_text(html)
        lo = local(html)
        cols.append(f"""<div class="col"><h2>{label}</h2>
<h3>Light mode</h3><div class="mail" style="background:#fff">{lo}</div>
<h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{outlook_dark(lo)}</div></div>""")
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>Brisa Victor signature</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px;width:480px}}</style>
<main><h1>Brisa Climate: Victor Rodriguez</h1>
<p>Real data, hardcoded. Address uses the ADR 0021 spelling "Land O' Lakes". Dark mode is simulated:
Outlook recolors text but not images or borders; the gray dark-mode text colors are estimates.</p>
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
