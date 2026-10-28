#!/usr/bin/env python3
"""Brisa compact-layout preview: today's default.html vs the compact candidate, next to PS and Boyette.

Renders the real template files with sample data and the hosted images.
Run: python3 brisa/_mockup/compact/build.py
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SAMPLE = {"{First name}": "Jordan", "{Last name}": "Rivera", "{Title}": "Service Technician",
          "{Phone}": "813-555-0142", "{Mobile}": "813-555-0177", "{E-mail}": "jrivera@brisaclimate.com"}
OUTLOOK_DARK = {"#2a2a2a": "#E0E0E0", "#48104F": "#FFC1FF", "#7a7a7a": "#A2A2A2",
                "#49104F": "#FFC1FF", "#808080": "#9B9B9B", "#A263D2": "#C17EF0",
                "#000000": "#FFFFFF", "#F93822": "#FF593B"}   # Outlook iOS samples; Brisa values approximate


def render(path, drop_banner=False):
    h = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    if drop_banner:
        h = re.sub(r'<tr>\s*<td[^>]*data-codetwo-visible="Banner".*?</tr>', "", h, flags=re.S)
    for k, v in SAMPLE.items():
        h = h.replace(k, v)
    return h.replace("{RT}", "").replace("{/RT}", "")


def dark(h):
    for a, b in OUTLOOK_DARK.items():
        h = re.sub(rf"(?<![-\w])color: ?{a}", f"color: {b}", h, flags=re.I)
    return h


TODAY = REPO / "brisa/default.html"
COMPACT = HERE / "signature-brisa-compact.html"
OPTIONS = [("today", "Today (700px)", render(TODAY)),
           ("compact", "Compact", render(COMPACT)),
           ("nobanner", "Compact, no banner (replies)", render(COMPACT, drop_banner=True))]
PEERS = [("PS", render(REPO / "purple_standard/default.html")), ("Boyette", render(REPO / "boyette/default.html"))]


def main():
    print("$ python3 " + " ".join(sys.argv))
    tabs, panels = [], []
    for i, (oid, name, sig) in enumerate(OPTIONS):
        peers = "".join(f'<div class="peer"><span>{p}</span>{s}</div>' for p, s in PEERS)
        panels.append(
            f'<section data-v="{oid}"{"" if i == 0 else " hidden"}>'
            f'<figure><figcaption>In an email (reading pane about 1000px wide), next to PS and Boyette at the same scale</figcaption>'
            f'<div class="pane"><div class="peer"><span>Brisa</span><div class="measure">{sig}</div></div>{peers}</div></figure>'
            f'<figure><figcaption>Outlook dark mode (approximate recolor)</figcaption><div class="mail" style="background:#1E1E1E">{dark(sig)}</div></figure>'
            f'<figure><figcaption>Phone (390px, shrink-to-fit like Outlook mobile)</figcaption><div class="phone"><div class="fit">{sig}</div></div></figure>'
            f'<p class="size" data-for="{oid}"></p></section>')
        tabs.append(f'<button role="tab" data-v="{oid}"{" aria-selected=true" if i == 0 else ""}>{html.escape(name)}</button>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Brisa Compact Signature</title>
<style>
body {{ margin:0; font:15px/1.5 -apple-system, system-ui, sans-serif; color:#1f1f24; background:#f6f6f8; }}
header {{ position:sticky; top:0; background:#fff; border-bottom:1px solid #e2e2e8; padding:14px 24px; z-index:2; }}
h1 {{ font-size:18px; margin:0 0 10px; }}
[role=tab] {{ font:inherit; padding:6px 14px; margin:0 6px 6px 0; border:1px solid #e2e2e8; border-radius:6px; background:#fff; cursor:pointer; }}
[role=tab][aria-selected=true] {{ background:#48104F; color:#fff; border-color:#48104F; }}
main {{ padding:16px 24px 48px; }}
figure {{ margin:0 0 20px; }} figcaption {{ font-size:13px; color:#5d5d66; margin-bottom:4px; }}
.pane {{ width:1000px; max-width:100%; background:#fff; border:1px solid #e2e2e8; border-radius:8px; padding:20px; box-sizing:border-box; overflow-x:auto;
  background-image:linear-gradient(to right, transparent 499px, #f0d6f2 499px, #f0d6f2 501px, transparent 501px); }}
.peer {{ margin-bottom:26px; }} .peer > span {{ display:block; font-size:12px; color:#8a8a93; margin-bottom:6px; }}
.measure {{ display:inline-block; }}
.mail {{ padding:20px; border:1px solid #e2e2e8; border-radius:8px; overflow-x:auto; }}
.phone {{ width:390px; height:340px; overflow:hidden; background:#fff; border:8px solid #222; border-radius:24px; }}
.fit {{ transform-origin:0 0; padding:16px; width:max-content; }}
.size, .note {{ font-size:13px; color:#5d5d66; max-width:75ch; }}
</style></head><body>
<header><h1>Brisa signature: compact layout</h1><div role="tablist">{"".join(tabs)}</div></header>
<main>{"".join(panels)}
<p class="note">The pink line marks the middle of a 1000px reading pane. Text sizes match PS and Boyette (10pt body, 13pt name).
The hosted 2&times; images cover the smaller sizes, so nothing new needs uploading. Sample person is fictional.</p></main>
<script>
const fit = () => document.querySelectorAll('section:not([hidden]) .fit').forEach(f => {{ f.style.transform = ''; const w = f.scrollWidth; if (w) f.style.transform = `scale(${{Math.min(1, 390 / w).toFixed(3)}})`; }});
const size = () => document.querySelectorAll('section:not([hidden])').forEach(s => {{ const m = s.querySelector('.measure').getBoundingClientRect();
  s.querySelector('.size').textContent = `Brisa signature here: ${{Math.round(m.width)}} × ${{Math.round(m.height)}} px (PS is 500 × 204, Boyette 480 × 215).`; }});
document.querySelectorAll('[role=tab]').forEach(b => b.onclick = () => {{
  document.querySelectorAll('[role=tab]').forEach(x => x.setAttribute('aria-selected', x === b));
  document.querySelectorAll('section[data-v]').forEach(s => s.hidden = s.dataset.v !== b.dataset.v);
  fit(); size();
}});
const only = new URLSearchParams(location.search).get('v');
if (only) document.querySelector(`[role=tab][data-v="${{only}}"]`)?.click();
window.addEventListener('load', () => {{ fit(); size(); }});
</script></body></html>"""
    (HERE / "index.html").write_text(page)
    print(f"RESULT: OK — open {HERE / 'index.html'}")


if __name__ == "__main__":
    main()
