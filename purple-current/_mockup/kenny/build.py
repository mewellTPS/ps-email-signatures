#!/usr/bin/env python3
"""Purple Current signature for Kenny Morrow: Brisa versions C and E, plus his current layout.

Hardcoded person fields (Entra lacks his full name and title; see docs/entra-fixes.md).
"Current" keeps his layout (name, title, logo | contact, rule, endorsement + social, banner), adds
name and title, and swaps the dark art for dark-mode-safe versions (Michael, 2026-10-28).
Dark-mode option C (ADR 0020): Outlook recolors text, not images or borders, so the purple
wordmark, social discs, endorsement and rule use the mid-tone ART. The icon keeps its colors.

Writes:
  out/                      2x / 96 DPI images (logos, badges, endorsement)
  signature-<variant>.html  CodeTwo paste source, hosted URLs
  index.html                preview: each variant on white and simulated Outlook dark, 
Run from anywhere: python3 purple-current/_mockup/kenny/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PC = HERE.parents[1]
REPO = PC.parent
OUT = HERE / "out"
WORK = HERE / "_work"             # intermediates, overwritten each run
PS_ASSETS = Path.home() / "Developer/purple-standard/websites/ps-assets"
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
PURPLE = "#48104F"                # text: Outlook dark -> #FFC1FF (sampled); PC's #411144 is visually the same
ART = "#A861B3"                   # PC purple lifted, lower saturation: 4.18:1 on white, 3.99:1 on #1E1E1E (Michael picked 2026-10-28)
DARK_BG = "#1E1E1E"

PERSON = {
    "name": "Kenny Morrow",       # Michael, 2026-10-28; live signature shows "K. Morrow"
    "title": "Operator",          # Michael, 2026-10-29; hardcoded until Ntiva fixes Entra
    "phone": "(813) 355-0865",
    "tel": "+18133550865",
    "email": "kmorrow@purple-current.com",
}
ADDRESS = ("21516 Carson Dr", "Land O' Lakes, FL 34639")   # ADR 0019 + 0021
SOCIAL = [("google", "https://share.google/SFB2Gbv8p9uJoWxwg"),
          ("facebook", "https://www.facebook.com/people/Purple-Current/61573255989927/"),
          ("instagram", "https://www.instagram.com/purplecurrent"),
          ("linkedin", "https://www.linkedin.com/company/purple-current/"),
          ("youtube", "https://www.youtube.com/@Purple-Current"),
          ("yelp", "https://www.yelp.com/biz/6WdDdQEcSfEJGduyyheRMw")]

SRC = PC / "assets/pc-logo-primary-color.png"   # 1136x493: icon cols 18-376, wordmark cols 469-1115
ICON_END, WORD_START = 420, 469
LINES = ((158, 262), (297, 401))  # PURPLE, CURRENT rows in the wordmark
LOGO_W = 105                      # stacked: display width, same column as Victor's
ICON_W = 150                      # file px (75 display)
STACK_GAP = 16                    # file px between icon and wordmark
LINE_GAP = 30                     # source px between the two wordmark lines
WIDE_W = 200                      # current layout: horizontal logo display width (as today)
GAP = 18
PLEDGE_OUT = REPO / "purple_standard/pledge/out"
PLEDGES = {"pledge": ("tps-pledge-clear.png", PLEDGE_OUT / "tps-pledge-clear-flow.png"),
           "pledge-text": ("tps-pledge-clear-text.png", PLEDGE_OUT / "tps-pledge-clear-text-flow.png")}
CORNER_BADGE_PX = 75
CORNER_BADGE = PLEDGE_OUT / "tps-badge-clear.png"

OUTLOOK_TEXT_MAP = {PURPLE: "#FFC1FF", "#333333": "#E0E0E0", "#6E6E6E": "#A8A8A8"}   # grays estimated


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def size(png):
    w, h = subprocess.run(["magick", "identify", "-format", "%w %h", str(png)],
                          check=True, capture_output=True, text=True).stdout.split()
    return int(w), int(h)


def even_canvas(src, w, dst):
    """Pad to width w and an even height, so display = file / 2 exactly."""
    _, h = size(src)
    magick(src, "-background", "none", "-gravity", "center", "-extent", f"{w}x{h + h % 2}", *DPI, dst)


def stacked_logo(tone, dst):
    sw, sh = size(SRC)
    magick(SRC, "-crop", f"{ICON_END}x{sh}+0+0", "+repage", "-trim", "+repage", "-resize", f"{ICON_W}x", WORK / "icon.png")
    for i, (top, bot) in enumerate(LINES):
        magick(SRC, "-crop", f"{sw - WORD_START}x{bot - top}+{WORD_START}+{top}", "+repage", "-trim", "+repage",
               WORK / f"line{i}.png")
    # the two lines centered on each other (the master left-aligns them)
    magick(WORK / "line0.png", "-size", f"1x{LINE_GAP}", "xc:none", WORK / "line1.png",
           "-background", "none", "-gravity", "center", "-append",
           "-resize", f"{LOGO_W * 2}x", "-fill", tone, "-colorize", "100", WORK / "word.png")
    iw, ih = size(WORK / "icon.png")
    ww, wh = size(WORK / "word.png")
    magick("-size", f"{LOGO_W * 2}x{ih + STACK_GAP + wh}", "xc:none",
           WORK / "icon.png", "-geometry", f"+{(LOGO_W * 2 - iw) // 2}+0", "-composite",
           WORK / "word.png", "-geometry", f"+{(LOGO_W * 2 - ww) // 2}+{ih + STACK_GAP}", "-composite",
           WORK / "stacked.png")
    even_canvas(WORK / "stacked.png", LOGO_W * 2, dst)


def build_images():
    OUT.mkdir(exist_ok=True)
    WORK.mkdir(exist_ok=True)
    print("step 1/3: images", flush=True)
    stacked_logo(ART, OUT / "pc-logo-stacked.png")
    # horizontal logo for the current layout: icon as is, wordmark -> ART
    sw, sh = size(SRC)
    magick(SRC, "-crop", f"{ICON_END}x{sh}+0+0", "+repage", WORK / "h-icon.png")
    magick(SRC, "-crop", f"{sw - ICON_END}x{sh}+{ICON_END}+0", "+repage", "-fill", ART, "-colorize", "100", WORK / "h-word.png")
    magick(WORK / "h-icon.png", WORK / "h-word.png", "-background", "none", "+append", "-trim", "+repage",
           "-resize", f"{WIDE_W * 2}x", WORK / "wide.png")
    even_canvas(WORK / "wide.png", WIDE_W * 2, OUT / "pc-logo-wide.png")
    # social badges: white FA 6.5.2 glyph at 50% on an ART disc (house recipe from the PC README), 48px file
    for b, _ in SOCIAL:
        magick("-size", "48x48", "xc:none", "-fill", ART, "-draw", "circle 23.5,23.5 23.5,-0.5", WORK / "disc.png")
        magick("-background", "none", "-density", "1200", PC / f"assets/_src-{b}.svg", "-resize", "24x24",
               "-fill", "white", "-colorize", "100", WORK / "glyph.png")
        magick(WORK / "disc.png", WORK / "glyph.png", "-gravity", "center", "-compose", "Over", "-composite",
               *DPI, OUT / f"badge-{b}-mid.png")
    # endorsement: one-color art on transparency (the tick is a cut-out), so a straight recolor
    magick(PC / "assets/endorsement.png", "-fill", ART, "-colorize", "100", *DPI, OUT / "endorsement-mid.png")


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; {style}"{v}>{inner}</p>'


def img(path):
    return HOST + path


def badges(px, gap, side="right"):
    return "".join(
        f'<a href="{u}" target="_blank" style="text-decoration: none"><img src="{img(f"current/email-signature/badge-{b}-mid.png")}" '
        f'border="0" alt="{b.title() if b != "linkedin" else "LinkedIn"}" width="{px}" height="{px}" style="width: {px}px; height: {px}px; display: inline-block'
        + (f'; margin-{side}: {gap}px' if (side == "left" or i < len(SOCIAL) - 1) else "") + '"></a>'
        for i, (b, u) in enumerate(SOCIAL))


def compact(footer, corner=False):
    """Brisa versions C / E (brisa/_mockup/victor), adapted."""
    cols = 4 if corner else 3
    lw, lh = (x // 2 for x in size(OUT / "pc-logo-stacked.png"))
    line = "font-size: 10pt; line-height: 1.5; color: #333333"
    contact = "\n        ".join([
        p(f"font-size: 13pt; line-height: 1.15; color: {PURPLE}", f"<b>{PERSON['name']}</b>", "Name"),
        p("margin: 2px 0 0 0; font-size: 10pt; color: #6E6E6E", PERSON["title"], "Job title"),
        p(f"margin: 8px 0 0 0; {line}", f'<b style="color: {PURPLE}">P:</b> <a href="tel:{PERSON["tel"]}" style="color: #333333; text-decoration: none">{PERSON["phone"]}</a>', "Phone"),
        p(line, f'<b style="color: {PURPLE}">E:</b> <a href="mailto:{PERSON["email"]}" style="color: #333333; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        p(line, ", ".join(ADDRESS), "Company address"),
        p(line, f'<a href="https://purple-current.com/" target="_blank" style="color: {PURPLE}; text-decoration: none"><b>www.purple-current.com</b></a>', "Website"),
        p("margin: 8px 0 0 0; font-size: 0; line-height: 0", badges(24, 6), "Social links"),
    ])
    corner_td = f"""
      <!-- TPS badge, top right, as in the Purple Standard signature -->
      <td width="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; padding: 0; vertical-align: top; text-align: right; line-height: 0" data-codetwo-visible="TPS badge">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/tps-badge-clear.png')}" border="0" alt="Purple Standard" width="{CORNER_BADGE_PX}" height="{CORNER_BADGE_PX}" style="width: {CORNER_BADGE_PX}px; height: {CORNER_BADGE_PX}px; display: inline-block"></a>
      </td>""" if corner else ""
    name, png = PLEDGES[footer]
    ph = size(png)[1] // 2
    return f"""<!-- Purple Current - Kenny Morrow. Person fields are HARDCODED (Entra lacks name and title; see docs/entra-fixes.md). -->
