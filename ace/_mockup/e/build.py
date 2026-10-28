#!/usr/bin/env python3
"""ACE Septic & Waste signature, version E: option D (brand stripe) overhauled into the E layout.

ACE is kept separate from Purple Standard branding (Michael, 2026-10-28): no Pledge, no TPS
badge, no endorsement. Layout as the other operators' E: stacked logo | divider | contact, 480px.
D's four-colour stripe stays as the signature's signature element, now an image (Outlook dark
mode can recolor table backgrounds) and with navy lifted so it shows on dark.
ACE keeps its own address, 8005 Land O' Lakes Blvd (ADR 0019).

PERSON is PLACEHOLDER sample data until Michael sends the ACE people list (one rule per
person: shared-mailbox issue). Nothing here ships with it.

Writes:
  out/                      2x / 96 DPI images (stacked logo, stripe, badges)
  signature-e.html          CodeTwo paste source, hosted URLs (no PS branding)
  signature-e-v2.html       the same with the Pledge + TPS badge underneath, as Boyette
  index.html                preview on white and simulated Outlook dark
Run from anywhere: python3 ace/_mockup/e/build.py
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACE = HERE.parents[1]
REPO = ACE.parent
OUT = HERE / "out"
WORK = HERE / "_work"             # intermediates, overwritten each run
DPI = ["-units", "PixelsPerInch", "-density", "96", "-define", "png:color-type=6"]   # ADR 0008

HOST = "https://assets.purple-standard.app/"
BLUE, GREEN, ORANGE, NAVY = "#3C81F5", "#0BA94B", "#F16522", "#335E89"   # ACE logo colors
NAVY_MID = "#4D7FB5"              # navy lifted for art on transparency: 4.18:1 on white, 3.98:1 on #1E1E1E
INK = "#111111"                   # name
TEXT = "#333333"                  # contact lines
LINK_GREEN = "#08803A"            # website text: ACE green darkened to 5.2:1 on white
DARK_BG = "#1E1E1E"

PERSON = {                        # PLACEHOLDER: replace per person
    "name": "First Last",
    "title": "Job Title",
    "office": "(813) 555-0100",
    "office_tel": "+18135550100",
    "mobile": "(813) 555-0101",
    "mobile_tel": "+18135550101",
    "email": "name@acesepticandwaste.com",
}
ADDRESS = ("8005 Land O' Lakes Blvd", "Land O' Lakes, FL 34638")   # ACE keeps 8005 (ADR 0019); two lines: one is 305px
SOCIAL = [("facebook", "https://www.facebook.com/acesepticandwaste"),
          ("google", "https://g.page/r/CR6AtyBWpp0-EBM/review"),
          ("instagram", "https://www.instagram.com/aceseptic/"),
          ("linkedin", "https://www.linkedin.com/company/ace-septic-and-waste/")]
GLYPHS = REPO / "purple-current/assets"   # Font Awesome 6.5.2 sources (_src-<name>.svg), same house badge

SRC = ACE / "assets/_src-logo-stacked.png"   # Michael's stacked master, 3000x3000, transparent
WORD_TOP = 2130                   # between the disc (ends row 2053) and the wordmark (starts row 2211)
AMP = (1625, 2500, 200, 215)      # the navy "&" (x, y, w, h)
LOGO_W = 180                      # display width: the widest that keeps every contact line on one line
DISC_W = 220                      # file px (110 display)
STACK_GAP = 14                    # file px, disc to wordmark
GAP = 18
WIDTH = 480
STRIPE_H = 4
PLEDGE = REPO / "purple_standard/pledge/out/tps-pledge-clear-flow.png"   # badge left, Neon Purple

# Outlook dark recolors text. #000000 -> #FFFFFF and #2E6DA6 -> #6DA2E0 were sampled; the rest estimated.
OUTLOOK_TEXT_MAP = {INK: "#F2F2F2", TEXT: "#E0E0E0", NAVY: "#8FB4DD", LINK_GREEN: "#4CC97F"}


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
    # Michael's stacked master: "&" navy -> NAVY_MID (it goes dark in dark mode); everything else as is
    x, y, w, h = AMP
    magick(SRC, "-crop", f"{w}x{h}+{x}+{y}", "+repage", "-fill", NAVY_MID, "-colorize", "100", WORK / "amp.png")
    magick(SRC, "(", "-size", f"{w}x{h}", "xc:black", ")", "-geometry", f"+{x}+{y}",   # -region mangles alpha
           "-compose", "DstOut", "-composite", WORK / "noamp.png")
    magick(WORK / "noamp.png", WORK / "amp.png", "-geometry", f"+{x}+{y}", "-compose", "Over", "-composite", WORK / "logo.png")
    # re-proportioned like Tyrian: disc and wordmark cut apart at WORD_TOP and trimmed, disc at DISC_W,
    # wordmark at the full column width, stacked centered with STACK_GAP
    sw, sh = size(SRC)
    magick(WORK / "logo.png", "-crop", f"{sw}x{WORD_TOP}+0+0", "+repage", "-trim", "+repage",
           "-resize", f"{DISC_W}x", WORK / "disc.png")
    magick(WORK / "logo.png", "-crop", f"{sw}x{sh - WORD_TOP}+0+{WORD_TOP}", "+repage", "-trim", "+repage",
           "-resize", f"{LOGO_W * 2}x", WORK / "word.png")
    iw, ih = size(WORK / "disc.png")
    ww, wh = size(WORK / "word.png")
    h = ih + STACK_GAP + wh
    h += h % 2                    # even, so display = file / 2 exactly
    magick("-size", f"{LOGO_W * 2}x{h}", "xc:none",
           WORK / "disc.png", "-geometry", f"+{(LOGO_W * 2 - iw) // 2}+0", "-composite",
           WORK / "word.png", "-geometry", f"+{(LOGO_W * 2 - ww) // 2}+{ih + STACK_GAP}", "-composite",
           *DPI, OUT / "ace-logo-stacked.png")
    # stripe: four equal bands, navy lifted
    q = WIDTH * 2 // 4
    magick(*[a for c in (BLUE, GREEN, ORANGE, NAVY_MID) for a in ("-size", f"{q}x{STRIPE_H * 2}", f"xc:{c}")],
           "+append", *DPI, OUT / "ace-stripe.png")
    # badges: white FA glyph at 50% on an ACE-blue disc (Sailfish navy disappears on dark), 48px file
    for b, _ in SOCIAL:
        magick("-size", "48x48", "xc:none", "-fill", BLUE, "-draw", "circle 23.5,23.5 23.5,-0.5", WORK / "badge-disc.png")
        magick("-background", "none", "-density", "1200", GLYPHS / f"_src-{b}.svg", "-resize", "24x24",
               "-fill", "white", "-colorize", "100", WORK / "glyph.png")
        magick(WORK / "badge-disc.png", WORK / "glyph.png", "-gravity", "center", "-compose", "Over", "-composite",
               *DPI, OUT / f"badge-{b}-blue.png")


def p(style, inner, visible=None):
    v = f' data-codetwo-visible="{visible}"' if visible else ""
    return f'<p style="margin: 0; font-family: Arial, Helvetica, sans-serif; {style}"{v}>{inner}</p>'


def signature(pledge=False):
    lw, lh = (x // 2 for x in size(OUT / "ace-logo-stacked.png"))
    img = lambda f: f"{HOST}ace/email-signature/{f}"
    line = f"font-size: 10pt; line-height: 1.5; color: {TEXT}"
    tel = lambda label, num, t: f'<b style="color: {NAVY}">{label}:</b> <a href="tel:{t}" style="color: {TEXT}; text-decoration: none">{num}</a>'
    contact = "\n        ".join([
        p(f"font-size: 13pt; line-height: 1.15; color: {INK}", f"<b>{PERSON['name']}</b>", "Name"),
        p(f"margin: 2px 0 0 0; font-size: 10pt; color: {NAVY}", PERSON["title"], "Job title"),
        p(f"margin: 8px 0 0 0; {line}", tel("O", PERSON["office"], PERSON["office_tel"])
          + "&nbsp;&nbsp;&nbsp;" + tel("M", PERSON["mobile"], PERSON["mobile_tel"]), "Phone"),
        p(line, f'<b style="color: {NAVY}">E:</b> <a href="mailto:{PERSON["email"]}" style="color: {TEXT}; text-decoration: none">{PERSON["email"]}</a>', "Email"),
        *(p(line, a, "Company address") for a in ADDRESS),
        p(line, f'<a href="https://acesepticandwaste.com" target="_blank" style="color: {LINK_GREEN}; text-decoration: none"><b>acesepticandwaste.com</b></a>', "Website"),
        p("margin: 8px 0 0 0; font-size: 0; line-height: 0", "".join(
            f'<a href="{u}" target="_blank" style="text-decoration: none"><img src="{img(f"badge-{b}-blue.png")}" border="0" '
            f'alt="{ {"linkedin": "LinkedIn", "google": "Google reviews"}.get(b, b.title()) }" width="24" height="24" style="width: 24px; height: 24px; display: inline-block'
            f'{"" if i == len(SOCIAL) - 1 else "; margin-right: 6px"}"></a>' for i, (b, u) in enumerate(SOCIAL)), "Social links"),
    ])
    return f"""<!-- ACE Septic & Waste - version E (option D overhauled). No Purple Standard branding: ACE is kept separate. -->
