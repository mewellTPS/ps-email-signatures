#!/usr/bin/env python3
"""Build preview.html as ONE self-contained file that can be emailed as an attachment.

Reads the three shipped signature files and inlines them directly — no iframes,
no <link>, no <script>, and every image (local PNG/GIF *and* the two remotely
hosted assets) converted to a base64 data: URI. The result opens correctly with
no network and no sibling files.

Verification at the bottom asserts self-containment by effect: it scans the
output for any src/href that is not a data: URI or an in-page anchor. A page
that merely "looks fine" in a browser that still has the sibling files on disk
is not evidence of anything.

Usage: python3 build-preview.py
"""
from __future__ import annotations

import base64
import html
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "preview.html"

V1 = HERE.parent / "signature-purple-standard.html"
SIGS = [
    ("v1 — current", "live", V1,
     "The baseline. v2 and v3 are both measured against this: a diff of either against v1 "
     "shows only the change it is named for."),
    ("v2 — static brand strip", "one row added", HERE / "signature-purple-standard-v2.html",
     "v1 plus a single &lt;tr&gt;. Six icons — MOR and ENG dropped, so the strip shows only "
     "brands with real artwork."),
    ("v3 — animated badge, no strip", "animated", HERE / "signature-purple-standard-v3.html",
     "v1's layout untouched — the badge slot itself cycles all seven marks. No strip on "
     "purpose: the animation already carries the portfolio."),
    ("v3 + strip — combined", "animated", HERE / "signature-purple-standard-v3-with-strip.html",
     "Both at once, generated from the other two files so it can't drift. It does state the "
     "portfolio twice."),
]

MIME = {".png": "image/png", ".gif": "image/gif", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}
_cache: dict[str, str] = {}


