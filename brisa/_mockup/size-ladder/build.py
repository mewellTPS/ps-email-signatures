#!/usr/bin/env python3
"""Brisa signature size ladder: today's 700px vs smaller widths, from the shipped template.

Only HTML width/height change; the hosted 2x images (logo 600x330, banner 1400x342)
cover every rung. Run: python3 brisa/_mockup/size-ladder/build.py
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parents[1] / "default.html"
SAMPLE = {"{First name}": "Jordan", "{Last name}": "Rivera", "{Title}": "Service Technician",
          "{Phone}": "813-555-0142", "{Mobile}": "813-555-0177", "{E-mail}": "jrivera@brisaclimate.com"}
OUTLOOK_DARK = {"#2a2a2a": "#E0E0E0", "#48104F": "#FFC1FF", "#7a7a7a": "#A2A2A2"}   # approx., from PS sample
RUNGS = [(700, "Today (700px)"), (600, "600px (email standard)")]   # below ~600 the no-wrap text row is wider than the banner


def scaled(tpl, width):
    s = width / 700
    h = re.sub(r"<!--.*?-->", "", tpl, flags=re.S)
    for k, v in SAMPLE.items():
        h = h.replace(k, v)
    h = h.replace("{RT}", "").replace("{/RT}", "")
    lw, lh, col = round(300 * s), round(165 * s), round(340 * s)
    bh = round(171 * s)
    h = h.replace('id="brisa-signature" style="width: 700px', f'id="brisa-signature" style="width: {width}px')
    h = h.replace('<td style="width: 340px;', f'<td style="width: {col}px;')
    h = h.replace('width="300" height="165" style="width: 300px; height: 165px',
                  f'width="{lw}" height="{lh}" style="width: {lw}px; height: {lh}px')
    h = h.replace('width="700" height="171" style="width: 700px; height: 171px',
                  f'width="{width}" height="{bh}" style="width: {width}px; height: {bh}px')
    return h


def dark(h):
    for a, b in OUTLOOK_DARK.items():
        h = re.sub(rf"(?<![-\w])color: ?{a}", f"color: {b}", h, flags=re.I)
    return h


def main():
    print("$ python3 " + " ".join(sys.argv))
    tpl = TPL.read_text()
    tabs, panels = [], []
    for i, (w, name) in enumerate(RUNGS):
        sig = scaled(tpl, w)
        panes = (f'<figure><figcaption>Desktop, light</figcaption><div class="mail">{sig}</div></figure>'
                 f'<figure><figcaption>Desktop, dark (approximate Outlook recolor)</figcaption><div class="mail" style="background:#1E1E1E">{dark(sig)}</div></figure>'
                 f'<figure><figcaption>Phone (390px wide, shrink-to-fit like Outlook mobile)</figcaption>'
                 f'<div class="phone"><div class="fit">{sig}</div></div></figure>')
        tabs.append(f'<button role="tab" data-v="{w}"{" aria-selected=true" if i == 0 else ""}>{html.escape(name)}</button>')
        panels.append(f'<section data-v="{w}"{"" if i == 0 else " hidden"}>{panes}</section>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Brisa Signature Sizes</title>
<style>
body {{ margin:0; font:15px/1.5 -apple-system, system-ui, sans-serif; color:#1f1f24; background:#f6f6f8; }}
header {{ position:sticky; top:0; background:#fff; border-bottom:1px solid #e2e2e8; padding:14px 24px; z-index:2; }}
h1 {{ font-size:18px; margin:0 0 10px; }}
[role=tab] {{ font:inherit; padding:6px 14px; margin:0 6px 6px 0; border:1px solid #e2e2e8; border-radius:6px; background:#fff; cursor:pointer; }}
[role=tab][aria-selected=true] {{ background:#48104F; color:#fff; border-color:#48104F; }}
main {{ padding:16px 24px 48px; }}
figure {{ margin:0 0 18px; }} figcaption {{ font-size:13px; color:#5d5d66; margin-bottom:4px; }}
.mail {{ background:#fff; padding:20px; border:1px solid #e2e2e8; border-radius:8px; overflow-x:auto; }}
.phone {{ width:390px; height:300px; overflow:hidden; background:#fff; border:8px solid #222; border-radius:24px; }}
.fit {{ transform-origin:0 0; padding:20px; width:max-content; }}
.note {{ font-size:13px; color:#5d5d66; max-width:75ch; }}
</style></head><body>
<header><h1>Brisa signature: size options</h1><div role="tablist">{"".join(tabs)}</div></header>
<main>{"".join(panels)}
<p class="note">Only the HTML sizes change; the hosted 2&times; images cover every option. Text stays 10.5pt.
Sample person is fictional. Phone view scales the whole signature to fit 390px, as Outlook mobile does.</p></main>
<script>
document.querySelectorAll('[role=tab]').forEach(b => b.onclick = () => {{
  document.querySelectorAll('[role=tab]').forEach(x => x.setAttribute('aria-selected', x === b));
  document.querySelectorAll('section[data-v]').forEach(s => s.hidden = s.dataset.v !== b.dataset.v);
}});
const only = new URLSearchParams(location.search).get('v');
if (only) document.querySelector(`[role=tab][data-v="${{only}}"]`)?.click();
const fit = () => document.querySelectorAll('.fit').forEach(f => {{ f.style.transform = ''; const w = f.scrollWidth; if (w) f.style.transform = `scale(${{(390 / w).toFixed(3)}})`; }});
fit(); document.querySelectorAll('[role=tab]').forEach(b => b.addEventListener('click', fit)); window.addEventListener('load', fit);
</script></body></html>"""
    (HERE / "index.html").write_text(page)
    print(f"RESULT: OK — open {HERE / 'index.html'}")


if __name__ == "__main__":
    main()
