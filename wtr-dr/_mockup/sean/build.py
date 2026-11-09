#!/usr/bin/env python3
"""WTR DR signature for Sean Myatt: Brisa versions C and E (brisa/_mockup/victor) adapted.

Hardcoded person fields (Entra is missing his title; see docs/entra-fixes.md).
Logo: the approved dark-mode C WTR DR logo (wordmark #3A80C0), no endorsement under it;
the Purple Standard Pledge replaces the endorsement. Name blue #2E6DA6 is WTR DR's own
link blue; Outlook dark recolors it to #6DA2E0 (sampled 2026-10-26), so it stays blue.

Writes:
  out/                      2x / 96 DPI logo
  signature-<variant>.html  CodeTwo paste source, hosted URLs
  index.html                preview: each variant on white and simulated Outlook dark
Run from anywhere: python3 wtr-dr/_mockup/sean/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE / "out"
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
BLUE = "#2E6DA6"                  # name, labels, website: 5.6:1 on white; Outlook dark -> #6DA2E0
BAR = "#3A80C0"                   # approved dark-mode C divider (borders are not recolored)
DARK_BG = "#1E1E1E"

PERSON = {
    "name": "Sean Myatt",
    "title": "Co-Owner/Operator",  # Michael, 2026-10-29; hardcoded until Ntiva fixes Entra
    "phone": "(813) 429-8737",
    "tel": "+18134298737",
    "email": "smyatt@wtrdr.com",
}
ADDRESSES = [("Operations", "21516 Carson Dr, Land O' Lakes, FL 34639"),   # Michael, 2026-11-09 (amends ADR 0019)
             ("Mailing", "8011 Land O' Lakes Blvd, Land O' Lakes, FL 34638")]

LOGO = REPO / "_mockup/dark-mode-c/out/wtrdr-logo.png"   # 200x200, wordmark #3A80C0
LOGO_W = LOGO_H = 100             # display size; file is 2x
GAP = 18                          # logo-to-bar = bar-to-text
PLEDGE_OUT = REPO / "purple_standard/pledge/out"
PLEDGES = {"pledge": ("tps-pledge-clear.png", PLEDGE_OUT / "tps-pledge-clear-flow.png"),          # badge left
           "pledge-text": ("tps-pledge-clear-text.png", PLEDGE_OUT / "tps-pledge-clear-text-flow.png")}   # no badge
CORNER_BADGE_PX = 75              # TPS badge top right, placed as in purple_standard/default.html
CORNER_BADGE = PLEDGE_OUT / "tps-badge-clear.png"

# Outlook dark recolors text: #2E6DA6 and #666666 sampled 2026-10-26 (dark-mode-c); #2A2A2A estimated.
OUTLOOK_TEXT_MAP = {BLUE: "#6DA2E0", "#2A2A2A": "#E6E6E6", "#666666": "#A2A2A2"}


def display_h(png):
    return int(subprocess.run(["magick", "identify", "-format", "%h", str(png)],
                              check=True, capture_output=True, text=True).stdout) // 2


def build_images():
    OUT.mkdir(exist_ok=True)
    print("step 1/3: images", flush=True)
    subprocess.run(["magick", str(LOGO), *DPI, str(OUT / "wtrdr-logo-clear.png")], check=True)


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; {style}"{v}>{inner}</p>'


def signature(footer, corner=False):
    cols = 4 if corner else 3
    img = lambda path: HOST + path
    # existing hosted WTR DR badges: white glyph on a #2E6DA6 disc (reads on white and dark)
    badge = lambda b, url, last=False: (
        f'<a href="{url}" target="_blank" style="text-decoration: none"><img src="{img(f"wtrdr/email-signature/badge-{b}.png")}" '
        f'border="0" alt="{b.title()}" width="24" height="24" style="width: 24px; height: 24px; display: inline-block'
        f'{"" if last else "; margin-right: 6px"}"></a>')
    line = "font-size: 10pt; line-height: 1.5; color: #2A2A2A"
    contact = "\n        ".join([
        p(f"font-size: 13pt; line-height: 1.15; color: {BLUE}", f"<b>{PERSON['name']}</b>", "Name"),
        p("margin: 2px 0 0 0; font-size: 10pt; color: #666666", PERSON["title"], "Job title"),
        p(f"margin: 8px 0 0 0; {line}", f'<b style="color: {BLUE}">P:</b> <a href="tel:{PERSON["tel"]}" style="color: #2A2A2A; text-decoration: none">{PERSON["phone"]}</a>', "Phone"),
        p(line, f'<b style="color: {BLUE}">E:</b> <a href="mailto:{PERSON["email"]}" style="color: #2A2A2A; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        *(p(line, f'<b style="color: {BLUE}">{k}:</b> {a.replace(", ", "<br>", 1)}', "Company address") for k, a in ADDRESSES),
        p(line, f'<a href="https://wtrdr.com/" target="_blank" style="color: {BLUE}; text-decoration: none"><b>www.wtrdr.com</b></a>', "Website"),
        p("margin: 8px 0 0 0; font-size: 0; line-height: 0",
          badge("google", "https://g.page/r/CXbaZrIdtlq-EBM/review")
          + badge("facebook", "https://www.facebook.com/profile.php?id=61574883176668")
          + badge("instagram", "https://www.instagram.com/wtrdr_", last=True), "Social links"),
    ])
    rows = f"""    <tr>
      <td width="{LOGO_W}" style="width: {LOGO_W}px; padding: 0; vertical-align: middle; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://wtrdr.com/" target="_blank"><img src="{img('wtrdr/email-signature/wtrdr-logo-clear.png')}" border="0" alt="WTR DR" width="{LOGO_W}" height="{LOGO_H}" style="width: {LOGO_W}px; height: {LOGO_H}px; display: block"></a>
      </td>
      <!-- fixed spacer = the same {GAP}px as the bar-to-text padding, so the bar sits centered in the gap -->
      <td width="{GAP}" style="width: {GAP}px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 0 0 0 {GAP}px; vertical-align: middle; border-left: 2px solid {BAR}">
        {contact}
      </td>""" + (f"""
      <!-- TPS badge, top right, as in the Purple Standard signature -->
      <td width="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; padding: 0; vertical-align: top; text-align: right; line-height: 0" data-codetwo-visible="TPS badge">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/tps-badge-clear.png')}" border="0" alt="Purple Standard" width="{CORNER_BADGE_PX}" height="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; height: {CORNER_BADGE_PX}px; display: inline-block"></a>
      </td>""" if corner else "") + """
    </tr>"""
    name, png = PLEDGES[footer]
    ph = display_h(png)
    rows += f"""
    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark (replaces the endorsement). Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="{cols}" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/' + name)}" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="480" height="{ph}" style="width: 480px; height: {ph}px; display: block"></a>
      </td>
    </tr>"""
    return f"""<!-- WTR DR - Sean Myatt. Person fields are HARDCODED (Entra lacks his title; see docs/entra-fixes.md). -->
<!-- Compact layout (ADR 0024), dark-mode option C (ADR 0020). Built by wtr-dr/_mockup/sean/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="wtrdr-signature" style="width: 480px; border-collapse: collapse; line-height: initial">
  <tbody>
{rows}
  </tbody>
</table>
"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = h.replace(HOST + "wtrdr/email-signature/wtrdr-logo-clear.png", "out/wtrdr-logo-clear.png")
    h = h.replace(HOST + "wtrdr/email-signature/", str(PS_ASSETS / "wtrdr/email-signature") + "/")
    for name, png in [*PLEDGES.values(), ("tps-badge-clear.png", CORNER_BADGE)]:
        h = h.replace(HOST + "standard/email-signature/" + name + '"', f'{png}"')
    return h


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


# same letters as Victor's Brisa versions, so the two operators can pick the same design
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
<title>WTR DR Sean signature</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px;width:480px}}</style>
<main><h1>WTR DR: Sean Myatt</h1>
<p>Real data, hardcoded. Title "Owner/Founder" confirmed by Michael.
Dark mode is simulated: Outlook recolors text but not images or borders. The blue and gray
mappings were sampled from Outlook; the near-black text mapping is an estimate.</p>
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