def data_uri_local(rel: str) -> str:
    path = (HERE / rel).resolve() if not rel.startswith("../") else (HERE / rel).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"asset not found: {rel} -> {path}")
    mime = MIME.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def data_uri_remote(url: str) -> str:
    """Fetch a hosted asset and inline it.

    Verify the bytes, not the status code: this project has already been bitten
    by a host returning HTTP 200 with WebP bytes from a .png URL. Sniff the
    magic number and trust that over the extension and over Content-Type.
    """
    # Cloudflare fronts assets.purple-standard.app and 403s urllib's default
    # User-Agent ("Python-urllib/3.x"). curl gets through, so this is UA
    # filtering rather than an auth or path problem — send a browser UA.
    req = urllib.request.Request(url, headers={
        "Accept": "image/png,image/*,*/*",
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            blob = r.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(
            f"error: {url} returned HTTP {e.code}.\n"
            "       The preview cannot be self-contained without this asset."
        ) from e
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        mime = "image/png"
    elif blob[:6] in (b"GIF87a", b"GIF89a"):
        mime = "image/gif"
    elif blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        raise ValueError(f"{url} served WEBP bytes — Outlook cannot render it. Fix the host.")
    elif blob[:3] == b"\xff\xd8\xff":
        mime = "image/jpeg"
    else:
        raise ValueError(f"{url} served unrecognised bytes: {blob[:12]!r}")
    print(f"    fetched {len(blob):>7,} B  {mime}  {url.rsplit('/', 1)[-1]}")
    return f"data:{mime};base64," + base64.b64encode(blob).decode()


def inline(src: str) -> str:
    if src in _cache:
        return _cache[src]
    uri = data_uri_remote(src) if src.startswith("http") else data_uri_local(src)
    _cache[src] = uri
    return uri


def strip_comments(markup: str) -> str:
    return re.sub(r"<!--.*?-->", "", markup, flags=re.S).strip()


def load_signature(path: Path) -> str:
    """Return the signature markup with every img src replaced by a data: URI."""
    body = strip_comments(path.read_text())
    return re.sub(r'src="([^"]+)"', lambda m: f'src="{inline(m.group(1))}"', body)


CSS = """
  :root { --ps-purple:#49104F; --ink:#1c1c1e; --muted:#6b6b70; --line:#e4e4e8; --bg:#f6f6f8; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  header { background:#fff; border-bottom:1px solid var(--line); padding:24px 28px 20px; }
  h1 { margin:0 0 5px; font-size:19px; color:var(--ps-purple); letter-spacing:-.01em; }
  header p { margin:0; color:var(--muted); font-size:13.5px; max-width:82ch; }
  main { padding:26px 28px 90px; max-width:1120px; }
  section { margin-bottom:34px; }
  .head { display:flex; align-items:baseline; gap:11px; margin:0 0 10px; flex-wrap:wrap; }
  h2 { font-size:15px; margin:0; color:var(--ps-purple); }
  .file { font:12px/1 ui-monospace, SFMono-Regular, Menlo, monospace; color:var(--muted); }
  .tag { font-size:10.5px; text-transform:uppercase; letter-spacing:.05em; padding:3px 8px;
         border-radius:999px; background:#efe7f2; color:var(--ps-purple); font-weight:700;
         white-space:nowrap; }
  .tag.live { background:#e7f2ea; color:#1d6b38; }
  .tag.animated { background:#fff3d6; color:#8a5a00; }
  .stage { background:#fff; border:1px solid var(--line); border-radius:6px;
           padding:24px 28px; overflow-x:auto; }
  .why { margin:9px 0 0; font-size:13px; color:#44444a; max-width:88ch; }
  .why b { color:var(--ps-purple); }
  .gifbox { display:flex; gap:26px; align-items:center; flex-wrap:wrap; }
  .gifbox figure { margin:0; text-align:center; }
  .gifbox img { display:block; margin:0 auto 6px; }
  .gifbox figcaption { font-size:11px; color:var(--muted); }
  table.facts { border-collapse:collapse; font-size:13px; }
  table.facts th, table.facts td { text-align:left; padding:5px 18px 5px 0; vertical-align:top; }
  table.facts th { color:var(--muted); font-weight:600; white-space:nowrap; }
  .strip { display:flex; gap:20px; flex-wrap:wrap; align-items:flex-end; }
  .strip figure { margin:0; text-align:center; width:92px; }
  .strip img { width:80px; height:80px; display:block; margin:0 auto 7px; }
  .strip figcaption { font-size:10.5px; color:var(--muted); line-height:1.3; }
  footer { border-top:1px solid var(--line); margin-top:8px; padding:18px 28px 40px;
           font-size:12.5px; color:var(--muted); }
"""

BRANDS = [
    ("brand-ace", "ACE Septic &amp; Waste"),
    ("brand-purple-current", "Purple Current"),
    ("brand-boyette", "Boyette Pump &amp; Well"),
    ("brand-wtr-dr", "WTR DR"),
    ("brand-brisa", "Brisa Climate"),
    ("brand-tyrian", "Tyrian Roofing"),
]


def main() -> int:
    print("  inlining assets…")
    parts = []
    for title, tag, path, why in SIGS:
        if not path.is_file():
            print(f"error: missing {path}", file=sys.stderr)
            return 1
        parts.append(f"""
  <section>
    <div class="head">
      <h2>{title}</h2>
      <span class="tag {tag.split()[0] if tag in ('live','animated') else ''}">{tag}</span>
      <span class="file">{html.escape(path.name)}</span>
    </div>
    <div class="stage">{load_signature(path)}</div>
    <p class="why">{why}</p>
  </section>""")

    icons = "".join(
        '<figure><img src="{}" alt="{}"><figcaption>{}</figcaption></figure>'.format(
            inline(f"out/c-native/{slug}.png"), name, name)
        for slug, name in BRANDS
    )

    gif = inline("out/ball/tps-badge-cycle.gif")
    frame0 = inline("out/ball-c/ball-0-ps.png")
    gif_kib = round(len((HERE / "out/ball/tps-badge-cycle.gif").read_bytes()) / 1024)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Purple Standard signature — v1 / v2 / v3</title>
<style>
  /* The GIF's base64 payload is ~221 KiB. Declaring it once here and reusing it
     for both demo sizes keeps the file from carrying three copies of it — the
     two signature panels below still need their own real <img> tags, because
     those are the shipped markup and must stay faithful. */
  :root {{ --ballgif: url({gif}); }}
  .gifdemo {{ background:var(--ballgif) center/contain no-repeat; }}
  .g75 {{ width:75px; height:75px; }}
  .g150 {{ width:150px; height:150px; }}
{CSS}</style>
</head>
<body>

<header>
  <h1>Purple Standard signature — v1, v2, v3</h1>
  <p>Each panel is the actual shipped signature markup, inlined here unchanged, so what renders
     is what CodeTwo will get. Brand icons use treatment C (native shapes). The v3 badge
     animates — give it a moment. This file is entirely self-contained: every image is embedded,
     so it works offline and can be sent as an attachment.</p>
</header>

<main>
{"".join(parts)}

  <section>
    <div class="head"><h2>The six brand icons</h2><span class="file">out/c-native/</span></div>
    <div class="stage"><div class="strip">{icons}</div></div>
    <p class="why">Shown at 80&nbsp;px — twice their 40&nbsp;px size in the signature, per the
      2× asset rule. <b>Brisa is now the real bear mark</b>, replacing the circular badge whose
      "FINE-TUNED FLORIDA COMFORT" ring was unreadable at 40&nbsp;px. <b>MOR and ENG are gone</b>
      — the strip carries only brands with real artwork.</p>
  </section>

  <section>
    <div class="head"><h2>The GIF on its own</h2>
      <span class="file">out/ball/tps-badge-cycle.gif</span></div>
    <div class="stage">
      <div class="gifbox">
        <figure><div class="gifdemo g75" role="img" aria-label="cycling badge, real size"></div>
          <figcaption>75&nbsp;px — real size</figcaption></figure>
        <figure><div class="gifdemo g150" role="img" aria-label="cycling badge, 2x"></div>
          <figcaption>150&nbsp;px — source, 2×</figcaption></figure>
        <figure><img src="{frame0}" width="75" height="75" alt="static fallback">
          <figcaption>frame 0 — static fallback</figcaption></figure>
        <table class="facts">
          <tr><th>Frames</th><td>63 — 7 marks, each held 1.4&nbsp;s then turned over 8 frames</td></tr>
          <tr><th>Cycle</th><td>13.2&nbsp;s, loops forever</td></tr>
          <tr><th>Canvas</th><td>150×150, displayed at 75×75 (2×)</td></tr>
          <tr><th>Weight</th><td>{gif_kib}&nbsp;KiB — Riemersma dither, 128 colours</td></tr>
          <tr><th>Fallback</th><td>frame 0 is tps-badge, so a client that won't animate renders v1's badge</td></tr>
        </table>
      </div>
      <p class="why" style="margin-top:18px">The turn is a horizontal squeeze: the outgoing mark
        compresses to edge-on at the centre line, then the incoming one expands out of it. Width
        follows a cosine rather than a straight ramp, so it reads as rotation instead of a squash.</p>
    </div>
  </section>
</main>

<footer>
  Generated by <code>build-preview.py</code>. Every image is embedded as a data: URI — no network,
  no sibling files. Note that some mail clients strip data: URIs from message bodies, so send this
  as an <b>attachment</b> rather than pasting it inline.
</footer>

</body>
</html>
"""
    OUT.write_text(page)

    # --- verify self-containment by effect, not by assumption ----------------
    t = OUT.read_text()
    external = [
        u for u in re.findall(r'(?:src|href)="([^"]+)"', t)
        if not u.startswith("data:") and not u.startswith("#")
    ]
    # links to brand websites are expected and fine; only *resources* must be inlined
    res_ext = [u for u in external if re.search(r"\.(png|gif|jpe?g|svg|css|js)(\?|$)", u, re.I)]
    size_kib = round(len(t.encode()) / 1024)

    checks = {
        "no external resources":  not res_ext,
        "no iframes":             "<iframe" not in t,
        "no <script>":            "<script" not in t.lower(),
        "no external stylesheet": '<link' not in t.lower(),
        "all 4 signatures":       t.count('class="stage"') >= 4,
        "6 icons in strip":       t.count('<figure><img src="data:image/png') >= 6,
        "gif embedded":           "data:image/gif;base64," in t,
    }
    print()
    for name, ok in checks.items():
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")
    if res_ext:
        for u in res_ext[:10]:
            print(f"       external resource: {u[:90]}")
    print(f"\n  {OUT.name}: {size_kib} KiB, {len(_cache)} unique assets embedded")
    print(f"  outbound links (fine, not resources): {len(set(external) - set(res_ext))}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
