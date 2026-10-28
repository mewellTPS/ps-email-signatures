#!/usr/bin/env python3
"""Tyrian Roofing signature for John Rodrigues: Brisa versions C and E (brisa/_mockup/victor) adapted.

Hardcoded person fields (Entra is missing his title and phone; see docs/entra-fixes.md).
Logo: Michael's stacked master assets/_src-logo-stacked.png (2026-10-28), no endorsement (the Purple
Standard Pledge replaces it). The wordmark #48104F would vanish in dark mode, so it is recolored to MID = #642164 (Michael, 2026-10-28; low contrast on dark by choice);
the shield keeps its brand colors. Social discs use MID too; the Pledge and TPS badge stay Neon Purple like the other operators.

Writes:
  out/                      2x / 96 DPI images (logo, badges)
  signature-<variant>.html  CodeTwo paste source, hosted URLs
  index.html                preview: each variant on white and simulated Outlook dark
Run from anywhere: python3 tyrian/_mockup/john/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TYRIAN = HERE.parents[1]
REPO = TYRIAN.parent
OUT = HERE / "out"
WORK = HERE / "_work"             # intermediates, overwritten each run
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
PURPLE = "#48104F"                # Tyrian purple, sampled from the logo master (= PS purple)
MID = "#642164"                   # shield left face, Michael's pick: 10.8:1 on white, ~1.5:1 on #1E1E1E (his call)
GOLD = "#E59519"                  # Tyrian gold divider (borders are not recolored; reads on both)
DARK_BG = "#1E1E1E"

PERSON = {
    "name": "John Rodrigues",
    "title": "Co-Owner/Founder",  # Michael, 2026-10-28; Entra has none
    "phone": "(813) 471-5201",
    "tel": "+18134715201",
    "email": "jrodrigues@tyrianroofing.com",
}
ADDRESS = "21516 Carson Dr, Land O' Lakes, FL 34639"   # ADR 0019 + 0021 spelling
SOCIAL = [("google", "https://share.google/wNanv1cHcJi2GktCp"),          # Michael, 2026-10-28
          ("instagram", "https://www.instagram.com/tyrianroofing")]      # Michael kept it; FB + YouTube dropped

LOGO_W = 105                      # display width, same column as Victor's; height follows the art
SHIELD_W = 150                    # file px (75 display)
STACK_GAP = 14                    # file px between shield and wordmark
WORD_TOP = 480                    # source row between the shield (ends 453) and the wordmark (starts 513)
GAP = 18                          # logo-to-bar = bar-to-text
PLEDGE_OUT = REPO / "purple_standard/pledge/out"
PLEDGES = {"pledge": ("tps-pledge-clear.png", PLEDGE_OUT / "tps-pledge-clear-flow.png"),          # badge left
           "pledge-text": ("tps-pledge-clear-text.png", PLEDGE_OUT / "tps-pledge-clear-text-flow.png")}   # no badge
# the Pledge and TPS badge stay Neon Purple, matching the other operators (Michael, 2026-10-28)
CORNER_BADGE_PX = 75              # TPS badge top right, placed as in purple_standard/default.html
CORNER_BADGE = PLEDGE_OUT / "tps-badge-clear.png"

# Outlook dark recolors text: #48104F -> #FFC1FF sampled (PS purple); the grays are estimates.
OUTLOOK_TEXT_MAP = {PURPLE: "#FFC1FF", "#2A2A2A": "#E6E6E6", "#6E6E6E": "#A8A8A8"}


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def size(png):
    w, h = subprocess.run(["magick", "identify", "-format", "%w %h", str(png)],
                          check=True, capture_output=True, text=True).stdout.split()
    return int(w), int(h)


def rgb(hx):
    return [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def build_images():
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    print("step 1/3: images", flush=True)
    # Michael's stacked master (transparent, 1010x885) re-proportioned: shield and wordmark cut apart
    # at WORD_TOP and trimmed, shield at SHIELD_W, wordmark at the full column width (its two lines
    # stay centered as in the master), stacked centered with STACK_GAP between them
    src = TYRIAN / "assets/_src-logo-stacked.png"
    sw, sh = size(src)
    w = LOGO_W * 2
    magick(src, "-crop", f"{sw}x{WORD_TOP}+0+0", "+repage", "-trim", "+repage",
           "-resize", f"{SHIELD_W}x", WORK / "shield.png")
    magick(src, "-crop", f"{sw}x{sh - WORD_TOP}+0+{WORD_TOP}", "+repage", "-trim", "+repage",
           "-resize", f"{w}x", "-fill", MID, "-colorize", "100", WORK / "word.png")
    shw, shh = size(WORK / "shield.png")
    _, wh = size(WORK / "word.png")
    h = shh + STACK_GAP + wh
    h += h % 2                    # even, so display = file / 2 exactly
    magick("-size", f"{w}x{h}", "xc:none",
           WORK / "shield.png", "-geometry", f"+{(w - shw) // 2}+0", "-composite",
           WORK / "word.png", "-geometry", f"+0+{shh + STACK_GAP}", "-composite",
           *DPI, OUT / "tyrian-logo-stacked.png")
    # badges: white glyph on a dark disc -> MID disc; t = how far toward white (0 disc, 1 glyph)
    srcs = {"google": (PS_ASSETS / "wtrdr/email-signature/badge-google.png", "u.r", 46 / 255),     # #2E6DA6 disc
            "instagram": (TYRIAN / "assets/badge-instagram.png", "u.g", 23 / 255)}              # #531757 disc
    for name, (src, ch, lo) in srcs.items():
        # t as one gray mask first: per-channel -fx steps would read channels already rewritten
        magick(src, "-alpha", "off", "-fx", f"clamp(({ch}-{lo})/(1-{lo}))", "-colorspace", "Gray", WORK / f"{name}-t.png")
        magick(src, "-alpha", "extract", WORK / f"{name}-a.png")
        w, h = size(src)
        magick("-size", f"{w}x{h}", f"xc:{MID}", "xc:white", WORK / f"{name}-t.png", "-composite",
               WORK / f"{name}-a.png", "-alpha", "off", "-compose", "CopyOpacity", "-composite",
               *DPI, OUT / f"badge-{name}-mid.png")


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; {style}"{v}>{inner}</p>'


def signature(footer, corner=False):
    cols = 4 if corner else 3
    img = lambda path: HOST + path
    lw, lh = (x // 2 for x in size(OUT / "tyrian-logo-stacked.png"))
    badge = lambda b, url, last=False: (
        f'<a href="{url}" target="_blank" style="text-decoration: none"><img src="{img(f"tyrian/email-signature/badge-{b}-mid.png")}" '
        f'border="0" alt="{b.title()}" width="24" height="24" style="width: 24px; height: 24px; display: inline-block'
        f'{"" if last else "; margin-right: 6px"}"></a>')
    line = "font-size: 10pt; line-height: 1.5; color: #2A2A2A"
    contact = "\n        ".join([
        p(f"font-size: 13pt; line-height: 1.15; color: {PURPLE}", f"<b>{PERSON['name']}</b>", "Name"),
        p("margin: 2px 0 0 0; font-size: 10pt; color: #6E6E6E", PERSON["title"], "Job title"),
        p(f"margin: 8px 0 0 0; {line}", f'<b style="color: {PURPLE}">P:</b> <a href="tel:{PERSON["tel"]}" style="color: #2A2A2A; text-decoration: none">{PERSON["phone"]}</a>', "Phone"),
        p(line, f'<b style="color: {PURPLE}">E:</b> <a href="mailto:{PERSON["email"]}" style="color: #2A2A2A; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        p(line, ADDRESS, "Company address"),
        p(line, f'<a href="https://tyrianroofing.com/" target="_blank" style="color: {PURPLE}; text-decoration: none"><b>www.tyrianroofing.com</b></a>', "Website"),
        p("margin: 8px 0 0 0; font-size: 0; line-height: 0",
          "".join(badge(b, u, i == len(SOCIAL) - 1) for i, (b, u) in enumerate(SOCIAL)), "Social links"),
    ])
    rows = f"""    <tr>
      <td width="{lw}" style="width: {lw}px; padding: 0; vertical-align: middle; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://tyrianroofing.com/" target="_blank"><img src="{img('tyrian/email-signature/tyrian-logo-stacked.png')}" border="0" alt="Tyrian Roofing" width="{lw}" height="{lh}" style="width: {lw}px; height: {lh}px; display: block"></a>
      </td>
      <!-- fixed spacer = the same {GAP}px as the bar-to-text padding, so the bar sits centered in the gap -->
      <td width="{GAP}" style="width: {GAP}px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 0 0 0 {GAP}px; vertical-align: middle; border-left: 2px solid {GOLD}">
        {contact}
      </td>""" + (f"""
      <!-- TPS badge, top right, as in the Purple Standard signature -->
      <td width="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; padding: 0; vertical-align: top; text-align: right; line-height: 0" data-codetwo-visible="TPS badge">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/tps-badge-clear.png')}" border="0" alt="Purple Standard" width="{CORNER_BADGE_PX}" height="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; height: {CORNER_BADGE_PX}px; display: inline-block"></a>
      </td>""" if corner else "") + """
    </tr>"""
    name, png = PLEDGES[footer]
    ph = size(png)[1] // 2
    rows += f"""
    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark (replaces the endorsement). Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="{cols}" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/' + name)}" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="480" height="{ph}" style="width: 480px; height: {ph}px; display: block"></a>
      </td>
    </tr>"""
    return f"""<!-- Tyrian Roofing - John Rodrigues. Person fields are HARDCODED (Entra lacks title and phone; see docs/entra-fixes.md). -->
<!-- Compact layout (ADR 0024), dark-mode option C (ADR 0020). Built by tyrian/_mockup/john/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="tyrian-signature" style="width: 480px; border-collapse: collapse; line-height: initial">
  <tbody>
{rows}
  </tbody>
</table>
"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = h.replace(HOST + "tyrian/email-signature/", "out/")
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
<title>Tyrian John signature</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px;width:480px}}</style>
<main><h1>Tyrian Roofing: John Rodrigues</h1>
<p>Real data, hardcoded. Dark mode is simulated: Outlook recolors text but not images or borders.
The purple mapping was sampled from Outlook; the gray mappings are estimates.</p>
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