<!-- Person fields are HARDCODED per person (shared-mailbox issue). Built by ace/_mockup/e/build.py - edit the script, not this file. -->
<table cellspacing="0" cellpadding="0" id="ace-signature" style="width: {WIDTH}px; border-collapse: collapse; line-height: initial">
  <tbody>
    <tr>
      <td colspan="3" style="padding: 0 0 16px 0; line-height: 0" data-codetwo-visible="Brand stripe">
        <img src="{img('ace-stripe.png')}" border="0" alt="" width="{WIDTH}" height="{STRIPE_H}" style="width: {WIDTH}px; height: {STRIPE_H}px; display: block">
      </td>
    </tr>
    <tr>
      <td width="{lw}" style="width: {lw}px; padding: 0; vertical-align: middle; line-height: 0" data-codetwo-visible="Logo">
        <a href="https://acesepticandwaste.com" target="_blank"><img src="{img('ace-logo-stacked.png')}" border="0" alt="ACE Septic &amp; Waste" width="{lw}" height="{lh}" style="width: {lw}px; height: {lh}px; display: block"></a>
      </td>
      <!-- fixed spacer = the same {GAP}px as the bar-to-text padding, so the bar sits centered in the gap -->
      <td width="{GAP}" style="width: {GAP}px; padding: 0; font-size: 0; line-height: 0">&nbsp;</td>
      <td style="padding: 0 0 0 {GAP}px; vertical-align: middle; border-left: 2px solid {GREEN}">
        {contact}
      </td>
    </tr>{pledge_row() if pledge else ""}
  </tbody>