<!-- Compact layout (ADR 0024), dark-mode option C (ADR 0020). Built by purple-current/_mockup/kenny/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="purple-current-signature" style="width: 480px; border-collapse: collapse; line-height: initial">
  <tbody>
    <tr>
      <td width="{lw}" style="width: {lw}px; padding: 0; vertical-align: middle; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://purple-current.com/" target="_blank"><img src="{img('current/email-signature/pc-logo-stacked.png')}" border="0" alt="Purple Current" width="{lw}" height="{lh}" style="width: {lw}px; height: {lh}px; display: block"></a>
      </td>
      <!-- fixed spacer = the same {GAP}px as the bar-to-text padding, so the bar sits centered in the gap -->
      <td width="{GAP}" style="width: {GAP}px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 0 0 0 {GAP}px; vertical-align: middle; border-left: 2px solid {ART}">
        {contact}
      </td>{corner_td}
    </tr>
    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark (replaces the endorsement). Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="{cols}" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{img('standard/email-signature/' + name)}" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="480" height="{ph}" style="width: 480px; height: {ph}px; display: block"></a>
      </td>
    </tr>
  </tbody>
</table>
"""


def current():
    """His current layout (purple-current/default.html) with name and title, dark-mode-safe art."""
    lw, lh = (x // 2 for x in size(OUT / "pc-logo-wide.png"))
    cell = "font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt"
    row = lambda label, value, visible, last=False: f"""            <tr data-codetwo-visible="{visible}">
              <td style="padding: 0 6px {0 if last else 6}px 0; vertical-align: top; {cell}; color: {PURPLE}"><b>{label}:</b></td>
              <td style="padding: 0 0 {0 if last else 6}px 0; vertical-align: top; {cell}; color: #333333">{value}</td>
            </tr>"""
    return f"""<!-- Purple Current - Kenny Morrow, current layout. Person fields are HARDCODED (Entra lacks name and title; see docs/entra-fixes.md). -->
