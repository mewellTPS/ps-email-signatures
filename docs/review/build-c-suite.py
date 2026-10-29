#!/usr/bin/env python3
"""One self-contained review page with every operator's chosen signature, for the c-suite.

Picks (Michael, 2026-10-28): version E for everyone except Boyette, which uses C, and ACE, which uses E v2. Each signature
comes from its own build's paste file, rendered with that build's local images and its simulated
Outlook dark mode. Images are inlined as data URIs, so the single HTML file can be passed along.
For this page only, Michael's title reads "SEO and Data Specialist".

Run the brand builds first, then: python3 docs/review/build-c-suite.py
Writes docs/review/signatures-c-suite-review.html
"""
import base64
import importlib.util
import mimetypes
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DARK_BG = "#1E1E1E"

# (brand, person, build dir, variant, note)
PICKS = [
    ("Purple Standard", "Michael Ewell", "purple_standard/_mockup/michael", "e", ""),
    ("Brisa Climate", "Victor Rodriguez", "brisa/_mockup/victor", "e", ""),
    ("WTR DR", "Sean Myatt", "wtr-dr/_mockup/sean", "c", ""),   # C, badge in the Pledge (Michael, 2026-10-29)
    ("Tyrian Roofing", "John Rodrigues", "tyrian/_mockup/john", "e", ""),
    ("Boyette Pump &amp; Well", "Danny Boyette", "boyette/_mockup/danny", "c", ""),
    ("Purple Current", "Kenny Morrow", "purple-current/_mockup/kenny", "e", ""),
    ("ACE Septic &amp; Waste", "Sample person", "ace/_mockup/e", "e-v2", ""),   # placeholder person until the ACE list arrives
]
TITLE_SWAP = {}   # Michael's build now carries "SEO and Data Specialist" (2026-10-29)


def load(build_dir):
    spec = importlib.util.spec_from_file_location(build_dir.name, build_dir / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def inline(html):
    def data_uri(m):
        path = Path(m.group(1))
        if not path.is_file():
            raise SystemExit(f"RESULT: FAILED: image missing: {path}. Next: run that brand's build.py.")
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        return f'src="data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"'
    return re.sub(r'src="(/[^"]+)"', data_uri, html)


def main():
    print("step 1/2: signatures", flush=True)
    cards = []
    for brand, person, rel, variant, note in PICKS:
        d = REPO / rel
        mod = load(d)
        html = mod.local((d / f"signature-{variant}.html").read_text())
        html = re.sub(r'src="(?!/|data:)([^"]+)"', lambda m: f'src="{d / m.group(1)}"', html)   # relative -> absolute
        if person in TITLE_SWAP:
            old, new = TITLE_SWAP[person]
            assert old in html, f"{person}: title {old!r} not found"
            html = html.replace(old, new)
        html = inline(html)
        print(f"  {brand}: {person}, version {variant.upper()}", flush=True)
        cards.append(f"""<section><h2>{brand} <span>{person}</span></h2>
{f'<p class="note">{note}</p>' if note else ''}<div class="pair">
<div><h3>Light mode</h3><div class="mail" style="background:#fff">{html}</div></div>
<div><h3>Outlook dark mode (simulated)</h3><div class="mail" style="background:{DARK_BG}">{mod.outlook_dark(html)}</div></div>
</div></section>""")
    print("step 2/2: page", flush=True)
    out = HERE / "signatures-c-suite-review.html"
    out.write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Email signatures review</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#222;background:#f4f4f4}}
main{{padding:16px 24px 48px;max-width:1160px}}h1{{font-size:22px;margin:8px 0}}
h2{{font-size:18px;margin:32px 0 4px}}h2 span{{font-weight:400;color:#555}}h3{{font-size:14px;margin:8px 0;color:#555}}
.note{{margin:0 0 4px;color:#7a4b00}}.pair{{display:flex;gap:24px;flex-wrap:wrap}}
.mail{{padding:24px;border:1px solid #ccc;border-radius:6px;width:fit-content}}</style>
<main><h1>Operator email signatures: review</h1>
<p>One signature per company, with real contact details. Every signature is about 480px wide and shown
on a white background and in Outlook dark mode. Dark mode is simulated: Outlook recolors text on its own
but leaves images unchanged, so the artwork uses colors that read on both backgrounds.</p>
{''.join(cards)}</main>
""")
    print(f"RESULT: ok {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
