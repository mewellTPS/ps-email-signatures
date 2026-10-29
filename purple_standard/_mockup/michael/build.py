#!/usr/bin/env python3
"""Purple Standard default signature, Michael Ewell as the sample: current layout, C, and E.

PS and ACE have shared-mailbox issues, so each person gets their own hardcoded rule (Michael,
2026-10-28); this build is the pattern; docs/review/build-rollout.py reuses it per person.

Layout: his current signature (purple_standard/default.html): name and title, contact lines,
brand strip, TPS badge top right, endorsement along the bottom. Changes:
  - dark mode (option C, ADR 0020): badge -> transparent Neon Purple; endorsement -> Neon Purple
    on transparency
  - WTR DR strip icon: the full droplet mark, no business name (Michael, 2026-10-29); the
    glossy mid-blue drop reads on white and dark
  - text >= 10pt (no tiny text); gray #808080 -> #666666 for contrast on white
  - 480px wide, the width of the Pledge
  - C: the Pledge (badge left) replaces the endorsement, no corner badge
  - E: the Pledge text replaces the endorsement, corner badge kept

Writes:
  out/                      2x / 96 DPI images
  signature-<variant>.html  CodeTwo paste source, hosted URLs
  index.html                preview: each variant on white and simulated Outlook dark
Run from anywhere: python3 purple_standard/_mockup/michael/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PS = HERE.parents[1]
REPO = PS.parent
OUT = HERE / "out"
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
STANDARD = "#49104F"              # text: Outlook dark -> #FFC1FF (sampled)
NEON = "#A263D2"                  # links (text: -> #C17EF0, sampled) and all art: 4.0:1 on white, 4.17:1 on #1E1E1E
GRAY = "#666666"                  # -> #A2A2A2 (sampled); #808080 was 3.9:1 on white
DARK_BG = "#1E1E1E"

PERSON = {
    "name": "Michael Ewell",
    "title": "SEO and Data Specialist",        # Michael, 2026-10-29
    "phone": "(801) 641-5387",                 # Michael, 2026-10-29
    "tel": "+18016415387",
    "email": "mewell@purple-standard.com",
}
ADDRESS = "21516 Carson Dr, Land O' Lakes, FL 34639"   # ADR 0019 + 0021
BRANDS = [("ace", "https://www.acesepticandwaste.com/", "ACE Septic &amp; Waste"),
          ("purple-current", "https://purple-current.com/", "Purple Current"),
          ("boyette", "https://www.boyettepumpwell.com/", "Boyette Pump &amp; Well"),
          ("wtr-dr", "https://wtrdr.com/", "WTR DR"),
          ("brisa", "https://brisaclimate.com/", "Brisa Climate"),
          ("tyrian", "https://tyrianroofing.com/", "Tyrian Roofing")]
WTR_ICON = Path.home() / "Developer/visual-assets/wtrdr/logos/wtrdr-mark.png"   # 830x1332 droplet, transparent

WIDTH = 480
CORNER_BADGE_PX = 75
PLEDGE_OUT = REPO / "purple_standard/pledge/out"
PLEDGES = {"pledge": ("tps-pledge-clear.png", PLEDGE_OUT / "tps-pledge-clear-flow.png"),
           "pledge-text": ("tps-pledge-clear-text.png", PLEDGE_OUT / "tps-pledge-clear-text-flow.png")}
CORNER_BADGE = PLEDGE_OUT / "tps-badge-clear.png"

OUTLOOK_TEXT_MAP = {STANDARD: "#FFC1FF", NEON: "#C17EF0", GRAY: "#A2A2A2"}   # all sampled 2026-10-26


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def size(png):
    w, h = subprocess.run(["magick", "identify", "-format", "%w %h", str(png)],
                          check=True, capture_output=True, text=True).stdout.split()
    return int(w), int(h)


def build_images():
    OUT.mkdir(exist_ok=True)
    print("step 1/3: images", flush=True)
    # endorsement: purple art with a white tick; t = how purple (green channel), alpha *= t, color -> NEON
    t = "clamp((1-u.g)/(1-0.063))"
    magick(PS_ASSETS / "standard/email-signature/tps-endorsement.png", "-channel", "A", "-fx", f"u.a*{t}",
           "+channel", "-fill", NEON, "-colorize", "100", "-resize", f"{WIDTH * 2}x", *DPI,
           OUT / "tps-endorsement-clear.png")
    # trim, then fit the droplet inside 80x80 like the other strip icons (C, native shapes: ADR 0010)
    magick(WTR_ICON, "-trim", "+repage", "-resize", "80x80", "-background", "none", "-gravity", "center",
           "-extent", "80x80", *DPI, OUT / "brand-wtr-dr-drop.png")


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; {style}"{v}>{inner}</p>'


def strip():
    cells = []
    for i, (slug, url, alt) in enumerate(BRANDS):
        f = "brand-wtr-dr-drop.png" if slug == "wtr-dr" else f"brand-{slug}.png"
        pad = "0" if i == len(BRANDS) - 1 else "0 12px 0 0"
        cells.append(f'<td style="padding: {pad}; vertical-align: middle; line-height: 0"><a href="{url}" target="_blank" title="{alt}">'
                     f'<img src="{HOST}standard/email-signature/{f}" border="0" alt="{alt}" width="36" height="36" style="width: 36px; height: 36px; display: block"></a></td>')
    return ('<table cellspacing="0" cellpadding="0" style="border-collapse: collapse; line-height: 0; margin-top: 8px" data-codetwo-visible="Brand icons"><tbody><tr>'
            + "".join(cells) + "</tr></tbody></table>")


def signature(footer):
    corner = footer != "pledge"
    line = f"font-size: 10pt; line-height: 1.5; color: {GRAY}"
    contact = "\n        ".join([
        p(f"font-size: 13pt; line-height: 1.15; color: {STANDARD}", f"<b>{PERSON['name']}</b>", "Name"),
        p(f"margin: 2px 0 0 0; font-size: 10pt; color: {STANDARD}", f"<b>{PERSON['title']}</b>", "Job title"),
        p(f"margin: 8px 0 0 0; {line}", f'<b style="color: {STANDARD}">P:</b> <a href="tel:{PERSON["tel"]}" style="color: {GRAY}; text-decoration: none">{PERSON["phone"]}</a>', "Phone"),
        p(line, f'<b style="color: {STANDARD}">E:</b> <a href="mailto:{PERSON["email"]}" style="color: {NEON}; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        p(line, ADDRESS, "Company address"),
        p(line, f'<a href="https://www.purple-standard.com" target="_blank" style="color: {NEON}; text-decoration: none"><b>www.purple-standard.com</b></a>', "Website"),
        strip(),
    ])
    corner_td = f"""
      <td width="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; padding: 0; vertical-align: top; text-align: right; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{HOST}standard/email-signature/tps-badge-clear.png" border="0" alt="Purple Standard" width="{CORNER_BADGE_PX}" height="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; height: {CORNER_BADGE_PX}px; display: inline-block"></a>
      </td>""" if corner else ""
    cols = 2 if corner else 1
    if footer == "endorsement":
        eh = size(OUT / "tps-endorsement-clear.png")[1] // 2
        foot = f"""    <tr data-codetwo-visible="Endorsement">
      <td colspan="{cols}" style="padding: 12px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{HOST}standard/email-signature/tps-endorsement-clear.png" border="0" alt="Powered by The Purple Standard" width="{WIDTH}" height="{eh}" style="width: {WIDTH}px; height: {eh}px; display: block"></a>
      </td>
    </tr>"""
    else:
        name, png = PLEDGES[footer]
        ph = size(png)[1] // 2
        foot = f"""    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark. Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="{cols}" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{HOST}standard/email-signature/{name}" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="{WIDTH}" height="{ph}" style="width: {WIDTH}px; height: {ph}px; display: block"></a>
      </td>
    </tr>"""
    return f"""<!-- Purple Standard - {PERSON['name']}. Person fields are HARDCODED until Ntiva fixes Entra (one rule per sender). Dark-mode option C (ADR 0020). -->