<!-- Dark-mode option C (ADR 0020). Built by purple-current/_mockup/kenny/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="purple-current-signature" style="width: 560px; border-collapse: collapse; line-height: initial">
  <tbody>
    <tr>
      <td colspan="3" style="padding: 0 0 2px 0; vertical-align: top">
        {p(f"font-size: 18pt; color: {PURPLE}", f"<b>{PERSON['name']}</b>", "Name")}
      </td>
    </tr>
    <tr>
      <td colspan="3" style="padding: 0 0 14px 0; vertical-align: top">
        {p(f"font-size: 10.5pt; color: {PURPLE}", PERSON["title"], "Job title")}
      </td>
    </tr>
    <tr>
      <td width="{lw}" style="width: {lw}px; padding: 0; vertical-align: top; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://purple-current.com/" target="_blank"><img src="{img('current/email-signature/pc-logo-wide.png')}" border="0" alt="Purple Current" width="{lw}" height="{lh}" style="width: {lw}px; height: {lh}px; display: block"></a>
      </td>
      <td width="30" style="width: 30px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 2px 0 0 0; vertical-align: top">
        <table cellspacing="0" cellpadding="0" style="border-collapse: collapse; line-height: initial">
          <tbody>
{row("P", f'<a href="tel:{PERSON["tel"]}" style="color: #333333; text-decoration: none">{PERSON["phone"]}</a>', "Phone")}
{row("A", ",<br>".join(ADDRESS), "Company address")}
{row("E", f'<a href="mailto:{PERSON["email"]}" style="color: #333333; text-decoration: none">{PERSON["email"]}</a>', "Email", last=True)}
          </tbody>
        </table>
      </td>
    </tr>
    <!-- Divider rule: mid-tone, because Outlook dark does not recolor borders -->
    <tr>
      <td colspan="3" style="padding: 16px 0 0 0; border-top: 1px solid {ART}; font-size: 0; line-height: 0">&nbsp;</td>
    </tr>
    <tr>
      <td colspan="3" style="padding: 0 0 16px 0; vertical-align: middle">
        <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse; line-height: initial">
          <tbody>
            <tr>
              <td style="padding: 0; vertical-align: middle; text-align: left; line-height: 0" data-codetwo-visible="Endorsement">
                <a href="https://www.purple-standard.com/" target="_blank"><img src="{img('current/email-signature/endorsement-mid.png')}" border="0" alt="Powered by The Purple Standard" width="360" height="17" style="width: 360px; height: 17px; display: block"></a>
              </td>
              <td style="padding: 0; vertical-align: middle; text-align: right; font-size: 0; line-height: 0" data-codetwo-visible="Social links">
                {badges(18, 9, side="left")}
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="3" style="padding: 0; vertical-align: top; line-height: 0" data-codetwo-visible="Banner">
        <a href="https://purple-current.com/" target="_blank"><img src="{img('current/email-signature/banner-standard.jpg')}" border="0" alt="Purple up. Power on. Speak with an expert." width="560" height="169" style="width: 560px; height: 169px; display: block"></a>
      </td>
    </tr>
  </tbody>