</table>
"""


def pledge_row():
    """v2: the Purple Standard Pledge with the TPS badge at its left, as in Boyette's C (Michael, 2026-10-28)."""
    ph = size(PLEDGE)[1] // 2
    return f"""
    <!-- The Purple Standard Pledge, transparent, mid-tone for light and dark. Built by purple_standard/pledge/build.py. -->
    <tr data-codetwo-visible="Pledge">
      <td colspan="3" style="padding: 14px 0 0 0; vertical-align: top; line-height: 0">
        <a href="https://www.purple-standard.com" target="_blank"><img src="{HOST}standard/email-signature/tps-pledge-clear.png" border="0" alt="The Purple Standard Pledge: Clear communication. Technology and solutions driven. Professionalism in action. Exceeding expectations." width="{WIDTH}" height="{ph}" style="width: {WIDTH}px; height: {ph}px; display: block"></a>
      </td>
    </tr>"""


def local(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S).replace(HOST + "ace/email-signature/", "out/")
    return h.replace(HOST + "standard/email-signature/tps-pledge-clear.png", str(PLEDGE))


def outlook_dark(h):
    for src, dst in OUTLOOK_TEXT_MAP.items():
        h = re.sub(rf"(?<![-\w])color: ?{src}", f"color: {dst}", h, flags=re.I)
    return h


VARIANTS = [("e", "E · No Purple Standard branding", False),
            ("e-v2", "E v2 · Pledge with TPS badge underneath (as Boyette)", True)]


def page():
    cols = []
    for key, label, pledge in VARIANTS:
        html = signature(pledge)
        (HERE / f"signature-{key}.html").write_text(html)
        lo = local(html)
        cols.append(f"""<div><h2>{label}</h2>
<h3>Light mode</h3><div class="mail" style="background:#fff">{lo}</div>
<h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{outlook_dark(lo)}</div></div>""")
    (HERE / "index.html").write_text(f"""<!doctype html><meta charset="utf-8">
<title>ACE signature E</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:8px 24px 40px}}h1{{font-size:20px}}h2{{font-size:18px;margin:20px 0 0}}h3{{font-size:15px;margin:16px 0 8px}}
.grid{{display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start}}
.mail{{padding:28px;border:1px solid #ccc;border-radius:6px;width:{WIDTH}px}}.ph{{color:#a14a00}}</style>
<main><h1>ACE Septic &amp; Waste: version E and v2</h1>
<p class="ph"><b>Placeholder person</b> (name, title, phones, email) until the ACE people list arrives.
Address, website and social links are real.</p>
<p>Dark mode is simulated: Outlook recolors text but not images or borders. Black-to-white was
sampled from Outlook; the navy, gray and green text mappings are estimates.</p>
<div class="grid">{''.join(cols)}</div></main>
""")


def main():
    build_images()
    print("step 2/3: signature", flush=True)
    page()
    print("step 3/3: done", flush=True)
    print("RESULT: ok", HERE / "index.html")


if __name__ == "__main__":
    main()