<!-- Built by purple_standard/_mockup/michael/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="ps-signature" style="width: {WIDTH}px; border-collapse: collapse; line-height: initial">
  <tbody>
    <tr>
      <td style="padding: 0; vertical-align: top">
        {contact}
      </td>{corner_td}
    </tr>
{foot}
  </tbody>
</table>
"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    for f in ("tps-endorsement-clear.png", "brand-wtr-dr-drop.png"):
        h = h.replace(HOST + "standard/email-signature/" + f, "out/" + f)
    for name, png in [*PLEDGES.values(), ("tps-badge-clear.png", CORNER_BADGE)]:
        h = h.replace(HOST + "standard/email-signature/" + name + '"', f'{png}"')
    return h.replace(HOST + "standard/email-signature/", str(PS_ASSETS / "standard/email-signature") + "/")


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


VARIANTS = [("current", "Current layout (endorsement)", "endorsement"),
            ("c", "C · Pledge, badge left (no corner badge)", "pledge"),
            ("e", "E · Pledge text, TPS badge top right", "pledge-text")]


def page():
    cols = []
    for key, label, footer in VARIANTS:
        html = signature(footer)
        (HERE / f"signature-{key}.html").write_text(html)
        lo = local(html)
        cols.append(f"""<div class="col"><h2>{label}</h2>
<h3>Light mode</h3><div class="mail" style="background:#fff">{lo}</div>
<h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{outlook_dark(lo)}</div></div>""")
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>Purple Standard default signature</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px;width:{WIDTH}px}}</style>
<main><h1>Purple Standard: Michael Ewell</h1>
<p>Real data. Dark mode is simulated:
Outlook recolors text but not images or borders. All text mappings were sampled from Outlook.</p>
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