</table>
"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    for f in ("pc-logo-stacked.png", "pc-logo-wide.png", "endorsement-mid.png", *(f"badge-{b}-mid.png" for b, _ in SOCIAL)):
        h = h.replace(HOST + "current/email-signature/" + f, "out/" + f)
    h = h.replace(HOST + "current/email-signature/", str(PS_ASSETS / "current/email-signature") + "/")
    for name, png in [*PLEDGES.values(), ("tps-badge-clear.png", CORNER_BADGE)]:
        h = h.replace(HOST + "standard/email-signature/" + name + '"', f'{png}"')
    return h


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


# same letters as Victor's Brisa versions, so operators can pick the same design
VARIANTS = [("c", "C · Pledge, badge left", lambda: compact("pledge")),
            ("e", "E · Pledge text, TPS badge top right", lambda: compact("pledge-text", True)),
            ("current", "Current layout + name and title", current)]


def page():
    cols = []
    for key, label, make in VARIANTS:
        html = make()
        (HERE / f"signature-{key}.html").write_text(html)
        lo = local(html)
        cols.append(f"""<div class="col"><h2>{label}</h2>
<h3>Light mode</h3><div class="mail" style="background:#fff">{lo}</div>
<h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{outlook_dark(lo)}</div></div>""")
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>Purple Current Kenny signature</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px}}
.tones{{display:flex;gap:24px;flex-wrap:wrap}}.pair{{display:flex;margin-top:6px;border:1px solid #ccc}}img{{display:block}}</style>
<main><h1>Purple Current: Kenny Morrow</h1>
<p>Real data, hardcoded. Dark mode is simulated: Outlook recolors text but not images or borders.
The purple text mapping was sampled from Outlook; the gray mappings are estimates.
Art (wordmark, badges, endorsement, divider) uses {ART}.</p>
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
